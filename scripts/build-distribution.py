#!/usr/bin/env python3
"""Builds the published catalogue (Spatial GM D147: packs share files by content, not by dependencies).

  python3 scripts/build-distribution.py            # local: a complete catalogue in dist/
  RELEASE_TAG=v1.0.7 GITHUB_REPOSITORY=owner/repo python3 scripts/build-distribution.py   # the Action

Every pack (an adventure, a kit, a kit's group, a hero) stays a self-contained folder. The build lists
each pack's files by SHA-256 (`packs/<pack hash>.json`) and groups the files by the set of packs using
them into archives named by their contents (`<archive id>.aar`, LZFSE Apple Archive, each file stored
flat under its own hash). An app downloads only the archives holding files it doesn't have yet.

Local mode writes dist/: manifest.json (archive URLs relative to it), archives/, packs/, covers/,
thumbs/ and index.html. Point the app at that folder (or a copy in iCloud Drive) as a source.

Release mode (RELEASE_TAG set) writes docs/ for GitHub Pages: the same files without the archives,
whose URLs point at releases. An archive already in the previous docs/manifest.json keeps its URL
and isn't rebuilt; only new archives are built, into dist/release/, for the Action to upload.
"""
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalogue  # noqa: E402

ROOT = catalogue.ROOT
MANIFEST_VERSION = 2


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class Pack:
    """One pack: its folder name when installed, and where each of its files comes from."""

    def __init__(self, *, id, kind, collection, name, folder, summary="", tags=(), part_of=None,
                 template=False, opens_first=False, author="", cover=None):
        self.id, self.kind, self.collection, self.name, self.folder = id, kind, collection, name, folder
        self.summary, self.tags, self.part_of, self.author = summary, list(tags), part_of, author
        self.template, self.opens_first, self.cover = template, opens_first, cover
        self.sources = {}    # path inside the pack → file on disk
        self.contents = []   # the pieces, for browsing before downloading

    def add_folder(self, folder: Path, only=None):
        for path in sorted(folder.rglob("*")):
            rel = path.relative_to(folder)
            if path.is_file() and catalogue.included(rel) and (only is None or str(rel) in only):
                self.sources[str(rel)] = path

    def listing(self, hashes):
        files = [{"path": p, "size": self.sources[p].stat().st_size, "sha256": hashes[self.sources[p]]}
                 for p in sorted(self.sources)]
        body = {"id": self.id, "folder": self.folder, "files": files}
        if self.contents:
            body["contents"] = self.contents
        # The pack hash names exactly this folder and these files.
        identity = json.dumps({"folder": self.folder, "files": files}, sort_keys=True, separators=(",", ":"))
        return sha256_text(identity), body


def piece_contents(pieces):
    return [{"name": p.name, "kind": "creature" if p.file.startswith("creatures/") else "scenery",
             "thumb": f"thumbs/{p.thumb}.jpg", "tags": p.tags} for p in pieces]


def group_markdown(group) -> str:
    kit = group.kit
    noun = catalogue.KIT_KINDS[kit.name][0].lower()
    names = ", ".join(p.name for p in group.pieces)
    count = len(group.pieces)
    return f"""---
format: 2
name: {group.title}
id: {group.id}
author: 3DAssets
cover: cover.jpg
summary: "{count} {group.name.lower()} {noun if count != 1 else noun.rstrip('s')} from the {kit.name}."
---
# {group.title}

The {group.name} group of the {kit.name}: {count} pieces to take from the Bookshelf into your campaign
(D139). The {kit.name} has the same pieces; with both on a device, their files are stored once.

Pieces: {names}.

Models are procedural reconstructions; see the 3DAssets repository's RIGHTS_PROVENANCE_REVIEW.txt.
"""


def collect_packs(generated: Path):
    packs = []
    for folder in sorted((ROOT / "adventures").glob("*.spatialgm")):
        meta = catalogue.front_matter(folder / "campaign.md")
        pack = Pack(id=meta["id"], kind="campaign", collection="adventures", name=meta.get("name", folder.stem),
                    folder=folder.name, summary=meta.get("summary", ""), author=meta.get("author", ""),
                    template=meta.get("template") == "true", opens_first=meta.get("opens-first") == "true",
                    cover=folder / meta["cover"] if meta.get("cover") else None)
        pack.add_folder(folder)
        packs.append(pack)
    for kit in catalogue.kits():
        meta = catalogue.front_matter(kit.folder / "campaign.md")
        noun, collection = catalogue.KIT_KINDS[kit.name]
        pack = Pack(id=kit.id, kind="campaign", collection="kits", name=kit.name, folder=kit.folder.name,
                    summary=meta.get("summary", ""), author=meta.get("author", ""), tags=[collection],
                    cover=kit.folder / meta["cover"] if meta.get("cover") else None)
        pack.add_folder(kit.folder)
        pack.contents = piece_contents([p for g in kit.groups for p in g.pieces])
        packs.append(pack)
        for group in kit.groups:
            made = generated / group.slug
            made.mkdir(parents=True, exist_ok=True)
            (made / "campaign.md").write_text(group_markdown(group), encoding="utf-8")
            cover = catalogue.COVERS / f"{group.slug}.jpg"
            pack = Pack(id=group.id, kind="campaign", collection=collection, name=group.title,
                        folder=f"{group.title}.spatialgm", summary=f"{len(group.pieces)} pieces from the {kit.name}.",
                        author="3DAssets", tags=[collection, group.tag], part_of=kit.id,
                        cover=cover if cover.exists() else None)
            pack.add_folder(kit.folder, only=set(group.files()) - {"campaign.md", "cover.jpg"})
            pack.sources["campaign.md"] = made / "campaign.md"
            if pack.cover:
                pack.sources["cover.jpg"] = pack.cover
            pack.contents = piece_contents(group.pieces)
            packs.append(pack)
    for folder in sorted((ROOT / "heroes").glob("*.spatialhero")):
        meta = catalogue.front_matter(folder / "hero.md")
        pack = Pack(id=meta["id"], kind="hero", collection="heroes", name=meta.get("name", folder.stem),
                    folder=folder.name, summary=meta.get("summary", ""), tags=[meta.get("uses-rule-set", "")],
                    cover=folder / meta["cover"] if meta.get("cover") else None)
        pack.tags = [t for t in pack.tags if t]
        pack.add_folder(folder)
        packs.append(pack)
    return packs


def bundles(packs):
    heroes = [p.id for p in packs if p.kind == "hero"]
    kits = [p.id for p in packs if p.collection == "kits"]
    found = []
    if heroes:
        found.append({"id": "all-heroes", "name": "All Heroes", "collection": "heroes", "packs": heroes,
                      "summary": f"All {len(heroes)} heroes: pick one at the table."})
    if kits:
        found.append({"id": "all-kits", "name": "Every Kit", "collection": "kits", "packs": kits,
                      "summary": "Every tile, prop and creature: the three kits whole."})
    return found


def image_tool(work: Path) -> Path:
    out = work / "images"
    subprocess.run(["xcrun", "swiftc", "-O", str(ROOT / "scripts/images.swift"), "-o", str(out)], check=True)
    return out


def make_archive(archive_id, hashes, files_by_hash, out: Path):
    """An LZFSE Apple Archive of the files, each stored flat under its SHA-256."""
    with tempfile.TemporaryDirectory() as temp:
        stage = Path(temp)
        for h in hashes:
            shutil.copyfile(files_by_hash[h], stage / h)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["/usr/bin/aa", "archive", "-d", str(stage), "-o", str(out), "-a", "lzfse"], check=True)


def size_text(n: int) -> str:
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


def write_index(out: Path, manifest, title):
    by_collection = {}
    for pack in manifest["packs"]:
        by_collection.setdefault(pack["collection"], []).append(pack)
    sections = []
    for c in manifest["collections"]:
        cards = []
        for p in by_collection.get(c["id"], []):
            cover = f'<img src="{html.escape(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="blank"></div>'
            pieces = f' · {p["pieces"]} pieces' if p.get("pieces") else ""
            cards.append(f'<article>{cover}<h3>{html.escape(p["name"])}</h3><p>{html.escape(p.get("summary", ""))}</p>'
                         f'<p class="meta">{size_text(p["bytes"])}{pieces}</p></article>')
        if cards:
            sections.append(f'<section><h2>{html.escape(c["name"])}</h2><p class="lede">{html.escape(c["summary"])}</p>'
                            f'<div class="grid">{"".join(cards)}</div></section>')
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ --bg:#f6f6f8; --fg:#1d1d1f; --muted:#6e6e73; --card:#fff; --line:#e3e3e8; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111214; --fg:#f2f2f7; --muted:#98989f; --card:#1c1d20; --line:#2c2d31; }} }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.45 -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:32px 16px 64px; }}
h1 {{ font-size:32px; margin:0 0 4px; }} h2 {{ margin:40px 0 4px; }} .lede, .meta {{ color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:16px; margin-top:16px; }}
article {{ background:var(--card); border:1px solid var(--line); border-radius:14px; overflow:hidden; }}
article img, .blank {{ width:100%; aspect-ratio:1; object-fit:cover; display:block; background:var(--line); }}
article h3 {{ font-size:15px; margin:10px 12px 2px; }} article p {{ margin:0 12px 10px; font-size:13px; }}
code {{ font-size:13px; }}
</style></head><body><main>
<h1>{html.escape(title)}</h1>
<p class="lede">Adventures, kits and heroes for Spatial GM. Open the app's Downloads to get them: a pack downloads only the files your device doesn't already have. The catalogue is <a href="manifest.json"><code>manifest.json</code></a>.</p>
{"".join(sections)}
</main></body></html>
"""
    (out / "index.html").write_text(page, encoding="utf-8")


def main():
    release = os.environ.get("RELEASE_TAG")
    repository = os.environ.get("GITHUB_REPOSITORY", "dylanbeadle/adventures")
    out = ROOT / ("docs" if release else "dist")
    dist = ROOT / "dist"
    version = (ROOT / "VERSION").read_text().strip() if (ROOT / "VERSION").exists() else "1.0.0"

    previous = {}
    old_manifest = ROOT / "docs" / "manifest.json"
    if release and old_manifest.exists():
        old = json.loads(old_manifest.read_text())
        if old.get("version") == MANIFEST_VERSION:
            previous = {a["id"]: a for a in old.get("archives", [])}

    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp)
        packs = collect_packs(work / "generated")

        # Every file's hash, once.
        hashes, files_by_hash = {}, {}
        for pack in packs:
            for path in pack.sources.values():
                if path not in hashes:
                    hashes[path] = sha256_file(path)
                    files_by_hash.setdefault(hashes[path], path)

        # Pack listings, and which packs use each file.
        users = {}
        listings = {}
        for pack in packs:
            pack_hash, body = pack.listing(hashes)
            listings[pack.id] = (pack_hash, body)
            for path in pack.sources.values():
                users.setdefault(hashes[path], set()).add(pack.id)

        # One archive per distinct set of packs, named by its files.
        sets = {}
        for h, ids in users.items():
            sets.setdefault(frozenset(ids), []).append(h)
        archives = []
        new = []
        for ids, contained in sorted(sets.items(), key=lambda kv: sorted(kv[1])):
            contained.sort()
            archive_id = sha256_text("\n".join(contained))
            if archive_id in previous:
                entry = dict(previous[archive_id])
                entry["contains"] = contained
            else:
                if release:
                    target = dist / "release" / f"{archive_id}.aar"
                    url = f"https://github.com/{repository}/releases/download/{release}/{archive_id}.aar"
                else:
                    target = dist / "archives" / f"{archive_id}.aar"
                    url = f"archives/{archive_id}.aar"
                if not target.exists():
                    make_archive(archive_id, contained, files_by_hash, target)
                    new.append(target)
                entry = {"id": archive_id, "url": url, "bytes": target.stat().st_size,
                         "sha256": sha256_file(target), "contains": contained}
            archives.append(entry)

        # Pack listings, covers and thumbnails beside the manifest.
        for sub in ("packs", "covers", "thumbs"):
            if (out / sub).exists():
                shutil.rmtree(out / sub)
            (out / sub).mkdir(parents=True)
        images = image_tool(work)
        manifest_packs = []
        thumbs = set()
        for pack in packs:
            pack_hash, body = listings[pack.id]
            (out / "packs" / f"{pack_hash}.json").write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            entry = {"id": pack.id, "kind": pack.kind, "collection": pack.collection, "name": pack.name,
                     "folder": pack.folder, "hash": pack_hash, "files": f"packs/{pack_hash}.json",
                     "bytes": sum(f["size"] for f in body["files"]), "fileCount": len(body["files"])}
            if pack.summary: entry["summary"] = pack.summary
            if pack.author: entry["author"] = pack.author
            if pack.tags: entry["tags"] = pack.tags
            if pack.part_of: entry["partOf"] = pack.part_of
            if pack.template: entry["template"] = True
            if pack.opens_first: entry["opensFirst"] = True
            if pack.contents:
                entry["pieces"] = len(pack.contents)
                thumbs.update(c["thumb"] for c in pack.contents)
            if pack.cover and pack.cover.exists():
                name = f"covers/{catalogue.slug(pack.folder.rsplit('.', 1)[0])}.jpg"
                subprocess.run([str(images), "fit", "480", str(out / name), str(pack.cover)], check=True)
                entry["cover"] = name
            manifest_packs.append(entry)
        for thumb in sorted(thumbs):
            source = catalogue.CATALOGUE / thumb
            if source.exists():
                shutil.copyfile(source, out / thumb)

        manifest_bundles = bundles(packs)
        covers_of = {p["id"]: p.get("cover") for p in manifest_packs}
        for bundle in manifest_bundles:
            members = [str(out / covers_of[i]) for i in bundle["packs"] if covers_of.get(i)][:9]
            if members:
                name = f"covers/bundle-{bundle['id']}.jpg"
                subprocess.run([str(images), "cover", "480", str(out / name)] + members, check=True)
                bundle["cover"] = name

        manifest = {"version": MANIFEST_VERSION, "catalogue": version, "name": "Spatial GM Adventures",
                    "collections": catalogue.COLLECTIONS, "packs": manifest_packs, "bundles": manifest_bundles,
                    "archives": archives}
        (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        write_index(out, manifest, "Spatial GM Adventures")

    total = sum(a["bytes"] for a in archives)
    print(f"{len(packs)} packs, {len(archives)} archives ({size_text(total)}), {len(new)} new → {out.relative_to(ROOT)}/")
    for pack in manifest_packs:
        if pack["collection"] in ("adventures", "kits", "heroes"):
            print(f"  {pack['name']}: {pack['fileCount']} files, {size_text(pack['bytes'])}")


if __name__ == "__main__":
    main()
