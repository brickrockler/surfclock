#!/usr/bin/env python3
import os
import sys
import shutil

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc
import importlib.util

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py",
)
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_07")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_04 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_04_Filmic_Dappled_Light_Composition.png")
REF_07 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_07_Poetry_Camera_16mm_Film_Bloom_Look.png")
REFS = [ING_07, REF_04, REF_07]

STILL_01 = os.path.join(OUT_DIR, "V6_A07_STILL_01_HeavyBokeh_BillyButtons_CreamWall_16mm_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A07_STILL_01_HeavyBokeh_BillyButtons_CreamWall_16mm_RAW_4K.jpg")
STILL_02 = os.path.join(OUT_DIR, "V6_A07_STILL_02_HeavyBokeh_Eucalyptus_SunFlare_16mm_4K.jpg")
STILL_02_RAW = os.path.join(OUT_DIR, "V6_A07_STILL_02_HeavyBokeh_Eucalyptus_SunFlare_16mm_RAW_4K.jpg")
VIDEO_01 = os.path.join(OUT_DIR, "V6_A07_VIDEO_01_HeavyBokeh_BillyButtons_Cinemagraph_4K60.mp4")
VIDEO_01_PREGRADE = os.path.join(OUT_DIR, "V6_A07_VIDEO_01_HeavyBokeh_BillyButtons_Cinemagraph_PREGRADE_4K60.mp4")

PROMPT_STILL_01 = (
    "Shot on 16mm Kodak Vision3 50D (7203) motion picture film with an Arriflex 16SR3 and a fast 58mm f/1.2 vintage prime lens wide open (Poetry Camera & Telepathic Instruments Orchid launch film aesthetic). "
    "Large, dreamy, heavily out-of-focus golden spheres of native Australian Billy Buttons (Craspedia globosa) and feathery bronze-gold Kangaroo Grass right in front of the lens along the left, right, and lower frame edges create glowing warm golden foreground bokeh orbs (+1.3 EV warm highlight bloom and subtle red-orange halation). "
    "The foreground botanicals part cleanly in the center of the frame to reveal the 100% unobstructed, razor-sharp deep matte slate-blue (#2D3E5E) rectangular Surf Clock (184 x 230 x 52 mm) mounted/resting against a bright, airy, sun-drenched warm cream / chalk-ivory plaster architectural wall with soft dappled afternoon sunlight shadows. "
    "IMPORTANT: Keep the entire rectangular Surf Clock dial face 100% unobstructed and razor-sharp in the center focal plane so every letter (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, WORTH IT?, NAH, YEAH), the 9 upper radial ticks (8 to 4 o'clock), the 100% blank smooth matte blue bottom arc (5, 6, 7 o'clock), and the 2 burnt-orange pointer needles are crystal clear."
)

PROMPT_STILL_02 = (
    "Shot on 16mm Kodak Vision3 50D (7203) motion picture film through a fast 58mm f/1.2 lens wide open. "
    "Heavy f/1.2 foreground bokeh of sun-kissed silver-green native Australian eucalyptus leaves right in front of the left and upper-right edges of the lens, glowing with warm golden sun-flare edge halation, +1.3 EV highlight bloom, and subtle lateral chromatic aberration. "
    "The blurred foreground eucalyptus leaves part cleanly to frame a razor-sharp focus on the unobstructed deep matte slate-blue (#2D3E5E) rectangular Surf Clock (184 x 230 x 52 mm) standing on a warm sunlit coastal Sydney sandstone ledge in front of a bright warm cream plaster wall with soft dappled leaf shadows. "
    "IMPORTANT: Keep the entire rectangular Surf Clock dial face 100% unobstructed and razor-sharp in the focal plane so all 9 upper radial ticks (8 to 4 o'clock), the 100% blank bottom arc (5, 6, 7 o'clock), the 5 beach labels, the lower WORTH IT? (NAH/YEAH) gauge, and the 2 burnt-orange pointer needles are completely clear and legible."
)

PROMPT_VIDEO_01 = (
    "Locked-off 16mm Arriflex tripod cinemagraph / moving photograph shot on Kodak Vision3 50D through a 58mm f/1.2 lens wide open. "
    "CAMERA LOCKED 100% STILL ON A HEAVY TRIPOD (ZERO camera pan, ZERO zoom, ZERO camera rotation). "
    "The deep matte slate-blue rectangular Surf Clock in the midground against the sunlit warm cream plaster wall stays 100% rock-solid, razor-sharp, and motionless like a still photograph (with its 9 upper ticks, blank 5-6-7 o'clock bottom arc, and 2 burnt-orange needles completely stationary and unobstructed), "
    "while ONLY the large dreamy out-of-focus golden Billy Buttons (Craspedia globosa) and feathery Kangaroo Grass bokeh in the extreme foreground and the dappled golden sunlight shadows on the cream plaster wall gently sway in a warm coastal breeze."
)

print("=== STEP 1: Generating STILL 01 ===")
ok1 = opc.generate_4k_still(
    prompt=PROMPT_STILL_01,
    out_path=STILL_01,
    ref_image_paths=REFS,
    aspect_ratio="16:9",
    max_retries=5,
)
print("STILL 01 generated:", ok1)
if os.path.exists(STILL_01):
    shutil.copy2(STILL_01, STILL_01_RAW)
    fm.apply_film_look_to_still(STILL_01_RAW, STILL_01, preset="poetry_camera_16mm_50D")
    audit1 = opc.self_audit_still(STILL_01)
    print("STILL 01 post-grade audit:", audit1)

print("=== STEP 2: Generating STILL 02 ===")
ok2 = opc.generate_4k_still(
    prompt=PROMPT_STILL_02,
    out_path=STILL_02,
    ref_image_paths=REFS,
    aspect_ratio="16:9",
    max_retries=5,
)
print("STILL 02 generated:", ok2)
if os.path.exists(STILL_02):
    shutil.copy2(STILL_02, STILL_02_RAW)
    fm.apply_film_look_to_still(STILL_02_RAW, STILL_02, preset="poetry_camera_16mm_50D")
    audit2 = opc.self_audit_still(STILL_02)
    print("STILL 02 post-grade audit:", audit2)

print("=== STEP 3: Generating VIDEO 01 (16mm Film Cinemagraph 4K60) ===")
start_img = STILL_01 if os.path.exists(STILL_01) else ING_07
ok_vid = opc.generate_omni_flash_4k60_video(
    prompt=PROMPT_VIDEO_01,
    start_image_path=start_img,
    out_mp4_4k60_path=VIDEO_01_PREGRADE,
    aspect_ratio="16:9",
    extra_ref_paths=REFS,
    max_retries=4,
)
print("VIDEO 01 pregrade generated:", ok_vid)
if os.path.exists(VIDEO_01_PREGRADE):
    fm.apply_16mm_film_master_to_video(VIDEO_01_PREGRADE, VIDEO_01, preset="poetry_camera_16mm_50D")
    print("VIDEO 01 mastered with poetry_camera_16mm_50D:", os.path.exists(VIDEO_01))
