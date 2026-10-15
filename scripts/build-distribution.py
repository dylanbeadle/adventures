#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import subprocess
import shutil
from pathlib import Path

def parse_frontmatter(file_path):
    metadata = {}
    body = []
    if not file_path.exists():
        return metadata, ""
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    in_fm = False
    fm_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                in_fm = False
                continue
        if in_fm:
            fm_lines.append(line)
        else:
            if not stripped.startswith("#"):
                body.append(stripped)
            
    for line in fm_lines:
        line_clean = line.split("#")[0].strip()
        if ":" in line_clean:
            key, val = line_clean.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            metadata[key] = val
            
    body_text = " ".join([b for b in body if b]).strip()
    return metadata, body_text

def sha256_of_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    root = Path(__file__).resolve().parent.parent
    campaigns_dir = root / "campaigns"
    dist_dir = root / "dist"
    docs_dir = root / "docs"
    covers_dir = docs_dir / "covers"
    
    dist_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)
    
    run_num = os.environ.get("GITHUB_RUN_NUMBER", "1")
    tag = os.environ.get("RELEASE_TAG", f"v1.0.{run_num}")
    repo = os.environ.get("GITHUB_REPOSITORY", "dylanbeadle/adventures")
    
    manifest_campaigns = []
    
    campaign_dirs = sorted([d for d in campaigns_dir.glob("*.spatialgm") if d.is_dir()])
    print(f"Found {len(campaign_dirs)} campaigns in {campaigns_dir}.")
    
    for c_dir in campaign_dirs:
        campaign_md = c_dir / "campaign.md"
        meta, body_text = parse_frontmatter(campaign_md)
        
        name = meta.get("name", c_dir.stem)
        cid = meta.get("id", "")
        summary = meta.get("summary") or body_text or f"{name} adventure."
        version = meta.get("version", "1.0.0")
        is_template = meta.get("template", "true").lower() == "true"
        opens_first = meta.get("opens-first", "false").lower() == "true"
        
        aar_name = f"{c_dir.name}.aar"
        aar_path = dist_dir / aar_name
        
        print(f"Archiving {c_dir.name} -> {aar_name}...")
        subprocess.run(["/usr/bin/aa", "archive", "-d", str(c_dir), "-o", str(aar_path)], check=True)
        
        byte_size = aar_path.stat().st_size
        sha256 = sha256_of_file(aar_path)
        
        # Check for cover image
        cover_url = None
        cover_rel = meta.get("cover")
        if cover_rel and (c_dir / cover_rel).exists():
            cover_src = c_dir / cover_rel
            dest_cover = covers_dir / f"{c_dir.stem}-cover{cover_src.suffix}"
            shutil.copy2(cover_src, dest_cover)
            cover_url = f"https://dylanbeadle.github.io/adventures/covers/{dest_cover.name}"
        elif (covers_dir / "demo-cover.png").exists() and "demo" in c_dir.name.lower():
            cover_url = "https://dylanbeadle.github.io/adventures/covers/demo-cover.png"
            
        download_url = f"https://github.com/{repo}/releases/download/{tag}/{aar_name}"
        
        entry = {
            "id": cid,
            "name": name,
            "version": version,
            "url": download_url,
            "sha256": sha256,
            "byteSize": byte_size,
            "isTemplate": is_template,
            "opensFirst": opens_first,
            "summary": summary
        }
        if cover_url:
            entry["coverURL"] = cover_url
            
        manifest_campaigns.append(entry)
        print(f"  ✓ {name}: {byte_size} bytes, sha256={sha256[:12]}...")

    manifest = {
        "version": 1,
        "campaigns": manifest_campaigns
    }
    
    manifest_path = docs_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote manifest to {manifest_path}")

    # Generate human synopsis index.html
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Spatial GM — Adventures & Campaigns</title>
  <style>
    :root {{
      --bg: #0d0f12;
      --card-bg: #161a20;
      --text: #e6edf3;
      --text-muted: #8b949e;
      --accent: #3373f2;
      --border: #30363d;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 0;
      line-height: 1.5;
    }}
    header {{
      padding: 48px 24px 32px;
      text-align: center;
      border-bottom: 1px solid var(--border);
      background: radial-gradient(circle at 50% 0%, #1c2638, transparent 70%);
    }}
    h1 {{
      font-size: 32px;
      font-weight: 700;
      margin: 0 0 12px;
      letter-spacing: -0.5px;
    }}
    p.lead {{
      font-size: 16px;
      color: var(--text-muted);
      max-width: 600px;
      margin: 0 auto;
    }}
    .manifest-badge {{
      display: inline-block;
      margin-top: 16px;
      padding: 6px 14px;
      background: rgba(51, 115, 242, 0.15);
      border: 1px solid rgba(51, 115, 242, 0.4);
      color: #58a6ff;
      border-radius: 20px;
      font-size: 13px;
      text-decoration: none;
      transition: background 0.15s ease;
    }}
    .manifest-badge:hover {{
      background: rgba(51, 115, 242, 0.25);
    }}
    main {{
      max-width: 1080px;
      margin: 40px auto;
      padding: 0 24px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 24px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: #58a6ff;
    }}
    .card-cover {{
      width: 100%;
      height: 160px;
      background: #1f242c;
      object-fit: cover;
    }}
    .cover-placeholder {{
      width: 100%;
      height: 160px;
      background: linear-gradient(135deg, #1f293d, #141822);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      font-size: 40px;
    }}
    .card-body {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}
    .card-title {{
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 6px;
    }}
    .card-meta {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      gap: 8px;
      align-items: center;
    }}
    .pill {{
      background: #21262d;
      padding: 2px 8px;
      border-radius: 6px;
    }}
    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 18px;
      flex-grow: 1;
    }}
    .btn {{
      display: inline-block;
      text-align: center;
      padding: 8px 14px;
      background: var(--accent);
      color: #fff;
      border-radius: 8px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      transition: background 0.15s ease;
    }}
    .btn:hover {{
      background: #285ec4;
    }}
    footer {{
      text-align: center;
      padding: 40px 24px;
      font-size: 13px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      margin-top: 60px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Spatial GM Adventures & Campaigns</h1>
    <p class="lead">Official and community campaign packages for Spatial GM on Apple Vision Pro and Mac.</p>
    <a class="manifest-badge" href="manifest.json">View manifest.json</a>
  </header>
  <main>
    <div class="grid">
"""
    for c in manifest_campaigns:
        size_mb = f"{c['byteSize'] / 1024 / 1024:.1f} MB" if c['byteSize'] >= 1048576 else f"{c['byteSize'] / 1024:.0f} KB"
        cover_html = f'<img class="card-cover" src="{c["coverURL"]}" alt="{c["name"]}">' if c.get("coverURL") else '<div class="cover-placeholder">🎲</div>'
        html += f"""      <div class="card">
        {cover_html}
        <div class="card-body">
          <div class="card-title">{c["name"]}</div>
          <div class="card-meta">
            <span class="pill">v{c["version"]}</span>
            <span class="pill">{size_mb}</span>
          </div>
          <div class="card-desc">{c["summary"]}</div>
          <a class="btn" href="{c["url"]}">Download Package</a>
        </div>
      </div>
"""
    html += """    </div>
  </main>
  <footer>
    <p>Published with GitHub Pages &bull; Formatted for Spatial GM</p>
  </footer>
</body>
</html>
"""
    index_path = docs_dir / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote synopsis site to {index_path}")

if __name__ == "__main__":
    main()
