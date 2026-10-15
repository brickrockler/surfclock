import os
import sys

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v6_film_explorations/v6_agent_05"
REF_POETRY = os.path.join(opc.USER_REF_DIR, "USER_REF_07_Poetry_Camera_16mm_Film_Bloom_Look.png")
REF_ING07 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_ING01 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")

STILL_01_PATH = os.path.join(OUT_DIR, "V6_A05_STILL_01_PoetryCamera_CoastalBlossoms_16mm_4K.jpg")
STILL_02_PATH = os.path.join(OUT_DIR, "V6_A05_STILL_02_PoetryCamera_SunlitGardenWall_16mm_4K.jpg")
VIDEO_01_PATH = os.path.join(OUT_DIR, "V6_A05_VIDEO_01_PoetryCamera_Blossoms_16mm_Cinemagraph_4K60.mp4")

PROMPT_STILL_02_FIXED = """
Authentic 16mm Kodak Vision3 50D (7203) photochemical film frame shot on an Arriflex 16SR3 with a Cooke Speed Panchro 50mm f/1.4 lens at f/1.6 (inspired by reference image 3's warm 16mm film bloom and coastal magnolia blossoms — do NOT include any title overlay text, letterbox bars, or the small camera from reference image 3).
Full-bleed 16:9 widescreen 4K photograph of the EXACT SHARP RECTANGULAR STEPPED-BEZEL MATTE SLATE-BLUE MONOLITH (#2D3E5E, 184 x 230 x 52 mm vertical rectangular hardcover-book enclosure from Reference Images 1 and 2 — NEVER a round or circular housing!) mounted on a sun-bleached warm cream architectural garden wall.
Overhanging pink-and-cream coastal magnolia blossoms and eucalyptus branches frame the left, right, and top edges of the 16:9 frame, casting soft out-of-focus dappled leaf and blossom shadows across the warm cream plaster wall and creating dreamy foreground petal bokeh in the corners and warm golden lens flare halation (+1.3 EV sunlit highlight bloom).
CRITICAL SCHEMATIC ACCURACY:
- The housing MUST be the vertical 90-degree rectangular stepped-bezel monolith from Reference Image 1 (NEVER circular/round).
- The upper beach dial has STRICTLY 9 individual white radial tick marks ONLY (at 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL — NO fine subdivision ticks between them, and NO continuous arch line).
- The bottom of the upper dial (5, 6, and 7 o'clock, between FRESHIE and CURL CURL) is 100% BLANK SMOOTH MATTE SLATE-BLUE PLASTIC.
- Strictly 1 long burnt-orange needle on the upper dial pointing to DEE WHY, and 1 short burnt-orange needle on the lower WORTH IT? (NAH / YEAH) gauge pointing to YEAH.
"""

print("=== Regenerating STILL 02 (Strict Rectangular Monolith + 9-Tick) ===")
if os.path.exists(STILL_02_PATH):
    os.remove(STILL_02_PATH)
ok2 = opc.generate_4k_still(
    PROMPT_STILL_02_FIXED,
    STILL_02_PATH,
    [REF_ING07, STILL_01_PATH, REF_POETRY],
    aspect_ratio="16:9",
    max_retries=4,
)
print(f"STILL 02 Fixed result: {ok2}")

PROMPT_VIDEO_01 = """
10-second 16mm Kodak Vision3 50D (7203) Moving Photograph / Cinemagraph shot on a heavy locked-off tripod with an Arriflex 16SR3 and Cooke Speed Panchro 50mm f/1.4 lens wide open.
CAMERA RESTRAINT (LOCKED-OFF TRIPOD): The camera is 100% stationary and locked-off on a heavy studio tripod. Zero camera pan, zero zoom, zero flying motion.
SUBJECT RESTRAINT: The deep matte slate-blue rectangular Surf Clock resting on the weathered timber post in the center is 100% rock-solid, stationary, and razor-sharp like a still photograph — its rectangular bezel, 9 upper radial tick marks, blank bottom arc, raised white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, WORTH IT?, NAH, YEAH), and 2 burnt-orange pointer needles remain completely crisp and motionless.
BOTANICAL & LIGHT MOTION ONLY: Only the surrounding sun-drenched pink-and-cream coastal magnolia blossoms, dreamy out-of-focus foreground petals right in front of the lens, and warm golden afternoon sunlight halation and dappled shadows gently sway and breathe in a soft warm coastal breeze. Authentic 16mm photochemical film grain and warm +1.3 EV golden highlight bloom.
"""

print("=== Generating VIDEO 01 (16mm Film Cinemagraph 4K60) ===")
ok_vid = opc.generate_omni_flash_4k60_video(
    prompt=PROMPT_VIDEO_01,
    start_image_path=STILL_01_PATH,
    out_mp4_4k60_path=VIDEO_01_PATH,
    aspect_ratio="16:9",
    extra_ref_paths=[REF_ING07, REF_ING01, REF_POETRY],
    max_retries=3,
)
print(f"VIDEO 01 result: {ok_vid}")
