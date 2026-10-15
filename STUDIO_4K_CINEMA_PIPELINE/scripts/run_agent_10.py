import os
import sys
import json
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
    FFPROBE,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_10"
os.makedirs(OUT_DIR, exist_ok=True)

ING_08 = os.path.join(GOLDEN_DIR, "INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
ING_06 = os.path.join(GOLDEN_DIR, "INGREDIENT_06_WHITE_CYCLORAMA_9TICK_4K.jpg")
ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
USER_REF_01 = os.path.join(USER_REF_DIR, "USER_REF_01_SlateBlue_Cyclorama_Caustic_Hero.jpg")
USER_REF_02 = os.path.join(USER_REF_DIR, "USER_REF_02_WarmCream_Sunlit_Plaster_Dappled.png")

STILL_SPECS = [
    {
        "filename": "A10_STILL_01_Vert9x16_SlateBlue_Cyclorama_Hero_4K.jpg",
        "refs": [ING_08, ING_01, USER_REF_01],
        "prompt": (
            "Vertical 9:16 4K studio hero photograph of the matte slate-blue Braun/Dieter Rams Surf Forecast Instrument "
            "(184 x 230 x 52 mm, proportions of a hardcover art monograph) standing upright on a seamless deep slate-blue architectural cyclorama. "
            "A warm golden-amber radial caustic light pool illuminates the cyclorama behind and beneath the clock, casting a crisp architectural shadow to the right. "
            "Shot on Hasselblad H6D-100c with 80mm f/2.8 lens at f/8, generous vertical headroom and pedestal breathing room for 9:16 luxury social cinema. "
            "Strictly 9 raised white tick marks along the top semicircular arc ONLY (8 to 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
            "100% blank smooth matte slate-blue plastic at the bottom of the upper circle (5, 6, and 7 o'clock), and 2 burnt-orange pointer needles total."
        ),
    },
    {
        "filename": "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg",
        "refs": [ING_08, ING_01, USER_REF_02],
        "prompt": (
            "Vertical 9:16 4K architectural portrait of the matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm) "
            "standing on a warm travertine-cream lime-plaster shelf against a sunlit warm cream plaster wall in a Sydney Northern Beaches architectural home. "
            "Golden afternoon sunlight filters through Australian eucalyptus leaves, casting organic dappled botanical shadows across the warm cream plaster wall and the stepped matte slate-blue housing. "
            "Shot on Hasselblad H6D-100c 90mm lens, f/5.6, authentic VDI-24 micro-bead matte plastic texture, open matte dial face with zero glass cover. "
            "Strictly 9 white radial tick marks on the upper top arc (8 to 4 o'clock), 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, and 2 burnt-orange needles total."
        ),
    },
    {
        "filename": "A10_STILL_03_Vert9x16_PureWhite_Studio_Plinth_4K.jpg",
        "refs": [ING_08, ING_01, ING_06],
        "prompt": (
            "Vertical 9:16 4K minimalist Dieter Rams / Braun / Leica industrial design gallery portrait of the matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm) "
            "standing atop a pure matte museum-white monolithic architectural plinth against a seamless pure white infinity cyclorama. "
            "Crisp directional key light from the upper left casts a long, graphic diagonal shadow across the white plinth surface. "
            "Ultra-clean high-key studio lighting highlights the stepped slate-blue bezel, deeply recessed dial well, raised white typography (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, WORTH IT?, NAH, YEAH), "
            "strictly 9 white tick marks on the upper semicircle (zero ticks at 5, 6, 7 o'clock), and 2 vibrant burnt-orange hands."
        ),
    },
    {
        "filename": "A10_STILL_04_Vert9x16_BillyButtons_AussieSandstone_16mm_4K.jpg",
        "refs": [ING_08, ING_01, USER_REF_02],
        "prompt": (
            "Vertical 9:16 4K Kodak Vision3 250D 16mm film portrait of the matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm) "
            "resting on a sun-warmed Australian coastal Hawkesbury sandstone ledge overlooking a soft-focus golden sunlit backdrop. "
            "Framed organically in the foreground/side by golden spherical Australian Billy Buttons (Craspedia globosa) and delicate native Kangaroo Grass (Themeda triandra) swaying in the coastal breeze. "
            "Authentic photochemical halation, fine organic film grain, tactile VDI-24 matte slate-blue molded plastic housing, "
            "strictly 9 white radial tick marks on the top arc only (8 to 4 o'clock), 100% blank smooth matte blue bottom arc at 5, 6, and 7 o'clock, and strictly 2 burnt-orange pointer needles."
        ),
    },
]

def run_still(spec):
    out_path = os.path.join(OUT_DIR, spec["filename"])
    print(f"=== Starting Still: {spec['filename']} ===", flush=True)
    ok = generate_4k_still(
        prompt=spec["prompt"],
        out_path=out_path,
        ref_image_paths=spec["refs"],
        aspect_ratio="9:16",
        max_retries=5,
        model_name="gemini-3-pro-image-preview",
    )
    audit = self_audit_still(out_path) if os.path.exists(out_path) else {"pass": False, "score": 0.0}
    print(f"=== Finished Still: {spec['filename']} (ok={ok}, score={audit.get('score')}) ===", flush=True)
    return spec["filename"], out_path, audit

def main():
    report = {"stills": {}, "videos": {}}

    # 1. Generate all 4 vertical 9:16 4K stills in parallel (2 workers to avoid rate limits)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(run_still, s) for s in STILL_SPECS]
        for f in futures:
            fname, path, audit = f.result()
            report["stills"][fname] = {"path": path, "audit": audit}

    still_01_path = os.path.join(OUT_DIR, "A10_STILL_01_Vert9x16_SlateBlue_Cyclorama_Hero_4K.jpg")
    still_02_path = os.path.join(OUT_DIR, "A10_STILL_02_Vert9x16_WarmCream_Dappled_Eucalyptus_4K.jpg")

    VIDEO_SPECS = [
        {
            "filename": "A10_VIDEO_01_Vert9x16_SlateBlue_Studio_Orbit_4K60.mp4",
            "start_image": still_01_path,
            "extra_refs": [ING_08, ING_01, USER_REF_01],
            "prompt": (
                "Vertical 9:16 studio cinema slow orbital dolly and subtle macro push-in on the matte slate-blue Surf Forecast Instrument "
                "standing on a deep slate-blue cyclorama in a warm golden radial caustic light pool. "
                "As the camera glides smoothly in a 15-degree arc and pushes in toward the recessed dial face, the warm key light grazes the VDI-24 micro-bead matte plastic texture, "
                "the stepped architectural bezel, the 9 raised white tick marks along the upper semicircle (with 5, 6, and 7 o'clock completely blank matte blue plastic), "
                "and the 2 burnt-orange pointer needles."
            ),
        },
        {
            "filename": "A10_VIDEO_02_Vert9x16_WarmCream_Eucalyptus_Light_4K60.mp4",
            "start_image": still_02_path,
            "extra_refs": [ING_08, ING_01, USER_REF_02],
            "prompt": (
                "Vertical 9:16 sunlit architectural cinema film of the matte slate-blue Surf Forecast Instrument on a warm cream plaster shelf. "
                "Soft golden afternoon sunlight filters through Australian eucalyptus leaves, creating gently swaying dappled botanical shadows across the warm cream plaster wall and the matte slate-blue clock bezel. "
                "The camera executes a slow, intimate vertical pedestal and push-in reveal of the open matte dial face, showcasing the 9 raised white tick marks on the top arc, "
                "the 100% blank smooth matte blue space at 5, 6, and 7 o'clock, and the 2 burnt-orange needles."
            ),
        },
    ]

    def run_video(vspec):
        out_mp4 = os.path.join(OUT_DIR, vspec["filename"])
        print(f"=== Starting Video: {vspec['filename']} ===", flush=True)
        ok = generate_omni_flash_4k60_video(
            prompt=vspec["prompt"],
            start_image_path=vspec["start_image"],
            out_mp4_4k60_path=out_mp4,
            aspect_ratio="9:16",
            extra_ref_paths=vspec["extra_refs"],
            max_retries=3,
        )
        grid_jpg = out_mp4.replace(".mp4", "_audit_grid.jpg")
        audit = self_audit_video_grid(grid_jpg) if os.path.exists(grid_jpg) else {"pass": False, "score": 0.0}
        print(f"=== Finished Video: {vspec['filename']} (ok={ok}, score={audit.get('score')}) ===", flush=True)
        return vspec["filename"], out_mp4, audit

    with ThreadPoolExecutor(max_workers=2) as ex:
        vfutures = [ex.submit(run_video, v) for v in VIDEO_SPECS]
        for vf in vfutures:
            vname, vpath, vaudit = vf.result()
            report["videos"][vname] = {"path": vpath, "audit": vaudit}

    report_path = os.path.join(OUT_DIR, "agent_10_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"=== ALL AGENT 10 OUTPUTS COMPLETED -> {report_path} ===", flush=True)

if __name__ == "__main__":
    main()
