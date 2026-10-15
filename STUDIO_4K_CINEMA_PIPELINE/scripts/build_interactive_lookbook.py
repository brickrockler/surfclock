import glob, os, time

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
STILLS_DIR = f"{BASE}/01_4K_STUDIO_KEYFRAMES_AND_STILLS"
CLIPS_DIR = f"{BASE}/02_INDIVIDUAL_4K_CLIPS_16x9"
OUT_HTML = f"{BASE}/00_V8_FRONTIER_100_LOOKBOOK.html"

stills = sorted(glob.glob(f"{STILLS_DIR}/CS_*_4K.jpg")) + sorted(glob.glob(f"{STILLS_DIR}/V8_*_4K.jpg"))
bust = int(time.time())

def get_world(shot_id):
    if shot_id.startswith("CS_"): return "cs", "CS: Bespoke Global Studio"
    num = int(shot_id.split("_")[1])
    if num <= 18: return "w1", "W1: Caustic Blue"
    if num <= 36: return "w2", "W2: 1974 Domus"
    if num <= 52: return "w3", "W3: Zero-Gravity"
    if num <= 68: return "w4", "W4: 100mm Macro"
    if num <= 84: return "w5", "W5: Marble & Alabaster"
    return "w6", "W6: 1970s Surf Cinema"

cards_html = []
for sp in stills:
    base_name = os.path.basename(sp).replace("_4K.jpg", "")
    shot_id = "_".join(base_name.split("_")[:2]) # e.g. V8_001
    short_title = "_".join(base_name.split("_")[2:])
    world_code, world_label = get_world(shot_id)
    # Add cache-buster for the newly remastered shots (or all shots using file mtime)
    s_mtime = int(os.path.getmtime(sp))
    vp = f"{CLIPS_DIR}/{base_name}_4K60.mp4"
    v_mtime = int(os.path.getmtime(vp)) if os.path.exists(vp) else bust

    remastered_badge = ""
    is_remastered = "false"
    if shot_id.startswith("CS_") or shot_id in ("V8_001", "V8_050", "V8_071"):
        remastered_badge = '<span class="badge-5k">★ NATIVE 5.5K + SIFT RELIT 4K60</span>'
        is_remastered = "true"

    card = f"""
  <div class="card" id="card-{shot_id}" data-id="{shot_id}" data-name="{base_name}" data-world="{world_code}" data-remastered="{is_remastered}" data-status="unreviewed">
    <div class="card-head">
      <div class="card-title-wrap">
        <span class="shot-id">{shot_id}</span>
        <span class="world-pill">{world_label}</span>
        <span class="shot-title">{short_title.replace('_', ' ')}</span>
        {remastered_badge}
      </div>
      <span class="spec-label">4K STILL + 4K60 CLIP</span>
    </div>
    <div class="media-pair">
      <a href="01_4K_STUDIO_KEYFRAMES_AND_STILLS/{base_name}_4K.jpg?v={s_mtime}" target="_blank" title="Click to open full 3840x2160 4K Still">
        <img src="01_4K_STUDIO_KEYFRAMES_AND_STILLS/{base_name}_4K.jpg?v={s_mtime}" loading="lazy" alt="{base_name}">
      </a>
      <video src="02_INDIVIDUAL_4K_CLIPS_16x9/{base_name}_4K60.mp4?v={v_mtime}" muted loop playsinline controls preload="metadata"></video>
    </div>
    <div class="review-bar">
      <div class="btn-group">
        <button class="v-btn btn-keep" onclick="setVerdict('{shot_id}', 'keep')">✓ KEEP</button>
        <button class="v-btn btn-fix" onclick="setVerdict('{shot_id}', 'fix')">↻ REMAKE / FIX</button>
        <button class="v-btn btn-kill" onclick="setVerdict('{shot_id}', 'kill')">✕ KILL</button>
      </div>
      <div class="quick-tags">
        <button class="tag-chip" onclick="toggleTag('{shot_id}', 'Make Dial/Text Crisp 5.5K')">+ Crisp 5.5K Dial</button>
        <button class="tag-chip" onclick="toggleTag('{shot_id}', 'Fix Motion')">+ Fix Motion</button>
        <button class="tag-chip" onclick="toggleTag('{shot_id}', 'Fix Clock Geometry')">+ Fix Clock</button>
        <button class="tag-chip" onclick="toggleTag('{shot_id}', 'Change Lighting/Set')">+ Change Set</button>
      </div>
      <input type="text" class="note-input" id="note-{shot_id}" placeholder="Notes for {shot_id} (e.g. 'love the angle, just make text razor sharp')..." oninput="saveNote('{shot_id}', this.value)">
    </div>
  </div>"""
    cards_html.append(card)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SURF CLOCK — V8 FRONTIER 100 CURATION & FEEDBACK CONSOLE</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ background: #0b0c0e; color: #f0f2f5; font-family: -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", sans-serif; margin: 0; padding: 0 28px 60px 28px; }}
  
  /* Sticky Curation Console Header */
  .console-header {{
    position: sticky; top: 0; z-index: 999;
    background: rgba(14, 16, 20, 0.96);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid #282c35;
    padding: 16px 28px;
    margin: 0 -28px 28px -28px;
    display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between;
  }}
  .header-left h1 {{ font-size: 18px; letter-spacing: 0.06em; text-transform: uppercase; margin: 0 0 4px 0; color: #fff; }}
  .header-left p {{ font-size: 12px; color: #8c93a0; margin: 0; }}
  
  .toolbar-controls {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
  .filter-pill {{
    background: #181b22; color: #b8c0cc; border: 1px solid #2b303b;
    padding: 6px 11px; border-radius: 5px; font-size: 12px; font-weight: 500; cursor: pointer;
    transition: all 0.12s ease;
  }}
  .filter-pill:hover {{ background: #222630; color: #fff; }}
  .filter-pill.active {{ background: #f0f2f5; color: #0b0c0e; border-color: #f0f2f5; font-weight: 600; }}
  
  .search-input {{
    background: #14171d; border: 1px solid #2b303b; color: #fff;
    padding: 6px 11px; border-radius: 5px; font-size: 12px; width: 170px;
  }}
  
  .export-group {{ display: flex; gap: 8px; align-items: center; }}
  .btn-copy {{
    background: #ff5500; color: #fff; border: none;
    padding: 8px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer;
    box-shadow: 0 2px 10px rgba(255, 85, 0, 0.25);
  }}
  .btn-copy:hover {{ background: #ff6a1f; }}
  .btn-dl {{
    background: #1f242d; color: #d0d6e0; border: 1px solid #343b48;
    padding: 8px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;
  }}
  .btn-dl:hover {{ background: #2a303c; color: #fff; }}

  /* Grid & Cards */
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(560px, 1fr)); gap: 22px; }}
  .card {{
    background: #13151a; border: 2px solid #22262e; border-radius: 8px; overflow: hidden;
    transition: border-color 0.15s ease, opacity 0.15s ease;
  }}
  .card[data-status="keep"] {{ border-color: #10b981; box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.3); }}
  .card[data-status="fix"]  {{ border-color: #f59e0b; box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.3); }}
  .card[data-status="kill"] {{ border-color: #ef4444; opacity: 0.42; }}
  .card[data-status="kill"]:hover {{ opacity: 0.88; }}

  .card-head {{
    padding: 10px 14px; background: #171a20; border-bottom: 1px solid #232730;
    display: flex; justify-content: space-between; align-items: center; gap: 8px;
  }}
  .card-title-wrap {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .shot-id {{ font-family: "SF Mono", Menlo, monospace; font-size: 13px; font-weight: 700; color: #fff; }}
  .world-pill {{ font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #232834; color: #9aa4b4; text-transform: uppercase; letter-spacing: 0.04em; }}
  .shot-title {{ font-size: 12px; color: #c4cad4; }}
  .badge-5k {{ font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px; background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.4); }}
  .spec-label {{ font-family: monospace; font-size: 11px; color: #6e7785; white-space: nowrap; }}

  .media-pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #000; }}
  .media-pair img, .media-pair video {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }}

  /* Review Bar */
  .review-bar {{ padding: 10px 14px; background: #111318; border-top: 1px solid #20242c; display: flex; flex-direction: column; gap: 8px; }}
  .btn-group {{ display: flex; gap: 8px; }}
  .v-btn {{
    flex: 1; padding: 7px 10px; border-radius: 5px; font-size: 12px; font-weight: 600;
    cursor: pointer; border: 1px solid #2a2f3a; background: #191c24; color: #a8b0be;
    transition: all 0.12s ease;
  }}
  .v-btn:hover {{ background: #232733; color: #fff; }}
  .card[data-status="keep"] .btn-keep {{ background: #059669; border-color: #10b981; color: #fff; }}
  .card[data-status="fix"]  .btn-fix  {{ background: #d97706; border-color: #f59e0b; color: #fff; }}
  .card[data-status="kill"] .btn-kill {{ background: #dc2626; border-color: #ef4444; color: #fff; }}

  .quick-tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .tag-chip {{
    font-size: 11px; padding: 3px 8px; border-radius: 4px; cursor: pointer;
    background: #1a1e26; border: 1px solid #2b313e; color: #9199a8;
  }}
  .tag-chip:hover {{ border-color: #f59e0b; color: #fff; }}
  .tag-chip.active {{ background: rgba(245, 158, 11, 0.2); border-color: #f59e0b; color: #fbbf24; font-weight: 600; }}

  .note-input {{
    width: 100%; background: #0d0f13; border: 1px solid #252932; color: #eef0f4;
    padding: 7px 10px; border-radius: 5px; font-size: 12px;
  }}
  .note-input:focus {{ outline: none; border-color: #f59e0b; }}
  
  .toast {{
    position: fixed; bottom: 24px; right: 24px; z-index: 2000;
    background: #10b981; color: #06281e; font-weight: 700; font-size: 13px;
    padding: 12px 18px; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    display: none;
  }}
</style>
</head>
<body>

<div class="console-header">
  <div class="header-left">
    <h1>001 Surf Clock — V8 Curation & Mass Feedback Console</h1>
    <p>Mark shots <b>KEEP</b>, <b>REMAKE / FIX</b>, or <b>KILL</b> (auto-saved in browser) • Click <b>Copy Feedback for Antigravity</b> and paste into chat</p>
  </div>
  
  <div class="toolbar-controls">
    <button class="filter-pill active" data-filter="all" onclick="setFilter('all', this)">All (<span id="cnt-all">100</span>)</button>
    <button class="filter-pill" data-filter="remastered" onclick="setFilter('remastered', this)" style="border-color:#10b981;color:#34d399;">★ Bespoke Studio Packet (12)</button>
    <button class="filter-pill" data-filter="unreviewed" onclick="setFilter('unreviewed', this)">Unreviewed (<span id="cnt-unreviewed">100</span>)</button>
    <button class="filter-pill" data-filter="keep" onclick="setFilter('keep', this)">✓ Keep (<span id="cnt-keep">0</span>)</button>
    <button class="filter-pill" data-filter="fix" onclick="setFilter('fix', this)">↻ Fix (<span id="cnt-fix">0</span>)</button>
    <button class="filter-pill" data-filter="kill" onclick="setFilter('kill', this)">✕ Kill (<span id="cnt-kill">0</span>)</button>
    
    <select id="world-select" class="filter-pill" onchange="applyFilters()">
      <option value="all">All Worlds + Bespoke Studio</option>
      <option value="cs">★ Bespoke Global Studio Collection (CS_02–CS_10)</option>
      <option value="w1">W1: Caustic Blue Cyclorama (001–018)</option>
      <option value="w2">W2: 1974 Domus Studio (019–036)</option>
      <option value="w3">W3: Zero-Gravity Suspension (037–052)</option>
      <option value="w4">W4: 100mm Macro Horology (053–068)</option>
      <option value="w5">W5: Marble & Alabaster (069–084)</option>
      <option value="w6">W6: 1970s Surf Cinema (085–100)</option>
    </select>
    
    <input type="text" id="search-box" class="search-input" placeholder="Search ID or keyword..." oninput="applyFilters()">
  </div>

  <div class="export-group">
    <button class="btn-copy" onclick="copyFeedbackToClipboard()">📋 Copy Feedback for Antigravity</button>
    <button class="btn-dl" onclick="downloadFeedbackJSON()">💾 JSON</button>
  </div>
</div>

<div class="grid" id="shot-grid">
{''.join(cards_html)}
</div>

<div class="toast" id="toast">✓ Copied feedback summary to clipboard! Paste directly into chat.</div>

<script>
const STORAGE_KEY = 'surf_clock_v8_feedback_v1';
let state = {{}};
let currentFilter = 'all';

function loadState() {{
  try {{
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) state = JSON.parse(raw) || {{}};
  }} catch (e) {{ state = {{}}; }}
  
  document.querySelectorAll('.card').forEach(card => {{
    const id = card.dataset.id;
    const item = state[id] || {{ status: 'unreviewed', note: '', tags: [] }};
    card.dataset.status = item.status || 'unreviewed';
    const input = document.getElementById('note-' + id);
    if (input) input.value = item.note || '';
    updateTagUI(id, item.tags || []);
  }});
  updateCounts();
}}

function persist() {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  updateCounts();
  applyFilters();
}}

function ensureItem(id) {{
  if (!state[id]) state[id] = {{ status: 'unreviewed', note: '', tags: [] }};
  if (!state[id].tags) state[id].tags = [];
  return state[id];
}}

function setVerdict(id, verdict) {{
  const item = ensureItem(id);
  item.status = (item.status === verdict) ? 'unreviewed' : verdict;
  const card = document.getElementById('card-' + id);
  if (card) card.dataset.status = item.status;
  if (item.status === 'fix') {{
    const inp = document.getElementById('note-' + id);
    if (inp) inp.focus();
  }}
  persist();
}}

function toggleTag(id, tagText) {{
  const item = ensureItem(id);
  const idx = item.tags.indexOf(tagText);
  if (idx >= 0) item.tags.splice(idx, 1);
  else {{
    item.tags.push(tagText);
    if (item.status === 'unreviewed') {{
      item.status = 'fix';
      const card = document.getElementById('card-' + id);
      if (card) card.dataset.status = 'fix';
    }}
  }}
  updateTagUI(id, item.tags);
  persist();
}}

function updateTagUI(id, tags) {{
  const card = document.getElementById('card-' + id);
  if (!card) return;
  card.querySelectorAll('.tag-chip').forEach(btn => {{
    const label = btn.textContent.replace('+ ', '').trim();
    const matched = tags.some(t => t.includes(label) || label.includes(t));
    btn.classList.toggle('active', matched);
  }});
}}

function saveNote(id, val) {{
  const item = ensureItem(id);
  item.note = val;
  if (val.trim().length > 0 && item.status === 'unreviewed') {{
    item.status = 'fix';
    const card = document.getElementById('card-' + id);
    if (card) card.dataset.status = 'fix';
  }}
  persist();
}}

function setFilter(filterName, btnEl) {{
  currentFilter = filterName;
  document.querySelectorAll('.filter-pill[data-filter]').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  applyFilters();
}}

function applyFilters() {{
  const worldVal = document.getElementById('world-select').value;
  const q = document.getElementById('search-box').value.trim().toLowerCase();
  document.querySelectorAll('.card').forEach(card => {{
    const st = card.dataset.status || 'unreviewed';
    const w = card.dataset.world;
    const name = (card.dataset.name || '').toLowerCase();
    const id = card.dataset.id;
    const note = ((state[id] && state[id].note) || '').toLowerCase();
    
    const matchStatus = (currentFilter === 'all') || (currentFilter === 'remastered' && card.dataset.remastered === 'true') || (st === currentFilter);
    const matchWorld = (worldVal === 'all') || (w === worldVal);
    const matchSearch = (!q) || name.includes(q) || note.includes(q);
    card.style.display = (matchStatus && matchWorld && matchSearch) ? '' : 'none';
  }});
}}

function updateCounts() {{
  let keep = 0, fix = 0, kill = 0, unrev = 0, total = 0;
  document.querySelectorAll('.card').forEach(card => {{
    total++;
    const st = card.dataset.status || 'unreviewed';
    if (st === 'keep') keep++;
    else if (st === 'fix') fix++;
    else if (st === 'kill') kill++;
    else unrev++;
  }});
  document.getElementById('cnt-all').textContent = total;
  document.getElementById('cnt-unreviewed').textContent = unrev;
  document.getElementById('cnt-keep').textContent = keep;
  document.getElementById('cnt-fix').textContent = fix;
  document.getElementById('cnt-kill').textContent = kill;
}}

function buildSummaryPayload() {{
  const keeps = [], fixes = [], kills = [];
  document.querySelectorAll('.card').forEach(card => {{
    const id = card.dataset.id;
    const item = state[id];
    if (!item || item.status === 'unreviewed') return;
    const tagsStr = (item.tags && item.tags.length) ? `[${{item.tags.join(', ')}}]` : '';
    const noteStr = (item.note && item.note.trim()) ? ` — "${{item.note.trim()}}"` : '';
    const line = `${{id}} ${{tagsStr}}${{noteStr}}`.trim();
    if (item.status === 'keep') keeps.push(line);
    else if (item.status === 'fix') fixes.push(line);
    else if (item.status === 'kill') kills.push(line);
  }});
  
  let md = `### V8 Lookbook Feedback Summary\\n`;
  md += `- **KEEP (${{keeps.length}})**: ${{keeps.length ? keeps.join(', ') : 'None yet'}}\\n`;
  md += `- **REMAKE / FIX (${{fixes.length}})**:\\n`;
  fixes.forEach(f => {{ md += `  - ${{f}}\\n`; }});
  md += `- **KILL (${{kills.length}})**: ${{kills.length ? kills.join(', ') : 'None yet'}}\\n`;
  return {{ md, raw: state }};
}}

function copyFeedbackToClipboard() {{
  const payload = buildSummaryPayload();
  navigator.clipboard.writeText(payload.md).then(() => {{
    const t = document.getElementById('toast');
    t.style.display = 'block';
    setTimeout(() => {{ t.style.display = 'none'; }}, 3200);
  }});
}}

function downloadFeedbackJSON() {{
  const payload = buildSummaryPayload();
  const blob = new Blob([JSON.stringify(payload.raw, null, 2)], {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'v8_surf_clock_feedback.json';
  a.click();
}}

loadState();
</script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote interactive lookbook: {OUT_HTML} ({len(html)/1024:.1f} KB)")
