#!/usr/bin/env python3
import os
import sys
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
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_18")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_03 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_03_WarmCream_Architectural_Studio.png")
ING_02 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
REFS = [ING_07, REF_03, ING_02]

STILL_01 = os.path.join(OUT_DIR, "V6_A18_STILL_01_Leica35mm_SunlitLimewash_Courtyard_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A18_STILL_01_Leica35mm_SunlitLimewash_Courtyard_RAW_4K.jpg")
STILL_02 = os.path.join(OUT_DIR, "V6_A18_STILL_02_Leica35mm_CreamStucco_Archway_4K.jpg")
STILL_02_RAW = os.path.join(OUT_DIR, "V6_A18_STILL_02_Leica35mm_CreamStucco_Archway_RAW_4K.jpg")
VIDEO_01 = os.path.join(OUT_DIR, "V6_A18_VIDEO_01_Leica35mm_Limewash_Courtyard_Cinemagraph_4K60.mp4")
VIDEO_01_PREGRADE = os.path.join(OUT_DIR, "V6_A18_VIDEO_01_Leica35mm_Limewash_Courtyard_Cinemagraph_PREGRADE_4K60.mp4")

PROMPT_STILL_01 = (
    "Shot on 35mm Kodak Vision3 250D (5207) motion picture film with a Leica M6 and vintage Leica 35mm Summilux f/1.4 pre-ASPH lens wide open (signature warm 'Leica glow' highlight halation, natural optical corner falloff vignette, tactile 35mm silver-halide film grain). "
    "The deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Clock (184 x 230 x 52 mm, hardcover-book scale) is mounted cleanly at eye level on a bright, airy, sun-baked chalk-cream limewash courtyard wall in an architectural Palm Beach / Whale Beach Sydney villa. "
    "Soft, organic out-of-focus dappled olive and native Australian eucalyptus tree branch shadows fall across the warm chalk-cream limewash wall, while sunlit warm travertine and limestone courtyard steps recede into creamy f/1.4 background bokeh on the side. "
    "Dreamy out-of-focus silver-green olive leaves at the extreme frame edge add depth, while the entire rectangular Surf Clock dial face in the center focal plane is 100% unobstructed and razor-sharp: "
    "strictly 9 raised white radial tick marks along the top semicircular arc only (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with crisp raised white labels 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', a 100% blank smooth matte slate-blue bottom arc (zero ticks at 5, 6, and 7 o'clock), the lower 'WORTH IT?' ('NAH' / 'YEAH') arc gauge, and strictly 2 skinny burnt-orange pointer needles total."
)

PROMPT_STILL_02 = (
    "Shot on 35mm Kodak Vision3 250D (5207) film with a vintage Leica 35mm Summilux f/1.4 pre-ASPH lens at f/1.4 (signature spherical highlight glow, warm sunlit Mediterranean/Sydney coastal architecture, subtle natural vignette, organic 35mm grain). "
    "A bright, airy, sun-drenched hand-troweled warm cream stucco archway in a Palm Beach / Whale Beach coastal villa frames the deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Clock (184 x 230 x 52 mm, hardcover-book scale) mounted on the sunlit cream stucco pillar wall in the foreground focal plane. "
    "Beyond the sculpted warm cream archway, a glimpse of bright azure coastal sky and sun-bleached limestone terrace is softly blurred in creamy f/1.4 background bokeh, with delicate dappled eucalyptus leaf shadows dancing across the warm chalk-ivory plaster. "
    "The entire rectangular Surf Clock dial face is 100% unobstructed and tack-sharp at the plane of focus: "
    "strictly 9 raised white radial tick marks along the top semicircular arc only (8 to 4 o'clock) around 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', a 100% blank smooth matte slate-blue bottom arc (5, 6, and 7 o'clock completely empty), the lower 'WORTH IT?' ('NAH' / 'YEAH') arc gauge, and strictly 2 skinny burnt-orange pointer needles total."
)

PROMPT_VIDEO_01 = (
    "Locked-off 35mm tripod cinemagraph / moving photograph shot on Kodak Vision3 250D through a vintage Leica 35mm Summilux f/1.4 pre-ASPH lens in a sunlit Palm Beach / Whale Beach Sydney architectural villa courtyard. "
    "CAMERA LOCKED 100% STILL ON A HEAVY TRIPOD (ZERO camera pan, ZERO zoom, ZERO camera rotation, ZERO geometry morphing). "
    "The deep matte slate-blue rectangular Surf Clock mounted on the bright, sun-baked chalk-cream limewash courtyard wall stays 100% rock-solid, razor-sharp, and motionless like a still photograph (with its 9 upper radial ticks from 8 to 4 o'clock, 100% blank bottom arc at 5, 6, 7 o'clock, and 2 burnt-orange pointer hands completely stationary), "
    "while ONLY the soft dappled olive and eucalyptus tree shadows across the sunlit cream limewash wall and warm limestone courtyard steps gently sway and ripple in the warm afternoon coastal breeze."
)

def gen_still_1():
    print("=== STEP 1: Generating STILL 01 ===")
    ok1 = opc.generate_4k_still(
        prompt=PROMPT_STILL_01,
        out_path=STILL_01,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
    )
    print("STILL 01 generated:", ok1)
    if os.path.exists(STILL_01):
        shutil.copy2(STILL_01, STILL_01_RAW)
        fm.apply_film_look_to_still(STILL_01_RAW, STILL_01, preset="orchid_35mm_250D_warm")
        audit1 = opc.self_audit_still(STILL_01)
        print("STILL 01 post-grade audit:", audit1)
    return ok1

def gen_still_2():
    print("=== STEP 2: Generating STILL 02 ===")
    ok2 = opc.generate_4k_still(
        prompt=PROMPT_STILL_02,
        out_path=STILL_02,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
    )
    print("STILL 02 generated:", ok2)
    if os.path.exists(STILL_02):
        shutil.copy2(STILL_02, STILL_02_RAW)
        fm.apply_film_look_to_still(STILL_02_RAW, STILL_02, preset="orchid_35mm_250D_warm")
        audit2 = opc.self_audit_still(STILL_02)
        print("STILL 02 post-grade audit:", audit2)
    return ok2

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(gen_still_1)
        f2 = ex.submit(gen_still_2)
        f1.result()
        f2.result()

    print("=== STEP 3: Generating VIDEO 01 (35mm Courtyard Cinemagraph 4K60) ===")
    start_img = STILL_01 if os.path.exists(STILL_01) else ING_07
    ok_vid = opc.generate_omni_flash_4k60_video(
        prompt=PROMPT_VIDEO_01,
        start_image_path=start_img,
        out_mp4_4k60_path=VIDEO_01_PREGRADE,
        aspect_ratio="16:9",
        extra_ref_paths=REFS,
        max_retries=4,
    )
    print("VIDEO 01 pregrade generated:", ok_vid)
    if os.path.exists(VIDEO_01_PREGRADE):
        fm.apply_16mm_film_master_to_video(VIDEO_01_PREGRADE, VIDEO_01, preset="orchid_35mm_250D_warm")
        print("VIDEO 01 mastered with orchid_35mm_250D_warm:", os.path.exists(VIDEO_01))
