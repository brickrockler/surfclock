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
ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_02 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")
ING_01 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
REFS = [ING_07, REF_02, ING_01]

STILL_01 = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_RAW_4K.jpg")
STILL_01_MASTER = os.path.join(OUT_DIR, "V6_A12_STILL_01_SunlitVerandah_Frangipani_Portra400_MASTER_Orchid35mm_4K.jpg")

PROMPT_STILL_01 = (
    "Shot on 35mm Kodak Portra 400 analog film (+1 EV warm sunlit overexposure, creamy golden highlights, Cooke Speed Panchro 50mm f/1.4 shallow depth of field): "
    "the exact deep matte slate-blue rectangular Surf Forecast Instrument from the reference images (184 x 230 x 52 mm, VDI-24 bead-blasted matte polymer #2D3E5E) cleanly mounted on a bright, airy warm-cream beach house verandah plaster wall "
    "above a natural woven rattan and honey travertine side table, with a hint of a woven wicker verandah chair in the soft-focus foreground corner. "
    "On the rattan/travertine side table sits a single fresh white-and-gold Australian Frangipani blossom and a crystal glass of iced coffee casting shimmering golden caustic light patterns onto the sun-drenched warm cream plaster wall alongside soft out-of-focus dappled eucalyptus leaf shadows. "
    "MANDATORY PHYSICAL HOUSING & DIAL GEOMETRY (MATCH INGREDIENT_07 AND INGREDIENT_01 EXACTLY): "
    "1. Sharp 90-degree rectangular stepped outer bezel surrounding a SINGLE CONTINUOUS FLAT RECESSED RECTANGULAR DIAL FACE. NEVER draw a circular recessed well or round cutout for the upper dial, and NEVER draw a recessed arched cutout for the lower dial — the entire inner rectangular face is one flat matte slate-blue plane! "
    "2. Strictly 9 raised white radial tick marks on the TOP semicircle only (at 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock). The 5 horizontal uppercase beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) sit OUTSIDE the 9 radial ticks on the flat rectangular dial face. "
    "3. 100% BLANK smooth matte slate-blue plastic at 5, 6, and 7 o'clock at the bottom of the upper circle. "
    "4. Lower gauge is a thin white semicircular arc line embossed directly on the flat rectangular dial face with 5 small inward ticks, flanked horizontally outside the ends by NAH (left) and YEAH (right), with WORTH IT? centered horizontally below the orange pivot hub. "
    "5. Strictly 2 burnt-orange pointer needles total: 1 long skinny burnt-orange needle on the upper dial + 1 short skinny burnt-orange needle on the lower gauge."
)

ok1 = opc.generate_4k_still(
    prompt=PROMPT_STILL_01,
    out_path=STILL_01,
    ref_image_paths=REFS,
    aspect_ratio="16:9",
    max_retries=5,
)
print("Regenerated STILL 01:", ok1)
if os.path.exists(STILL_01):
    shutil.copy2(STILL_01, STILL_01_RAW)
    fm.apply_film_look_to_still(STILL_01_RAW, STILL_01, preset="orchid_35mm_250D_warm")
    shutil.copy2(STILL_01, STILL_01_MASTER)
    audit1 = opc.self_audit_still(STILL_01)
    print("STILL 01 post-grade audit:", json.dumps(audit1))
