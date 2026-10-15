#!/usr/bin/env python3
"""
V5 Complete Blind Adversarial Judge (`models/gemini-3.8-flash`)
Audits all 40 native 4K stills and all 20 native `models/gemini-omni-1.1-flash` 4K 60fps videos
against the strict 12-Point Product & Cinema Contract.
"""
import os
import io
import sys
import glob
import json
import time
import base64
import urllib.request
import subprocess
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
FFMPEG = "/Users/jcolley/.gemini/jetski/bin/ffmpeg"

def load_api_key():
    key_path = os.path.expanduser("~/.config/pickleball-coach/gemini.key")
    return open(key_path).read().strip()

API_KEY = load_api_key()

def encode_pil_jpg(img, max_dim=1600, quality=92):
    im = img.copy().convert("RGB")
    im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

ING_REF = f"{BASE}/00_GOLDEN_INGREDIENTS_4K/INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg"
ING_B64 = encode_pil_jpg(Image.open(ING_REF), max_dim=1400)

JUDGE_PROMPT_STILL = """You are the Blind Adversarial Industrial Design & Cinema QA Judge (`blind_gauntlet_judge`).
Compare the CANDIDATE 4K STILL (Image 2: Full Frame, Image 3: 1:1 Dial Crop) against the Ground-Truth CAD Reference (Image 1).

Evaluate strictly against the Non-Negotiable 12-Point Contract:
1. `rectangular_monolith`: True ONLY if the Surf Clock is a sharp-cornered rectangular stepped-bezel monolith (`184 x 230 x 52 mm`, hardcover-book scale) with a single flat recessed rectangular face. False if the clock housing is circular/round, has arched cutouts around the dials, or is giant toaster-oven sized.
2. `nine_upper_ticks`: True ONLY if the upper beach dial has radial tick marks spanning ONLY the upper semicircle (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL).
3. `bottom_arc_blank`: True ONLY if the bottom arc of the upper dial (5, 6, and 7 o'clock between FRESHIE and CURL CURL) is 100% BLANK matte slate-blue plastic with ZERO tick marks and ZERO numbers.
4. `two_hands_total`: True ONLY if there is 1 burnt-orange pointer needle on the upper dial and 1 shorter burnt-orange pointer needle on the lower `WORTH IT?` (`NAH` / `YEAH`) arc gauge (never 2 hands on the same dial).
5. `no_comping_or_artifacts`: True ONLY if there is zero 2D sticker/paste seam, zero black corner smudge, zero glass reflection glare, zero blue LED glow, zero calipers/wires.
6. `score`: Integer 0-100 rating overall industrial design photography, lighting, tactile VDI-24 matte surface realism, and geometric fidelity.
7. `pass`: True ONLY if `rectangular_monolith`, `nine_upper_ticks`, `bottom_arc_blank`, `two_hands_total`, and `no_comping_or_artifacts` are ALL True AND `score >= 95`.
8. `notes`: Concise 1-2 sentence explanation of why it passed or failed.

Respond ONLY in valid JSON with keys:
{"pass": true/false, "score": 97, "rectangular_monolith": true/false, "nine_upper_ticks": true/false, "bottom_arc_blank": true/false, "two_hands_total": true/false, "no_comping_or_artifacts": true/false, "notes": "..."}
"""

JUDGE_PROMPT_VIDEO = """You are the Blind Adversarial Industrial Design & Cinema QA Judge (`blind_gauntlet_judge`).
Compare the CANDIDATE 4K60 VIDEO 2x2 FRAME GRID (Image 2, showing 4 frames across the 10-second `gemini-omni-1.1-flash` video) against the Ground-Truth CAD Reference (Image 1).

Evaluate strictly against the Non-Negotiable 12-Point Contract:
1. `rectangular_monolith`: True ONLY if the Surf Clock remains a sharp-cornered rectangular stepped-bezel monolith (`184 x 230 x 52 mm`) with a single flat recessed rectangular face across all frames (never morphing into a round/circular clock or arched cutouts).
2. `nine_upper_ticks`: True ONLY if the upper beach dial has radial tick marks spanning ONLY the upper semicircle (8..4 o'clock).
3. `bottom_arc_blank`: True ONLY if the bottom arc of the upper dial (5, 6, and 7 o'clock) is 100% BLANK matte slate-blue plastic with ZERO tick marks across all frames.
4. `two_hands_total`: True ONLY if there is 1 burnt-orange pointer needle on the upper dial and 1 shorter burnt-orange pointer needle on the lower `WORTH IT?` gauge.
5. `temporal_stability`: True ONLY if the camera motion and lighting are smooth, physically grounded, and free of weird AI morphing or 2D comping seams.
6. `score`: Integer 0-100 rating overall cinema quality, lighting, and industrial design accuracy.
7. `pass`: True ONLY if all boolean checks are True AND `score >= 95`.
8. `notes`: Concise 1-2 sentence explanation of why it passed or failed.

Respond ONLY in valid JSON with keys:
{"pass": true/false, "score": 97, "rectangular_monolith": true/false, "nine_upper_ticks": true/false, "bottom_arc_blank": true/false, "two_hands_total": true/false, "temporal_stability": true/false, "notes": "..."}
"""

def call_gemini_judge(parts_b64, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
    parts = [{"inlineData": {"mimeType": "image/jpeg", "data": b}} for b in parts_b64]
    parts.append({"text": prompt})
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json"
        }
    }
    last_err = ""
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                res = json.loads(resp.read().decode("utf-8"))
            txt = res["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(txt)
        except Exception as e:
            last_err = str(e)
            time.sleep(2 * (attempt + 1))
    return {"pass": False, "score": 0, "notes": f"API error: {last_err}"}

def audit_one_still(path):
    fn = os.path.basename(path)
    agent = os.path.basename(os.path.dirname(path))
    img = Image.open(path).convert("RGB")
    w, h = img.size
    full_b64 = encode_pil_jpg(img, max_dim=1600, quality=92)
    crop_box = (int(w * 0.20), int(h * 0.12), int(w * 0.80), int(h * 0.88))
    crop_b64 = encode_pil_jpg(img.crop(crop_box), max_dim=1400, quality=95)
    res = call_gemini_judge([ING_B64, full_b64, crop_b64], JUDGE_PROMPT_STILL)
    res["pass"] = bool(
        res.get("pass")
        and res.get("rectangular_monolith")
        and res.get("nine_upper_ticks")
        and res.get("bottom_arc_blank")
        and res.get("two_hands_total")
        and res.get("no_comping_or_artifacts", True)
        and int(res.get("score", 0)) >= 95
    )
    res["filename"] = fn
    res["agent"] = agent
    res["path"] = path
    res["resolution"] = f"{w}x{h}"
    return res

def audit_one_video(path):
    fn = os.path.basename(path)
    agent = os.path.basename(os.path.dirname(path))
    grid_path = path.replace(".mp4", "_judge_grid.jpg")
    subprocess.run([
        FFMPEG, "-y", "-i", path,
        "-vf", "fps=1/2.2,scale=960:-1,tile=2x2",
        "-frames:v", "1", "-q:v", "2", grid_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(grid_path):
        return {"filename": fn, "agent": agent, "path": path, "pass": False, "score": 0, "notes": "Failed grid extraction"}
    grid_b64 = encode_pil_jpg(Image.open(grid_path), max_dim=1920, quality=92)
    res = call_gemini_judge([ING_B64, grid_b64], JUDGE_PROMPT_VIDEO)
    res["pass"] = bool(
        res.get("pass")
        and res.get("rectangular_monolith")
        and res.get("nine_upper_ticks")
        and res.get("bottom_arc_blank")
        and res.get("two_hands_total")
        and res.get("temporal_stability", True)
        and int(res.get("score", 0)) >= 95
    )
    res["filename"] = fn
    res["agent"] = agent
    res["path"] = path
    return res

def main():
    stills = sorted(glob.glob(f"{BASE}/raw_renders/v5_tournament/agent_*/*_4K.jpg"))
    vids = sorted(glob.glob(f"{BASE}/raw_renders/v5_tournament/agent_*/*_4K60.mp4"))
    print(f"Auditing {len(stills)} 4K stills and {len(vids)} 4K60 videos in parallel (max_workers=6)...")

    still_results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(audit_one_still, s): s for s in stills}
        for fut in as_completed(futs):
            r = fut.result()
            still_results.append(r)
            status = "PASS" if r.get("pass") else "FAIL"
            print(f"[STILL {status} {r.get('score',0):3d}] {r['filename']} -> {r.get('notes', '')[:95]}", flush=True)

    still_results.sort(key=lambda x: x["filename"])
    passing_stills = [r for r in still_results if r.get("pass")]
    passing_stills.sort(key=lambda x: (-x.get("score", 0), x["filename"]))

    video_results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(audit_one_video, v): v for v in vids}
        for fut in as_completed(futs):
            r = fut.result()
            video_results.append(r)
            status = "PASS" if r.get("pass") else "FAIL"
            print(f"[VIDEO {status} {r.get('score',0):3d}] {r['filename']} -> {r.get('notes', '')[:95]}", flush=True)

    video_results.sort(key=lambda x: x["filename"])
    passing_videos = [r for r in video_results if r.get("pass")]
    passing_videos.sort(key=lambda x: (-x.get("score", 0), x["filename"]))

    out_stills = {
        "audit_version": "v5_blind_adversarial_gauntlet_stills_wave2",
        "total_candidates_audited": len(still_results),
        "total_passed": len(passing_stills),
        "total_rejected": len(still_results) - len(passing_stills),
        "pass_rate_percent": round(100.0 * len(passing_stills) / max(1, len(still_results)), 1),
        "passing_winners": passing_stills,
        "candidates": still_results
    }
    with open(f"{BASE}/04_CONTACT_SHEETS_AND_AUDIT/blind_judge_stills_audit_v5.json", "w") as f:
        json.dump(out_stills, f, indent=2)

    out_videos = {
        "audit_version": "v5_blind_adversarial_gauntlet_videos_wave2",
        "total_candidates_audited": len(video_results),
        "total_passed": len(passing_videos),
        "total_rejected": len(video_results) - len(passing_videos),
        "pass_rate_percent": round(100.0 * len(passing_videos) / max(1, len(video_results)), 1),
        "passing_winners": passing_videos,
        "candidates": video_results
    }
    with open(f"{BASE}/04_CONTACT_SHEETS_AND_AUDIT/blind_judge_videos_audit_v5.json", "w") as f:
        json.dump(out_videos, f, indent=2)

    print(f"\nSUMMARY: Stills passed: {len(passing_stills)}/{len(still_results)}, Videos passed: {len(passing_videos)}/{len(video_results)}", flush=True)

if __name__ == "__main__":
    main()
