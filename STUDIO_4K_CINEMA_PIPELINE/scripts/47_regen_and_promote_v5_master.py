#!/usr/bin/env python3
import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
GOLDEN = f"{BASE}/00_GOLDEN_INGREDIENTS_4K"

def gen_a02():
    a02_dir = f"{BASE}/raw_renders/v5_tournament/agent_02"
    v_a02 = f"{a02_dir}/A02_VIDEO_01_WarmCream_Dappled_Eucalyptus_Breeze_4K60.mp4"
    return opc.generate_omni_flash_4k60_video(
        prompt=(
            "10-second 4K industrial design cinema shot on 35mm Arri Alexa Mini LF. "
            "Camera performs a slow, ultra-smooth lateral slider track across the SHARP-CORNERED RECTANGULAR matte slate-blue "
            "Surf Forecast Instrument monolith (184 x 230 x 52 mm) in a sunlit warm cream limewash plaster alcove while soft dappled "
            "Australian eucalyptus leaf shadows sway gently across the plaster wall and stepped rectangular bezel. "
            "Maintain the exact rectangular housing geometry, strictly 9 upper white radial ticks (8 to 4 o'clock), 100% blank bottom arc at 5, 6, 7 o'clock, "
            "and 2 burnt-orange pointer needles throughout all frames."
        ),
        start_image_path=f"{a02_dir}/A02_STILL_02_WarmCream_Architectural_Corner_4K.jpg",
        out_mp4_4k60_path=v_a02,
        aspect_ratio="16:9",
        extra_ref_paths=[
            f"{a02_dir}/A02_STILL_03_Sunlit_Sandstone_Plaster_ThreeQuarter_4K.jpg",
            f"{GOLDEN}/INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg",
        ],
        max_retries=2,
    )

def gen_a04():
    a04_dir = f"{BASE}/raw_renders/v5_tournament/agent_04"
    s1_path = f"{a04_dir}/A04_STILL_01_SageGreen_GridMat_HardcoverBook_Scale_4K.jpg"
    s2_path = f"{a04_dir}/A04_STILL_02_SageGreen_GridMat_HighAngle_Editorial_4K.jpg"
    v_a04 = f"{a04_dir}/A04_VIDEO_01_SageGreen_GridMat_Editorial_Dolly_4K60.mp4"
    return opc.generate_omni_flash_4k60_video(
        prompt=(
            "10-second 4K industrial design cinema shot on 35mm lens. "
            "Camera performs a slow, smooth editorial dolly push-in across a horizontal matte sage-green architectural drafting cutting mat "
            "showing the SHARP-CORNERED RECTANGULAR matte slate-blue Surf Forecast Instrument monolith (184 x 230 x 52 mm) standing beside "
            "a clothbound hardcover art monograph book for 1:1 scale. "
            "Maintain the exact sharp rectangular housing, strictly 9 upper radial ticks (8 to 4 o'clock), 100% blank bottom arc at 5, 6, 7 o'clock, "
            "and 2 burnt-orange pointer needles throughout all frames."
        ),
        start_image_path=s1_path,
        out_mp4_4k60_path=v_a04,
        aspect_ratio="16:9",
        extra_ref_paths=[
            s2_path,
            f"{GOLDEN}/INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg",
        ],
        max_retries=2,
    )

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(gen_a02)
        f2 = ex.submit(gen_a04)
        print("A02_VIDEO_01 result:", f1.result())
        print("A04_VIDEO_01 result:", f2.result())
