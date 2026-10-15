import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
    GOLDEN_DIR,
    USER_REF_DIR,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_10"
ING_08 = os.path.join(GOLDEN_DIR, "INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
USER_REF_01 = os.path.join(USER_REF_DIR, "USER_REF_01_SlateBlue_Cyclorama_Caustic_Hero.jpg")
USER_REF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")

still_01 = os.path.join(OUT_DIR, "A10_STILL_01_Vert9x16_SlateBlue_Cyclorama_Hero_4K.jpg")
still_02 = os.path.join(OUT_DIR, "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg")

VIDEOS = [
    {
        "filename": "A10_VIDEO_01_Vert9x16_SlateBlue_Studio_Orbit_4K60.mp4",
        "start_image": still_01,
        "extra_refs": [ING_08, ING_01, USER_REF_01],
        "prompt": (
            "Vertical 9:16 studio cinema slow orbital dolly and subtle macro push-in on the exact sharp-cornered rectangular matte slate-blue Surf Forecast Instrument "
            "from Image 1 and Image 2 standing on a deep slate-blue cyclorama with a warm caustic studio light sweep. "
            "Maintain 100% geometric fidelity to Image 1: sharp rectangular stepped bezel housing, 9 separate floating white tick marks on the upper arc, "
            "horizontal white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, "
            "lower semicircular gauge with NAH, YEAH, and WORTH IT? centered underneath, and strictly 2 burnt-orange pointer needles total."
        ),
    },
    {
        "filename": "A10_VIDEO_02_Vert9x16_WarmCream_Eucalyptus_Light_4K60.mp4",
        "start_image": still_02,
        "extra_refs": [USER_REF_02, ING_08, ING_07],
        "prompt": (
            "Vertical 9:16 sunlit architectural cinema film of the exact sharp-cornered rectangular matte slate-blue Surf Forecast Instrument from Image 1 "
            "mounted on a warm cream sunlit plaster wall with gently swaying dappled Australian eucalyptus leaf shadows. "
            "The camera performs a slow, intimate cinema push-in across the warm sunlit plaster and matte slate-blue housing. "
            "Maintain 100% geometric fidelity to Image 1: sharp rectangular stepped bezel housing, 9 separate floating white tick marks on the upper arc, "
            "horizontal white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, "
            "lower semicircular gauge with NAH, YEAH, and WORTH IT? centered underneath, and strictly 2 burnt-orange pointer needles total."
        ),
    },
]

def run_v(v):
    out_mp4 = os.path.join(OUT_DIR, v["filename"])
    generate_omni_flash_4k60_video(
        prompt=v["prompt"],
        start_image_path=v["start_image"],
        out_mp4_4k60_path=out_mp4,
        aspect_ratio="9:16",
        extra_ref_paths=v["extra_refs"],
        max_retries=1,
    )
    grid_jpg = out_mp4.replace(".mp4", "_audit_grid.jpg")
    return v["filename"], out_mp4, self_audit_video_grid(grid_jpg)

with ThreadPoolExecutor(max_workers=2) as ex:
    results = list(ex.map(run_v, VIDEOS))

report = {"stills": {}, "videos": {}}
for sname in [
    "A10_STILL_01_Vert9x16_SlateBlue_Cyclorama_Hero_4K.jpg",
    "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg",
    "A10_STILL_03_Vert9x16_PureWhite_Studio_Plinth_4K.jpg",
    "A10_STILL_04_Vert9x16_BillyButtons_AussieSandstone_16mm_4K.jpg",
]:
    spath = os.path.join(OUT_DIR, sname)
    report["stills"][sname] = {"path": spath, "audit": self_audit_still(spath)}

for vname, vpath, vaudit in results:
    report["videos"][vname] = {"path": vpath, "audit": vaudit}

report_path = os.path.join(OUT_DIR, "agent_10_audit_report.json")
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)
print("SAVED FINAL REPORT:", report_path)
