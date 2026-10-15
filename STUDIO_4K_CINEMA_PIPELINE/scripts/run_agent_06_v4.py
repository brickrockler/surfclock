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
STILL_REFS = [REF_ING_02, REF_ING_07, REF_USER_03]
VIDEO_EXTRA_REFS = [REF_ING_02, REF_ING_07]

GEOMETRY_LOCK = (
    "CRITICAL GEOMETRY LOCK (MUST MATCH IMAGE 1 & IMAGE 2 EXACTLY):\n"
    "- HOUSING SHAPE: Vertical portrait rectangular box (184 mm wide x 230 mm tall x 52 mm deep) with sharp rectangular outer corners and a SINGLE FLAT RECESSED RECTANGULAR DIAL FACE. "
    "Do NOT round the corners, and do NOT create a circular dial well.\n"
    "- UPPER DIAL (STRICTLY 9 TICKS, HORIZONTAL LABELS OUTSIDE TICKS): Directly on the upper portion of the flat rectangular slate-blue face are STRICTLY 9 small raised white radial tick marks at clock positions 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock (strictly 9 ticks total, never 11 or 13). "
    "The 5 horizontal white uppercase labels ('FRESHIE' at 8 o'clock, 'QUEENSIE' at 10 o'clock, 'LONG REEF' at 12 o'clock, 'DEE WHY' at 2 o'clock, 'CURL CURL' at 4 o'clock) are strictly horizontal and positioned OUTSIDE the 9 radial tick marks on the flat rectangular face.\n"
    "- SEAMLESS BLANK BOTTOM OF UPPER DIAL: The area at 5, 6, and 7 o'clock between FRESHIE and CURL CURL is 100% seamless uniform matte slate-blue plastic (zero tick marks, and zero discolored semicircle patch).\n"
    "- LOWER GAUGE: Centered on the lower portion of the same flat rectangular face is the raised white semicircular 'WORTH IT?' arch with 3 small inner ticks, 'NAH' on the left, 'YEAH' on the right, and 'WORTH IT?' centered below.\n"
    "- HANDS: Strictly 1 long burnt-orange needle on the upper beach dial and 1 short burnt-orange needle on the lower WORTH IT? gauge.\n"
)

STILL_01_PROMPT = (
    "16:9 4K industrial design studio tabletop photograph, ZERO plinth, ZERO pedestal. "
    "The vertical rectangular matte slate-blue Surf Forecast Instrument (exact rectangular flat-recessed-face housing from Image 1 and Image 2) "
    "stands upright resting directly on sun-warmed matte handmade terracotta quarry tiles in a daylight architectural studio. "
    "Three-quarter front-left hero angle matching Image 1 and Image 2. "
    "Visible organic mineral grain, subtle kiln-fired clay texture, and thin recessed mortar joints between the warm terracotta tiles. "
    "Warm directional natural morning window light casts a soft architectural shadow across the terracotta surface against a warm sunlit plaster studio background.\n"
    + GEOMETRY_LOCK
)

VIDEOS = [
    {
        "filename": "A06_VIDEO_01_Terracotta_Tabletop_Sunlight_Glide_4K60.mp4",
        "start_still": "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "prompt": (
            "Smooth, slow low-angle tabletop dolly push-in gliding across the sun-warmed matte handmade terracotta quarry tiles "
            "toward the standing vertical rectangular matte slate-blue Surf Forecast Instrument. "
            "Warm natural morning window sunlight softly illuminates the terracotta tile texture and the flat rectangular recessed matte slate-blue dial face. "
            "No camera equipment in frame. Keep the 9-tick upper beach dial (with horizontal labels outside the 9 ticks and 100% uniform seamless blank matte slate-blue bottom at 5, 6, 7 o'clock) "
            "and lower WORTH IT? gauge with their 2 burnt-orange pointer needles rock-solid and razor-sharp."
        ),
    },
    {
        "filename": "A06_VIDEO_02_TasmanianOak_Tabletop_Track_4K60.mp4",
        "start_still": "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "prompt": (
            "Smooth, slow tabletop tracking and push-in shot across the flat matte oiled Australian Tasmanian oak tabletop against a warm limewash wall, "
            "with a gentle cinematic focus pull onto the standing vertical rectangular matte slate-blue Surf Forecast Instrument's 9-tick upper beach dial and lower WORTH IT? gauge. "
            "Warm architectural daylight, no camera equipment in frame, zero glass glare, rock-solid geometry with 9 upper ticks, horizontal labels outside the ticks, 100% uniform seamless blank matte slate-blue bottom space at 5, 6, 7 o'clock (zero grey semicircle patch), and 2 burnt-orange hands."
        ),
    },
]

def safe_audit_still(path):
    for _ in range(3):
        res = self_audit_still(path)
        if "HTTP Error" not in str(res.get("reason", "")):
            return res
        time.sleep(3)
    return res

def safe_audit_video(grid_path):
    for _ in range(3):
        res = self_audit_video_grid(grid_path)
        if "HTTP Error" not in str(res.get("reason", "")):
            return res
        time.sleep(3)
    return res

def main():
    s1_path = os.path.join(OUT_DIR, "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg")
    print("=== Regenerating A06_STILL_01 with gemini-nano-banana-2.1 ===", flush=True)
    generate_4k_still(
        prompt=STILL_01_PROMPT,
        out_path=s1_path,
        ref_image_paths=STILL_REFS,
        aspect_ratio="16:9",
        max_retries=4,
        model_name="gemini-nano-banana-2.1",
    )

    for vitem in VIDEOS:
        out_mp4 = os.path.join(OUT_DIR, vitem["filename"])
        start_path = os.path.join(OUT_DIR, vitem["start_still"])
        print(f"\n=== Generating Video: {vitem['filename']} ===", flush=True)
        generate_omni_flash_4k60_video(
            prompt=vitem["prompt"],
            start_image_path=start_path,
            out_mp4_4k60_path=out_mp4,
            aspect_ratio="16:9",
            extra_ref_paths=VIDEO_EXTRA_REFS,
            max_retries=3,
        )

    all_stills = [
        "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "A06_STILL_02_Unbleached_Canvas_Drape_StudioTable_4K.jpg",
        "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "A06_STILL_04_RawConcrete_StudioFloor_LowAngle_4K.jpg",
    ]
    report = {"stills": {}, "videos": {}}
    for fn in all_stills:
        p = os.path.join(OUT_DIR, fn)
        report["stills"][fn] = {
            "path": p,
            "exists": os.path.exists(p),
            "size_bytes": os.path.getsize(p) if os.path.exists(p) else 0,
            "audit": safe_audit_still(p),
        }
        print(f"Final Still Audit {fn}: {report['stills'][fn]['audit']}", flush=True)

    for vitem in VIDEOS:
        fn = vitem["filename"]
        p = os.path.join(OUT_DIR, fn)
        grid_p = p.replace(".mp4", "_audit_grid.jpg")
        report["videos"][fn] = {
            "path": p,
            "exists": os.path.exists(p),
            "size_bytes": os.path.getsize(p) if os.path.exists(p) else 0,
            "audit": safe_audit_video(grid_p),
        }
        print(f"Final Video Audit {fn}: {report['videos'][fn]['audit']}", flush=True)

    report_path = os.path.join(OUT_DIR, "agent_06_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nSaved final audit report to {report_path}", flush=True)

if __name__ == "__main__":
    main()
