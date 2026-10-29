"""The content catalogue: what this repository publishes, as packs (Spatial GM D147).

Every folder under `adventures/`, `kits/` and `heroes/` is a pack. Each kit is also published as
its groups (the rows of the `| Group | Tag | Pieces |` table in its campaign.md): a group pack is a
complete kit of its own, made of the big kit's files for that group (its pieces, their models, the
shared material library) plus a generated campaign.md and cover. A file shared by a group and its kit
is the same file, so downloading both, or every group, stores it once.

Used by build-distribution.py (archives, manifest, site) and make-images.py (thumbnails, covers).
"""
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "catalogue"          # thumbnails and group covers (committed; 3DAssets will go away)
THUMBS = CATALOGUE / "thumbs"           # <talespire uuid>.jpg, 160 px
COVERS = CATALOGUE / "covers"           # <pack slug>.jpg for generated group packs

# Where each kind of pack lives, and the collection it's listed under.
SOURCES = [("adventures", ".spatialgm", "adventure"), ("kits", ".spatialgm", "kit"),
           ("heroes", ".spatialhero", "hero")]

# A kit's noun for its group packs ("Tavern Tiles"), and the collection its groups are listed under.
KIT_KINDS = {"Tiles Kit": ("Tiles", "tiles"), "Props Kit": ("Props", "props"), "Creatures Kit": ("Creatures", "creatures")}

COLLECTIONS = [
    {"id": "adventures", "name": "Adventures", "symbol": "book.closed",
     "summary": "Campaigns to play: encounters, story, music and sound, ready for the table."},
    {"id": "heroes", "name": "Heroes", "symbol": "person.crop.square",
     "summary": "Ready-made heroes for players who don't have one yet."},
    {"id": "kits", "name": "Kits", "symbol": "shippingbox",
     "summary": "Whole kits of pieces to build boards with. Each is also offered in groups below."},
    {"id": "tiles", "name": "Tiles", "symbol": "square.grid.3x3", "parent": "kits",
     "summary": "Floors, walls, stairs and arches, one set at a time."},
    {"id": "props", "name": "Props", "symbol": "cube", "parent": "kits",
     "summary": "Furniture, containers, lights and nature, one kind at a time."},
    {"id": "creatures", "name": "Creatures", "symbol": "pawprint", "parent": "kits",
     "summary": "Miniatures for monsters and people, one family at a time."},
]

IGNORED_PARTS = (".DS_Store", ".cache")


def included(rel: Path) -> bool:
    """Whether a file belongs in a published pack (Finder files, app caches and iCloud placeholders don't)."""
    return not any(part in IGNORED_PARTS or part.endswith(".icloud") or part.startswith("._") for part in rel.parts)


def front_matter(path: Path) -> dict:
    """The simple `key: value` lines of a Markdown file's front matter (comments removed, lists as strings)."""
    meta = {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return meta
    for line in text.split("\n")[1:]:
        if line.strip() == "---":
            break
        line = re.sub(r"\s+#.*$", "", line)
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def tags(meta: dict) -> list:
    value = meta.get("tags", "").strip()
    return [t.strip() for t in value.strip("[]").split(",") if t.strip()] if value else []


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@dataclass
class Piece:
    file: str           # path inside the kit ("scenery/bar-counter.md")
    name: str
    model: str          # "media/tiles/Tavern/Bar Counter.usd"
    tags: list
    talespire: str      # the TaleSpire catalogue id ("" if none)

    @property
    def thumb(self) -> str:
        """Its thumbnail's name in catalogue/thumbs: the TaleSpire id, else the kit folder and model ("roof-door-doorframe")."""
        return self.talespire or slug(self.model.split("/")[1] + "-" + Path(self.model).stem)


@dataclass
class Group:
    kit: "Kit"
    name: str           # "Tavern"
    tag: str            # "tavern"
    pieces: list = field(default_factory=list)

    @property
    def title(self) -> str:
        return f"{self.name} {KIT_KINDS[self.kit.name][0]}"

    @property
    def slug(self) -> str:
        return slug(self.title)

    @property
    def id(self) -> str:
        """Stable: derived from the kit's id and the group's tag."""
        return str(uuid.uuid5(uuid.UUID(self.kit.id), "group:" + self.tag))

    def folders(self) -> list:
        """The media folders this group's models live in (all their files are included)."""
        found = []
        for piece in self.pieces:
            parts = piece.model.split("/")
            folder = "/".join(parts[:2]) if parts[1] == "roof-door" else "/".join(parts[:3])
            if folder not in found:
                found.append(folder)
        return found

    def files(self) -> list:
        """The kit's files this group uses, as paths inside the kit."""
        root = self.kit.folder
        chosen = {p.file for p in self.pieces}
        for folder in self.folders() + ["media/materials"]:
            for path in (root / folder).rglob("*"):
                rel = path.relative_to(root)
                if path.is_file() and included(rel):
                    chosen.add(str(rel))
        return sorted(chosen)


@dataclass
class Kit:
    folder: Path
    name: str
    id: str
    groups: list


def read_kit(folder: Path) -> Kit:
    meta = front_matter(folder / "campaign.md")
    kit = Kit(folder=folder, name=meta["name"], id=meta["id"], groups=[])
    table = re.findall(r"^\| ([^|]+?) \| `([^`]+)` \| \d+ \|$", (folder / "campaign.md").read_text(encoding="utf-8"), re.M)
    kit.groups = [Group(kit=kit, name=name, tag=tag) for name, tag in table]
    by_name = {g.name: g for g in kit.groups}
    by_tag = {g.tag: g for g in kit.groups}
    for sub in ("scenery", "creatures"):
        for path in sorted((folder / sub).glob("*.md")):
            meta = front_matter(path)
            model = meta.get("model", "")
            parts = model.split("/")
            piece = Piece(file=f"{sub}/{path.name}", name=meta.get("name", path.stem), model=model, tags=tags(meta),
                          talespire=meta.get("same-as", "").removeprefix("talespire:"))
            # The model's group folder names its group; failing that, the first tag that is a group's.
            group = by_name.get(parts[2]) if len(parts) > 3 and parts[1] != "roof-door" else None
            group = group or next((by_tag[t] for t in piece.tags if t in by_tag), None)
            if group is None:
                raise SystemExit(f"{folder.name}: {path.name} belongs to no group")
            group.pieces.append(piece)
    for group in kit.groups:
        if not group.pieces:
            raise SystemExit(f"{folder.name}: group {group.name} has no pieces")
    return kit


def kits() -> list:
    return [read_kit(folder) for folder in sorted((ROOT / "kits").glob("*.spatialgm")) if folder.stem in KIT_KINDS]


def cover_pieces(pieces: list, count: int = 8) -> list:
    """Up to `count` pieces with thumbnails, spread evenly through the list (the same every build)."""
    with_thumbs = [p for p in pieces if (THUMBS / f"{p.thumb}.jpg").exists()]
    if len(with_thumbs) <= count:
        return with_thumbs
    step = len(with_thumbs) / count
    return [with_thumbs[int(i * step)] for i in range(count)]
