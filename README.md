# Spatial GM Adventures & Campaigns

Source repository for official and community campaign packages for **Spatial GM** on Apple Vision Pro and Mac.

## Repository Structure

* **`campaigns/`**: Source `.spatialgm` folders containing Markdown files, YAML front matter, 3D miniatures, and audio.
* **`docs/`**: GitHub Pages web root containing `manifest.json`, campaign cover images, and the web synopsis portal.
* **`scripts/`**: Automation scripts to package campaigns into `.spatialgm.aar` (Apple Archive with LZFSE) and build the manifest.

## Automated Pipeline (GitHub Actions)

Pushing changes to `campaigns/` automatically triggers the GitHub Action (`.github/workflows/package-and-release.yml`), which:
1. Validates each campaign folder.
2. Packages each `.spatialgm` into a compressed `.spatialgm.aar` using `/usr/bin/aa`.
3. Computes cryptographic SHA-256 hashes and byte counts.
4. Updates `docs/manifest.json` and the web portal `docs/index.html`.
5. Creates a versioned GitHub Release and attaches the `.aar` packages.

## Enabling GitHub Pages

1. Go to **Settings › Pages**.
2. Under **Build and deployment › Source**, select **Deploy from a branch**.
3. Branch: **`main`**, folder: **`/docs`**.
4. Save. Your manifest will be live at `https://dylanbeadle.github.io/adventures/manifest.json`.
