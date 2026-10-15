with open("/Users/jcolley/surf_clock/generate_te_4k_plates.py", "r") as f:
    code = f.read()

code = code.replace("from playwright.sync_api import sync_playwright", "import subprocess\nfrom PIL import Image")

old_main = '''def main():
    with open(MANIFEST_PATH, "r") as f:
        man = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)

            for cid, (idx, fn_html) in CHAPTER_HTML_BUILDERS.items():'''

new_main = '''def main():
    with open(MANIFEST_PATH, "r") as f:
        man = json.load(f)

    for cid, (idx, fn_html) in CHAPTER_HTML_BUILDERS.items():
        full_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{CSS_COMMON}</style></head>
<body>
  <div class="grain-overlay"></div>
  {build_topbar_html(idx)}
  <main class="workspace-grid">
    <div class="viewport-frame"></div>
    <div class="schematic-sheet">
      {fn_html()}
    </div>
  </main>
</body>
</html>"""
        tmp_html = f"/tmp/te_plate_{cid}.html"
        with open(tmp_html, "w") as hf:
            hf.write(full_html)
        out_png = os.path.join(OUT_DIR, f"plate_{cid}_4k.png")
        subprocess.run(["/tmp/render_html_4k", tmp_html, out_png, "1920", "1080"], check=True)
        print(f"Rendered 4K plate: {out_png}")

    # Render all unique subtitle pills in a single 2x Retina sheet and slice them!
    all_subs = []
    for ch in man["chapters"]:
        for _, _, stxt in ch["cards"]:
            if stxt not in all_subs:
                all_subs.append(stxt)

    row_h = 72
    total_h = len(all_subs) * row_h
    rows_html = []
    for stxt in all_subs:
        rows_html.append(f'<div class="sub-row"><div class="sub-pill"><span class="sub-dot"></span><span>{stxt}</span></div></div>')

    sheet_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700&display=swap');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  width: 1920px; height: {total_h}px; background: transparent;
  -webkit-font-smoothing: antialiased;
}}
.sub-row {{
  width: 1920px; height: {row_h}px;
  display: flex; align-items: center; justify-content: center;
}}
.sub-pill {{
  background: #111111;
  color: #FFFFFF;
  font-family: 'Inter', -apple-system, sans-serif;
  font-size: 21px;
  font-weight: 600;
  letter-spacing: -0.01em;
  padding: 10px 28px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 6px 18px rgba(17, 17, 17, 0.14);
}}
.sub-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #FF4F00;
  flex-shrink: 0;
}}
</style></head>
<body>
{''.join(rows_html)}
</body></html>"""
    tmp_sh = "/tmp/te_sub_sheet.html"
    with open(tmp_sh, "w") as sf:
        sf.write(sheet_html)
    sheet_png = os.path.join(OUT_DIR, "sub_sheet_4k.png")
    subprocess.run(["/tmp/render_html_4k", tmp_sh, sheet_png, "1920", str(total_h)], check=True)
    im_sheet = Image.open(sheet_png).convert("RGBA")
    sub_map = {}
    for s_idx, stxt in enumerate(all_subs):
        y0 = s_idx * row_h * 2
        y1 = (s_idx + 1) * row_h * 2
        crop = im_sheet.crop((0, y0, 3840, y1))
        sp_png = os.path.join(OUT_DIR, f"sub_{s_idx:03d}_4k.png")
        crop.save(sp_png)
        sub_map[stxt] = sp_png

    with open(os.path.join(OUT_DIR, "sub_map.json"), "w") as mf:
        json.dump(sub_map, mf, indent=2)
    print(f"Rendered and sliced {len(sub_map)} 4K subtitle pills")

if __name__ == "__main__":
    main()
'''

idx_start = code.index("def main():")
code = code[:idx_start] + new_main
with open("/Users/jcolley/surf_clock/generate_te_4k_plates.py", "w") as f:
    f.write(code)
print("Patched generate_te_4k_plates.py")
