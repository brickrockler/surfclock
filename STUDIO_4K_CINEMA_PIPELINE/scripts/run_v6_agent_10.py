#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
    GOLDEN_DIR,
    USER_REF_DIR,
    FFMPEG,
    FFPROBE,
)
import importlib.util
spec_m = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py"
)
film_mastering = importlib.util.module_from_spec(spec_m)
spec_m.loader.exec_module(film_mastering)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v6_film_explorations/v6_agent_10"
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_05_UPPER = os.path.join(GOLDEN_DIR, "INGREDIENT_05_MACRO_UPPER_DIAL_9TICK_4K.jpg")
USER_REF_05 = os.path.join(USER_REF_DIR, "USER_REF_05_Tactile_VDI24_Molded_Plastic_Macro_LowerWorthIt_4K.jpg")
USER_REF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")
USER_REF_07 = os.path.join(USER_REF_DIR, "USER_REF_07_Poetry_Camera_16mm_Film_Bloom_Look.png")

STILL_SPECS = [
    {
        "filename": "V6_A10_STILL_01_Bolex16mm_Macro_SunlitCream_Bezel_4K.jpg",
        "refs": [ING_07, ING_05_UPPER, USER_REF_05],
        "prompt": (
            "16:9 widescreen 4K photochemical 16mm close-up product photograph of the deep matte slate-blue (#2D3E5E) Braun / Dieter Rams rectangular Surf Forecast Instrument "
            "(184 x 230 x 52 mm, sharp 90-degree rectangular stepped outer bezel and recessed flat rectangular dial well) mounted against a bright, airy, sun-drenched warm cream / chalk-ivory plaster wall "
            "with soft out-of-focus dappled eucalyptus leaf shadows. "
            "Shot on a spring-wound Bolex H16 16mm film camera with a Kern Macro-Switar 75mm f/1.9 lens on Kodak Vision3 50D (7203): "
            "extreme shallow depth of field softly blurring a golden sunlit eucalyptus leaf tip in the immediate foreground edge and the outer corner of the stepped bezel, "
            "while the entire recessed matte slate-blue dial face in the center of the frame is in razor-sharp optical focus, revealing the tactile VDI-24 micro-bead injection-molded plastic grain, "
            "the upper open semicircle with STRICTLY 9 raised white radial tick marks along the top arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) and raised white beach labels "
            "(FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), the 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom ticks), "
            "the lower WORTH IT? (NAH / YEAH) semicircular arc gauge, and strictly 2 skinny burnt-orange pointer needles (1 on upper dial, 1 on lower gauge) glowing with warm +1.3 EV 16mm golden highlight halation."
        ),
    },
    {
        "filename": "V6_A10_STILL_02_SplitDiopter_16mm_ForegroundShell_4K.jpg",
        "refs": [ING_07, ING_05_UPPER, USER_REF_05],
        "prompt": (
            "16:9 widescreen 4K art-house split-diopter 16mm cinema photograph shot on Arriflex 16SR3 / Bolex H16 with a 50mm lens + +2 optical split-field diopter attachment on Kodak Vision3 50D (7203). "
            "In the left foreground (left 28% of frame), a tactile sun-bleached spiral Australian Nautilus shell rests on a warm cream woven linen table surface in razor-sharp close-up macro focus. "
            "A soft, dreamy vertical optical split-diopter blur band separates the left foreground from the center-right background. "
            "In the center-right of the frame (occupying the central focal zone), the deep matte slate-blue (#2D3E5E) rectangular stepped-bezel Surf Forecast Instrument (184 x 230 x 52 mm) "
            "stands against a bright, airy, sun-drenched warm cream plaster wall with soft dappled golden afternoon light, ALSO in simultaneous razor-sharp optical focus! "
            "The Surf Clock dial clearly displays the tactile VDI-24 matte plastic grain, the upper open semicircle with STRICTLY 9 raised white radial tick marks on the top arc ONLY "
            "(8 to 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), a 100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock, "
            "the lower WORTH IT? (NAH / YEAH) gauge, and strictly 2 burnt-orange pointer needles total (1 upper, 1 lower). Warm 16mm photochemical bloom and organic silver-halide film texture."
        ),
    },
]

def run_still(spec):
    out_path = os.path.join(OUT_DIR, spec["filename"])
    raw_ungraded_path = out_path.replace("_4K.jpg", "_4K_raw_ungraded.jpg")
    graded_copy_path = out_path.replace("_4K.jpg", "_4K_poetry_camera_16mm_50D.jpg")
    print(f"=== Starting Still: {spec['filename']} ===", flush=True)
    ok = generate_4k_still(
        prompt=spec["prompt"],
        out_path=out_path,
        ref_image_paths=spec["refs"],
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image-preview",
    )
    if os.path.exists(out_path):
        shutil.copy2(out_path, raw_ungraded_path)
        film_mastering.apply_film_look_to_still(raw_ungraded_path, out_path, preset="poetry_camera_16mm_50D")
        shutil.copy2(out_path, graded_copy_path)
    audit = self_audit_still(out_path) if os.path.exists(out_path) else {"pass": False, "score": 0.0}
    print(f"=== Finished Still & 16mm 50D Grade: {spec['filename']} (ok={ok}, score={audit.get('score')}, pass={audit.get('pass')}) ===", flush=True)
    return spec["filename"], out_path, raw_ungraded_path, audit

def main():
    report = {"stills": {}, "videos": {}}

    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(run_still, s) for s in STILL_SPECS]
        for f in futures:
            fname, path, raw_path, audit = f.result()
            report["stills"][fname] = {"path": path, "raw_ungraded_path": raw_path, "audit": audit}

    still_01_raw = os.path.join(OUT_DIR, "V6_A10_STILL_01_Bolex16mm_Macro_SunlitCream_Bezel_4K_raw_ungraded.jpg")
    still_01_master = os.path.join(OUT_DIR, "V6_A10_STILL_01_Bolex16mm_Macro_SunlitCream_Bezel_4K.jpg")
    start_img = still_01_raw if os.path.exists(still_01_raw) else still_01_master

    video_filename = "V6_A10_VIDEO_01_Bolex16mm_Macro_Sunlight_Cinemagraph_4K60.mp4"
    out_mp4 = os.path.join(OUT_DIR, video_filename)
    ungraded_mp4 = out_mp4.replace("_4K60.mp4", "_4K60_raw_ungraded.mp4")
    graded_copy_mp4 = out_mp4.replace("_4K60.mp4", "_4K60_poetry_camera_16mm_50D.mp4")

    video_prompt = (
        "Locked-off 16mm Bolex H16 macro cinemagraph (moving photograph) on a heavy studio tripod with a Kern Macro-Switar 75mm f/1.9 lens on Kodak Vision3 50D film. "
        "ZERO camera movement: the camera is 100% locked-off and rock-solid so the deep matte slate-blue rectangular Surf Forecast Instrument stays completely still and razor-sharp like a photograph. "
        "ONLY the warm golden afternoon sunlight and soft out-of-focus Australian eucalyptus leaf shadows slowly and organically sweep and breathe across the bright warm cream plaster background, "
        "the stepped rectangular slate-blue bezel, the tactile VDI-24 micro-bead matte blue dial face, the raised white 3D letters (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, WORTH IT?, NAH, YEAH), "
        "the 9 upper radial white tick marks (with the bottom arc at 5, 6, and 7 o'clock remaining 100% blank smooth matte blue plastic), and the 2 skinny burnt-orange pointer needles."
    )

    print(f"=== Starting Video: {video_filename} ===", flush=True)
    ok_vid = generate_omni_flash_4k60_video(
        prompt=video_prompt,
        start_image_path=start_img,
        out_mp4_4k60_path=out_mp4,
        aspect_ratio="16:9",
        extra_ref_paths=[ING_07, ING_05_UPPER, USER_REF_05],
        max_retries=4,
    )

    if os.path.exists(out_mp4):
        shutil.copy2(out_mp4, ungraded_mp4)
        # Apply 49_world_class_film_mastering.py (poetry_camera_16mm_50D)
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

    report_path = os.path.join(OUT_DIR, "v6_agent_10_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"=== ALL V6 AGENT 10 OUTPUTS COMPLETED -> {report_path} ===", flush=True)

if __name__ == "__main__":
    main()
