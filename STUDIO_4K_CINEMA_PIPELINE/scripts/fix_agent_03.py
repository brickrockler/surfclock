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
ING_06 = os.path.join(GOLDEN_DIR, "INGREDIENT_06_WHITE_CYCLORAMA_9TICK_4K.jpg")
ING_01 = os.path.join(GOLDEN_DIR, "INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg")
UREF_03 = os.path.join(USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")
STILL_03 = os.path.join(OUT_DIR, "A03_STILL_03_WhitePedestal_Gallery_ThreeQuarter_4K.jpg")
STILL_04 = os.path.join(OUT_DIR, "A03_STILL_04_CoolGrey_Anodized_Studio_Table_4K.jpg")

# Use INGREDIENT_06, INGREDIENT_01, USER_REF_03, and STILL_03 so the rectangular 9-tick geometry is 100% locked
REFS = [ING_06, ING_01, UREF_03, STILL_03]

stills_to_fix = [
    (
        "A03_STILL_01_PureWhite_Cyclorama_Braun_Hero_4K.jpg",
        "Iconic Dieter Rams / Braun Kronberg archive product photography — reproduce the EXACT VERTICAL RECTANGULAR MONOLITHIC BOX HOUSING (184 mm wide x 230 mm tall x 52 mm deep, sharp rectangular outer frame with recessed flat rectangular dial face, NEVER a circular housing) of the deep matte slate-blue Surf Forecast Instrument from the reference images, standing upright on a seamless pure chalk-white infinite studio cyclorama. Soft overhead scrim-diffused lighting with subtle contact shadow on the white floor. Flat unbroken matte slate-blue dial surface with strictly 9 raised white radial tick marks along the upper semicircle (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock, labeled FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte blue plastic at 5, 6, and 7 o'clock, raised white lower WORTH IT? (NAH / YEAH) semicircular gauge, and strictly 2 burnt-orange pointer needles."
    ),
    (
        "A03_STILL_02_WhiteStudio_LongShadow_Architectural_4K.jpg",
        "High-key pure white architectural design studio floor with a crisp, long late-afternoon directional shadow cast to the right by the VERTICAL RECTANGULAR MONOLITHIC BOX HOUSING (184 x 230 x 52 mm, rectangular outer bezel framing a SINGLE FLAT UNBROKEN rectangular matte slate-blue dial face — NEVER recessed semicircular sub-wells) of the Surf Forecast Instrument from the reference images. Strictly 9 raised white radial tick marks along the upper arc (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock, labeled FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), 100% blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock, raised white lower WORTH IT? (NAH / YEAH) arc gauge below, and strictly 2 burnt-orange pointer hands casting crisp micro-shadows."
    ),
]

for fname, prompt in stills_to_fix:
    out_path = os.path.join(OUT_DIR, fname)
    print(f"=== Regenerating rectangular 9-tick {fname} ===")
    generate_4k_still(
        prompt=prompt,
        out_path=out_path,
        ref_image_paths=REFS,
        aspect_ratio="16:9",
        max_retries=4,
        model_name="gemini-nano-banana-2.1",
    )

still_01_path = os.path.join(OUT_DIR, "A03_STILL_01_PureWhite_Cyclorama_Braun_Hero_4K.jpg")

videos_to_fix = [
    (
        "A03_VIDEO_01_PureWhite_Cyclorama_Parallax_4K60.mp4",
        still_01_path,
        "Ultra-clean Dieter Rams / Braun industrial design film tracking shot: slow, subtle motorized camera parallax arc around the rectangular matte slate-blue Surf Forecast Instrument standing on a pure chalk-white infinite studio cyclorama. Keep the full rectangular instrument in a medium studio hero framing throughout (do not extreme-zoom), preserving the exact 5 labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) and 3 lower labels (NAH, YEAH, WORTH IT?) with zero extra words on the dial face."
    ),
    (
        "A03_VIDEO_02_WhitePedestal_Gallery_LightShift_4K60.mp4",
        STILL_03,
        "Slow, subtle gallery plinth dolly move around the rectangular matte slate-blue Surf Forecast Instrument resting on a museum-grade matte white pedestal in a minimalist studio as natural architectural skylight shifts across the matte blue housing. Keep the full rectangular instrument in medium gallery framing throughout (do not extreme-zoom), preserving the exact 5 upper beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL) and 3 lower labels (NAH, YEAH, WORTH IT?) with zero extra words on the dial face."
    ),
]

for vname, start_img, vprompt in videos_to_fix:
    out_vpath = os.path.join(OUT_DIR, vname)
    print(f"=== Regenerating {vname} ===")
    generate_omni_flash_4k60_video(
        prompt=vprompt,
        start_image_path=start_img,
        out_mp4_4k60_path=out_vpath,
        aspect_ratio="16:9",
        extra_ref_paths=[ING_06, ING_01, UREF_03],
        max_retries=2,
    )

# Compile full audit report
report = {"stills": {}, "videos": {}}
for sname in [
    "A03_STILL_01_PureWhite_Cyclorama_Braun_Hero_4K.jpg",
    "A03_STILL_02_WhiteStudio_LongShadow_Architectural_4K.jpg",
    "A03_STILL_03_WhitePedestal_Gallery_ThreeQuarter_4K.jpg",
    "A03_STILL_04_CoolGrey_Anodized_Studio_Table_4K.jpg",
]:
    p = os.path.join(OUT_DIR, sname)
    report["stills"][sname] = {"path": p, "audit": self_audit_still(p)}

for vname in [
    "A03_VIDEO_01_PureWhite_Cyclorama_Parallax_4K60.mp4",
    "A03_VIDEO_02_WhitePedestal_Gallery_LightShift_4K60.mp4",
]:
    p = os.path.join(OUT_DIR, vname)
    gp = p.replace(".mp4", "_audit_grid.jpg")
    report["videos"][vname] = {"path": p, "audit": self_audit_video_grid(gp)}

with open(os.path.join(OUT_DIR, "agent_03_audit_report.json"), "w") as f:
    json.dump(report, f, indent=2)
print("=== FINAL REPORT ===")
print(json.dumps(report, indent=2))
