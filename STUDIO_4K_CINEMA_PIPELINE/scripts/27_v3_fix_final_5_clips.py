#!/usr/bin/env python3
"""
Regenerates the final 5 clips (V3_REAL_11, V3_REAL_18, V3_REAL_20, V3_9x16_REAL_01, V3_9x16_REAL_11)
at native 1080p + 3 Close-Up Ingredients without the "Braun meter" phrase that caused a filled white semicircle or round housing,
strictly enforcing the vertical 3:4 rectangular Surf Clock with sharp 90-degree corners and thin hollow white semicircle line arc.
"""

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import importlib
m26 = importlib.import_module("26_v3_polish_and_expand_real_1080p_veo_suite")

STRICT_RECT_CLOCK_RULE = (
    "CRITICAL GEOMETRY & DIAL LOCK: The product is the exact vertical 3:4 rectangular Surf Clock shown in the reference images "
    "with sharp 90-degree outer corners and a deep rectangular recessed dark matte dial cavity (NEVER a round or circular housing, "
    "NEVER rounded corners). The bottom WORTH IT? dial is a thin white hollow semicircular line arc over the dark matte dial background "
    "(NEVER a solid white filled semicircle). The top dial has strictly ONE stationary orange pointer hand fixed at DEE WHY (2 o'clock) "
    "and the bottom arc has strictly ONE stationary orange pointer hand fixed at YEAH (4 o'clock). The hands never move or split. "
    "The front dial stays facing the camera with razor-sharp LONG REEF, QUEENSIE, DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT? text."
)

FINAL_5_JOBS = [
    {
        "id": "V3_REAL_11_Float_DieterRams_IceGrey_Weightless_In_Sunbeam",
        "aspect": "16:9",
        "keyframe": m26.resolve_kf(m26.STILLS_16x9_DIR, "V3_15"),
        "force": True,
        "prompt": (
            "Real 35mm cinema shot of the vertical 3:4 rectangular Surf Clock (Matte Ice-Grey RAL 7035 rectangular outer frame, "
            "dark charcoal-black rectangular recessed dial face) levitating weightlessly in mid-air inside a sunlit minimalist "
            "architectural studio with warm Venetian blind shadow stripes on the plaster wall behind it. Smooth 3D camera slider "
            "movement with real parallax while the clock hovers facing the camera. " + STRICT_RECT_CLOCK_RULE
        ),
    },
    {
        "id": "V3_REAL_18_Studio_Clean_SlateBlue_Chiaroscuro_3D_Orbit",
        "aspect": "16:9",
        "keyframe": m26.resolve_kf(m26.STILLS_16x9_DIR, "V3_31"),
        "force": True,
        "prompt": (
            "High-end real commercial studio cinema shot on Arri Alexa 65 with 85mm Master Prime lens. "
            "The vertical 3:4 rectangular matte slate-blue Surf Clock with sharp 90-degree corners stands on a dark cleft slate stone "
            "plinth in a darkslate studio. The camera executes a gentle 10-degree front 3D slider movement while the rectangular clock "
            "stays facing the camera as soft warm tungsten rim lighting glides across the tactile VDI-24 matte bezel. "
            + STRICT_RECT_CLOCK_RULE
        ),
    },
    {
        "id": "V3_REAL_20_Studio_Rear_Fluted_Borosilicate_WarmLight_Orbit",
        "aspect": "16:9",
        "keyframe": m26.resolve_kf(m26.STILLS_16x9_DIR, "V3_32"),
        "force": True,
        "prompt": (
            "High-end real commercial studio macro cinema shot on Arri Alexa 65 with 100mm Macro Prime lens. "
            "Slow, smooth 3D camera slider movement across the front of the vertical 3:4 rectangular matte slate-blue Surf Clock on a "
            "dark slate studio plinth, showcasing the tactile VDI-24 micro-bead polymer grain, sharp 90-degree stepped bezel, matte "
            "orange pointer hand fixed at DEE WHY, and thin hollow white semicircle arc with orange pointer hand fixed at YEAH. "
            + STRICT_RECT_CLOCK_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_01_Studio_SlateBlue_Chiaroscuro_3D_Dolly",
        "aspect": "9:16",
        "keyframe": m26.resolve_kf(m26.STILLS_9x16_DIR, "V3_9x16_01"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real studio cinema shot on Arri Alexa 65. The vertical 3:4 rectangular matte slate-blue Surf Clock "
            "with sharp 90-degree corners stands on a dark cleft slate plinth. Smooth, slow 3D camera slider push-in with warm tungsten "
            "chiaroscuro key lighting across the rectangular stepped bezel and recessed dark matte slate-blue dial. "
            + STRICT_RECT_CLOCK_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_11_Handycam_90s_Hi8_Coastal_Headland_SurfCheck",
        "aspect": "9:16",
        "keyframe": m26.resolve_kf(m26.STILLS_9x16_DIR, "V3_9x16_10"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real 1990s Sony Hi8 Handycam camcorder video on a weathered sandstone ledge overlooking a coastal "
            "headland. Real turquoise ocean waves roll toward the beach in the background while green spinifex grass sways in the sea "
            "breeze beside the vertical 3:4 rectangular matte slate-blue Surf Clock. " + STRICT_RECT_CLOCK_RULE
        ),
    },
]

def get_dur(mp4: Path) -> float:
    import cv2
    cap = cv2.VideoCapture(str(mp4))
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
    cap.release()
    return frames / fps if fps > 0 else 5.0

def main():
    print("=== REGENERATING FINAL 5 CLIPS WITH STRICT RECTANGULAR 3:4 + HOLLOW ARC LOCK ===", flush=True)
    completed = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = {pool.submit(m26.generate_and_wait, job): job for job in FINAL_5_JOBS}
        for fut in as_completed(futs):
            job = futs[fut]
            raw_mp4 = fut.result()
            completed.append((job, raw_mp4))

    for job, raw_mp4 in completed:
        m26.master_clip_to_4k_60fps(raw_mp4, job["aspect"], job["id"])

    print("=== FINAL 5 CLIPS MASTERED TO 4K 60FPS ===", flush=True)

if __name__ == "__main__":
    main()
