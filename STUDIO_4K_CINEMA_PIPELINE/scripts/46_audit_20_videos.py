import glob, json, os, io, time, base64, urllib.request
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
API_KEY = open(os.path.expanduser("~/.config/pickleball-coach/gemini.key")).read().strip()

def encode_pil_jpg(img, max_dim=1600, quality=92):
    im = img.copy().convert("RGB")
    im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

ING_B64 = encode_pil_jpg(Image.open(f"{BASE}/00_GOLDEN_INGREDIENTS_4K/INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg"), max_dim=1400)

PROMPT = """You are the Blind Adversarial Industrial Design & Cinema QA Judge (`blind_gauntlet_judge`).
Compare the CANDIDATE 4K60 VIDEO 2x2 FRAME GRID (Image 2, showing 4 frames across the 10-second `gemini-omni-1.1-flash` video) against the Ground-Truth CAD Reference (Image 1).

Evaluate strictly against the Non-Negotiable 12-Point Contract:
1. `rectangular_monolith`: True ONLY if the Surf Clock remains a sharp-cornered rectangular stepped-bezel monolith (`184 x 230 x 52 mm`) with a single flat recessed rectangular face across all frames (never morphing into a round/circular clock or arched cutouts).
2. `nine_upper_ticks`: True ONLY if the upper beach dial has radial tick marks spanning ONLY the upper semicircle (8..4 o clock).
3. `bottom_arc_blank`: True ONLY if the bottom arc of the upper dial (5, 6, and 7 o clock) is 100% BLANK matte slate-blue plastic with ZERO tick marks across all frames.
4. `two_hands_total`: True ONLY if there is 1 burnt-orange pointer needle on the upper dial and 1 shorter burnt-orange pointer needle on the lower `WORTH IT?` gauge.
5. `temporal_stability`: True ONLY if the camera motion and lighting are smooth, physically grounded, and free of weird AI morphing or 2D comping seams.
6. `notes`: Concise 1-2 sentence explanation of why it passed or failed.

Respond ONLY in valid JSON with keys:
{"rectangular_monolith": true/false, "nine_upper_ticks": true/false, "bottom_arc_blank": true/false, "two_hands_total": true/false, "temporal_stability": true/false, "notes": "..."}
"""

def audit_vid(vpath):
    fn = os.path.basename(vpath)
    agent = os.path.basename(os.path.dirname(vpath))
    grid_path = vpath.replace(".mp4", "_audit_grid.jpg")
    if not os.path.exists(grid_path):
        grid_path = vpath.replace(".mp4", "_judge_grid.jpg")
    if not os.path.exists(grid_path):
        return {"filename": fn, "agent": agent, "path": vpath, "pass": False, "notes": "No grid"}
    gb64 = encode_pil_jpg(Image.open(grid_path), max_dim=1600)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": ING_B64}},
            {"inlineData": {"mimeType": "image/jpeg", "data": gb64}},
            {"text": PROMPT}
        ]}],
        "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
    }
    for att in range(3):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                res = json.loads(resp.read().decode("utf-8"))
            d = json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
            d["pass"] = bool(d.get("rectangular_monolith") and d.get("nine_upper_ticks") and d.get("bottom_arc_blank") and d.get("two_hands_total") and d.get("temporal_stability"))
            d["score"] = 97 if d["pass"] else 25
            d["filename"] = fn
            d["agent"] = agent
            d["path"] = vpath
            return d
        except Exception as e:
            time.sleep(2)
    return {"filename": fn, "agent": agent, "path": vpath, "pass": False, "score": 0, "notes": "Error"}

vids = sorted(glob.glob(f"{BASE}/raw_renders/v5_tournament/agent_*/*_4K60.mp4"))
results = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(audit_vid, vids):
        results.append(r)
        st = "PASS" if r.get("pass") else "FAIL"
        print(f"[{st}] {r['filename']:58s} rect={r.get('rectangular_monolith')} 9t={r.get('nine_upper_ticks')} blank={r.get('bottom_arc_blank')} 2h={r.get('two_hands_total')} | {r.get('notes','')[:80]}")

passed = [r for r in results if r.get("pass")]
out = {
    "audit_version": "v5_blind_adversarial_gauntlet_videos",
    "total_candidates_audited": len(results),
    "total_passed": len(passed),
    "total_rejected": len(results) - len(passed),
    "passing_winners": passed,
    "candidates": results
}
with open(f"{BASE}/04_CONTACT_SHEETS_AND_AUDIT/blind_judge_videos_audit_v5.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\nVIDEOS PASSED: {len(passed)}/{len(results)}")
