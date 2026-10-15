#!/usr/bin/env python3
import os
import sys
import json
import importlib.util

SCRIPT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts"
sys.path.insert(0, SCRIPT_DIR)

import omni_pro_client as opc

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    os.path.join(SCRIPT_DIR, "49_world_class_film_mastering.py")
)
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_02")

ING_07 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_02 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
REF_03 = os.path.join(opc.USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")
REFS = [ING_07, ING_02, REF_03]

still_01_path = os.path.join(OUT_DIR, "V6_A02_STILL_01_Levitating_Sunlit_Cream_Studio_4K.jpg")
still_02_path = os.path.join(OUT_DIR, "V6_A02_STILL_02_BrightAiry_Cream_Alcove_FloatingWall_4K.jpg")

prompt_01 = (
    "Surreal, hyper-clean high-fashion industrial design study shot on 35mm Kodak Vision3 50D film: "
    "the exact deep matte slate-blue rectangular Surf Clock (184 x 230 x 52 mm) effortlessly floating and levitating in mid-air "
    "8cm above a bright sunlit warm-cream travertine shelf against a bright airy cream plaster wall, casting a soft floating shadow underneath, "
    "bathed in golden morning coastal sunlight with soft out-of-focus eucalyptus leaf shadows. "
    "CRITICAL DIAL GEOMETRY: Match the reference dial 1:1 — strictly 9 raised white radial tick marks total on the upper semicircle "
    "(1 tick at FRESHIE 8 o'clock, 1 at 9 o'clock, 1 at QUEENSIE 10 o'clock, 1 at 11 o'clock, 1 at LONG REEF 12 o'clock, 1 at 1 o'clock, 1 at DEE WHY 2 o'clock, 1 at 3 o'clock, 1 at CURL CURL 4 o'clock — NEVER add extra ticks between them!). "
    "The bottom of the upper circle (5, 6, and 7 o'clock) MUST be 100% blank smooth matte slate-blue plastic with zero ticks."
)

print("=== Re-generating STILL 01 with gemini-3-pro-image for exact 9-tick perfection ===")
for i in range(3):
    opc.generate_4k_still(prompt_01, still_01_path, REFS, aspect_ratio="16:9", max_retries=1, model_name="gemini-3-pro-image")
    a01 = opc.self_audit_still(still_01_path)
    print(f"STILL 01 attempt {i+1} audit:", json.dumps(a01))
    if a01.get("pass"):
        break

# Re-run film mastering on STILL 01
s01_airy = still_01_path.replace("_4K.jpg", "_MASTER_AiryCream_4K.jpg")
s01_orchid = still_01_path.replace("_4K.jpg", "_MASTER_Orchid35mm_4K.jpg")
fm.apply_film_look_to_still(still_01_path, s01_airy, preset="airy_cream_sunlit_cinema")
fm.apply_film_look_to_still(still_01_path, s01_orchid, preset="orchid_35mm_250D_warm")

# Now generate the 16:9 4K 60fps 10-second Cinemagraph / Moving Photograph
video_01_path = os.path.join(OUT_DIR, "V6_A02_VIDEO_01_AiryCream_Sunlight_Cinemagraph_4K60.mp4")
video_prompt = (
    "10-second 4K 60fps Cinemagraph / Moving Photograph shot on 35mm Kodak Vision3 50D film on a heavy locked-off studio tripod. "
    "The camera and the deep matte slate-blue rectangular Surf Clock remain 100% rock-solid, stationary, and razor-sharp like a still fine-art photograph—ZERO camera movement, ZERO zooming, ZERO morphing of the clock or its hands. "
    "While the Surf Clock stays 100% still and crisp, warm golden morning coastal sunlight and delicate gossamer sheer linen curtain and eucalyptus leaf shadows gently drift and breathe across the bright airy warm-cream limewash plaster backdrop and travertine surface."
)

print("=== Generating VIDEO 01 Cinemagraph 4K60 ===")
opc.generate_omni_flash_4k60_video(
    prompt=video_prompt,
    start_image_path=still_02_path,
    out_mp4_4k60_path=video_01_path,
    aspect_ratio="16:9",
    extra_ref_paths=[ING_07, ING_02, REF_03],
    max_retries=3,
)

grid_path = video_01_path.replace(".mp4", "_audit_grid.jpg")
vid_audit = opc.self_audit_video_grid(grid_path) if os.path.exists(grid_path) else {}
print("FINAL VIDEO 01 AUDIT:", json.dumps(vid_audit))

# Apply 49_world_class_film_mastering.py to video as well (both airy_cream_sunlit_cinema & orchid_35mm_250D_warm)
v01_airy = video_01_path.replace("_4K60.mp4", "_MASTER_AiryCream_4K60.mp4")
v01_orchid = video_01_path.replace("_4K60.mp4", "_MASTER_Orchid35mm_4K60.mp4")
fm.apply_16mm_film_master_to_video(video_01_path, v01_airy, preset="airy_cream_sunlit_cinema")
fm.apply_16mm_film_master_to_video(video_01_path, v01_orchid, preset="orchid_35mm_250D_warm")
print("Film mastered videos saved:", v01_airy, v01_orchid)
