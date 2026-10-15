import os
import sys
import json

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    generate_omni_flash_4k60_video,
    self_audit_still,
    self_audit_video_grid,
    GOLDEN_DIR,
    USER_REF_DIR,
)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_06"
os.makedirs(OUT_DIR, exist_ok=True)

REF_ING_02 = os.path.join(GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
REF_ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
REF_USER_03 = os.path.join(USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")

REFS = [REF_ING_02, REF_ING_07, REF_USER_03]

STILLS = [
    {
        "filename": "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "prompt": (
            "16:9 4K industrial design studio tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The matte slate-blue Braun/Orchid Surf Forecast Instrument (184 x 230 x 52 mm, proportions of a thick hardcover art monograph book) "
            "rests directly on sun-warmed matte handmade terracotta quarry tiles in a daylight architectural studio. "
            "Visible organic mineral grain, subtle kiln-fired clay texture, and thin recessed mortar joints between the warm terracotta tiles. "
            "Warm directional natural morning window light casts a soft architectural shadow across the terracotta surface against a soft warm limewash studio background. "
            "Shot on Hasselblad H6D-100c with 80mm f/2.8 lens, shallow-to-medium depth of field keeping the entire 9-tick upper beach dial and lower WORTH IT? gauge razor-sharp."
        ),
    },
    {
        "filename": "A06_STILL_02_Unbleached_Canvas_Drape_StudioTable_4K.jpg",
        "prompt": (
            "16:9 4K tactile studio tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The matte slate-blue Braun/Orchid Surf Forecast Instrument (184 x 230 x 52 mm) stands directly on heavy unbleached raw Belgian linen and painter's canvas "
            "draped organically across a wide studio worktable. "
            "Soft raking side light highlights the tactile contrast between the coarse woven natural oatmeal linen fibers, soft organic fabric folds, "
            "and the precision VDI-24 micro-bead matte slate-blue injection-molded plastic housing. "
            "Quiet, editorial Cereal Magazine / Dieter Rams archive atmosphere, warm neutral studio backdrop, shot on medium format 85mm lens."
        ),
    },
    {
        "filename": "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "prompt": (
            "16:9 4K architectural studio interior tabletop photograph, ZERO plinth, ZERO pedestal. "
            "The matte slate-blue Braun/Orchid Surf Forecast Instrument (184 x 230 x 52 mm) stands directly on a flat matte oiled Australian Tasmanian oak tabletop / mid-century credenza "
            "against a warm textured limewash architectural wall. "
            "Clean, honest timber grain in warm honey-smoked oak, subtle warm daylight grazing across the wood surface and illuminating the deeply recessed matte slate-blue dial well. "
            "Minimalist architectural simplicity, razor-sharp typography on the 9-tick upper beach dial and lower WORTH IT? gauge."
        ),
    },
    {
        "filename": "A06_STILL_04_RawConcrete_StudioFloor_LowAngle_4K.jpg",
        "prompt": (
            "16:9 4K low-angle studio photograph, ZERO plinth, ZERO pedestal. "
            "The matte slate-blue Braun/Orchid Surf Forecast Instrument (184 x 230 x 52 mm) is placed directly on a power-troweled matte raw concrete studio floor "
            "inside a luminous pool of natural window light. "
            "Low tabletop-level camera angle looking slightly across the smooth, subtly mottled matte grey-warm concrete floor toward the monolithic slate-blue instrument. "
            "Crisp natural sunlight illuminates the stepped bezel, the 9-tick upper semicircular beach arc (with 100% blank bottom at 5, 6, 7 o'clock), "
            "the lower WORTH IT? gauge, and the two burnt-orange pointer needles."
        ),
    },
]

VIDEOS = [
    {
        "filename": "A06_VIDEO_01_Terracotta_Tabletop_Sunlight_Glide_4K60.mp4",
        "start_still": "A06_STILL_01_Terracotta_QuarryTiles_SunlitStudio_4K.jpg",
        "prompt": (
            "Low tabletop cinema camera glide on an Arri Alexa Mini LF with 50mm master prime lens, gliding smoothly across the sun-warmed matte handmade terracotta quarry tiles "
            "toward the matte slate-blue Surf Forecast Instrument resting directly on the tiled tabletop. "
            "Natural morning window sunlight subtly shifts across the tactile VDI-24 matte slate-blue bezel and recessed dial well. "
            "Keep the 9-tick upper beach dial (blank bottom at 5, 6, 7 o'clock) and lower WORTH IT? gauge with their 2 burnt-orange pointer hands rock-solid and razor-sharp."
        ),
    },
    {
        "filename": "A06_VIDEO_02_TasmanianOak_Tabletop_Track_4K60.mp4",
        "start_still": "A06_STILL_03_SmokedOak_MidCentury_Credenza_4K.jpg",
        "prompt": (
            "Smooth lateral-to-forward tabletop tracking shot across the flat matte oiled Australian Tasmanian oak tabletop against a warm limewash wall, "
            "with a gentle cinematic focus pull from the warm timber grain onto the matte slate-blue Surf Forecast Instrument's 9-tick upper beach dial and lower WORTH IT? gauge. "
            "Warm architectural daylight, zero glass glare, rock-solid geometry with 9 upper ticks, blank bottom space at 5, 6, 7 o'clock, and 2 burnt-orange hands."
        ),
    },
]

def main():
    report = {"stills": {}, "videos": {}}

    for item in STILLS:
        out_path = os.path.join(OUT_DIR, item["filename"])
        print(f"\n=== Generating Still: {item['filename']} ===", flush=True)
        ok = generate_4k_still(
            prompt=item["prompt"],
            out_path=out_path,
            ref_image_paths=REFS,
            aspect_ratio="16:9",
            max_retries=5,
        )
        audit = self_audit_still(out_path) if os.path.exists(out_path) else {"pass": False, "score": 0.0}
        report["stills"][item["filename"]] = {
            "path": out_path,
            "exists": os.path.exists(out_path),
            "ok": ok,
            "audit": audit,
        }
        print(f"Result for {item['filename']}: {report['stills'][item['filename']]}", flush=True)

    for vitem in VIDEOS:
        out_mp4 = os.path.join(OUT_DIR, vitem["filename"])
        start_path = os.path.join(OUT_DIR, vitem["start_still"])
        print(f"\n=== Generating Video: {vitem['filename']} ===", flush=True)
        ok = generate_omni_flash_4k60_video(
            prompt=vitem["prompt"],
            start_image_path=start_path,
            out_mp4_4k60_path=out_mp4,
            aspect_ratio="16:9",
            extra_ref_paths=REFS,
            max_retries=3,
        )
        grid_jpg = out_mp4.replace(".mp4", "_audit_grid.jpg")
        audit = self_audit_video_grid(grid_jpg) if os.path.exists(grid_jpg) else {"pass": False, "score": 0.0}
        report["videos"][vitem["filename"]] = {
            "path": out_mp4,
            "exists": os.path.exists(out_mp4),
            "ok": ok,
            "audit": audit,
        }
        print(f"Result for {vitem['filename']}: {report['videos'][vitem['filename']]}", flush=True)

    report_path = os.path.join(OUT_DIR, "agent_06_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nSaved full audit report to {report_path}", flush=True)

if __name__ == "__main__":
    main()
