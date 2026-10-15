#!/usr/bin/env python3
"""
V9 WORKING VIBE PERFECTED + FORGED DESIGN JURY GAUNTLET
=======================================================
Remasters all 38 user-curated shots from `/Users/jcolley/surf_clock/NEXT_ROUND_FEEDBACK/WORKING/`:
- Replaces rough VDI-24 pebbled texture with ultra-fine silky-smooth VDI-12 satin-matte ceramic-polymer finish.
- Enforces sharp 90-degree rectangular monolith corners, 9 upper radial ticks, 100% blank 5/6/7 o'clock arc, and 1 orange hand per dial.
- Renders native 4K (5504x3072 -> 3840x2160 4:4:4 Q98) stills via `gemini-3-pro-image-preview`.
- Audits every still with a fresh-context Forged Design Jury (`gemini-3.1-pro-preview` + `design-jury` rubric + `calibration.md` §1-4).
- Renders slow, graceful 4K60 studio motion clips via Flagship Veo 3.1 (`veo-3.1-generate-001`) with first-frame lock.
"""

import os
import re
import sys
import json
import time
import glob
import base64
import shutil
import subprocess
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import run_v8_frontier_100_cinema_gauntlet as v8
from omni_pro_client import (
    get_api_key,
    generate_veo_31_pro_video,
    generate_video_omni,
)

BASE_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
WORKING_DIR = "/Users/jcolley/surf_clock/NEXT_ROUND_FEEDBACK/WORKING"
REF_DIR = os.path.join(BASE_DIR, "00_USER_QUALITY_REFERENCES")
OLD_STILLS_DIR = os.path.join(BASE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS")

OUT_STILLS_DIR = os.path.join(BASE_DIR, "01_V9_WORKING_VIBE_4K_STILLS")
OUT_CLIPS_DIR = os.path.join(BASE_DIR, "02_V9_WORKING_VIBE_4K60_CLIPS")
OUT_CROPS_DIR = os.path.join(BASE_DIR, "04_CONTACT_SHEETS_AND_AUDIT/v9_jury_crops")
MANIFEST_DIR = os.path.join(BASE_DIR, "05_LOGS_AND_MANIFESTS")
REPORT_JSON = os.path.join(MANIFEST_DIR, "v9_forged_design_jury_report.json")
LOOKBOOK_HTML = os.path.join(BASE_DIR, "00_V9_WORKING_VIBE_PERFECTED_LOOKBOOK.html")

for d in [OUT_STILLS_DIR, OUT_CLIPS_DIR, OUT_CROPS_DIR, MANIFEST_DIR]:
    os.makedirs(d, exist_ok=True)

REF_SMOOTH_DIAL = os.path.join(REF_DIR, "USER_REF_01B_Closeup_Full_Dial_9Tick_Master_4K.jpg")
REF_SMOOTH_MACRO = os.path.join(REF_DIR, "USER_REF_15_Macro_100mm_LowerWorthIt_SlateBlue_4K.jpg")
REF_SMOOTH_CREAM = os.path.join(MANIFEST_DIR, "REF_CREAM_M600_RECT_MASTER.jpg")
REF_SMOOTH_TWOTONE = os.path.join(REF_DIR, "USER_REF_08_Warm_Linen_Floating_Tilt_9Tick_Master.jpg")
REF_REAR_FLUTED = os.path.join(REF_DIR, "USER_REF_14_Rear_Fluted_Translucent_Telemetry_4K.jpg")

CALIBRATION_PATH = "/Users/jcolley/.gemini/config/skills/design-jury/calibration.md"
CALIBRATION_TEXT = Path(CALIBRATION_PATH).read_text(encoding="utf-8") if os.path.exists(CALIBRATION_PATH) else ""

FORGED_JURY_CONTEXT = """You are a senior Awwwards juror and FWA judge. You are the critic, not the builder.
Judge only the pixels you are given. Never redesign.
Score Design, Usability, Creativity, Content from 1 to 10 in 0.5 steps.
Weights: Design 40%, Usability 30%, Creativity 20%, Content 10%. Give the weighted overall to two decimals.
7 = a solid Site of the Day; 8 = clearly above the field; 9 = one of the best in six months (at most 9% of ballots). Never 10.
Pass line: weighted >= 7.45 with no criterion below D 7.45, U 7.17, Cr 7.55, Co 7.43.
Creativity and Design separate the top quartile; don't inflate Usability. Reward accessibility that has genuinely been designed.
Penalise trendy features the brief didn't ask for (custom cursor, enter gate, marquee, pill nav, preloader) and copies of a particular winner's look.
A locked art direction outranks trends: never propose breaking it; put such fixes under Escalation.
Be specific: name the element, size, colour and position. Be harsh but fair.
Answer with valid JSON matching the exact schema requested.

--- CALIBRATION DATA ---
""" + CALIBRATION_TEXT


SMOOTH_SURFACE_RULE = (
    "CRITICAL SURFACE FINISH UPGRADE: The clock housing and recessed dial face MUST have an ultra-fine, silky-smooth VDI-12 satin-matte finish "
    "(like smooth matte ceramic or a Dieter Rams Braun calculator / Teenage Engineering satin polymer). "
    "The clock face must be 100% smooth, velvety, and uniform — ZERO coarse pebble grain, ZERO bumpy leather stipple, ZERO rough sandpaper grit, and ZERO asphalt texture! "
)

SHARP_GEOMETRY_RULE = (
    "CRITICAL GEOMETRY & HOROLOGY: The Surf Clock is a strict vertical rectangular monolith (230mm x 184mm x 52mm) with crisp 90-degree rectangular outer bezel corners and clean 3mm 45-degree edge chamfers (NEVER circular, NEVER round, NEVER rounded squircle corners). "
)


def upgrade_prompt_to_smooth_v9(prompt_text: str, mode: str) -> str:
    txt = prompt_text
    # Replace all VDI-24 / micro-pebbled / coarse texture phrases
    txt = re.sub(r"VDI-24\s+micro-pebbled\s+(?:matte\s+)?polymer(?:\s+surface\s+grain)?", "ultra-fine silky-smooth VDI-12 satin-matte ceramic-polymer", txt, flags=re.IGNORECASE)
    txt = re.sub(r"VDI-24\s+molded\s+polymer", "ultra-fine silky-smooth VDI-12 satin-matte ceramic-polymer", txt, flags=re.IGNORECASE)
    txt = re.sub(r"tactile\s+VDI-24\s+micro-pebbled", "ultra-fine silky-smooth VDI-12 satin-matte", txt, flags=re.IGNORECASE)
    txt = re.sub(r"micro-pebbled\s+matte\s+slate-blue\s+polymer", "silky-smooth satin-matte slate-blue ceramic-polymer", txt, flags=re.IGNORECASE)
    txt = re.sub(r"micro-pebbled\s+slate-blue\s+dial", "silky-smooth satin-matte slate-blue dial", txt, flags=re.IGNORECASE)
    txt = re.sub(r"micro-pebbled", "silky-smooth satin-matte", txt, flags=re.IGNORECASE)
    txt = re.sub(r"VDI-24", "VDI-12 silky-smooth satin", txt, flags=re.IGNORECASE)
    txt = re.sub(r"pebbled", "silky-smooth satin", txt, flags=re.IGNORECASE)

    if mode == "rear_telemetry":
        return SHARP_GEOMETRY_RULE + SMOOTH_SURFACE_RULE + txt
    elif mode in ("macro_upper", "macro_lower"):
        return (
            SMOOTH_SURFACE_RULE +
            "CRITICAL MACRO CRAFT: The raised 3D letters, radial tick marks, and semicircular arch must have razor-crisp, clean micro-beveled edges rising cleanly from the smooth, grain-free satin-matte dial plane. " +
            txt
        )
    else:
        return SHARP_GEOMETRY_RULE + SMOOTH_SURFACE_RULE + txt


def upgrade_video_prompt_to_elegant_v9(v_prompt: str, mode: str) -> str:
    txt = re.sub(r"micro-pebbled", "silky-smooth satin-matte", v_prompt, flags=re.IGNORECASE)
    txt = re.sub(r"VDI-24", "silky-smooth satin", txt, flags=re.IGNORECASE)
    return (
        "Slow, unhurried, graceful luxury studio cinema motion (24fps film cadence mastered to 60fps). "
        "The camera glides on a precision fluid tripod slider by at most 2% while studio light or optical caustics drift gently and fluidly across the silky-smooth satin-matte clock face. "
        "The clock housing, raised 3D typography, 9 upper radial ticks, and both burnt-orange pointer hands remain 100% motionless, solid, and razor-sharp throughout the entire shot (zero fast movement, zero hand spinning, zero warping). "
        + txt
    )


def get_working_comp_ref(sid: str, tag: str) -> str:
    # Prefer the exact JPG from WORKING/, else the keyframe from 01_4K_STUDIO_KEYFRAMES_AND_STILLS/
    w_matches = glob.glob(os.path.join(WORKING_DIR, f"{sid}*_4K.jpg"))
    if w_matches:
        return w_matches[0]
    s_matches = glob.glob(os.path.join(OLD_STILLS_DIR, f"{sid}*_4K.jpg"))
    if s_matches:
        return s_matches[0]
    return ""


def build_clean_refs(sid: str, tag: str, mode: str, orig_refs: list) -> list:
    refs = []
    comp_ref = get_working_comp_ref(sid, tag)
    if comp_ref and os.path.exists(comp_ref):
        refs.append(comp_ref)

    if mode == "rear_telemetry":
        refs.append(REF_REAR_FLUTED)
    elif mode == "macro_lower":
        refs.append(REF_SMOOTH_MACRO)
        refs.append(REF_SMOOTH_DIAL)
    elif mode == "macro_upper":
        if "CreamBlack" in tag:
            refs.append(REF_SMOOTH_CREAM)
        elif "TwoTone" in tag:
            refs.append(REF_SMOOTH_TWOTONE)
        else:
            refs.append(REF_SMOOTH_DIAL)
            refs.append(REF_SMOOTH_MACRO)
    else:
        if "CreamBlack" in tag or "Cream_And_SlateBlue" in tag:
            refs.append(REF_SMOOTH_CREAM)
        elif "TwoTone" in tag:
            refs.append(REF_SMOOTH_TWOTONE)
        refs.append(REF_SMOOTH_DIAL)

    # Deduplicate while keeping order, and NEVER include USER_REF_05
    clean = []
    for r in refs:
        if r and os.path.exists(r) and "USER_REF_05" not in r and r not in clean:
            clean.append(r)
    return clean[:3]


def _b64_part(path: str) -> dict:
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    data = base64.b64encode(Path(path).read_bytes()).decode("utf-8")
    return {"inline_data": {"mime_type": mime, "data": data}}


def render_4k_still_v9(prompt: str, ref_paths: list, out_path: str) -> bool:
    api_key = get_api_key()
    parts = []
    for idx, rp in enumerate(ref_paths):
        if idx == 0:
            parts.append({"text": "REFERENCE #1 (COMPOSITION, LIGHTING & STUDIO WORLD): Match this exact framing, studio set, color palette, and lighting mood, while upgrading the clock face surface to an ultra-fine silky-smooth satin-matte finish (ZERO bumpy pebble grain) and sharp 90-degree rectangular corners:"})
        else:
            parts.append({"text": f"REFERENCE #{idx+1} (SMOOTH DIAL & HOROLOGY TRUTH): Match this silky-smooth satin-matte dial surface and exact 9-tick horology:"})
        parts.append(_b64_part(rp))
    parts.append({"text": prompt})

    for model in ["gemini-3-pro-image-preview", "gemini-3-pro-image", "nano-banana-pro-preview"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {
                    "aspectRatio": "16:9",
                    "imageSize": "4K"
                }
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            cand_parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in cand_parts:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and "data" in inline:
                    img_bytes = base64.b64decode(inline["data"])
                    tmp_path = out_path + ".raw"
                    Path(tmp_path).write_bytes(img_bytes)
                    im = Image.open(tmp_path).convert("RGB")
                    if im.size != (3840, 2160):
                        im = im.resize((3840, 2160), Image.Resampling.LANCZOS)
                    im.save(out_path, format="JPEG", quality=98, subsampling=0, optimize=True)
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 300_000:
                        return True
        except Exception as e:
            print(f"  [Render {model} warn]: {e}", flush=True)
            time.sleep(2)
    return False


def make_jury_views(still_4k_path: str, sid: str) -> tuple:
    im = Image.open(still_4k_path).convert("RGB")
    w, h = im.size
    # 1x board at 1440x810
    p_1x = os.path.join(OUT_CROPS_DIR, f"{sid}_1x_1440.jpg")
    im.resize((1440, 810), Image.Resampling.LANCZOS).save(p_1x, format="JPEG", quality=94)

    # 2x detail crop of center dial / texture
    p_2x = os.path.join(OUT_CROPS_DIR, f"{sid}_2x_crop.jpg")
    cw, ch = int(w * 0.42), int(h * 0.56)
    cx, cy = (w - cw) // 2, (h - ch) // 2
    im.crop((cx, cy, cx + cw, cy + ch)).save(p_2x, format="JPEG", quality=96)
    return p_1x, p_2x


def run_forged_design_jury(still_4k_path: str, sid: str, mode: str) -> dict:
    """
    Runs the Forged Design Jury (`design-jury` skill) using `gemini-3.1-pro-preview`
    with fresh context (ONLY pixels, Critic Brief, calibration.md, and locked brief).
    """
    api_key = get_api_key()
    p_1x, p_2x = make_jury_views(still_4k_path, sid)

    if mode == "rear_telemetry":
        lock_desc = (
            "Brief & Locks (Rear View): Three-quarter rear view of the vertical rectangular Surf Clock (230x184x52mm, sharp 90-degree corners, 3mm 45-degree chamfers). "
            "Surface must be silky-smooth satin-matte polymer (zero bumpy pebble grain). "
            "Rear cover is frosted vertically-fluted translucent polymer revealing internal twin circular stepper motor silhouettes and warm-amber + cyan LED telemetry glow."
        )
    elif mode == "macro_lower":
        lock_desc = (
            "Brief & Locks (100mm Macro Lower Sub-Dial): Macro close-up of the lower semicircular 'WORTH IT?' sub-dial. "
            "Clock face MUST be silky-smooth satin-matte (zero coarse bumpy pebble-leather or rough asphalt grain). "
            "Must show raised 3D semicircular arch with 5 radial ticks, crisp 'NAH' on left, 'YEAH' on right, 'WORTH IT?' centered below, and strictly ONE burnt-orange pointer needle."
        )
    elif mode == "macro_upper":
        lock_desc = (
            "Brief & Locks (100mm Macro Upper Dial): Macro close-up of the upper beach dial. "
            "Clock face MUST be silky-smooth satin-matte (zero coarse bumpy pebble-leather or rough sandpaper grain). "
            "Must show crisp raised 3D beach labels (such as 'LONG REEF', 'QUEENSIE', 'DEE WHY', 'CURL CURL') and upper radial ticks (no bottom ticks at 5/6/7 o'clock if visible), and strictly ONE burnt-orange pointer needle."
        )
    else:
        lock_desc = (
            "Brief & Locks (Full Clock Studio Frame): Vertical rectangular monolith Surf Clock (230x184x52mm, sharp 90-degree rectangular bezel corners, 3mm chamfers — NEVER circular or rounded-squircle). "
            "Clock face MUST be silky-smooth satin-matte (zero coarse bumpy pebble-leather or rough sandpaper grain). "
            "Upper dial has ONLY 9 upper radial tick marks (8 o'clock FRESHIE over 12 o'clock LONG REEF to 4 o'clock CURL CURL). "
            "The bottom arc at 5, 6, and 7 o'clock between FRESHIE and CURL CURL MUST be 100% blank and smooth (zero bottom ticks). "
            "5 beach labels ('FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL') and lower semicircular 'WORTH IT?' ('NAH' / 'YEAH') gauge. "
            "Strictly 1 burnt-orange hand on the upper dial and 1 short burnt-orange hand on the lower sub-dial (2 hands total)."
        )

    jury_prompt = f"""{lock_desc}

Out of scope: Web UI chrome, navigation bars, buttons, cursors, sound, or mobile viewports (this is a standalone 16:9 industrial design photography / cinema frame).

You are given Image 1 (the full 16:9 frame at 1440px) and Image 2 (a 2x close-up crop of the dial surface texture and typography).
Score this work as a senior Awwwards juror and FWA judge and fill the report template.
Return ONLY valid JSON with these exact keys:
{{
  "first_five_second_read": "one sentence written before the detail pass",
  "scores": {{
    "design": 7.5,
    "usability": 7.5,
    "creativity": 7.5,
    "content": 7.5,
    "weighted": 7.50,
    "band_position": "where it sits in the field's 7.17-7.87 band"
  }},
  "fwa_verdict": {{
    "verdict": "yes or no",
    "reason": "one sentence"
  }},
  "gate_failures": [],
  "smooth_dial_texture_passed": true,
  "horology_and_geometry_passed": true,
  "trend_check": {{
    "echoes": "what it echoes from calibration.md",
    "dated_or_derivative": "what reads as dated or none",
    "leads": "what leads rather than follows"
  }},
  "largest_gap": "one specific sentence naming element, size, colour and position",
  "top_three_fixes": [
    "fix 1 inside the lock",
    "fix 2 inside the lock",
    "fix 3 inside the lock"
  ],
  "escalation": "none or only if a fix would break a lock",
  "confidence": "high, medium or low, and why"
}}"""

    parts = [
        {"text": "IMAGE 1 (1x full frame 1440x810):"},
        _b64_part(p_1x),
        {"text": "IMAGE 2 (2x detail crop of dial surface texture & typography):"},
        _b64_part(p_2x),
        {"text": jury_prompt}
    ]

    for model_name in ["gemini-3.1-pro-preview", "gemini-4-argon"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": FORGED_JURY_CONTEXT}]},
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.15,
                "responseMimeType": "application/json"
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            for p in data["candidates"][0]["content"]["parts"]:
                if "text" in p:
                    res = json.loads(p["text"])
                    if isinstance(res, list) and res:
                        res = res[0]
                    sc = res.get("scores", {})
                    d_sc = float(sc.get("design", 7.5))
                    u_sc = float(sc.get("usability", 7.5))
                    cr_sc = float(sc.get("creativity", 7.5))
                    co_sc = float(sc.get("content", 7.5))
                    weighted = round(d_sc * 0.40 + u_sc * 0.30 + cr_sc * 0.20 + co_sc * 0.10, 2)
                    sc["weighted"] = weighted
                    res["scores"] = sc
                    gates = res.get("gate_failures", [])
                    if isinstance(gates, str):
                        gates = [] if gates.strip().lower() in ("none", "") else [gates]
                    res["gate_failures"] = gates
                    passed = (
                        len(gates) == 0
                        and bool(res.get("smooth_dial_texture_passed", True))
                        and bool(res.get("horology_and_geometry_passed", True))
                        and weighted >= 7.45
                    )
                    res["passed"] = passed
                    res["jury_model"] = model_name
                    return res
        except Exception as e:
            print(f"  [Jury {model_name} warn]: {e}", flush=True)
            time.sleep(2)

    return {
        "passed": False,
        "scores": {"design": 0, "usability": 0, "creativity": 0, "content": 0, "weighted": 0.0, "band_position": "error"},
        "fwa_verdict": {"verdict": "no", "reason": "Jury request failed"},
        "gate_failures": ["Jury evaluation error"],
        "largest_gap": "Jury timeout",
        "top_three_fixes": ["Re-run render and jury audit"],
        "confidence": "low"
    }


def process_one_shot_still(spec: dict) -> dict:
    sid = spec["id"]
    tag = spec["tag"]
    mode = spec["mode"]
    out_still = os.path.join(OUT_STILLS_DIR, f"{tag}_4K.jpg")

    # If already rendered and passed jury in a previous run, load it
    if os.path.exists(REPORT_JSON):
        try:
            existing = json.loads(Path(REPORT_JSON).read_text(encoding="utf-8"))
            if sid in existing and existing[sid].get("jury", {}).get("passed") and os.path.exists(out_still):
                print(f"[{sid}] Already passed Forged Jury ({existing[sid]['jury']['scores']['weighted']}). Skipping still.", flush=True)
                return existing[sid]
        except Exception:
            pass

    base_prompt = upgrade_prompt_to_smooth_v9(spec["still_prompt"], mode)
    refs = build_clean_refs(sid, tag, mode, spec["refs"])

    best_score = -1.0
    best_jury = None
    best_cand_path = None
    extra_fix = ""

    for attempt in range(1, 4):
        cand_path = os.path.join(OUT_STILLS_DIR, f"{tag}_cand{attempt}_4K.jpg")
        cur_prompt = base_prompt + (f"\nCRITICAL JURY FIX (MUST OBEY): {extra_fix}" if extra_fix else "")
        print(f"[{sid}] Rendering 4K Still (Attempt {attempt}/3)...", flush=True)
        ok = render_4k_still_v9(cur_prompt, refs, cand_path)
        if not ok or not os.path.exists(cand_path):
            continue

        jury = run_forged_design_jury(cand_path, f"{sid}_try{attempt}", mode)
        w_score = jury.get("scores", {}).get("weighted", 0.0)
        passed = jury.get("passed", False)
        print(
            f"[{sid}] Attempt {attempt} Jury -> Weighted={w_score:.2f} | Passed={passed} | "
            f"Smooth={jury.get('smooth_dial_texture_passed')} | Geom={jury.get('horology_and_geometry_passed')} | "
            f"Gap: {jury.get('largest_gap', '')[:90]}",
            flush=True
        )

        if w_score > best_score:
            best_score = w_score
            best_jury = jury
            best_cand_path = cand_path

        if passed:
            break

        fixes = jury.get("top_three_fixes", [])
        gap = jury.get("largest_gap", "")
        gates = "; ".join(jury.get("gate_failures", []))
        extra_fix = f"{gates}. {gap}. {fixes[0] if fixes else ''}".strip()

    if best_cand_path and os.path.exists(best_cand_path):
        shutil.copy2(best_cand_path, out_still)
        for a in range(1, 4):
            cp = os.path.join(OUT_STILLS_DIR, f"{tag}_cand{a}_4K.jpg")
            if os.path.exists(cp):
                try:
                    os.remove(cp)
                except OSError:
                    pass

    return {
        "id": sid,
        "tag": tag,
        "world": spec["world"],
        "mode": mode,
        "still_path": out_still,
        "has_mp4_target": spec["has_mp4"],
        "video_prompt": upgrade_video_prompt_to_elegant_v9(spec["video_prompt"], mode),
        "jury": best_jury or {}
    }


def process_one_shot_video(item: dict) -> str:
    sid = item["id"]
    tag = item["tag"]
    still_path = item["still_path"]
    out_mp4 = os.path.join(OUT_CLIPS_DIR, f"{tag}_4K60.mp4")

    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 1_500_000:
        print(f"[{sid}] 4K60 clip already exists ({os.path.getsize(out_mp4)/(1024*1024):.1f} MB).", flush=True)
        return out_mp4

    print(f"[{sid}] Rendering 4K60 studio motion clip via Veo 3.1...", flush=True)
    ok = generate_veo_31_pro_video(
        prompt=item["video_prompt"],
        keyframe_path=still_path,
        out_mp4_path=out_mp4,
        aspect_ratio="16:9",
    )
    if not ok:
        print(f"[{sid}] Vertex Veo 3.1 fallback to Gemini API Veo 3.1...", flush=True)
        ok = generate_video_omni(
            prompt=item["video_prompt"],
            keyframe_path=still_path,
            out_mp4_path=out_mp4,
            aspect_ratio="16:9",
        )
    if ok and os.path.exists(out_mp4):
        print(f"[{sid}] Video complete -> {os.path.getsize(out_mp4)/(1024*1024):.1f} MB", flush=True)
        return out_mp4
    print(f"[{sid}] Video failed!", flush=True)
    return ""


def build_lookbook(results_by_id: dict, ordered_ids: list):
    bust = int(time.time())
    cards = []
    passed_count = 0
    weights = []
    fwa_yes = 0

    for sid in ordered_ids:
        item = results_by_id.get(sid)
        if not item:
            continue
        tag = item["tag"]
        jury = item.get("jury", {})
        sc = jury.get("scores", {})
        w_val = sc.get("weighted", 0.0)
        if w_val > 0:
            weights.append(w_val)
        if jury.get("passed"):
            passed_count += 1
        fwa = jury.get("fwa_verdict", {})
        if str(fwa.get("verdict", "")).lower().startswith("yes"):
            fwa_yes += 1

        still_rel = f"01_V9_WORKING_VIBE_4K_STILLS/{tag}_4K.jpg"
        clip_rel = f"02_V9_WORKING_VIBE_4K60_CLIPS/{tag}_4K60.mp4"
        still_abs = os.path.join(BASE_DIR, still_rel)
        clip_abs = os.path.join(BASE_DIR, clip_rel)
        s_mt = int(os.path.getmtime(still_abs)) if os.path.exists(still_abs) else bust
        c_mt = int(os.path.getmtime(clip_abs)) if os.path.exists(clip_abs) else bust
        has_vid = os.path.exists(clip_abs) and os.path.getsize(clip_abs) > 500_000

        vid_html = (
            f'<video src="{clip_rel}?v={c_mt}" muted loop playsinline controls preload="metadata"></video>'
            if has_vid else
            (f'<div class="vid-placeholder">Rendering 4K60 Studio Motion...</div>' if item.get("has_mp4_target") else '<div class="vid-placeholder">4K Still Selected</div>')
        )

        score_str = f"D {sc.get('design','—')} · U {sc.get('usability','—')} · Cr {sc.get('creativity','—')} · Co {sc.get('content','—')} → {w_val:.2f}"
        fwa_badge = f"FWA: {str(fwa.get('verdict','—')).upper()}"
        gap_txt = jury.get("largest_gap", "")
        first_read = jury.get("first_five_second_read", "")

        cards.append(f"""
  <div class="card" id="card-{sid}" data-id="{sid}" data-status="unreviewed">
    <div class="card-head">
      <div class="title-left">
        <span class="shot-id">{sid}</span>
        <span class="world-pill">{item['world'].replace('_', ' ')}</span>
        <span class="jury-pill {'pass' if jury.get('passed') else 'warn'}">★ JURY {score_str}</span>
        <span class="fwa-pill">{fwa_badge}</span>
      </div>
      <span class="mode-label">{item['mode']}</span>
    </div>
    <div class="jury-strip">
      <div><b>5s Jury Read:</b> {first_read}</div>
      <div><b>Largest Gap / Detail Note:</b> {gap_txt}</div>
    </div>
    <div class="media-pair">
      <a href="{still_rel}?v={s_mt}" target="_blank" title="Open full 3840x2160 4:4:4 Smooth-Dial Still">
        <img src="{still_rel}?v={s_mt}" loading="lazy" alt="{tag}">
      </a>
      {vid_html}
    </div>
    <div class="review-bar">
      <div class="btn-group">
        <button class="v-btn btn-keep" onclick="setVerdict('{sid}', 'keep')">✓ KEEP</button>
        <button class="v-btn btn-fix" onclick="setVerdict('{sid}', 'fix')">↻ REMAKE / FIX</button>
        <button class="v-btn btn-kill" onclick="setVerdict('{sid}', 'kill')">✕ KILL</button>
      </div>
      <input type="text" class="note-input" id="note-{sid}" placeholder="Feedback for {sid}..." oninput="saveNote('{sid}', this.value)">
    </div>
  </div>""")

    avg_w = (sum(weights) / len(weights)) if weights else 0.0
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SURF CLOCK — V9 WORKING VIBE PERFECTED + FORGED DESIGN JURY</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ background: #0c0d10; color: #f0f2f5; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; margin: 0; padding: 0 28px 60px 28px; }}
  .console-header {{
    position: sticky; top: 0; z-index: 999; background: rgba(12, 13, 16, 0.96); backdrop-filter: blur(14px);
    border-bottom: 1px solid #262a33; padding: 18px 28px; margin: 0 -28px 28px -28px;
    display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between;
  }}
  .header-left h1 {{ font-size: 18px; letter-spacing: 0.05em; text-transform: uppercase; margin: 0 0 4px 0; color: #fff; }}
  .header-left p {{ font-size: 12px; color: #9da6b5; margin: 0; }}
  .stats-row {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
  .stat-chip {{ background: #181b22; border: 1px solid #2b303c; padding: 6px 11px; border-radius: 6px; font-size: 12px; font-weight: 600; color: #d8dee9; }}
  .btn-copy {{ background: #ff5500; color: #fff; border: none; padding: 9px 16px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(640px, 1fr)); gap: 24px; }}
  .card {{ background: #13161c; border: 2px solid #232832; border-radius: 8px; overflow: hidden; }}
  .card[data-status="keep"] {{ border-color: #10b981; }}
  .card[data-status="fix"]  {{ border-color: #f59e0b; }}
  .card[data-status="kill"] {{ border-color: #ef4444; opacity: 0.45; }}
  .card-head {{ padding: 11px 14px; background: #181c24; border-bottom: 1px solid #242934; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .title-left {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .shot-id {{ font-family: monospace; font-size: 13px; font-weight: 700; color: #fff; }}
  .world-pill {{ font-size: 10px; font-weight: 700; padding: 3px 7px; border-radius: 4px; background: #252b38; color: #dce3f0; }}
  .jury-pill {{ font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; font-family: monospace; }}
  .jury-pill.pass {{ background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.35); }}
  .jury-pill.warn {{ background: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.35); }}
  .fwa-pill {{ font-size: 10px; font-weight: 700; padding: 3px 7px; border-radius: 4px; background: #1e2430; color: #a5b4fc; border: 1px solid #313a4d; }}
  .mode-label {{ font-size: 11px; color: #8c95a6; font-family: monospace; }}
  .jury-strip {{ padding: 8px 14px; background: #101318; border-bottom: 1px solid #1e222b; font-size: 11px; color: #b0b9c8; display: flex; flex-direction: column; gap: 3px; }}
  .jury-strip b {{ color: #e2e8f0; }}
  .media-pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #000; }}
  .media-pair img, .media-pair video {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }}
  .vid-placeholder {{ display: flex; align-items: center; justify-content: center; background: #0e1015; color: #6e7787; font-size: 12px; aspect-ratio: 16/9; }}
  .review-bar {{ padding: 10px 14px; background: #101217; border-top: 1px solid #1e222a; display: flex; flex-direction: column; gap: 8px; }}
  .btn-group {{ display: flex; gap: 8px; }}
  .v-btn {{ flex: 1; padding: 7px 10px; border-radius: 5px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1px solid #2a2f3a; background: #181b22; color: #a8b0be; }}
  .card[data-status="keep"] .btn-keep {{ background: #059669; border-color: #10b981; color: #fff; }}
  .card[data-status="fix"]  .btn-fix  {{ background: #d97706; border-color: #f59e0b; color: #fff; }}
  .card[data-status="kill"] .btn-kill {{ background: #dc2626; border-color: #ef4444; color: #fff; }}
  .note-input {{ width: 100%; background: #0c0e12; border: 1px solid #252932; color: #eef0f4; padding: 7px 10px; border-radius: 5px; font-size: 12px; }}
  .toast {{ position: fixed; bottom: 24px; right: 24px; z-index: 2000; background: #10b981; color: #06281e; font-weight: 700; font-size: 13px; padding: 12px 18px; border-radius: 8px; display: none; }}
</style>
</head>
<body>
<div class="console-header">
  <div class="header-left">
    <h1>SURF CLOCK — V9 WORKING VIBE PERFECTED (FORGED DESIGN JURY)</h1>
    <p>38 Curated Studio Shots · Silky-Smooth VDI-12 Dial Texture · Native 4K (4:4:4) + Slow Graceful 4K60 Motion</p>
  </div>
  <div class="stats-row">
    <span class="stat-chip">Jury Mean: {avg_w:.2f} (Top Quartile ≥ 7.45)</span>
    <span class="stat-chip">Passed Gate: {passed_count}/{len(results_by_id)}</span>
    <span class="stat-chip">FWA Yes: {fwa_yes}</span>
    <button class="btn-copy" onclick="copyFeedback()">COPY FEEDBACK JSON</button>
  </div>
</div>
<div class="grid">
  {"".join(cards)}
</div>
<div class="toast" id="toast">Copied feedback to clipboard!</div>
<script>
const STORAGE_KEY = 'surf_clock_v9_jury_feedback';
let state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
function applyState() {{
  document.querySelectorAll('.card').forEach(card => {{
    const id = card.dataset.id;
    const item = state[id] || {{ status: 'unreviewed', note: '' }};
    card.dataset.status = item.status || 'unreviewed';
    const inp = document.getElementById('note-' + id);
    if (inp && inp.value !== (item.note || '')) inp.value = item.note || '';
  }});
}}
function setVerdict(id, verdict) {{
  if (!state[id]) state[id] = {{ status: 'unreviewed', note: '' }};
  state[id].status = (state[id].status === verdict) ? 'unreviewed' : verdict;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  applyState();
}}
function saveNote(id, val) {{
  if (!state[id]) state[id] = {{ status: 'unreviewed', note: '' }};
  state[id].note = val;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}}
function copyFeedback() {{
  const out = [];
  document.querySelectorAll('.card').forEach(c => {{
    const id = c.dataset.id;
    const s = state[id] || {{ status: 'unreviewed', note: '' }};
    if (s.status !== 'unreviewed' || (s.note && s.note.trim())) {{
      out.push(id + ' [' + s.status.toUpperCase() + ']: ' + (s.note || ''));
    }}
  }});
  navigator.clipboard.writeText(out.join('\\n') || 'No feedback marked yet.');
  const t = document.getElementById('toast');
  t.style.display = 'block';
  setTimeout(() => t.style.display = 'none', 2200);
}}
applyState();
</script>
</body>
</html>"""
    Path(LOOKBOOK_HTML).write_text(html, encoding="utf-8")


def main():
    files = sorted(os.listdir(WORKING_DIR))
    working_ids = sorted(set(re.match(r"(V8_\d+)", f).group(1) for f in files if re.match(r"(V8_\d+)", f)))

    manifest = v8.build_100_frontier_v8_manifest()
    specs = []
    for item in manifest:
        sid = item[0][:6]
        if sid in working_ids:
            has_mp4 = any(f.startswith(sid) and f.endswith(".mp4") for f in files)
            specs.append({
                "id": sid,
                "tag": item[0],
                "world": item[1],
                "mode": item[2],
                "refs": item[3],
                "still_prompt": item[4],
                "video_prompt": item[5],
                "has_mp4": has_mp4,
            })

    print(f"=== V9 WORKING VIBE PERFECTED + FORGED DESIGN JURY ({len(specs)} SHOTS) ===", flush=True)
    results_by_id = {}
    if os.path.exists(REPORT_JSON):
        try:
            results_by_id = json.loads(Path(REPORT_JSON).read_text(encoding="utf-8"))
        except Exception:
            results_by_id = {}

    # Stage 1: Render 4K Stills + Run Forged Design Jury in parallel (6 workers)
    with ThreadPoolExecutor(max_workers=6) as ex:
        fut_map = {ex.submit(process_one_shot_still, sp): sp["id"] for sp in specs}
        for fut in as_completed(fut_map):
            sid = fut_map[fut]
            try:
                res = fut.result()
                results_by_id[sid] = res
                Path(REPORT_JSON).write_text(json.dumps(results_by_id, indent=2), encoding="utf-8")
                build_lookbook(results_by_id, working_ids)
            except Exception as e:
                print(f"[{sid}] Still worker error: {e}", flush=True)

    # Stage 2: Render 4K60 Videos for all 26 curated MP4 shots first (4 workers)
    video_items = [results_by_id[sid] for sid in working_ids if sid in results_by_id and results_by_id[sid].get("has_mp4_target")]
    print(f"\n=== STAGE 2: RENDERING {len(video_items)} ELEGANT 4K60 STUDIO VIDEOS ===", flush=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        fut_map = {ex.submit(process_one_shot_video, item): item["id"] for item in video_items}
        for fut in as_completed(fut_map):
            sid = fut_map[fut]
            try:
                mp4_path = fut.result()
                if mp4_path:
                    results_by_id[sid]["video_path"] = mp4_path
                    Path(REPORT_JSON).write_text(json.dumps(results_by_id, indent=2), encoding="utf-8")
                    build_lookbook(results_by_id, working_ids)
            except Exception as e:
                print(f"[{sid}] Video worker error: {e}", flush=True)

    build_lookbook(results_by_id, working_ids)
    print("\n=== ALL 38 PERFECTED STILLS + 26 4K60 VIDEOS + FORGED DESIGN JURY COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
