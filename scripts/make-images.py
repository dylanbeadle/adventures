#!/usr/bin/env python3
"""Makes the catalogue's images (committed, so builds never need the 3DAssets library):

  python3 scripts/make-images.py [--assets <3DAssets folder>] [--force]

- With --assets: each kit piece's thumbnail, `catalogue/thumbs/<TaleSpire id>.jpg` (160 px), from
  3DAssets' `previews/<tiles|props|creatures>/<id>.png`.
- Each kit group's cover, `catalogue/covers/<group slug>.jpg`, and each big kit's `cover.jpg`
  (480 px, nine of its pieces), from the thumbnails.

Existing images are kept unless --force: a cover's bytes are part of its pack, so remaking it would
change the pack's hash and publish a new archive.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalogue  # noqa: E402

KIND_FOLDERS = {"Tiles Kit": "tiles", "Props Kit": "props", "Creatures Kit": "creatures"}


def tool(work: Path) -> Path:
    out = work / "images"
    subprocess.run(["xcrun", "swiftc", "-O", str(catalogue.ROOT / "scripts/images.swift"), "-o", str(out)], check=True)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, help="the 3DAssets folder, to import thumbnails")
    parser.add_argument("--force", action="store_true", help="remake existing images")
    args = parser.parse_args()
    kits = catalogue.kits()
    with tempfile.TemporaryDirectory() as temp:
        images = tool(Path(temp))
        if args.assets:
            for kit in kits:
                previews = args.assets / "previews" / KIND_FOLDERS[kit.name]
                # A piece's preview: by TaleSpire id, or (the original roof and door) by model name in its kit's folder.
                wanted = [(previews / f"{p.talespire}.png" if p.talespire else
                           args.assets / "kits" / p.model.split("/")[1] / "previews" / f"{Path(p.model).stem}.png", p.thumb)
                          for g in kit.groups for p in g.pieces]
                todo = [(src, name) for src, name in wanted
                        if src.exists() and (args.force or not (catalogue.THUMBS / f"{name}.jpg").exists())]
                missing = [src.name for src, _ in wanted if not src.exists()]
                with tempfile.TemporaryDirectory() as named:
                    # Named as the thumbnail will be (the tool keeps the input's name).
                    links = []
                    for src, name in todo:
                        link = Path(named) / f"{name}.png"
                        link.symlink_to(src)
                        links.append(str(link))
                    for i in range(0, len(links), 200):
                        subprocess.run([str(images), "thumbs", "160", str(catalogue.THUMBS)] + links[i:i + 200], check=True)
                print(f"{kit.name}: {len(todo)} thumbnails made, {len(missing)} pieces without a preview")
        for kit in kits:
            for group in kit.groups:
                out = catalogue.COVERS / f"{group.slug}.jpg"
                pieces = catalogue.cover_pieces(group.pieces, 9)
                if pieces and (args.force or not out.exists()):
                    subprocess.run([str(images), "cover", "480", str(out)] +
                                   [str(catalogue.THUMBS / f"{p.thumb}.jpg") for p in pieces], check=True)
            # The big kit's cover: one piece from each of nine groups, spread through the kit.
            out = kit.folder / "cover.jpg"
            firsts = [catalogue.cover_pieces(g.pieces, 1) for g in kit.groups]
            firsts = [f[0] for f in firsts if f]
            chosen = catalogue.cover_pieces(firsts, 9)
            if chosen and (args.force or not out.exists()):
                subprocess.run([str(images), "cover", "480", str(out)] +
                               [str(catalogue.THUMBS / f"{p.thumb}.jpg") for p in chosen], check=True)
            print(f"{kit.name}: covers for {len(kit.groups)} groups and the kit")


if __name__ == "__main__":
    main()
