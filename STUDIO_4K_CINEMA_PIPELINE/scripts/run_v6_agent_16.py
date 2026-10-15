#!/usr/bin/env python3
import os
import sys
import json
import shutil
import importlib.util
from concurrent.futures import ThreadPoolExecutor

SCRIPT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts"
sys.path.insert(0, SCRIPT_DIR)

import omni_pro_client as opc
from omni_pro_client import (
    GOLDEN_DIR,
    USER_REF_DIR,
    generate_4k_still,
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
)

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    os.path.join(SCRIPT_DIR, "49_world_class_film_mastering.py"),
)
film_mastering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(film_mastering)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_16")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_02 = os.path.join(GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
USER_REF_04 = os.path.join(USER_REF_DIR, "USER_REF_04_Filmic_Dappled_Light_Composition.png")

REFS = [ING_07, ING_02, USER_REF_04]

STILL_SPECS = [
    {
        "filename": "V6_A16_STILL_01_Super16_RockPool_MirrorReflection_4K.jpg",
        "refs": REFS,
        "prompt": (
            "16:9 widescreen 4K photochemical Super16 motion picture frame shot on Kodak Vision3 50D (7203) with an Arriflex 16SR3 and a Zeiss Super Speed 50mm T1.3 lens at f/1.4 at a low cinematic angle (Poetry Camera & Telepathic Instruments Orchid launch film aesthetic): "
            "the exact deep matte slate-blue (#2D3E5E) rectangular Braun / Dieter Rams Surf Forecast Instrument (184 x 230 x 52 mm, hardcover art monograph scale, sharp 90-degree rectangular stepped outer bezel and deeply recessed flat rectangular dial well) "
            "standing upright on a dry, sun-bleached pale warm-cream Sydney coastal sandstone rock ledge right beside a still, glassy coastal tidal rock pool in the foreground. "
            "The tranquil mirror-like surface of the shallow coastal rock pool reflects the warm golden-ivory late-afternoon sky and the soft inverted silhouette of the slate-blue rectangular Surf Clock, "
            "while the distant background melts into heavy f/1.4 creamy golden-hour bokeh of turquoise Australian ocean swell and sunlit sea spray (+1.3 EV warm highlight bloom, subtle red-orange halation around sunlit sandstone edges, organic 16mm silver-halide grain). "
            "IMPORTANT: Keep the entire rectangular Surf Clock dial face 100% unobstructed and in razor-sharp optical focus in the center-upper focal plane, clearly showing the tactile VDI-24 micro-bead matte plastic texture, "
            "the upper open semicircle with STRICTLY 9 raised white radial tick marks along the top arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) and 5 raised white beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
            "the 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom ticks), the lower WORTH IT? (NAH / YEAH) semicircular gauge, and strictly 2 skinny burnt-orange pointer needles total (1 upper, 1 lower)."
        ),
    },
    {
        "filename": "V6_A16_STILL_02_Super16_Sunbleached_TimberPier_4K.jpg",
        "refs": REFS,
        "prompt": (
            "16:9 widescreen 4K photochemical Super16 film frame shot on Kodak Vision3 50D (7203) with an Arriflex 16SR3 and Cooke Speed Panchro 50mm lens at f/1.6 (Poetry Camera & Telepathic Instruments Orchid launch film aesthetic): "
            "the exact deep matte slate-blue (#2D3E5E) rectangular Braun / Dieter Rams Surf Forecast Instrument (184 x 230 x 52 mm, hardcover-book scale, sharp 90-degree rectangular stepped outer bezel and recessed flat rectangular dial well) "
            "resting cleanly on weathered, sun-bleached silver-cream Australian coastal timber pier planks bathed in luminous golden-hour coastal sunlight, with soft dappled eucalyptus shadows, warm golden highlight halation (+1.3 EV bloom), "
            "and dreamy out-of-focus shimmering sea-spray light bokeh orbs glowing in the background and extreme foreground edge. "
            "IMPORTANT: Keep the entire rectangular Surf Clock dial face 100% unobstructed and in razor-sharp optical focus so the tactile VDI-24 matte plastic grain, "
            "the upper open semicircle with STRICTLY 9 raised white radial tick marks along the top arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
            "the 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom ticks), the lower WORTH IT? (NAH / YEAH) gauge, and strictly 2 skinny burnt-orange pointer needles total (1 upper, 1 lower) are crystal clear."
        ),
    },
]

def run_still(spec_item):
    out_path = os.path.join(OUT_DIR, spec_item["filename"])
    raw_ungraded_path = out_path.replace("_4K.jpg", "_4K_raw_ungraded.jpg")
    graded_copy_path = out_path.replace("_4K.jpg", "_4K_poetry_camera_16mm_50D.jpg")
    print(f"=== Starting Still: {spec_item['filename']} ===", flush=True)
    ok = generate_4k_still(
        prompt=spec_item["prompt"],
        out_path=out_path,
        ref_image_paths=spec_item["refs"],
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image",
    )
    if os.path.exists(out_path):
        shutil.copy2(out_path, raw_ungraded_path)
        film_mastering.apply_film_look_to_still(raw_ungraded_path, out_path, preset="poetry_camera_16mm_50D")
        shutil.copy2(out_path, graded_copy_path)
    audit = self_audit_still(out_path) if os.path.exists(out_path) else {"pass": False, "score": 0.0}
    print(f"=== Finished Still & 16mm 50D Grade: {spec_item['filename']} (ok={ok}, score={audit.get('score')}, pass={audit.get('pass')}) ===", flush=True)
    return spec_item["filename"], out_path, raw_ungraded_path, graded_copy_path, audit

def main():
    report = {"stills": {}, "videos": {}}

    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(run_still, s) for s in STILL_SPECS]
        for f in futures:
            fname, path, raw_path, graded_path, audit = f.result()
            report["stills"][fname] = {
                "path": path,
                "raw_ungraded_path": raw_path,
                "graded_copy_path": graded_path,
                "audit": audit,
            }

    still_01_raw = os.path.join(OUT_DIR, "V6_A16_STILL_01_Super16_RockPool_MirrorReflection_4K_raw_ungraded.jpg")
    still_01_master = os.path.join(OUT_DIR, "V6_A16_STILL_01_Super16_RockPool_MirrorReflection_4K.jpg")
    start_img = still_01_raw if os.path.exists(still_01_raw) else (still_01_master if os.path.exists(still_01_master) else ING_07)

    video_filename = "V6_A16_VIDEO_01_Super16_RockPool_Ripple_Cinemagraph_4K60.mp4"
    out_mp4 = os.path.join(OUT_DIR, video_filename)
    ungraded_mp4 = out_mp4.replace("_4K60.mp4", "_4K60_raw_ungraded.mp4")
    graded_copy_mp4 = out_mp4.replace("_4K60.mp4", "_4K60_poetry_camera_16mm_50D.mp4")

    video_prompt = (
        "Locked-off Super16 Arriflex 16SR3 tripod cinemagraph (moving photograph) shot on Kodak Vision3 50D film at low angle with a Zeiss Super Speed T1.3 lens at f/1.4. "
        "CAMERA 100% LOCKED-OFF AND STATIONARY ON A HEAVY TRIPOD (ZERO camera pan, ZERO zoom, ZERO camera rotation). "
        "The deep matte slate-blue rectangular Surf Forecast Instrument standing on the dry pale warm-cream sandstone rock ledge stays 100% rock-solid, motionless, and razor-sharp like a still photograph "
        "(with its 9 upper radial white tick marks from 8 to 4 o'clock, 100% blank smooth matte blue bottom arc at 5, 6, and 7 o'clock, 5 beach labels FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, lower WORTH IT? NAH/YEAH gauge, and 2 skinny burnt-orange pointer needles completely stationary and crisp), "
        "while ONLY the golden-hour water reflection in the shallow glassy coastal tidal pool in the foreground gently ripples in a soft coastal breeze and the distant f/1.4 turquoise ocean bokeh softly shimmers."
    )

    print(f"=== Starting Video: {video_filename} ===", flush=True)
    ok_vid = generate_omni_flash_4k60_video(
        prompt=video_prompt,
        start_image_path=start_img,
        out_mp4_4k60_path=out_mp4,
        aspect_ratio="16:9",
        extra_ref_paths=REFS,
        max_retries=4,
    )

    if os.path.exists(out_mp4):
        shutil.copy2(out_mp4, ungraded_mp4)
        film_mastering.apply_16mm_film_master_to_video(ungraded_mp4, graded_copy_mp4, preset="poetry_camera_16mm_50D")
        shutil.copy2(graded_copy_mp4, out_mp4)

    grid_jpg = out_mp4.replace(".mp4", "_audit_grid.jpg")
    vaudit = self_audit_video_grid(grid_jpg) if os.path.exists(grid_jpg) else {"pass": False, "score": 0.0}
    report["videos"][video_filename] = {
        "path": out_mp4,
        "graded_copy_path": graded_copy_mp4,
        "raw_ungraded_path": ungraded_mp4,
        "audit": vaudit,
    }

    report_path = os.path.join(OUT_DIR, "v6_agent_16_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"=== ALL V6 AGENT 16 OUTPUTS COMPLETED -> {report_path} ===", flush=True)

if __name__ == "__main__":
    main()
