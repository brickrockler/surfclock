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
os.makedirs(OUT_DIR, exist_ok=True)

ING_01 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_03 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_03_WarmCream_Architectural_Studio.png")
REFS = [ING_01, ING_07, REF_03]

STILL_01_RAW = os.path.join(OUT_DIR, "V6_A15_STILL_01_HighKey_CreamCyclorama_OpticalPrism_4K_RAW.jpg")
STILL_01_FINAL = os.path.join(OUT_DIR, "V6_A15_STILL_01_HighKey_CreamCyclorama_OpticalPrism_4K.jpg")
STILL_01_MASTERED = os.path.join(OUT_DIR, "V6_A15_STILL_01_HighKey_CreamCyclorama_OpticalPrism_4K_MASTERED.jpg")

STILL_02_RAW = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K_RAW.jpg")
STILL_02_FINAL = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K.jpg")
STILL_02_MASTERED = os.path.join(OUT_DIR, "V6_A15_STILL_02_HighKey_Floating_CreamPlaster_Minimal_4K_MASTERED.jpg")

VIDEO_01_PRE = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60_PRE.mp4")
VIDEO_01_FINAL = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60.mp4")
VIDEO_01_MASTERED = os.path.join(OUT_DIR, "V6_A15_VIDEO_01_HighKey_CreamPrism_Cinemagraph_4K60_MASTERED.mp4")

PROMPT_STILL_01 = """
High-key, ultra-elevated Braun / Dieter Rams / Vitsoe museum exhibition studio photograph shot on Hasselblad H6D-100c with 80mm f/2.8 lens and Kodak Vision3 50D photochemical grade.
The exact deep matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm, hardcover-monograph scale) stands upright on a warm-cream honed limestone plinth inside a bright, airy, sun-drenched warm cream cyclorama studio (matching Reference Image 2).
To the lower left on the warm-cream limestone tabletop sits a heavy, museum-grade solid optical crown-glass triangular prism, catching a crisp shaft of warm morning sunlight and casting a subtle, authentic, soft-edged warm golden-amber and pale-spectrum optical caustic light band across the cream limestone plinth and background cream cyclorama wall to the side — NEVER covering or obscuring the slate-blue dial face.
The recessed dial face is a completely uniform, seamless deep matte slate-blue VDI-24 micro-bead plastic (matching Reference Images 1 and 2) with crisp raised white typography:
- Upper semicircular beach dial has STRICTLY 9 raised white radial tick marks along the top arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with labels 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', and 1 long skinny burnt-orange pointer hand pointing to 'DEE WHY'.
- The bottom of the upper circle (5, 6, and 7 o'clock, between FRESHIE and CURL CURL) is 100% BLANK smooth uniform deep matte slate-blue plastic with ZERO tick marks and ZERO color patches.
- Lower 'WORTH IT?' semicircular arc gauge has 3 white ticks, 'NAH' on left, 'YEAH' on right, 'WORTH IT?' below, and 1 short skinny burnt-orange pointer hand pointing toward 'YEAH'.
Crisp architectural shadows, pure tactile industrial design photography.
"""

PROMPT_STILL_02 = """
Ultra-minimal Dieter Rams / Vitsoe / Braun gallery wall presentation shot on 35mm Kodak Vision3 50D with a Zeiss Master Prime 50mm lens.
The exact dark matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm) is mounted flush on a bright, sunlit warm cream / chalk-ivory architectural plaster wall (matching Reference Image 2 and 3's warm cream sunlit palette).
Soft, airy golden-hour sunlight rakes gently from the upper left across the fine mineral grain of the warm cream plaster wall, casting a clean, architectural soft-edged drop shadow to the lower right of the sharp 90-degree rectangular stepped bezel. Subtle, dreamy out-of-focus warm sunlight falloff graces the left edge of the cream wall.
The recessed dial face is a 100% uniform, seamless deep matte slate-blue (#2D3E5E) VDI-24 micro-bead injection-molded plastic texture (matching Reference Images 1 and 2, with ZERO lighter discoloration patch in the middle):
- Upper semicircular beach dial has STRICTLY 9 raised white radial tick marks on the top semicircle ONLY (8 to 4 o'clock) with raised white labels 'FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL', and strictly 1 long skinny burnt-orange pointer hand.
- The bottom arc of the upper dial (5, 6, and 7 o'clock, between FRESHIE and CURL CURL) is 100% BLANK smooth matte slate-blue plastic with ZERO tick marks.
- Lower 'WORTH IT?' semicircular arc gauge has 3 white ticks, 'NAH', 'YEAH', 'WORTH IT?', and strictly 1 short skinny burnt-orange pointer hand.
Razor-sharp geometry, open matte face with zero glass cover, museum-grade tactile realism.
"""

PROMPT_VIDEO_01 = """
Locked-off heavy studio tripod cinemagraph (0.0mm camera movement; the camera and the matte slate-blue Surf Forecast Instrument remain 100% rock-solid still like a high-resolution studio photograph).
The deep matte slate-blue rectangular Surf Clock stands completely motionless on the warm-cream honed limestone plinth next to the heavy solid optical glass prism in a bright sunlit warm-cream cyclorama studio.
ONLY the warm optical caustic light band refracted by the glass prism and the soft sunlit glow on the bright warm-cream background cyclorama wall and limestone plinth slowly, hypnotically drift and breathe across the cream backdrop (never crossing over the dial face).
The Surf Clock housing, its 9 upper radial white tick marks (8 to 4 o'clock), its 100% blank bottom arc (5, 6, 7 o'clock), and its 2 burnt-orange pointer needles remain 100% crisp, locked, and motionless throughout the entire 10-second shot.
"""

def gen_still_1():
    print(">>> Generating STILL 01...")
    ok = omni_pro_client.generate_4k_still(
        prompt=PROMPT_STILL_01,
        out_path=STILL_01_RAW,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image",
    )
    if os.path.exists(STILL_01_RAW):
        film_mastering.apply_film_look_to_still(STILL_01_RAW, STILL_01_FINAL, preset="airy_cream_sunlit_cinema")
        shutil.copy2(STILL_01_FINAL, STILL_01_MASTERED)
        audit = omni_pro_client.self_audit_still(STILL_01_FINAL)
        print(f">>> STILL 01 FINAL AUDIT: {audit}")
    return ok

def gen_still_2():
    print(">>> Generating STILL 02...")
    ok = omni_pro_client.generate_4k_still(
        prompt=PROMPT_STILL_02,
        out_path=STILL_02_RAW,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image",
    )
    if os.path.exists(STILL_02_RAW):
        film_mastering.apply_film_look_to_still(STILL_02_RAW, STILL_02_FINAL, preset="airy_cream_sunlit_cinema")
        shutil.copy2(STILL_02_FINAL, STILL_02_MASTERED)
        audit = omni_pro_client.self_audit_still(STILL_02_FINAL)
        print(f">>> STILL 02 FINAL AUDIT: {audit}")
    return ok

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(gen_still_1)
        f2 = ex.submit(gen_still_2)
        f1.result()
        f2.result()

    print(">>> Generating VIDEO 01 Cinemagraph...")
    start_img = STILL_01_FINAL if os.path.exists(STILL_01_FINAL) else ING_07
    ok_vid = omni_pro_client.generate_omni_flash_4k60_video(
        prompt=PROMPT_VIDEO_01,
        start_image_path=start_img,
        out_mp4_4k60_path=VIDEO_01_PRE,
        aspect_ratio="16:9",
        extra_ref_paths=REFS,
        max_retries=3,
    )
    if os.path.exists(VIDEO_01_PRE):
        print(">>> Applying 49_world_class_film_mastering (airy_cream_sunlit_cinema) to VIDEO 01...")
        film_mastering.apply_16mm_film_master_to_video(VIDEO_01_PRE, VIDEO_01_FINAL, preset="airy_cream_sunlit_cinema")
        shutil.copy2(VIDEO_01_FINAL, VIDEO_01_MASTERED)
        print(">>> VIDEO 01 MASTERED READY:", VIDEO_01_FINAL)
