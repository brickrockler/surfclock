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

STILL_01_PROMPT = (
    "16:9 4K industrial design studio tabletop photograph, ZERO plinth, ZERO pedestal. "
    "Reproduce the EXACT vertical rectangular matte slate-blue Surf Forecast Instrument from Image 1 and Image 2 (identical camera angle, identical flat rectangular recessed dial face, identical horizontal typography, identical 9 small radial tick marks, identical lower gauge) "
    "standing upright directly on sun-warmed matte handmade terracotta quarry tiles in a daylight architectural studio. "
    "Visible organic mineral grain, subtle kiln-fired clay texture, and thin recessed mortar joints between the warm terracotta tiles. "
    "Warm directional natural morning window light casts a soft architectural shadow across the terracotta surface against a warm sunlit plaster studio background.\n"
    "CRITICAL TYPOGRAPHY & GEOMETRY LOCK (MATCH IMAGE 1 & IMAGE 2 PIXEL-FOR-PIXEL):\n"
    "- All 5 beach labels ('FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL') MUST BE STRICTLY HORIZONTAL (level with the top and bottom edges of the rectangular frame, NEVER curved or rotated along the arc) and placed OUTSIDE the 9 small white radial tick marks.\n"
    "- The lower semicircular arch has 'NAH' horizontally on the left, 'YEAH' horizontally on the right, and 'WORTH IT?' printed STRICTLY ONCE horizontally underneath the center pivot (never above the arch).\n"
    "- Strictly 9 small white radial tick marks at 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock, and 100% blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock.\n"
    "- Strictly 1 long burnt-orange needle on the upper dial and 1 short burnt-orange needle on the lower gauge."
)

VIDEOS = [
    {
        "filename": "A06_VIDEO_01_Terracotta_Tabletop_Sunlight_Glide_4K60.mp4",
        "start_still": "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "prompt": (
            "Smooth, slow low-angle tabletop dolly push-in gliding across the sun-warmed matte handmade terracotta quarry tiles "
            "toward the standing vertical rectangular matte slate-blue Surf Forecast Instrument. "
            "Warm natural morning window sunlight softly illuminates the terracotta tile texture and the flat rectangular recessed matte slate-blue dial face. "
            "No camera equipment in frame. Keep the 9-tick upper beach dial (with horizontal labels outside the 9 ticks and 100% blank bottom at 5, 6, 7 o'clock) "
            "and lower WORTH IT? gauge with their 2 burnt-orange pointer needles rock-solid and razor-sharp."
        ),
    },
    {
        "filename": "A06_VIDEO_02_TasmanianOak_Tabletop_Track_4K60.mp4",
        "start_still": "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "prompt": (
            "Smooth, slow tabletop tracking and push-in shot across the flat matte oiled Australian Tasmanian oak tabletop against a warm limewash wall, "
            "with a gentle cinematic focus pull onto the standing vertical rectangular matte slate-blue Surf Forecast Instrument's 9-tick upper beach dial and lower WORTH IT? gauge. "
            "Warm architectural daylight, no camera equipment in frame, zero glass glare, rock-solid geometry with 9 upper ticks, horizontal labels outside the ticks, blank bottom space at 5, 6, 7 o'clock, and 2 burnt-orange hands."
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
    print("=== Regenerating A06_STILL_01 with Strictly Horizontal Labels ===", flush=True)
    generate_4k_still(
        prompt=STILL_01_PROMPT,
        out_path=s1_path,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
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
            extra_ref_paths=REFS,
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
