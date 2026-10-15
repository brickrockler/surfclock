#!/usr/bin/env python3
import os
import sys
import json
import shutil
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc
import importlib.util

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py",
)
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_19")
os.makedirs(OUT_DIR, exist_ok=True)

ING_08 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg")
ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_02 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")
REFS = [ING_08, ING_07, REF_02]

STILL_01 = os.path.join(OUT_DIR, "V6_A19_STILL_01_Vert9x16_Floating_WarmCream_Eucalyptus_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A19_STILL_01_Vert9x16_Floating_WarmCream_Eucalyptus_RAW_4K.jpg")

STILL_02 = os.path.join(OUT_DIR, "V6_A19_STILL_02_Vert9x16_BillowingLinen_SunlitCream_35mm_4K.jpg")
STILL_02_RAW = os.path.join(OUT_DIR, "V6_A19_STILL_02_Vert9x16_BillowingLinen_SunlitCream_35mm_RAW_4K.jpg")

VIDEO_01 = os.path.join(OUT_DIR, "V6_A19_VIDEO_01_Vert9x16_Floating_Cream_Dappled_Cinemagraph_4K60.mp4")
VIDEO_01_PREGRADE = os.path.join(OUT_DIR, "V6_A19_VIDEO_01_Vert9x16_Floating_Cream_Dappled_Cinemagraph_PREGRADE_4K60.mp4")

PROMPT_STILL_01 = (
    "Vertical 9:16 4K architectural & editorial film photograph (shot on 35mm Kodak Vision3 50D with a Cooke Speed Panchro 50mm lens at f/2.0, bright airy sunlit coastal palette matching USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png). "
    "The deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Clock (184 x 230 x 52 mm, hardcover-book scale, sharp 90-degree rectangular outer bezel with a single flat recessed rectangular dial face) is mounted floating flush in the center of a bright, airy, sun-drenched warm cream / chalk-ivory Venetian plaster wall (#F6EFE2) with generous vertical headroom and lower breathing room. "
    "Soft, dreamy out-of-focus dappled Australian eucalyptus leaf shadows fall organically across the top and left of the warm cream plaster wall, while a crisp golden diagonal afternoon sunbeam slices across the right side of the plaster wall, casting a clean architectural drop shadow to the right of the matte slate-blue housing. "
    "The entire rectangular Surf Clock dial face is 100% unobstructed and tack-sharp at the focal plane, showing real VDI-24 micro-bead matte plastic texture, an open face with zero glass cover: "
    "strictly 9 raised white radial tick marks along the top semicircular arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with crisp raised white labels 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', "
    "a 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom ticks and zero numbers), the lower 'WORTH IT?' ('NAH' / 'YEAH') semicircular arc gauge, and strictly 2 skinny burnt-orange pointer needles total (1 on the upper beach dial, 1 on the lower WORTH IT? gauge)."
)

PROMPT_STILL_02 = (
    "Vertical 9:16 4K 35mm photochemical film portrait (shot on Arriflex 35BL / Leica M6 with a fast 50mm f/1.4 Summilux lens on Kodak Vision3 250D 5207 film, warm +1.3 EV sunlit highlight bloom, subtle halation, and fine organic 35mm grain). "
    "The deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Clock (184 x 230 x 52 mm, hardcover-book scale) is mounted flush on a bright, airy, sun-drenched warm cream (#F6EFE2) Australian beach-house plaster wall. "
    "Along the extreme left and lower-left edge of the foreground right in front of the lens, a sheer, translucent white woven linen curtain billows softly in the warm afternoon sea breeze, glowing with golden backlit sunlight in dreamy f/1.4 foreground bokeh while parting completely around the center so the entire rectangular Surf Clock dial face is 100% unobstructed and razor-sharp! "
    "Soft out-of-focus dappled eucalyptus leaf shadows grace the upper warm cream plaster wall. "
    "On the tack-sharp recessed matte slate-blue dial face: strictly 9 raised white radial tick marks along the top semicircle ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with raised white beach labels 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', "
    "a 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom tick marks), the lower 'WORTH IT?' ('NAH' / 'YEAH') semicircular arc gauge, and strictly 2 skinny burnt-orange pointer needles total."
)

PROMPT_VIDEO_01 = (
    "Vertical 9:16 locked-off tripod cinemagraph / moving photograph shot on 35mm Kodak Vision3 50D film in a bright, sun-drenched Australian coastal home. "
    "CAMERA LOCKED 100% STILL ON A HEAVY STUDIO TRIPOD (ZERO camera pan, ZERO tilt, ZERO zoom, ZERO camera rotation, ZERO geometry morphing). "
    "The deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Clock floating flush on the bright warm cream plaster wall (#F6EFE2) stays 100% stationary, rock-solid, and razor-sharp like a still photograph (with its 9 upper radial white tick marks from 8 to 4 o'clock, 100% blank smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock, raised white typography, and 2 skinny burnt-orange pointer needles completely motionless), "
    "while ONLY the soft out-of-focus dappled Australian eucalyptus leaf shadows gently sway, ripple, and breathe across the sunlit warm cream plaster wall and diagonal sunbeam in a gentle coastal breeze."
)

def gen_still_1():
    print("=== STEP 1: Generating STILL 01 (Vert 9:16 Floating Warm Cream & Eucalyptus) ===", flush=True)
    ok1 = opc.generate_4k_still(
        prompt=PROMPT_STILL_01,
        out_path=STILL_01,
        ref_image_paths=REFS,
        aspect_ratio="9:16",
        max_retries=5,
    )
    print("STILL 01 generated:", ok1, flush=True)
    audit1 = {"pass": False, "score": 0.0}
    if os.path.exists(STILL_01):
        shutil.copy2(STILL_01, STILL_01_RAW)
        fm.apply_film_look_to_still(STILL_01_RAW, STILL_01, preset="airy_cream_sunlit_cinema")
        audit1 = opc.self_audit_still(STILL_01)
        print("STILL 01 post-grade (airy_cream_sunlit_cinema) audit:", audit1, flush=True)
    return ok1, audit1

def gen_still_2():
    print("=== STEP 2: Generating STILL 02 (Vert 9:16 Billowing Linen & Sunlit Cream 35mm) ===", flush=True)
    ok2 = opc.generate_4k_still(
        prompt=PROMPT_STILL_02,
        out_path=STILL_02,
        ref_image_paths=REFS,
        aspect_ratio="9:16",
        max_retries=5,
    )
    print("STILL 02 generated:", ok2, flush=True)
    audit2 = {"pass": False, "score": 0.0}
    if os.path.exists(STILL_02):
        shutil.copy2(STILL_02, STILL_02_RAW)
        fm.apply_film_look_to_still(STILL_02_RAW, STILL_02, preset="airy_cream_sunlit_cinema")
        audit2 = opc.self_audit_still(STILL_02)
        print("STILL 02 post-grade (airy_cream_sunlit_cinema) audit:", audit2, flush=True)
    return ok2, audit2

if __name__ == "__main__":
    report = {"stills": {}, "videos": {}}
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(gen_still_1)
        f2 = ex.submit(gen_still_2)
        ok1, audit1 = f1.result()
        ok2, audit2 = f2.result()

    report["stills"][os.path.basename(STILL_01)] = {"path": STILL_01, "raw_path": STILL_01_RAW, "audit": audit1}
    report["stills"][os.path.basename(STILL_02)] = {"path": STILL_02, "raw_path": STILL_02_RAW, "audit": audit2}

    print("=== STEP 3: Generating VIDEO 01 (Vert 9:16 Floating Cream Dappled Cinemagraph 4K60) ===", flush=True)
    start_img = STILL_01 if os.path.exists(STILL_01) else ING_08
    ok_vid = opc.generate_omni_flash_4k60_video(
        prompt=PROMPT_VIDEO_01,
        start_image_path=start_img,
        out_mp4_4k60_path=VIDEO_01_PREGRADE,
        aspect_ratio="9:16",
        extra_ref_paths=REFS,
        max_retries=4,
    )
    print("VIDEO 01 pregrade generated:", ok_vid, flush=True)
    if os.path.exists(VIDEO_01_PREGRADE):
        fm.apply_16mm_film_master_to_video(VIDEO_01_PREGRADE, VIDEO_01, preset="airy_cream_sunlit_cinema")
        print("VIDEO 01 mastered with airy_cream_sunlit_cinema:", os.path.exists(VIDEO_01), flush=True)

    grid_jpg = VIDEO_01_PREGRADE.replace(".mp4", "_audit_grid.jpg")
    vaudit = opc.self_audit_video_grid(grid_jpg) if os.path.exists(grid_jpg) else {"pass": False, "score": 0.0}
    report["videos"][os.path.basename(VIDEO_01)] = {
        "path": VIDEO_01,
        "pregrade_path": VIDEO_01_PREGRADE,
        "audit_grid": grid_jpg,
        "audit": vaudit,
    }

    report_path = os.path.join(OUT_DIR, "v6_agent_19_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"=== ALL V6 AGENT 19 OUTPUTS COMPLETED -> {report_path} ===", flush=True)
