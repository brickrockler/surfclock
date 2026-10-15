#!/usr/bin/env python3
import os
import sys
import shutil
import json
import importlib.util

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py",
)
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_12")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_02 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")
ING_01 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
REFS = [ING_07, REF_02, ING_01]

STILL_01 = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_RAW_4K.jpg")
STILL_01_MASTER = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_MASTER_Orchid35mm_4K.jpg")

STILL_02 = os.path.join(OUT_DIR, "V6_A12_STILL_02_SunlitVerandah_CreamWall_ThreeQuarter_4K.jpg")
STILL_02_RAW = os.path.join(OUT_DIR, "V6_A12_STILL_02_SunlitVerandah_CreamWall_ThreeQuarter_RAW_4K.jpg")
STILL_02_MASTER = os.path.join(OUT_DIR, "V6_A12_STILL_02_SunlitVerandah_CreamWall_ThreeQuarter_MASTER_Orchid35mm_4K.jpg")

VIDEO_01 = os.path.join(OUT_DIR, "V6_A12_VIDEO_01_SunlitVerandah_Dappled_Cinemagraph_4K60.mp4")
VIDEO_01_PREGRADE = os.path.join(OUT_DIR, "V6_A12_VIDEO_01_SunlitVerandah_Dappled_Cinemagraph_PREGRADE_4K60.mp4")
VIDEO_01_MASTER = os.path.join(OUT_DIR, "V6_A12_VIDEO_01_SunlitVerandah_Dappled_Cinemagraph_MASTER_Orchid35mm_4K60.mp4")

PROMPT_STILL_01 = (
    "Shot on 35mm Kodak Portra 400 analog film (+1 EV warm sunlit overexposure, creamy golden highlights, subtle warm halation, Cooke Speed Panchro 50mm f/1.4 shallow depth of field): "
    "the deep matte slate-blue rectangular Surf Forecast Instrument (184 x 230 x 52 mm, VDI-24 bead-blasted matte polymer #2D3E5E) cleanly mounted on a bright, airy warm-cream beach house verandah plaster wall "
    "directly above a natural woven rattan and honey travertine side table, with the soft edge of a vintage woven wicker verandah chair in the out-of-focus foreground corner. "
    "On the side table below the clock sits a single fresh white-and-gold Australian Frangipani blossom and a crystal glass of iced coffee with condensation droplets casting shimmering golden caustic light patterns onto the sun-drenched warm cream plaster wall, alongside soft out-of-focus dappled eucalyptus leaf shadows. "
    "CRITICAL DIAL GEOMETRY (100% UNOBSTRUCTED, RAZOR-SHARP FOCUS ON THE CLOCK FACE): "
    "1. Sharp rectangular stepped-bezel monolith (184 x 230 x 52 mm) with a single recessed flat rectangular matte slate-blue dial face. "
    "2. Strictly 9 raised white radial tick marks on the TOP semicircle only (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) with NO continuous semicircular arch line. "
    "3. 100% BLANK smooth matte slate-blue plastic at the bottom of the upper circle (5, 6, and 7 o'clock between FRESHIE and CURL CURL — zero ticks, zero numbers). "
    "4. Strictly 2 burnt-orange pointer needles total: 1 long skinny burnt-orange needle on the upper beach dial + 1 short skinny burnt-orange needle on the lower WORTH IT? (NAH / YEAH) arc gauge."
)

PROMPT_STILL_02 = (
    "Shot on 35mm Kodak Portra 400 film (+1 EV warm sunlit exposure, Arriflex 35BL, Cooke Speed Panchro 50mm f/1.8): "
    "bright, airy sunlit warm-cream and chalk-ivory Australian beach house verandah wall with soft, dreamy out-of-focus dappled eucalyptus and frangipani leaf shadows draped across the plaster, "
    "and the deep matte slate-blue rectangular Surf Forecast Instrument (184 x 230 x 52 mm, #2D3E5E) captured in razor-sharp three-quarter 35mm focus. "
    "In the soft-focus foreground lower corner, a hint of a natural woven wicker verandah armchair and warm golden glass caustic reflections on the sunlit cream wall evoke an elevated coastal morning. "
    "CRITICAL DIAL GEOMETRY (100% UNOBSTRUCTED, RAZOR-SHARP FOCUS ON THE CLOCK FACE): "
    "1. Sharp rectangular stepped-bezel monolith with a single recessed flat rectangular matte slate-blue dial face (no glass cover, no glare). "
    "2. Strictly 9 raised white radial tick marks on the TOP semicircle only (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL). "
    "3. 100% BLANK smooth matte slate-blue plastic at 5, 6, and 7 o'clock at the bottom of the upper circle. "
    "4. Strictly 2 burnt-orange pointer needles total: 1 long burnt-orange needle on the upper dial and 1 short burnt-orange needle on the lower WORTH IT? (NAH / YEAH) gauge."
)

PROMPT_VIDEO_01 = (
    "Locked-off 35mm Kodak Portra 400 / Vision3 250D tripod cinemagraph / moving photograph on a bright, airy sunlit warm-cream Australian beach house verandah. "
    "CAMERA LOCKED 100% STILL ON A HEAVY TRIPOD (ZERO camera pan, ZERO zoom, ZERO camera rotation). "
    "The deep matte slate-blue rectangular Surf Clock mounted on the warm-cream plaster wall above the rattan/travertine table with the white-and-gold Frangipani blossom stays 100% rock-solid, razor-sharp, and motionless like a still photograph "
    "(strictly 9 upper radial ticks from 8 to 4 o'clock, 100% blank smooth matte blue bottom arc at 5, 6, 7 o'clock, and 2 stationary burnt-orange pointer hands), "
    "while ONLY the soft out-of-focus dappled verandah eucalyptus/frangipani leaf shadows and warm golden iced-coffee glass caustics gently dance and shimmer in the coastal morning breeze across the bright cream plaster wall."
)

print("=== [v6_agent_12] STEP 1: Generating STILL 01 ===")
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
    shutil.copy2(STILL_01, STILL_01_MASTER)
    audit1 = opc.self_audit_still(STILL_01)
    print("STILL 01 post-grade audit (orchid_35mm_250D_warm):", json.dumps(audit1))

print("=== [v6_agent_12] STEP 2: Generating STILL 02 ===")
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
    shutil.copy2(STILL_02, STILL_02_MASTER)
    audit2 = opc.self_audit_still(STILL_02)
    print("STILL 02 post-grade audit (orchid_35mm_250D_warm):", json.dumps(audit2))

print("=== [v6_agent_12] STEP 3: Generating VIDEO 01 (35mm Film Cinemagraph 4K60) ===")
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
    shutil.copy2(VIDEO_01, VIDEO_01_MASTER)
    print("VIDEO 01 mastered with orchid_35mm_250D_warm:", os.path.exists(VIDEO_01))

print("=== [v6_agent_12] ALL STEPS COMPLETE ===")
