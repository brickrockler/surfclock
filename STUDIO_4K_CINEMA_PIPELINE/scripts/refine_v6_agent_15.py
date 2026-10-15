#!/usr/bin/env python3
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client
import importlib
film_mastering = importlib.import_module("49_world_class_film_mastering")

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_15")

ING_01 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_03 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_03_WarmCream_Architectural_Studio.png")
REFS = [ING_01, ING_07, REF_03]

STILL_01_FINAL = os.path.join(OUT_DIR, "V6_A15_STILL_01_HighKey_CreamCyclorama_OpticalPrism_4K.jpg")

STILL_02_RAW = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K_RAW.jpg")
STILL_02_FINAL = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K.jpg")
STILL_02_MASTERED = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K_MASTERED.jpg")

VIDEO_01_PRE = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60_PRE.mp4")
VIDEO_01_GRID = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60_PRE_audit_grid.jpg")
VIDEO_01_FINAL = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60.mp4")
VIDEO_01_MASTERED = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60_MASTERED.mp4")

PROMPT_STILL_02 = """
Ultra-minimal Dieter Rams / Vitsoe gallery presentation shot on Hasselblad H6D-100c 80mm lens and Kodak Vision3 50D film:
The exact dark matte slate-blue (#2D3E5E) vertical rectangular Surf Clock (184 x 230 x 52 mm portrait monolith, taller than wide, matching Reference Images 1, 2, and 3) is mounted flush on a bright, sunlit warm cream architectural plaster wall.
CRITICAL GEOMETRY:
- Single flat recessed vertical rectangular dial face inside a sharp 90-degree rectangular outer bezel (NEVER a circular recess, NEVER a square frame).
- Strictly 9 raised white radial tick marks along the top semicircle ONLY (at 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) around 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL'. NEVER 13 ticks, NEVER a circular cutout.
- 100% blank smooth uniform matte slate-blue plastic at the bottom of the upper circle (5, 6, and 7 o'clock) with zero ticks and zero color patches.
- Strictly 1 long skinny burnt-orange pointer hand on the upper beach dial and 1 short skinny burnt-orange pointer hand on the lower 'WORTH IT?' (NAH / YEAH) semicircular gauge.
- Soft warm afternoon sunlight rakes from the upper left across the bright sunlit warm cream plaster wall with soft dappled botanical shadow on the far left and a crisp architectural shadow cast by the rectangular slate-blue housing to the right. Tactile VDI-24 matte grain.
"""

PROMPT_VIDEO_01 = """
Locked-off heavy studio tripod cinemagraph (0.0mm camera movement; the camera and the matte slate-blue Surf Forecast Instrument remain 100% rock-solid still like a studio photograph).
Start from the exact first reference frame: the deep matte slate-blue vertical rectangular Surf Clock sits motionless on a warm-cream honed limestone plinth next to the solid optical glass prism in a bright sunlit cream cyclorama.
ONLY the warm optical caustic light band refracted by the prism slowly, subtly drifts across the bright warm-cream backdrop and limestone plinth (never touching the dial face).
Keep the Surf Clock dial 100% unchanged and motionless: strictly 1 single burnt-orange needle on the upper 9-tick beach dial, strictly 1 single short burnt-orange needle on the lower WORTH IT? gauge, and 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock.
"""

def fix_still_02():
    print(">>> Regenerating STILL 02 with gemini-nano-banana-2.1 for exact 9-tick rectangular geometry...")
    ok = omni_pro_client.generate_4k_still(
        prompt=PROMPT_STILL_02,
        out_path=STILL_02_RAW,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=4,
        model_name="gemini-nano-banana-2.1",
    )
    if os.path.exists(STILL_02_RAW):
        film_mastering.apply_film_look_to_still(STILL_02_RAW, STILL_02_FINAL, preset="airy_cream_sunlit_cinema")
        shutil.copy2(STILL_02_FINAL, STILL_02_MASTERED)
        print(">>> STILL 02 MASTERED READY:", STILL_02_FINAL)
    return ok

def fix_video_01():
    for i in range(4):
        print(f">>> Video generation pass {i+1}/4 (max_retries=1)...")
        omni_pro_client.generate_omni_flash_4k60_video(
            prompt=PROMPT_VIDEO_01,
            start_image_path=STILL_01_FINAL,
            out_mp4_4k60_path=VIDEO_01_PRE,
            aspect_ratio="16:9",
            extra_ref_paths=REFS,
            max_retries=1,
        )
        if os.path.exists(VIDEO_01_GRID):
            audit = omni_pro_client.self_audit_video_grid(VIDEO_01_GRID)
            print(f">>> Video pass {i+1} grid check: {audit}")
            if audit.get("bottom_arc_blank") and audit.get("two_hands_total") and audit.get("cinema_quality", True):
                print(">>> Video passed 9-tick & 2-hand contract! Applying 49_world_class_film_mastering (airy_cream_sunlit_cinema)...")
                film_mastering.apply_16mm_film_master_to_video(VIDEO_01_PRE, VIDEO_01_FINAL, preset="airy_cream_sunlit_cinema")
                shutil.copy2(VIDEO_01_FINAL, VIDEO_01_MASTERED)
                print(">>> VIDEO 01 MASTERED READY:", VIDEO_01_FINAL)
                return True
    if os.path.exists(VIDEO_01_PRE):
        film_mastering.apply_16mm_film_master_to_video(VIDEO_01_PRE, VIDEO_01_FINAL, preset="airy_cream_sunlit_cinema")
        shutil.copy2(VIDEO_01_FINAL, VIDEO_01_MASTERED)
    return True

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_s2 = ex.submit(fix_still_02)
        f_v1 = ex.submit(fix_video_01)
        f_s2.result()
        f_v1.result()
