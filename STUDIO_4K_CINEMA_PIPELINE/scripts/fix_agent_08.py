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

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v5_tournament/agent_08"
REFS = [
    os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg"),
    os.path.join(GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg"),
    os.path.join(USER_REF_DIR, "USER_REF_04_Filmic_Dappled_Light_Composition.png"),
]

still_04_path = os.path.join(OUT_DIR, "A08_STILL_04_FlannelFlowers_And_BillyButtons_Tabletop_4K.jpg")
still_04_prompt = (
    "Warm sunlit Australian morning architectural tabletop photograph — reproduce the exact matte slate-blue Braun/Orchid Surf Forecast Instrument from the reference images with 100% geometric and typographic fidelity, standing on a honed travertine and warm timber morning table beside a handmade matte stoneware vessel holding native velvety white Australian Flannel Flowers (Actinotus helianthi) and golden yellow Billy Buttons (Craspedia globosa). Soft morning light streams through sheer linen curtains, casting gentle botanical shadows. Shot on 16mm Kodak Vision3 250D film with rich tonal latitude and fine organic film texture. "
    "CRITICAL DIAL GEOMETRY: Match the reference bezel and dial 1:1 — single slim outer bezel, strictly 9 thin white radial tick marks at 8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock, and 5 HORIZONTAL white labels ('FRESHIE' at 8 o'clock, 'QUEENSIE' at 10 o'clock, 'LONG REEF' at 12 o'clock, 'DEE WHY' at 2 o'clock, 'CURL CURL' at 4 o'clock — NEVER curve the text). The bottom section between FRESHIE and CURL CURL (5, 6, 7 o'clock) is 100% BLANK matte slate-blue plastic with ZERO tick marks. Strictly 1 long burnt-orange hand on the upper dial and 1 short burnt-orange hand on the lower thin white WORTH IT? (NAH / YEAH) semicircular arc."
)

print("=== Regenerating A08_STILL_04 with gemini-nano-banana-2.1 ===")
generate_4k_still(
    prompt=still_04_prompt,
    out_path=still_04_path,
    ref_image_paths=REFS,
    aspect_ratio="16:9",
    max_retries=4,
    model_name="gemini-nano-banana-2.1",
)

still_01_path = os.path.join(OUT_DIR, "A08_STILL_01_BillyButtons_Craspedia_Sandstone_16mm_4K.jpg")
video_01_path = os.path.join(OUT_DIR, "A08_VIDEO_01_BillyButtons_And_NativeGrasses_16mm_Film_4K60.mp4")
video_01_prompt = (
    "Full-bleed 16:9 widescreen cinema shot (ZERO film frame borders, ZERO sprocket overlays, ZERO text overlays): golden spherical Australian Billy Buttons (Craspedia globosa) and wispy native Kangaroo Grass sway gently in the warm afternoon coastal breeze beside the stationary matte slate-blue 9-tick Surf Forecast Instrument resting on weathered Hawkesbury sandstone. Gentle locked-off or subtle slow push-in camera movement with warm golden afternoon sunlight. Preserve the exact dial face from the starting image with ONLY the 5 horizontal beach labels (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL — zero extra text between labels), strictly 9 upper white ticks (5, 6, 7 o'clock blank), and strictly 2 burnt-orange pointer needles."
)

print("=== Regenerating A08_VIDEO_01 ===")
generate_omni_flash_4k60_video(
    prompt=video_01_prompt,
    start_image_path=still_01_path,
    out_mp4_4k60_path=video_01_path,
    aspect_ratio="16:9",
    extra_ref_paths=REFS,
    max_retries=3,
)

# Refresh full report
stills_list = [
    "A08_STILL_01_BillyButtons_Craspedia_Sandstone_16mm_4K.jpg",
    "A08_STILL_02_SilverDollar_Eucalyptus_ClayStudio_16mm_4K.jpg",
    "A08_STILL_03_NativeKangarooGrass_CoastalHeadland_16mm_4K.jpg",
    "A08_STILL_04_FlannelFlowers_And_BillyButtons_Tabletop_4K.jpg",
]
videos_list = [
    "A08_VIDEO_01_BillyButtons_And_NativeGrasses_16mm_Film_4K60.mp4",
    "A08_VIDEO_02_CoastalHeadland_NativeGrass_Bokeh_4K60.mp4",
]

report = {"stills": {}, "videos": {}}
for s in stills_list:
    p = os.path.join(OUT_DIR, s)
    report["stills"][s] = {
        "path": p,
        "exists": os.path.exists(p),
        "audit": self_audit_still(p),
    }
for v in videos_list:
    p = os.path.join(OUT_DIR, v)
    g = p.replace(".mp4", "_audit_grid.jpg")
    report["videos"][v] = {
        "path": p,
        "exists": os.path.exists(p),
        "audit": self_audit_video_grid(g),
    }

report_path = os.path.join(OUT_DIR, "agent_08_audit_report.json")
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)
print("=== UPDATED REPORT ===")
print(json.dumps(report, indent=2))
