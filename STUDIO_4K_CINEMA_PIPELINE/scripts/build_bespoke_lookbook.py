import os, time

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
STILLS_DIR = f"{BASE}/01_4K_STUDIO_KEYFRAMES_AND_STILLS"
CLIPS_DIR = f"{BASE}/02_INDIVIDUAL_4K_CLIPS_16x9"
OUT_HTML = f"{BASE}/00_BESPOKE_STUDIO_COLLECTION_LOOKBOOK.html"

COLLECTION = [
    {
        "id": "CS_01",
        "file_stem": "V8_050_ZERO_GRAVITY_Three_Colorways_Floating_ZeroG_Constellation",
        "region": "3-UP GLOBAL EDITION • SF / HAWAII / PORTUGAL",
        "beaches": "SF (Ocean Beach) • Hawaii (Pipeline) • Portugal (Coxos)",
        "colorway": "Sea-Kelp Green / Slate-Blue / Warm Limestone Cream",
        "studio": "Warm Sand Plaster Cyclorama • Zero-Gravity Trio"
    },
    {
        "id": "CS_02",
        "file_stem": "CS_02_SAN_FRANCISCO_OCEAN_BEACH_SeaKelp_Dark_Tonal_Slate_Stone",
        "region": "SAN FRANCISCO • NORCAL",
        "beaches": "BOLINAS • SLOAT • OCEAN BEACH • FORT POINT • PACIFICA",
        "colorway": "Monochrome Matte Sea-Kelp Forest Green",
        "studio": "Dark Tonal Forest-Charcoal Backdrop & Honed Slate Stone"
    },
    {
        "id": "CS_03",
        "file_stem": "CS_03_PORTUGAL_ERICEIRA_Warm_Sand_Travertine_and_Belgian_Linen",
        "region": "ERICEIRA & PENICHE • PORTUGAL",
        "beaches": "BALEAL • RIBEIRA • GUINCHO • COXOS • SUPERTUBOS",
        "colorway": "Monochrome Matte Warm Sand Limestone Cream",
        "studio": "Porous Roman Travertine Stone & Raw Unbleached Belgian Linen"
    },
    {
        "id": "CS_04",
        "file_stem": "CS_04_HAWAII_NORTH_SHORE_Pure_Gallery_White_and_Alabaster",
        "region": "NORTH SHORE OAHU • HAWAII",
        "beaches": "PIPELINE • LANIAKEA • HALEIWA • WAIMEA • SUNSET",
        "colorway": "Two-Tone Pure Chalk-White & Deep Pacific Navy",
        "studio": "Pure Gallery White Cyclorama & Honed White Alabaster"
    },
    {
        "id": "CS_05",
        "file_stem": "CS_05_SOCAL_MALIBU_TRESTLES_Terracotta_Clay_on_Sand_Plaster",
        "region": "MALIBU & SAN CLEMENTE • SOCAL",
        "beaches": "RINCON • MALIBU • TRESTLES • LOWERS • BLACKS",
        "colorway": "Two-Tone Matte Desert Terracotta & Bone Cream",
        "studio": "Warm Sand Venetian Plaster & Raw Unglazed Stoneware"
    },
    {
        "id": "CS_06",
        "file_stem": "CS_06_BYRON_GOLD_COAST_Pebble_Putty_on_Raw_Belgian_Linen",
        "region": "BYRON BAY & GOLD COAST • AUSTRALIA",
        "beaches": "LENNOX • WATEGOS • THE PASS • BURLEIGH • SNAPPER",
        "colorway": "1970s Braun Pebble-Putty & Deep Graphite Charcoal",
        "studio": "Natural Oat Belgian Linen & Honed Pale Limestone"
    },
    {
        "id": "CS_07",
        "file_stem": "CS_07_FRANCE_BIARRITZ_HOSSEGOR_Oxblood_on_Dark_Tonal_Basalt",
        "region": "HOSSEGOR & BIARRITZ • FRANCE",
        "beaches": "BIARRITZ • GUETHARY • HOSSEGOR • GRAVIERE • CAPBRETON",
        "colorway": "Monochrome Matte Deep Bordeaux Oxblood",
        "studio": "Matching Dark Tonal Burgundy-Espresso Backdrop & Basalt Stone"
    },
    {
        "id": "CS_08",
        "file_stem": "CS_08_SANTA_CRUZ_Matte_Obsidian_Black_on_Honed_Limestone",
        "region": "SANTA CRUZ • CALIFORNIA",
        "beaches": "WADDELL • FOUR MILE • STEAMERS • PLEASURE • CAPITOLA",
        "colorway": "Monochrome Matte Braun Obsidian Black",
        "studio": "Honed Sand-Beige Limestone Slab & Gallery Chalk-White Studio"
    },
    {
        "id": "CS_09",
        "file_stem": "CS_09_MONTAUK_EAST_END_Dune_Sand_on_Bleached_Linen_and_Stone",
        "region": "MONTAUK • NEW YORK",
        "beaches": "TERRACE • DITCH • MONTAUK • TURTLE • CAMP HERO",
        "colorway": "Two-Tone Coastal Dune-Sand & Deep Atlantic Slate",
        "studio": "Bleached Belgian Linen & Unpolished Travertine Stone"
    },
    {
        "id": "CS_10",
        "file_stem": "CS_10_SYDNEY_BONDI_EAST_Pure_White_Monochrome_on_Carrara_Marble",
        "region": "EASTERN SUBURBS • SYDNEY",
        "beaches": "COOGEE • MAROUBRA • BONDI • BRONTE • TAMARAMA",
        "colorway": "Monochrome Matte Pure Architectural White",
        "studio": "Honed White Carrara Marble & White-on-White Gallery Shadow"
    },
    {
        "id": "CS_11",
        "file_stem": "V8_001_CAUSTIC_BLUE_Signature_Curved_Cyclorama_Prism_Sweep",
        "region": "NORTHERN BEACHES • SYDNEY",
        "beaches": "FRESHIE • QUEENSIE • LONG REEF • DEE WHY • CURL CURL",
        "colorway": "Monochrome Matte Deep Ocean Navy-Slate",
        "studio": "Matching Deep Tonal Navy-Teal Curved Cyclorama & Prism Caustics"
    },
    {
        "id": "CS_12",
        "file_stem": "V8_071_MARBLE_ARCH_HighAngle_Interlocking_Clear_Statuario_Blocks",
        "region": "NORTHERN BEACHES • SYDNEY",
        "beaches": "FRESHIE • QUEENSIE • LONG REEF • DEE WHY • CURL CURL",
        "colorway": "Two-Tone Matte Chalk-White & Deep Ocean Navy",
        "studio": "Interlocking Honed Statuario Marble Blocks & Warm Sand Plaster"
    }
]

bust = int(time.time())
cards_html = []

for item in COLLECTION:
    cid = item["id"]
    stem = item["file_stem"]
    sp = f"{STILLS_DIR}/{stem}_4K.jpg"
    vp = f"{CLIPS_DIR}/{stem}_4K60.mp4"
    s_mtime = int(os.path.getmtime(sp)) if os.path.exists(sp) else bust
    v_mtime = int(os.path.getmtime(vp)) if os.path.exists(vp) else bust
    has_vid = os.path.exists(vp)

    vid_html = (
        f'<video src="02_INDIVIDUAL_4K_CLIPS_16x9/{stem}_4K60.mp4?v={v_mtime}" muted loop playsinline controls preload="metadata"></video>'
        if has_vid else
        f'<div style="display:flex;align-items:center;justify-content:center;background:#111318;color:#8c93a0;font-size:12px;">Rendering 4K60 SIFT Master...</div>'
    )

    cards_html.append(f"""
  <div class="card" id="card-{cid}" data-id="{cid}" data-name="{stem}" data-status="unreviewed">
    <div class="card-head">
      <div class="card-title-wrap">
        <span class="shot-id">{cid}</span>
        <span class="region-pill">{item['region']}</span>
        <span class="badge-5k">★ NATIVE 5.5K + SIFT 4K60</span>
      </div>
      <span class="spec-label">{item['colorway']}</span>
    </div>
    <div class="meta-strip">
      <div><b>CUSTOM DIAL:</b> {item['beaches']}</div>
      <div><b>STUDIO SET:</b> {item['studio']}</div>
    </div>
    <div class="media-pair">
      <a href="01_4K_STUDIO_KEYFRAMES_AND_STILLS/{stem}_4K.jpg?v={s_mtime}" target="_blank" title="Open full 3840x2160 4:4:4 Still">
        <img src="01_4K_STUDIO_KEYFRAMES_AND_STILLS/{stem}_4K.jpg?v={s_mtime}" loading="lazy" alt="{stem}">
      </a>
      {vid_html}
    </div>
    <div class="review-bar">
      <div class="btn-group">
        <button class="v-btn btn-keep" onclick="setVerdict('{cid}', 'keep')">✓ KEEP</button>
        <button class="v-btn btn-fix" onclick="setVerdict('{cid}', 'fix')">↻ REMAKE / FIX</button>
        <button class="v-btn btn-kill" onclick="setVerdict('{cid}', 'kill')">✕ KILL</button>
      </div>
      <input type="text" class="note-input" id="note-{cid}" placeholder="Feedback for {cid} ({item['region']})..." oninput="saveNote('{cid}', this.value)">
    </div>
  </div>""")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SURF CLOCK — BESPOKE GLOBAL STUDIO COLLECTION (4K STILLS + 4K60 CLIPS)</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ background: #0d0e11; color: #f0f2f5; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; margin: 0; padding: 0 28px 60px 28px; }}
  .console-header {{
    position: sticky; top: 0; z-index: 999; background: rgba(13, 14, 17, 0.96); backdrop-filter: blur(14px);
    border-bottom: 1px solid #282c35; padding: 18px 28px; margin: 0 -28px 28px -28px;
    display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between;
  }}
  .header-left h1 {{ font-size: 18px; letter-spacing: 0.06em; text-transform: uppercase; margin: 0 0 4px 0; color: #fff; }}
  .header-left p {{ font-size: 12px; color: #9aa3b2; margin: 0; }}
  .btn-copy {{
    background: #ff5500; color: #fff; border: none; padding: 9px 16px; border-radius: 6px;
    font-size: 12px; font-weight: 600; cursor: pointer;
  }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(600px, 1fr)); gap: 24px; }}
  .card {{ background: #14171d; border: 2px solid #242933; border-radius: 8px; overflow: hidden; }}
  .card[data-status="keep"] {{ border-color: #10b981; }}
  .card[data-status="fix"]  {{ border-color: #f59e0b; }}
  .card[data-status="kill"] {{ border-color: #ef4444; opacity: 0.45; }}
  .card-head {{ padding: 11px 14px; background: #181c24; border-bottom: 1px solid #252a34; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .card-title-wrap {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .shot-id {{ font-family: monospace; font-size: 13px; font-weight: 700; color: #fff; }}
  .region-pill {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: #262c3a; color: #f0f3f8; letter-spacing: 0.04em; }}
  .badge-5k {{ font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px; background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.35); }}
  .spec-label {{ font-size: 11px; color: #9aa3b2; }}
  .meta-strip {{ padding: 8px 14px; background: #12151b; border-bottom: 1px solid #20242d; font-size: 11px; color: #b5becc; display: flex; flex-direction: column; gap: 3px; }}
  .meta-strip b {{ color: #e2e6ee; }}
  .media-pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #000; }}
  .media-pair img, .media-pair video {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }}
  .review-bar {{ padding: 10px 14px; background: #111318; border-top: 1px solid #20242c; display: flex; flex-direction: column; gap: 8px; }}
  .btn-group {{ display: flex; gap: 8px; }}
  .v-btn {{ flex: 1; padding: 7px 10px; border-radius: 5px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1px solid #2a2f3a; background: #191c24; color: #a8b0be; }}
  .card[data-status="keep"] .btn-keep {{ background: #059669; border-color: #10b981; color: #fff; }}
  .card[data-status="fix"]  .btn-fix  {{ background: #d97706; border-color: #f59e0b; color: #fff; }}
  .card[data-status="kill"] .btn-kill {{ background: #dc2626; border-color: #ef4444; color: #fff; }}
  .note-input {{ width: 100%; background: #0d0f13; border: 1px solid #252932; color: #eef0f4; padding: 7px 10px; border-radius: 5px; font-size: 12px; }}
  .toast {{ position: fixed; bottom: 24px; right: 24px; z-index: 2000; background: #10b981; color: #06281e; font-weight: 700; font-size: 13px; padding: 12px 18px; border-radius: 8px; display: none; }}
</style>
</head>
<body>
<div class="console-header">
  <div class="header-left">
    <h1>001 Surf Clock — Bespoke Global Studio Collection (12 Custom Coastlines & Colorways)</h1>
    <p>Pure Studio & Tactile Material Photography (Sand Plaster, Travertine Stone, Belgian Linen, Gallery White, Dark Tonal) • Native 5.5K→4K Stills + SIFT Relit 4K60 Clips</p>
  </div>
  <div style="display:flex;gap:10px;align-items:center;">
    <a href="00_V8_FRONTIER_100_LOOKBOOK.html" style="color:#9aa3b2;font-size:12px;text-decoration:none;border:1px solid #2b303b;padding:8px 12px;border-radius:6px;">← Full 100-Shot Archive</a>
    <button class="btn-copy" onclick="copyFeedback()">📋 Copy Feedback for Antigravity</button>
  </div>
</div>
<div class="grid">{''.join(cards_html)}</div>
<div class="toast" id="toast">✓ Copied Bespoke Studio feedback to clipboard!</div>
<script>
const KEY = 'surf_clock_bespoke_studio_v1';
let state = JSON.parse(localStorage.getItem(KEY) || '{{}}');
function applyUI() {{
  document.querySelectorAll('.card').forEach(c => {{
    const id = c.dataset.id;
    const st = (state[id] && state[id].status) || 'unreviewed';
    c.dataset.status = st;
    const inp = document.getElementById('note-' + id);
    if (inp && state[id] && state[id].note) inp.value = state[id].note;
  }});
}}
function setVerdict(id, v) {{
  if (!state[id]) state[id] = {{ status: 'unreviewed', note: '' }};
  state[id].status = (state[id].status === v) ? 'unreviewed' : v;
  localStorage.setItem(KEY, JSON.stringify(state));
  applyUI();
}}
function saveNote(id, val) {{
  if (!state[id]) state[id] = {{ status: 'fix', note: '' }};
  state[id].note = val;
  if (val.trim() && state[id].status === 'unreviewed') state[id].status = 'fix';
  localStorage.setItem(KEY, JSON.stringify(state));
  applyUI();
}}
function copyFeedback() {{
  let lines = ['### Bespoke Global Studio Collection Feedback'];
  document.querySelectorAll('.card').forEach(c => {{
    const id = c.dataset.id;
    const item = state[id];
    if (item && item.status !== 'unreviewed') {{
      lines.push(`- **${{id}}** (${{item.status.toUpperCase()}}): ${{item.note || ''}}`);
    }}
  }});
  navigator.clipboard.writeText(lines.join('\\n')).then(() => {{
    const t = document.getElementById('toast');
    t.style.display = 'block';
    setTimeout(() => t.style.display = 'none', 3000);
  }});
}}
applyUI();
</script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote Bespoke Studio Lookbook: {OUT_HTML} ({len(html)/1024:.1f} KB)")
