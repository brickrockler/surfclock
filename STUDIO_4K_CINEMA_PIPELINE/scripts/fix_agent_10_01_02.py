import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    self_audit_still,
    GOLDEN_DIR,
    USER_REF_DIR,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_10"
ING_08 = os.path.join(GOLDEN_DIR, "INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
USER_REF_01 = os.path.join(USER_REF_DIR, "USER_REF_01_SlateBlue_Cyclorama_Caustic_Hero.jpg")
USER_REF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")

SPECS = [
    {
        "filename": "A10_STILL_01_Vert9x16_SlateBlue_Cyclorama_Hero_4K.jpg",
        "refs": [ING_08, USER_REF_01, ING_01],
        "prompt": (
            "Vertical 9:16 4K studio hero photograph of the exact SHARP-CORNERED RECTANGULAR matte slate-blue Braun/Dieter Rams Surf Forecast Instrument "
            "(184 x 230 x 52 mm rectangular box housing with 4 straight 90-degree corners and stepped rectangular bezel — NEVER an arched or rounded top) "
            "standing upright on a seamless deep slate-blue architectural cyclorama. "
            "A dramatic warm caustic studio light sweep illuminates the slate-blue cyclorama behind and beneath the rectangular clock, casting a crisp architectural shadow to the right (matching USER_REF_01 and INGREDIENT_08). "
            "Horizontal raised white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) sit cleanly around the 9 raised white tick marks on the top arc, "
            "with 100% blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock, and the lower semicircular gauge with NAH on the left, YEAH on the right, and WORTH IT? centered BELOW the hub."
        ),
    },
    {
        "filename": "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg",
        "refs": [USER_REF_02, ING_08, ING_01],
        "prompt": (
            "Vertical 9:16 4K architectural portrait of the exact SHARP-CORNERED RECTANGULAR matte slate-blue Surf Forecast Instrument "
            "(184 x 230 x 52 mm rectangular box housing with 4 straight 90-degree corners and stepped rectangular bezel — NEVER an arched or rounded top) "
            "mounted on or standing against a warm cream sunlit plaster wall with organic dappled Australian eucalyptus leaf shadows (matching USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png in a vertical 9:16 composition). "
            "Horizontal raised white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) sit cleanly around the strictly 9 raised white radial tick marks on the upper arc, "
            "with 100% blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock, and the lower semicircular gauge with NAH on the left, YEAH on the right, and WORTH IT? centered BELOW the hub."
        ),
    },
]

def run_one(s):
    out_path = os.path.join(OUT_DIR, s["filename"])
    generate_4k_still(
        prompt=s["prompt"],
        out_path=out_path,
        ref_image_paths=s["refs"],
        aspect_ratio="9:16",
        max_retries=4,
        model_name="gemini-3-pro-image-preview",
    )

with ThreadPoolExecutor(max_workers=2) as ex:
    list(ex.map(run_one, SPECS))
