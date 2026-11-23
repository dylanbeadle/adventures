# Spatial GM Adventures

The official catalogue for **Spatial GM**: adventures, kits and heroes for the table, and the media
packs they share — the sounds and the room moods. Published at
<https://dylanbeadle.github.io/adventures/> and downloaded by the app (Downloads on the Mac, Vision Pro,
iPhone and iPad).

## What's here

| Folder | What | Published as |
|---|---|---|
| `adventures/` | Campaigns to play (`.spatialgm`): Demo. The Empty template is built into the app. | one pack each |
| `kits/` | Tiles, Props and Creatures Kit (`.spatialgm`): the 3DAssets library's USD files sharing one material library; the app packages a piece when it's used (D146). Made with 3DAssets' `scripts/export_spatialgm_kit.py --kit <kind> --sources`. | one pack each, and one per group (52: Tavern Tiles, Furniture Props, Undead Creatures…) |
| `heroes/` | Pre-made heroes (`.spatialhero`), idle animation only, textures compressed (`scripts/make-hero-model.swift`). | one pack each, and the All Heroes bundle |
| `sounds/` | Core Sounds (`.spatialgm`, `kind: sounds`): the SoundFont the generated music plays on, and the table's sound effects. Media only — a pack campaigns require, never offered as something to play. | one pack, required by the Demo |
| `moods/` | Core Moods (`.spatialgm`, `kind: moods`): room moods — Candlelight, Fog, Rolling Fog and Storm. Each is a document, a compiled `.reality` and the JavaScript that moves it. | one pack, required by the Demo |
| `catalogue/` | Each kit piece's thumbnail (`thumbs/`) and each group's cover (`covers/`), made by `scripts/make-images.py`. `default.jpg` is the cover a pack without one of its own gets. | the site and the app's browser |
| `docs/` | GitHub Pages, written by the Action: `manifest.json`, `index/`, `packs/`, `covers/`, `thumbs/`, `index.html`. | |
| `scripts/` | Everything that builds the catalogue (below). | |
| `.github/workflows/` | The Action that builds `docs/` and publishes a release (below). | |
| `VERSION` | The catalogue's version, written into the manifest's `catalogue` field. | |

A kit's groups are the rows of the `| Group | Tag | Pieces |` table in its `campaign.md`; a piece belongs to the group its model's folder names (`media/tiles/Tavern/…`). A group pack is a complete kit of its own: its pieces, their models, the shared material library, a generated `campaign.md` and its cover.

## Packs that carry media, not an adventure (D178, D180)

`adventures/`, `kits/` and `heroes/` hold things to play with. `sounds/` and `moods/` hold media that
other packs use, and are installed like any other pack. A campaign finds one through its `requires:`
line, which names the pack's folder in lower case with hyphens — `CoreSounds.spatialgm` is
`core-sounds`, `CoreMoods.spatialgm` is `core-moods` — and that pack's `media/…` paths are then found
as if they were in the campaign's own folder. The Demo requires both.

### Core Sounds

- `media/instruments/orchestra.sf2` — the GeneralUser GS SoundFont (7.2 MB) the generated music is
  rendered on (D79), with its licence beside it. The Demo's `instruments:` points at this file
  through `requires:`.
- `media/sounds/` — 26 takes of 12 effects: beast growl, coins, door creak, draw sword, footsteps,
  giant, rockfall, shade, spell, sword clash, sword swing and thunder. Mono, 48 kHz, silence trimmed,
  peak −1 dBFS, AAC 64 kb/s, all CC0. `PROVENANCE.md` gives every take's source and licence; the app
  repository's `Scripts/prepare-sounds.py` makes them from `Scripts/sound-effects.tsv`.
- `cover.jpg`.

### Core Moods

Four moods, each a document in `moods/`, a compiled scene in `media/moods/` and a script beside the
document:

| Mood | Document | Scene | Script | What it adds |
|---|---|---|---|---|
| Candlelight | `moods/candlelight.md` | `candlelight.reality` | `candlelight.js` | Embers and two flickering lights; the script sets the particle parameters, which USD can't author. |
| Fog | `moods/fog.md` | `fog.reality` | `fog.js` | A shader-graph sea of mist that damps the room's reverb. |
| Rolling Fog | `moods/rolling-fog.md` | `rolling-fog.reality` | `rolling-fog.js` | A solved, baked fog volume sampled as eight drifting height slices: deeper than Fog, with a warm glow over the table. The script sets the same dry reverb and its Shader Graph inputs — density, coverage, loop speed and phase, warmth, glow, texture LOD bias, brightness, a density floor and a wisp field. |
| Storm | `moods/storm.md` | `storm.reality` | `storm.js` | Rain, with `lightning: true` and `audio: media/moods/thunder.m4a`. |

A mood document's front matter is what the app reads (D180):

| Key | What |
|---|---|
| `id` | What `mood:` in an encounter, cutscene or node names. `candlelight` and `storm` **replace** the app's built-ins of the same id; any other id adds a mood. |
| `name`, `symbol` | The mood's name and its SF Symbol. |
| `scene` | The compiled `.reality`, relative to the pack. Without one, the app draws the mood itself. |
| `script` | The `.js` that moves the scene, relative to the pack. Without one, the app animates it. |
| `tint`, `dim` | The room's passthrough tint (`#RRGGBB`) and how far it dims, 0 to 1. |
| `sound` | A built-in soundscape voice to play with the mood: `fire`, `wind` or `storm` here. |
| `lightning` | Flash the room like lightning. The passthrough tint is the app's to drive, so a mood asks for a flash rather than scripting one. |
| `audio` | A sound placed above the table, a beat after each flash (the storm's thunder). |
| `environment` | An equirectangular image (`.exr`, `.hdr`, `.png`) whose light falls on the scene. Unused so far. |

- The scenes are built in the app repository: `Experiments/MoodScripting/Moods/build.sh` checks each
  `src/<id>.rkassets` with `usdchecker --arkit` and compiles it with
  `realitytool compile --platform xros --deployment-target 27.0`. Fog's USD is generated first by
  `src/fog.rkassets/make_fog.py` (`Fog.spatialgm/build.sh`). Rolling Fog's is `src/fog-bank.rkassets`:
  `build.sh` runs the fluid solve, bakes eight height slices and their four time keys, writes the
  scene and compiles it. This repository keeps the compiled `.reality` only — never hand-edit one, it
  won't load. Rebuild in the app repository, copy the pack in, then run the build here.
- Rolling Fog's nine Shader Graph inputs are set from `moods/rolling-fog.js` — the `FOG` object at the
  top is the tuning surface, so thickness, floor, brightness, loop speed, phase, warmth and glow can
  change without rebuilding the `.reality`. The eight slice heights and the 12 s bake are the only
  things the script cannot change. In a Debug build the app watches the mood's `.reality` and `.js`
  (size and modification date) and re-dresses when either changes, and a pinch-and-hold on a mood tile
  opens a Mood Tuning window whose sliders write any float Shader Graph input live — Fog's `Density`
  and `Billow` as well as Rolling Fog's inputs.
- Thunder is a copy of Core Sounds' `thunder-1.m4a` (same bytes), because a pack never reads another
  pack's files (D147).
- The pack has no `cover:` yet, so the site and the app show `catalogue/covers/default.jpg`
  (published as `covers/coremoods.jpg`).

## How packs share files (D147)

Every pack is a self-contained folder; nothing refers to another pack. Sharing happens by content instead:

- The build lists each pack's files with their SHA-256 (`packs/<pack hash>.json`, with its pieces and thumbnails for browsing).
- Files are grouped by the set of packs that use them, into archives named by their contents (`<id>.aar`, LZFSE Apple Archive, each file stored flat under its hash). The Tavern Tiles group needs three: its own `campaign.md` and cover, the Tavern models it shares with the Tiles Kit, and the material library every kit and group shares.
- The app keeps one store of files by hash, downloads only the archives holding files it lacks, verifies every file, and builds the pack's folder from the store. Downloading Tavern Tiles and then the Tiles Kit fetches only what's new; deleting one keeps what the other uses.
- An archive is published once and keeps its URL: a release uploads only archives whose contents are new.

`index/<sha256>.json` (named in the manifest's `index`) lists every pack's metadata and every kit piece (tags, `same-as` id, size, footprint, packs, files) and where each piece's files are in the blobs (`<sha256>.blob`: files DEFLATEd one by one and laid end to end; each release's blob holds only new files). The app searches with it and fetches single pieces with HTTP Range requests.

`manifest.json` (version 2) lists `collections` (Adventures, Sounds, Moods, Heroes, Kits › Tiles, Props, Creatures), `packs` (id, kind `campaign` or `hero`, collection, name, folder, hash, files, bytes, cover, summary, tags, `partOf` for a group's kit), `bundles` (All Heroes, Every Kit) and `archives` (id, url, bytes, sha256, contains). Every URL is relative to the manifest, except archives published in releases.

## Building

- `python3 scripts/build-distribution.py` writes a complete catalogue to `dist/` (ignored): the manifest, archives, pack lists, covers, thumbnails and site. Add `dist/` (or a copy of it in iCloud Drive) to the app as a source to try it before publishing.
- Everything is found on disk, never listed: each `*.spatialgm` in `adventures/`, `sounds/` and `moods/`, each kit and each of its groups in `kits/`, and each `*.spatialhero` in `heroes/`. Needs macOS 27 (USDKit), which cooks the kit models.
- With `RELEASE_TAG` (and `GITHUB_REPOSITORY`) it writes `docs/` for Pages instead, and puts the new archives and the blob in `dist/release/`: the Action's mode.
- The Action (`.github/workflows/package-and-release.yml`) runs it with `RELEASE_TAG` on every push to `adventures/`, `sounds/`, `moods/`, `kits/`, `catalogue/`, `heroes/`, `scripts/` or the workflow: it writes `docs/`, commits it, and publishes a release with the new archives.
- `python3 scripts/make-images.py [--assets <3DAssets>] [--force]` makes missing thumbnails and covers (`--force` remakes them; a remade cover changes its pack).
- `xcrun swift scripts/make-hero-model.swift <source.usdz> <out.usdz> [clip]` makes a hero's model from a 3DAssets hero master.
- Check a folder with the app's checker before pushing: `Scripts/check-campaign.sh <folder>` in the Spatial GM repository.

### The scripts

| Script | What it does |
|---|---|
| `build-distribution.py` | The build: packs, content-named archives, blobs and index, manifest, covers and site. Writes `dist/`, or `docs/` and `dist/release/` with `RELEASE_TAG`. |
| `catalogue.py` | The vocabulary the two Python tools share: front matter, what a kit's pieces and groups are and which files a group uses, the collection list, and where covers and thumbnails live. |
| `make-images.py` | Thumbnails (`catalogue/thumbs/`, 160 px) and covers (`catalogue/covers/`, 480 px; the big kits' own `cover.jpg`). |
| `images.swift` | The image tool those two compile and run: `thumbs`, `cover` and `fit` with ImageIO, square, on the catalogue's dark backdrop so a transparent render reads on light and dark pages. |
| `make-hero-model.swift` | One hero model: one clip (`Idle` by default), Y-up metres, AVIF textures, the same bytes every run. |
| `model-cook.swift` | **Generated, don't edit.** The tool that cooks kit models (below). |
| `model-cook 2.swift` | A duplicate of `model-cook.swift`, byte for byte. Nothing reads it. Delete it. |

### Model cooking (D154)

A kit's models are source layers that read one shared material library. Cooking turns each into what a
device can use without USD: a flattened, Y-up, metre-scale layer with its textures copied beside it
and the materials nothing binds removed, then one binary layer packaged with AVIF textures. The
published pack holds the layer at its `model:` path and a `<name>.cooked/` folder beside it (its
textures and a `cooked.txt` with the cook version), so a device puts the package back together from
files alone (D154).

The build cooks only what changed. A cache in `$COOK_CACHE` (default `~/Library/Caches/SpatialGM-Cook`)
is keyed by the tool, the material library and the source layer. It compiles `scripts/model-cook.swift`
with `swiftc -O -enable-bare-slash-regex` and runs up to eight copies, each fed one job per line on
standard input:

```
<source layer>	<layer to write>	<cooked folder to write>
```

A line that fails is reported and the rest carry on; the exit code is 1 if any did. A Gaussian splat
source skips the flattening and is packaged as it stands (D152).

**`model-cook.swift` is generated, never edited.** The app repository is private and not linked to
this one, so the Action can't build the app's package. `Scripts/gen-model-cook.sh` there joins the
app's own `USDZArchive.swift`, `ModelCook.swift` and `model-cook/main.swift` into this one file:

```
Scripts/gen-model-cook.sh Content/scripts/model-cook.swift
```

Change the cooking in the app, run that, and commit the result. Any change to the file changes the
Action's `cook-` cache key, so the next release cooks every model again.

**`model-cook 2.swift` is that same file twice.** It is byte-for-byte identical to `model-cook.swift`
— a duplicate left by a Finder or iCloud Drive copy, not a second tool. Nothing reads it: the build
compiles `scripts/model-cook.swift` and the Action's cache key hashes that path. Regenerate one file;
delete the duplicate (`git rm "scripts/model-cook 2.swift"`) so there is only ever one copy to keep in
step.

## GitHub Pages

Settings › Pages: deploy from branch `main`, folder `/docs`. The catalogue is then at `https://dylanbeadle.github.io/adventures/manifest.json`.

## Git LFS

Models, pictures, sounds, instruments and videos are in Git LFS (`.gitattributes`); `docs/` stays in plain git because Pages can't serve LFS files. Install it once with `git lfs install`. The Action caches LFS objects between runs. To clone without the binaries: `GIT_LFS_SKIP_SMUDGE=1 git clone …`, then `git lfs pull --include "heroes/**"` for what you need.
