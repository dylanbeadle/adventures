# Spatial GM Adventures

The official catalogue for **Spatial GM**: adventures, kits and heroes, published at
<https://dylanbeadle.github.io/adventures/> and downloaded by the app (Downloads on the Mac, Vision Pro, iPhone and iPad).

## What's here

| Folder | What | Published as |
|---|---|---|
| `adventures/` | Campaigns to play (`.spatialgm`): Demo. The Empty template is built into the app. | one pack each |
| `kits/` | Tiles, Props and Creatures Kit (`.spatialgm`): the 3DAssets library's USD files sharing one material library; the app packages a piece when it's used (D146). Made with 3DAssets' `scripts/export_spatialgm_kit.py --kit <kind> --sources`. | one pack each, and one per group (52: Tavern Tiles, Furniture Props, Undead Creatures…) |
| `heroes/` | Pre-made heroes (`.spatialhero`), idle animation only, textures compressed (`scripts/make-hero-model.swift`). | one pack each, and the All Heroes bundle |
| `catalogue/` | Each kit piece's thumbnail (`thumbs/`) and each group's cover (`covers/`), made by `scripts/make-images.py`. | the site and the app's browser |
| `docs/` | GitHub Pages, written by the Action: `manifest.json`, `packs/`, `covers/`, `thumbs/`, `index.html`. | |
| `scripts/` | Everything that builds the catalogue (below). | |

A kit's groups are the rows of the `| Group | Tag | Pieces |` table in its `campaign.md`; a piece belongs to the group its model's folder names (`media/tiles/Tavern/…`). A group pack is a complete kit of its own: its pieces, their models, the shared material library, a generated `campaign.md` and its cover.

## How packs share files (D147)

Every pack is a self-contained folder; nothing refers to another pack. Sharing happens by content instead:

- The build lists each pack's files with their SHA-256 (`packs/<pack hash>.json`, with its pieces and thumbnails for browsing).
- Files are grouped by the set of packs that use them, into archives named by their contents (`<id>.aar`, LZFSE Apple Archive, each file stored flat under its hash). The Tavern Tiles group needs three: its own `campaign.md` and cover, the Tavern models it shares with the Tiles Kit, and the material library every kit and group shares.
- The app keeps one store of files by hash, downloads only the archives holding files it lacks, verifies every file, and builds the pack's folder from the store. Downloading Tavern Tiles and then the Tiles Kit fetches only what's new; deleting one keeps what the other uses.
- An archive is published once and keeps its URL: a release uploads only archives whose contents are new.

`manifest.json` (version 2) lists `collections` (Adventures, Heroes, Kits › Tiles, Props, Creatures), `packs` (id, kind `campaign` or `hero`, collection, name, folder, hash, files, bytes, cover, summary, tags, `partOf` for a group's kit), `bundles` (All Heroes, Every Kit) and `archives` (id, url, bytes, sha256, contains). Every URL is relative to the manifest, except archives published in releases.

## Building

- `python3 scripts/build-distribution.py` writes a complete catalogue to `dist/` (ignored): the manifest, archives, pack lists, covers, thumbnails and site. Add `dist/` (or a copy of it in iCloud Drive) to the app as a source to try it before publishing.
- The Action (`.github/workflows/package-and-release.yml`) runs it with `RELEASE_TAG` on every push to `adventures/`, `kits/`, `heroes/`, `catalogue/` or `scripts/`: it writes `docs/`, commits it, and publishes a release with the new archives.
- `python3 scripts/make-images.py [--assets <3DAssets>]` makes missing thumbnails and covers (`--force` remakes them; a remade cover changes its pack).
- `xcrun swift scripts/make-hero-model.swift <source.usdz> <out.usdz> [clip]` makes a hero's model from a 3DAssets hero master.
- Check a folder with the app's checker before pushing: `Scripts/check-campaign.sh <folder>` in the Spatial GM repository.

## GitHub Pages

Settings › Pages: deploy from branch `main`, folder `/docs`. The catalogue is then at `https://dylanbeadle.github.io/adventures/manifest.json`.

## Git LFS

Models, pictures, sounds, instruments and videos are in Git LFS (`.gitattributes`); `docs/` stays in plain git because Pages can't serve LFS files. Install it once with `git lfs install`. The Action caches LFS objects between runs. To clone without the binaries: `GIT_LFS_SKIP_SMUDGE=1 git clone …`, then `git lfs pull --include "heroes/**"` for what you need.
