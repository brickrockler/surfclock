import os
import sys

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    GOLDEN_DIR,
    USER_REF_DIR,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_10"
ING_08 = os.path.join(GOLDEN_DIR, "INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg")
ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
USER_REF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")

out_path = os.path.join(OUT_DIR, "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg")
prompt = (
    "Vertical 9:16 4K architectural portrait of the exact matte slate-blue rectangular Surf Forecast Instrument from Image 1, Image 2, and Image 3 "
    "mounted on a warm cream sunlit plaster wall with organic dappled Australian eucalyptus leaf shadows (matching Image 3 USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png in a vertical 9:16 frame). "
    "CRITICAL DIAL GEOMETRY (MATCH IMAGE 1, IMAGE 2, AND IMAGE 3 EXACTLY): "
    "1. Sharp-cornered rectangular single-stepped bezel housing (184 x 230 x 52 mm). "
    "2. The upper beach dial has STRICTLY 9 separate floating white radial tick marks with NO connecting semicircular line on the upper dial, and ZERO numbers anywhere on the clock (NEVER print clock numbers). "
    "3. Horizontal white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) sit cleanly outside the 9 floating tick marks. "
    "4. The bottom of the upper dial is 100% blank smooth matte slate-blue plastic. "
    "5. Only the lower gauge has a connected white semicircular arch line with 3 inward ticks, NAH on the left, YEAH on the right, and WORTH IT? centered underneath."
)

generate_4k_still(
    prompt=prompt,
    out_path=out_path,
    ref_image_paths=[ING_08, ING_07, USER_REF_02, ING_01],
    aspect_ratio="9:16",
    max_retries=4,
    model_name="gemini-3-pro-image-preview",
)
