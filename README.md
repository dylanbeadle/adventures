# Spatial GM Adventures & Campaigns

Source repository for official and community campaign packages for **Spatial GM** on Apple Vision Pro and Mac.

## Repository Structure

* **`adventures/`**: Campaigns to play (`.spatialgm` folders: Markdown files with YAML front matter, models, pictures and audio): Starter, Demo. (The Empty template is built into the app.)
* **`library/`**: My Library, pieces shared across campaigns.
* **`kits/`**: Building blocks (Tiles, Props, Creatures Kit): the 3DAssets library's USD files with one material library each; Spatial GM makes each piece's USDZ when it is used (D146). Made with 3DAssets' `scripts/export_spatialgm_kit.py --kit <kind> --sources`.
* **`heroes/`**: Pre-made player heroes (`.spatialhero` folders), listed under `heroes` in the manifest.
* **`docs/`**: GitHub Pages web root containing `manifest.json`, campaign cover images, and the web synopsis portal.
* **`scripts/`**: Automation scripts to package campaigns into `.spatialgm.aar` (Apple Archive with LZFSE) and build the manifest.

## Automated Pipeline (GitHub Actions)

Pushing changes to `adventures/`, `library/`, `kits/` or `heroes/` automatically triggers the GitHub Action (`.github/workflows/package-and-release.yml`), which:
1. Validates each campaign folder.
2. Packages each `.spatialgm` and `.spatialhero` that changed since the last release into a compressed `.aar` using `/usr/bin/aa` (without `.DS_Store` and `.cache/`); unchanged ones keep their archive and URL (`sourceHash` in the manifest).
3. Computes cryptographic SHA-256 hashes and byte counts.
4. Updates `docs/manifest.json` and the web portal `docs/index.html`.
5. Creates a versioned GitHub Release and attaches the `.aar` packages.

## Enabling GitHub Pages

1. Go to **Settings › Pages**.
2. Under **Build and deployment › Source**, select **Deploy from a branch**.
3. Branch: **`main`**, folder: **`/docs`**.
4. Save. Your manifest will be live at `https://dylanbeadle.github.io/adventures/manifest.json`.

## Building locally

`python3 scripts/build-distribution.py` writes the archives to `dist/` (ignored) and the manifest and site to `docs/`, exactly as the Action does. Set `RELEASE_TAG` to the release the manifest's URLs should point at. Check a folder with the app's checker first (`Scripts/check-campaign.sh <folder>` in the Spatial GM repo).

## Git LFS

Models, pictures, sounds, instruments and videos are stored in Git LFS (`.gitattributes`); `docs/` stays in plain git because GitHub Pages can't serve LFS files. Install it once with `git lfs install`. The Action caches LFS objects between runs. To clone without the binaries: `GIT_LFS_SKIP_SMUDGE=1 git clone …`, then `git lfs pull --include "adventures/Demo.spatialgm/**"` for what you need.
