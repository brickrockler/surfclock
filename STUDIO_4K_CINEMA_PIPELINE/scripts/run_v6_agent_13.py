#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

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
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_13")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(BASE, "00_GOLDEN_INGREDIENTS_4K", "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_04 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_04_Filmic_Dappled_Light_Composition.png")
REF_07 = os.path.join(BASE, "00_USER_QUALITY_REFERENCES", "USER_REF_07_Poetry_Camera_16mm_Film_Bloom_Look.png")
REFS = [ING_07, REF_04, REF_07]

STILL_01 = os.path.join(OUT_DIR, "V6_A13_STILL_01_Anamorphic16mm_LouverSunbeam_CreamWall_4K.jpg")
STILL_01_RAW = os.path.join(OUT_DIR, "V6_A13_STILL_01_Anamorphic16mm_LouverSunbeam_CreamWall_RAW_4K.jpg")

STILL_02 = os.path.join(OUT_DIR, "V6_A13_STILL_02_Anamorphic16mm_GoldenDustMotes_4K.jpg")
STILL_02_RAW = os.path.join(OUT_DIR, "V6_A13_STILL_02_Anamorphic16mm_GoldenDustMotes_RAW_4K.jpg")

VIDEO_01 = os.path.join(OUT_DIR, "V6_A13_VIDEO_01_Anamorphic16mm_DustMotes_Cinemagraph_4K60.mp4")
VIDEO_01_PREGRADE = os.path.join(OUT_DIR, "V6_A13_VIDEO_01_Anamorphic16mm_DustMotes_Cinemagraph_PREGRADE_4K60.mp4")

PROMPT_STILL_01 = (
    "16:9 widescreen 4K photochemical 16mm motion-picture frame shot on Kodak Vision3 250D (5207) with an Arriflex 16SR3 and a vintage Lomo round-front anamorphic lens "
    "(Poetry Camera & Telepathic Instruments Orchid launch film aesthetic). "
    "The deep matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm, hardcover-book scale, sharp 90-degree rectangular stepped outer bezel and recessed flat rectangular dial face) "
    "is mounted cleanly on a bright, airy, sun-drenched warm cream / chalk-ivory coastal plaster wall inside an elevated Australian surf shack. "
    "Warm golden late-afternoon slats of coastal sunlight pass diagonally through frosted and clear glass jalousie louvers on the left, casting luminous parallel golden sunbeams and soft louvered shadow bands across the warm cream plaster wall and kissing the outer stepped bezel. "
    "Authentic vintage Lomo anamorphic optical character: creamy vertically-stretched oval bokeh in the out-of-focus foreground/background edges, a delicate warm amber horizontal anamorphic streak flare gliding cleanly across the upper bezel edge without obscuring the dial, +1.3 EV golden highlight halation, subtle lateral chromatic aberration at the extreme frame edges, and organic 16mm silver-halide grain. "
    "IMPORTANT: Keep the recessed matte slate-blue dial face in razor-sharp optical focus and 100% unobstructed: strictly 9 raised white radial tick marks along the top semicircle ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock) with raised white rounded-sans beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
    "100% BLANK smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock (zero bottom ticks), lower WORTH IT? (NAH / YEAH) semicircular gauge, and strictly 2 skinny burnt-orange pointer needles total (1 upper, 1 lower)."
)

PROMPT_STILL_02 = (
    "16:9 widescreen 4K photochemical 16mm motion-picture frame shot on Kodak Vision3 250D / 50D with an Arriflex 16SR3 and a vintage Lomo anamorphic lens wide open at T2.0 "
    "(Poetry Camera & Telepathic Instruments Orchid launch film aesthetic). "
    "Intimate 16mm film vignette with glowing golden dust motes suspended in a diagonal shaft of warm coastal afternoon sun slanting across the deep matte slate-blue (#2D3E5E) rectangular Surf Forecast Instrument (184 x 230 x 52 mm) "
    "against a bright, airy, sunlit warm cream / chalk-ivory plaster backdrop with soft dappled eucalyptus and louver light. "
    "Out-of-focus foreground dust motes catch the backlight as dreamy, vertically-oval Lomo anamorphic golden bokeh orbs around the periphery of the frame, with subtle warm amber horizontal anamorphic edge flare and +1.3 EV golden halation. "
    "IMPORTANT: The entire rectangular matte slate-blue Surf Clock dial face in the center focal plane is 100% unobstructed and in razor-sharp focus, showing the tactile VDI-24 micro-bead matte plastic texture, "
    "strictly 9 raised white radial tick marks on the upper semicircle ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock around FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
    "100% BLANK smooth matte slate-blue plastic at the bottom of the upper dial (5, 6, and 7 o'clock), the lower WORTH IT? (NAH / YEAH) semicircular gauge, and strictly 2 skinny burnt-orange pointer needles total (1 on upper dial, 1 on lower gauge)."
)

PROMPT_VIDEO_01 = (
    "CRITICAL 16MM FILM CINEMAGRAPH / MOVING PHOTOGRAPH DIRECTION: 100% LOCKED-OFF HEAVY TRIPOD CAMERA (ZERO CAMERA PAN, ZERO ZOOM, ZERO TILT, ZERO CAMERA DRIFT!). "
    "Shot on 16mm Kodak Vision3 film with a vintage Lomo anamorphic lens on a locked-off studio tripod. "
    "The deep matte slate-blue rectangular Surf Forecast Instrument against the bright sunlit warm cream plaster wall is 100% motionless, rock-solid, and razor-sharp like a still photograph "
    "(with its 9 upper radial white ticks from 8 to 4 o'clock, 100% blank bottom arc at 5, 6, and 7 o'clock, raised white beach typography, and 2 burnt-orange pointer needles completely stationary and unobstructed). "
    "ONLY the glowing golden dust motes suspended in the diagonal shaft of warm coastal afternoon sunlight float, drift, and shimmer lazily through the sunbeam with soft oval anamorphic bokeh."
)

def generate_and_master_still(name, out_path, raw_path, prompt):
    print(f"=== Starting {name} ===", flush=True)
    ok = opc.generate_4k_still(
        prompt=prompt,
        out_path=out_path,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image",
    )
    audit_raw = None
    audit_graded = None
    if os.path.exists(out_path):
        shutil.copy2(out_path, raw_path)
        audit_raw = opc.self_audit_still(raw_path)
        fm.apply_film_look_to_still(raw_path, out_path, preset="poetry_camera_16mm_50D")
        audit_graded = opc.self_audit_still(out_path)
        print(f"=== Completed {name}: ok={ok}, graded_audit={audit_graded} ===", flush=True)
    return {"ok": ok, "path": out_path, "raw_path": raw_path, "audit_raw": audit_raw, "audit_graded": audit_graded}

def main():
    report = {"agent": "v6_agent_13", "stills": {}, "videos": {}}

    with ThreadPoolExecutor(max_workers=2) as ex:
        f1 = ex.submit(generate_and_master_still, "STILL_01", STILL_01, STILL_01_RAW, PROMPT_STILL_01)
        f2 = ex.submit(generate_and_master_still, "STILL_02", STILL_02, STILL_02_RAW, PROMPT_STILL_02)
        report["stills"]["V6_A13_STILL_01_Anamorphic16mm_LouverSunbeam_CreamWall_4K.jpg"] = f1.result()
        report["stills"]["V6_A13_STILL_02_Anamorphic16mm_GoldenDustMotes_4K.jpg"] = f2.result()

    # Use the ungraded STILL_02_RAW as start frame so we apply the 16mm 50D film master once cleanly to the video
    start_img = STILL_02_RAW if os.path.exists(STILL_02_RAW) else (STILL_01_RAW if os.path.exists(STILL_01_RAW) else ING_07)
    print(f"=== Starting VIDEO_01 conditioned on {os.path.basename(start_img)} ===", flush=True)
    ok_vid = opc.generate_omni_flash_4k60_video(
        prompt=PROMPT_VIDEO_01,
        start_image_path=start_img,
        out_mp4_4k60_path=VIDEO_01_PREGRADE,
        aspect_ratio="16:9",
        extra_ref_paths=REFS,
        max_retries=4,
    )
    print(f"=== VIDEO_01 pregrade finished: ok={ok_vid} ===", flush=True)

    if os.path.exists(VIDEO_01_PREGRADE):
        fm.apply_16mm_film_master_to_video(VIDEO_01_PREGRADE, VIDEO_01, preset="poetry_camera_16mm_50D")
        grid_final = VIDEO_01.replace(".mp4", "_audit_grid.jpg")
        subprocess.run(
            [opc.FFMPEG, "-y", "-i", VIDEO_01, "-vf", "select='eq(n,0)+eq(n,60)+eq(n,120)+eq(n,180)',scale=1280:-1,tile=2x2", "-frames:v", "1", grid_final],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        audit_vid = opc.self_audit_video_grid(grid_final) if os.path.exists(grid_final) else {"pass": False}
        report["videos"]["V6_A13_VIDEO_01_Anamorphic16mm_DustMotes_Cinemagraph_4K60.mp4"] = {
            "ok": ok_vid,
            "path": VIDEO_01,
            "pregrade_path": VIDEO_01_PREGRADE,
            "audit_grid": grid_final,
            "audit": audit_vid,
        }
        print(f"=== VIDEO_01 mastered & audited: {audit_vid} ===", flush=True)

    report_path = os.path.join(OUT_DIR, "v6_agent_13_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"=== ALL V6 AGENT 13 TASKS COMPLETE: {report_path} ===", flush=True)

if __name__ == "__main__":
    main()
