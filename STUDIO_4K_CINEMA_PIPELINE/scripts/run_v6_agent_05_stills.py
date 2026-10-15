import os
import sys
import shutil

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc
import importlib
mastering = importlib.import_module("49_world_class_film_mastering")

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v6_film_explorations/v6_agent_05"
os.makedirs(OUT_DIR, exist_ok=True)

REF_POETRY = os.path.join(opc.USER_REF_DIR, "USER_REF_07_Poetry_Camera_16mm_Film_Bloom_Look.png")
REF_ING07 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_ING01 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")

REFS = [REF_ING07, REF_ING01, REF_POETRY]

STILL_01_PATH = os.path.join(OUT_DIR, "V6_A05_STILL_01_PoetryCamera_CoastalBlossoms_16mm_4K.jpg")
STILL_02_PATH = os.path.join(OUT_DIR, "V6_A05_STILL_02_PoetryCamera_SunlitGardenWall_16mm_4K.jpg")

PROMPT_STILL_01 = """
Direct homage to the Poetry Camera 16mm launch film aesthetic (reference image 3 color and lighting ONLY — do NOT copy any floating title text, letterbox bars, or the small red/white camera from reference image 3).
Full-bleed 16:9 widescreen 4K frame shot on an Arriflex 16SR3 16mm motion picture film camera with a vintage Cooke Speed Panchro 50mm f/1.4 lens wide open at f/1.4 on Kodak Vision3 50D (7203) color negative film (+1.3 EV sunlit overexposure, warm golden halation bloom, lifted warm-cream shadows, subtle edge chromatic aberration, organic 16mm silver-halide film grain).
The deep matte slate-blue rectangular Surf Clock (#2D3E5E, 184 x 230 x 52 mm, exact product from reference images 1 and 2) rests solidly upright on a sun-bleached, weathered coastal garden timber post surrounded by sun-drenched pink-and-cream coastal magnolia and banksia blossoms and dappled branches.
Dreamy, ultra-soft out-of-focus foreground pink-and-cream blossom petals right in front of the lens (heavy f/1.4 foreground bokeh) frame the composition, while warm golden afternoon sunlight glows through translucent petals behind the clock with creamy optical bokeh and subtle red-orange halation around sunlit edges.
The matte slate-blue Surf Clock dial is in tack-sharp focus at the center: stepped rectangular bezel, recessed matte blue dial face, strictly 9 white radial tick marks on the top semicircle ONLY (8 to 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte blue plastic at the bottom of the upper dial (5, 6, 7 o'clock), 1 single long burnt-orange needle on the upper dial, and 1 single short burnt-orange needle on the lower WORTH IT? (NAH / YEAH) gauge. Zero watermark, zero overlay typography, zero letterbox bars.
"""

PROMPT_STILL_02 = """
Authentic 16mm Kodak Vision3 50D (7203) photochemical film frame shot on an Arriflex 16SR3 with a Zeiss Super Speed 50mm T1.3 lens at f/1.6 (inspired by reference image 3's warm 16mm film bloom and botanical framing — do NOT include any title overlay text, letterbox bars, or the small camera from reference image 3).
Full-bleed 16:9 widescreen 4K photograph of the deep matte slate-blue rectangular Surf Clock (#2D3E5E, 184 x 230 x 52 mm, exact product from reference images 1 and 2) mounted flush on an airy, sun-bleached warm cream limewash garden wall.
Overhanging flowering coastal magnolia and eucalyptus branches frame the top and sides of the shot, casting soft, dreamy dappled leaf and blossom shadows across the warm cream plaster wall.
Warm golden late-morning sunlight grazes the stepped slate-blue VDI-24 matte plastic bezel and creates gentle golden lens flare halation and warm +1.3 EV highlight bloom on the surrounding cream blossoms, with blurred foreground petals in the lower corner bokeh.
The Surf Clock dial is crisp and tack-sharp: strictly 9 raised white radial tick marks along the top semicircle ONLY (8 to 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, 1 single burnt-orange pointer needle on the upper beach dial, and 1 single short burnt-orange pointer needle on the lower WORTH IT? (NAH / YEAH) gauge. Zero overlay text, zero letterbox bars.
"""

print("=== Generating STILL 01 ===")
ok1 = opc.generate_4k_still(PROMPT_STILL_01, STILL_01_PATH, REFS, aspect_ratio="16:9", max_retries=4)
print(f"STILL 01 result: {ok1}")

print("=== Generating STILL 02 ===")
ok2 = opc.generate_4k_still(PROMPT_STILL_02, STILL_02_PATH, REFS, aspect_ratio="16:9", max_retries=4)
print(f"STILL 02 result: {ok2}")
