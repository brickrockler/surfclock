#!/usr/bin/env python3
import os
import sys
import json
import importlib.util

sys.path.append("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
from omni_pro_client import (
    generate_4k_still,
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
    GOLDEN_DIR,
    USER_REF_DIR,
    FFMPEG,
)

# Load 49_world_class_film_mastering.py
spec = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py",
)
film_mastering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(film_mastering)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v6_film_explorations/v6_agent_01"
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
UREF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
UREF_03 = os.path.join(USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")

REFS_STILL_01 = [UREF_02, ING_07, ING_01]
REFS_STILL_02 = [UREF_02, UREF_03, ING_07, ING_01]

still_01_name = "V6_A01_STILL_01_Floating_WarmCream_Eucalyptus_Hero_4K.jpg"
still_01_path = os.path.join(OUT_DIR, still_01_name)
still_01_prompt = (
    "Breathtaking, bright, airy Australian coastal architectural product photography matching the exact composition and lighting of Reference Image 1 (USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png): "
    "Direct orthographic front-facing floating shot of the deep matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm, hardcover art monograph book scale) mounted flush and floating cleanly in the center of a bright, airy, sun-drenched warm cream plaster wall (#F6EFE2). "
    "Soft, out-of-focus dappled coastal eucalyptus leaf shadows fall organically across the left side of the warm cream limewash plaster wall and subtly kiss the left edge of the frame, while a crisp diagonal golden morning sunbeam illuminates the right side of the wall, casting a clean architectural contact and drop shadow to the bottom-right of the rectangular slate-blue clock. "
    "Shot on medium-format Hasselblad H6D-100c 80mm lens with Kodak Vision3 50D daylight color sensitivity: tactile VDI-24 micro-bead matte slate-blue injection-molded casing, sharp 90-degree rectangular stepped outer bezel, deeply recessed flat rectangular dial face with zero glass cover. "
    "Upper beach dial features strictly 9 raised white radial tick marks along the top semicircle ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with raised white rounded-sans beach names ('FRESHIE' at 8, 'QUEENSIE' at 10, 'LONG REEF' at 12, 'DEE WHY' at 2, 'CURL CURL' at 4 o'clock). "
    "The bottom arc of the upper dial (5, 6, and 7 o'clock, between FRESHIE and CURL CURL) is 100% BLANK SMOOTH MATTE SLATE-BLUE PLASTIC with zero tick marks and zero numbers. "
    "Below sits the raised white semicircular 'WORTH IT?' gauge ('NAH' on left, 'YEAH' on right, 'WORTH IT?' centered below). "
    "Strictly 2 burnt-orange pointer hands total: 1 long skinny burnt-orange needle on the upper dial pointing toward DEE WHY, and 1 short skinny burnt-orange needle on the lower WORTH IT? gauge pointing toward YEAH."
)

still_02_name = "V6_A01_STILL_02_Floating_ChalkIvory_WideAiry_Wall_4K.jpg"
still_02_path = os.path.join(OUT_DIR, still_02_name)
still_02_prompt = (
    "Wide, airy, high-key architectural editorial photograph of the deep matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm, hardcover-book scale) floating mounted on an expansive, sun-drenched chalk-ivory Venetian plaster wall (#F8F3E8) in a minimal Northern Beaches architectural residence. "
    "Generous negative space surrounds the floating rectangular monolith, with delicate, soft-focus dancing Australian eucalyptus and banksia botanical shadows dappling the warm chalk-ivory plaster wall in bright morning coastal sunlight, feeling beachy, minimal, serene, and expensive. "
    "Crisp natural architectural drop shadow cast to the bottom-right of the 52mm-deep slate-blue rectangular housing. "
    "Razor-sharp focus on the tactile VDI-24 matte slate-blue dial face (zero glass cover, zero glare): strictly 9 raised white radial tick marks on the upper semicircle (8 to 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte slate-blue plastic at the bottom arc (5, 6, and 7 o'clock), raised white lower WORTH IT? (NAH / YEAH) semicircular gauge, and strictly 2 burnt-orange pointer needles total (1 upper needle, 1 lower needle)."
)

results = {"stills": {}, "videos": {}}

print(f"=== 1. Generating {still_01_name} ===")
generate_4k_still(
    prompt=still_01_prompt,
    out_path=still_01_path,
    ref_image_paths=REFS_STILL_01,
    aspect_ratio="16:9",
    max_retries=5,
    model_name="gemini-3-pro-image",
)
audit_s1 = self_audit_still(still_01_path)
results["stills"][still_01_name] = {"path": still_01_path, "audit": audit_s1}

print(f"=== 2. Generating {still_02_name} ===")
generate_4k_still(
    prompt=still_02_prompt,
    out_path=still_02_path,
    ref_image_paths=REFS_STILL_02,
    aspect_ratio="16:9",
    max_retries=5,
    model_name="gemini-3-pro-image",
)
audit_s2 = self_audit_still(still_02_path)
results["stills"][still_02_name] = {"path": still_02_path, "audit": audit_s2}

video_01_name = "V6_A01_VIDEO_01_Floating_WarmCream_Dappled_Cinemagraph_4K60.mp4"
video_01_path = os.path.join(OUT_DIR, video_01_name)
video_01_prompt = (
    "CRITICAL CINEMAGRAPH / MOVING PHOTOGRAPH DIRECTION: 100% LOCKED-OFF HEAVY TRIPOD CAMERA (ZERO CAMERA MOVEMENT, ZERO ZOOM, ZERO PAN, ZERO ORBIT!). "
    "The deep matte slate-blue rectangular Surf Forecast Instrument mounted floating on the bright, airy warm cream plaster wall (#F6EFE2) remains 100% rock-solid, stationary, and razor-sharp like a still photograph. "
    "ONLY the soft, out-of-focus dappled eucalyptus leaf shadows on the warm cream plaster wall gently ripple, breathe, and sway in the slow coastal morning breeze, while the warm diagonal sunlight and the clock housing, typography, 9 upper radial ticks (with 100% blank bottom arc at 5, 6, 7 o'clock), and 2 burnt-orange pointer needles remain completely still and rock-solid."
)

print(f"=== 3. Generating {video_01_name} ===")
generate_omni_flash_4k60_video(
    prompt=video_01_prompt,
    start_image_path=still_01_path,
    out_mp4_4k60_path=video_01_path,
    aspect_ratio="16:9",
    extra_ref_paths=[UREF_02, ING_07, ING_01],
    max_retries=4,
)
grid_v1 = video_01_path.replace(".mp4", "_audit_grid.jpg")
audit_v1 = self_audit_video_grid(grid_v1) if os.path.exists(grid_v1) else {"pass": False}
results["videos"][video_01_name] = {"path": video_01_path, "audit": audit_v1}

# 4. Kodak Vision3 50D photochemical film-graded versions
still_01_film_name = "V6_A01_STILL_01_FilmGrade_50D_4K.jpg"
still_01_film_path = os.path.join(OUT_DIR, still_01_film_name)
print(f"=== 4. Mastering {still_01_film_name} (Kodak Vision3 50D) ===")
film_mastering.apply_film_look_to_still(
    in_path=still_01_path,
    out_path=still_01_film_path,
    preset="poetry_camera_16mm_50D",
)
audit_s1_film = self_audit_still(still_01_film_path)
results["stills"][still_01_film_name] = {"path": still_01_film_path, "audit": audit_s1_film}

video_01_film_name = "V6_A01_VIDEO_01_FilmGrade_50D_4K60.mp4"
video_01_film_path = os.path.join(OUT_DIR, video_01_film_name)
print(f"=== 5. Mastering {video_01_film_name} (Kodak Vision3 50D) ===")
film_mastering.apply_16mm_film_master_to_video(
    in_mp4=video_01_path,
    out_mp4=video_01_film_path,
    preset="poetry_camera_16mm_50D",
)
grid_v1_film = video_01_film_path.replace(".mp4", "_audit_grid.jpg")
import subprocess
subprocess.run(
    [FFMPEG, "-y", "-i", video_01_film_path, "-vf", "select='eq(n,0)+eq(n,60)+eq(n,120)+eq(n,180)',scale=1280:-1,tile=2x2", "-frames:v", "1", grid_v1_film],
    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
audit_v1_film = self_audit_video_grid(grid_v1_film) if os.path.exists(grid_v1_film) else {"pass": False}
results["videos"][video_01_film_name] = {"path": video_01_film_path, "audit": audit_v1_film}

report_path = os.path.join(OUT_DIR, "v6_agent_01_audit_report.json")
with open(report_path, "w") as f:
    json.dump(results, f, indent=2)

print("=== V6 AGENT 01 COMPLETE ===")
print(json.dumps(results, indent=2))
