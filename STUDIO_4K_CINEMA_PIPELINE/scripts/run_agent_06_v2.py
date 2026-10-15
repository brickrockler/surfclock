import os
import sys
import json
import time

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
    GOLDEN_DIR,
    USER_REF_DIR,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_06"
os.makedirs(OUT_DIR, exist_ok=True)

REF_ING_02 = os.path.join(GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
REF_ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_USER_03 = os.path.join(USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")

REFS = [REF_ING_02, REF_ING_07, REF_USER_03]

GEOMETRY_LOCK = (
    "CRITICAL GEOMETRY LOCK (MUST MATCH IMAGE 1 & IMAGE 2 EXACTLY):\n"
    "- HOUSING SHAPE: Vertical portrait rectangular box (184 mm wide x 230 mm tall x 52 mm deep) with a clean rectangular outer frame and a SINGLE FLAT RECESSED RECTANGULAR DIAL FACE. "
    "Do NOT create a circular dial well, round clock cutout, or arched top bezel. The recessed face is a flat matte slate-blue rectangle.\n"
    "- UPPER DIAL (STRICTLY 9 TICKS, LABELS OUTSIDE TICKS): Directly on the upper portion of the flat rectangular slate-blue face are STRICTLY 9 small raised white radial tick marks at clock positions 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock (count: 9 ticks total, never 11 or 13). "
    "The 5 horizontal white uppercase labels ('FRESHIE' at 8 o'clock, 'QUEENSIE' at 10 o'clock, 'LONG REEF' at 12 o'clock, 'DEE WHY' at 2 o'clock, 'CURL CURL' at 4 o'clock) are positioned OUTSIDE the 9 radial tick marks on the flat rectangular face.\n"
    "- SEAMLESS BLANK BOTTOM OF UPPER DIAL: The area at 5, 6, and 7 o'clock between FRESHIE and CURL CURL is 100% seamless uniform matte slate-blue plastic (zero tick marks, and zero discolored semicircle patch).\n"
    "- LOWER GAUGE: Centered on the lower portion of the same flat rectangular face is the raised white semicircular 'WORTH IT?' arch with 3 small inner ticks, 'NAH' on the left, 'YEAH' on the right, and 'WORTH IT?' centered below.\n"
    "- HANDS: Strictly 1 long burnt-orange needle on the upper beach dial and 1 short burnt-orange needle on the lower WORTH IT? gauge.\n"
)

STILLS = [
    {
        "filename": "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "prompt": (
            "16:9 4K industrial design studio tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The vertical rectangular matte slate-blue Surf Forecast Instrument (exact rectangular flat-recessed-face housing from Image 1 and Image 2) "
            "stands upright resting directly on sun-warmed matte handmade terracotta quarry tiles in a daylight architectural studio. "
            "Three-quarter front-left hero angle matching Image 1 and Image 2. "
            "Visible organic mineral grain, subtle kiln-fired clay texture, and thin recessed mortar joints between the warm terracotta tiles. "
            "Warm directional natural morning window light casts a soft architectural shadow across the terracotta surface against a warm sunlit plaster studio background (lighting mood of Image 3).\n"
            + GEOMETRY_LOCK
        ),
    },
    {
        "filename": "A06_STILL_02_Unbleached_Canvas_Drape_StudioTable_4K.jpg",
        "prompt": (
            "16:9 4K tactile studio tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The vertical rectangular matte slate-blue Surf Forecast Instrument (exact rectangular flat-recessed-face housing from Image 1 and Image 2) "
            "stands upright resting directly on heavy unbleached raw Belgian linen and painter's canvas draped organically across a wide wooden studio worktable. "
            "Soft raking side light highlights the tactile contrast between the coarse woven natural oatmeal linen fibers, soft fabric folds, "
            "and the precision VDI-24 micro-bead matte slate-blue rectangular housing.\n"
            + GEOMETRY_LOCK
        ),
    },
    {
        "filename": "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "prompt": (
            "16:9 4K architectural studio interior tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The vertical rectangular matte slate-blue Surf Forecast Instrument (exact rectangular flat-recessed-face housing from Image 1 and Image 2) "
            "stands upright directly on a flat matte oiled Australian Tasmanian oak tabletop / mid-century credenza against a warm textured limewash architectural wall. "
            "Clean, honest timber grain in warm honey-smoked oak, warm natural daylight grazing across the wood surface and illuminating the flat rectangular recessed matte slate-blue dial face.\n"
            + GEOMETRY_LOCK
        ),
    },
    {
        "filename": "A06_STILL_04_RawConcrete_StudioFloor_LowAngle_4K.jpg",
        "prompt": (
            "16:9 4K low-angle studio photograph, ZERO plinth, ZERO pedestal. "
            "The vertical rectangular matte slate-blue Surf Forecast Instrument (exact rectangular flat-recessed-face housing from Image 1 and Image 2) "
            "stands upright directly on a power-troweled matte raw concrete studio floor inside a luminous pool of natural window light. "
            "Low floor-level camera angle looking slightly up and across the smooth, subtly mottled matte warm-grey concrete floor toward the standing rectangular slate-blue instrument. "
            "Crisp natural window light casts a clean architectural shadow across the concrete floor.\n"
            + GEOMETRY_LOCK
        ),
    },
]

def main():
    for item in STILLS:
        out_path = os.path.join(OUT_DIR, item["filename"])
        if os.path.exists(out_path):
            os.remove(out_path)
        print(f"\n=== Regenerating Still with Strict Rectangular Flat-Face Geometry: {item['filename']} ===", flush=True)
        ok = generate_4k_still(
            prompt=item["prompt"],
            out_path=out_path,
            ref_image_paths=REFS,
            aspect_ratio="16:9",
            max_retries=5,
        )
        print(f"Finished {item['filename']}: ok={ok}", flush=True)

if __name__ == "__main__":
    main()
