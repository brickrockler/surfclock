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

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_03"
os.makedirs(OUT_DIR, exist_ok=True)

ING_06 = os.path.join(GOLDEN_DIR, "INGREDIENT_06_WHITE_CYCLORAMA_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
UREF_03 = os.path.join(USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")
REFS = [ING_06, ING_01, UREF_03]

stills = [
    (
        "A03_STILL_01_PureWhite_Cyclorama_Braun_Hero_4K.jpg",
        "Iconic Dieter Rams / Braun Kronberg archive product photography — the deep matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm, proportions of a thick hardcover art monograph book) standing upright on a seamless pure chalk-white infinite studio cyclorama. Soft overhead scrim-diffused commercial lighting with subtle, natural contact shadow on the white studio floor. Shot on Hasselblad H6D-100c 80mm f/8, razor-sharp VDI-24 micro-bead matte slate-blue plastic texture, crisp raised white beach typography (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) with strictly 9 upper radial tick marks (8 to 4 o'clock) and 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, plus the lower WORTH IT? (NAH / YEAH) gauge and strictly 2 burnt-orange pointer hands total."
    ),
    (
        "A03_STILL_02_WhiteStudio_LongShadow_Architectural_4K.jpg",
        "High-key pure white architectural design studio floor with a crisp, sculptural long late-afternoon directional shadow cast to the right by the matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm). Eye-level architectural product photography on a Phase One IQ4 150MP 90mm lens, showcasing the stepped bezel, deeply recessed matte dial well, strictly 9 raised white radial tick marks along the upper horseshoe arc (8 to 4 o'clock), 100% blank smooth matte slate-blue plastic at the bottom of the upper dial (5, 6, and 7 o'clock), raised white lower WORTH IT? (NAH / YEAH) gauge, and 2 burnt-orange needles casting micro-shadows on the open matte dial face."
    ),
    (
        "A03_STILL_03_WhitePedestal_Gallery_ThreeQuarter_4K.jpg",
        "Museum-grade matte white gallery plinth in a bright minimalist industrial design studio, 3/4 perspective view showcasing the 52mm deep monolithic hardcover-book casing profile and stepped architectural bezel of the deep matte slate-blue Surf Forecast Instrument. Soft gallery skylight illumination, authentic VDI-24 matte molded plastic grain, open face with zero glass cover, strictly 9 white radial tick marks on the top arc of the upper dial (FRESHIE at 8 o'clock through LONG REEF at 12 o'clock to CURL CURL at 4 o'clock), 100% blank matte blue plastic at 5, 6, and 7 o'clock, and strictly 2 burnt-orange pointer hands total."
    ),
    (
        "A03_STILL_04_CoolGrey_Anodized_Studio_Table_4K.jpg",
        "Resting upright on a bead-blasted matte silver-grey anodized aluminum studio table against a crisp off-white architectural cyclorama backdrop — Teenage Engineering / Leica minimalist industrial film aesthetic. The deep matte slate-blue Surf Forecast Instrument (184 x 230 x 52 mm) exhibits tactile VDI-24 injection-molded surface grain, open matte dial with zero glass glare, strictly 9 upper white radial ticks (8 to 4 o'clock), completely blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock, crisp raised white labels, and strictly 1 burnt-orange hand on the upper beach dial and 1 short burnt-orange hand on the lower WORTH IT? gauge."
    ),
]

results = {"stills": {}, "videos": {}}

for fname, prompt in stills:
    out_path = os.path.join(OUT_DIR, fname)
    print(f"=== Generating {fname} ===")
    generate_4k_still(
        prompt=prompt,
        out_path=out_path,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=5,
        model_name="gemini-3-pro-image",
    )
    audit = self_audit_still(out_path)
    results["stills"][fname] = {"path": out_path, "audit": audit}

still_01_path = os.path.join(OUT_DIR, "A03_STILL_01_PureWhite_Cyclorama_Braun_Hero_4K.jpg")
still_03_path = os.path.join(OUT_DIR, "A03_STILL_03_WhitePedestal_Gallery_ThreeQuarter_4K.jpg")

videos = [
    (
        "A03_VIDEO_01_PureWhite_Cyclorama_Parallax_4K60.mp4",
        still_01_path,
        "Ultra-clean Dieter Rams / Braun industrial design film tracking shot: slow, fluid motorized motion-control camera parallax arc around the matte slate-blue Surf Forecast Instrument standing on a pure chalk-white infinite studio cyclorama, revealing the 52mm deep architectural casing, stepped bezel, VDI-24 matte plastic grain, strictly 9 upper white radial tick marks (with 5, 6, and 7 o'clock 100% blank smooth blue plastic), and 2 burnt-orange pointer needles under soft overhead studio scrim lighting."
    ),
    (
        "A03_VIDEO_02_WhitePedestal_Gallery_LightShift_4K60.mp4",
        still_03_path,
        "Slow, cinematic gallery plinth dolly move toward the matte slate-blue Surf Forecast Instrument resting on a museum-grade matte white pedestal as natural architectural skylight smoothly shifts across the 52mm deep matte blue housing, casting subtle moving shadows across the raised white beach typography, strictly 9 upper tick marks (blank at 5, 6, 7 o'clock), and 2 burnt-orange pointer hands."
    ),
]

for vname, start_img, vprompt in videos:
    out_vpath = os.path.join(OUT_DIR, vname)
    print(f"=== Generating {vname} ===")
    generate_omni_flash_4k60_video(
        prompt=vprompt,
        start_image_path=start_img,
        out_mp4_4k60_path=out_vpath,
        aspect_ratio="16:9",
        extra_ref_paths=REFS,
        max_retries=3,
    )
    grid_path = out_vpath.replace(".mp4", "_audit_grid.jpg")
    vaudit = self_audit_video_grid(grid_path) if os.path.exists(grid_path) else {"pass": False}
    results["videos"][vname] = {"path": out_vpath, "audit": vaudit}

report_path = os.path.join(OUT_DIR, "agent_03_audit_report.json")
with open(report_path, "w") as f:
    json.dump(results, f, indent=2)
print("=== ALL DONE ===")
print(json.dumps(results, indent=2))
