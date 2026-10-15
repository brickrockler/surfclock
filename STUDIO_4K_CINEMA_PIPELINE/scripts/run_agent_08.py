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
os.makedirs(OUT_DIR, exist_ok=True)

REFS = [
    os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg"),
    os.path.join(GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg"),
    os.path.join(USER_REF_DIR, "USER_REF_04_Filmic_Dappled_Light_Composition.png"),
]

STILLS = [
    (
        "A08_STILL_01_BillyButtons_Craspedia_Sandstone_16mm_4K.jpg",
        "Authentic Australian botanical cinema still — reproduce the exact matte slate-blue Braun/Orchid Surf Forecast Instrument from the reference images with 100% geometric and typographic fidelity, resting upright on a warm weathered Hawkesbury sandstone ledge framed by golden spherical Australian Billy Buttons (Craspedia globosa) and wispy native Kangaroo Grass (Themeda triandra) trembling in warm golden afternoon light. Shot on Arriflex 16SR3 16mm Kodak Vision3 250D film with Zeiss Super Speed 50mm T1.3 lens, organic warm highlight halation, and fine photochemical film grain. CRITICAL DIAL GEOMETRY: The upper beach dial has STRICTLY 9 white radial tick marks arranged in an upper horseshoe arc from 8 o'clock (FRESHIE) through 12 o'clock (LONG REEF) to 4 o'clock (CURL CURL). The bottom section of the upper circle between FRESHIE (8 o'clock) and CURL CURL (4 o'clock) — i.e., the 5, 6, and 7 o'clock positions — is 100% BLANK matte slate-blue plastic with ZERO tick marks. CRITICAL HANDS: Strictly 2 burnt-orange pointer hands total on the entire clock (1 long burnt-orange hand on the upper beach dial pointing near LONG REEF, 1 short burnt-orange hand on the lower WORTH IT? semicircular gauge pointing near YEAH). CRITICAL TEXTURE & SCALE: Authentic VDI-24 micro-bead injection-molded matte slate-blue plastic surface texture, open matte dial face with ZERO glass cover and ZERO blue LED glow, physical dimensions 184mm wide x 230mm tall x 52mm deep (the exact size of a large hardcover art monograph book)."
    ),
    (
        "A08_STILL_02_SilverDollar_Eucalyptus_ClayStudio_16mm_4K.jpg",
        "Art-directed Australian botanical studio still life — reproduce the exact matte slate-blue Braun/Orchid Surf Forecast Instrument from the reference images with 100% geometric and typographic fidelity, standing on a raw warm ochre-clay plinth beside a single sculptural stem of dusty sage-green Silver Dollar Eucalyptus (Eucalyptus cinerea) and an organic dried Banksia cone, bathed in dappled late-afternoon directional window sunlight with soft organic leaf shadows across warm textured plaster. Shot on Arriflex 16SR3 16mm Kodak Vision3 250D film with subtle warm halation and authentic photochemical grain. CRITICAL DIAL GEOMETRY: The upper beach dial has STRICTLY 9 white radial tick marks arranged in an upper horseshoe arc from 8 o'clock (FRESHIE) through 12 o'clock (LONG REEF) to 4 o'clock (CURL CURL). The bottom section of the upper circle between FRESHIE (8 o'clock) and CURL CURL (4 o'clock) — i.e., the 5, 6, and 7 o'clock positions — is 100% BLANK matte slate-blue plastic with ZERO tick marks. CRITICAL HANDS: Strictly 2 burnt-orange pointer hands total on the entire clock (1 long burnt-orange hand on the upper beach dial, 1 short burnt-orange hand on the lower WORTH IT? semicircular gauge). CRITICAL TEXTURE & SCALE: Authentic VDI-24 micro-bead injection-molded matte slate-blue plastic surface texture, open matte dial face with ZERO glass cover and ZERO blue LED glow, physical dimensions 184mm wide x 230mm tall x 52mm deep (the exact size of a large hardcover art monograph book)."
    ),
    (
        "A08_STILL_03_NativeKangarooGrass_CoastalHeadland_16mm_4K.jpg",
        "Authentic Australian coastal headland 16mm film photograph — reproduce the exact matte slate-blue Braun/Orchid Surf Forecast Instrument from the reference images with 100% geometric and typographic fidelity, resting solidly on a sun-bleached weathered coastal hardwood timber post surrounded by feathery copper-gold Australian Kangaroo Grass (Themeda triandra) and silvery coastal Spinifex, with a soft out-of-focus deep cobalt-blue Pacific Ocean horizon bokeh shimmering in the background. Shot on Arriflex 16SR3 16mm Kodak Vision3 50D daylight film with natural sunlit contrast, subtle halation, and fine organic grain. CRITICAL DIAL GEOMETRY: The upper beach dial has STRICTLY 9 white radial tick marks arranged in an upper horseshoe arc from 8 o'clock (FRESHIE) through 12 o'clock (LONG REEF) to 4 o'clock (CURL CURL). The bottom section of the upper circle between FRESHIE (8 o'clock) and CURL CURL (4 o'clock) — i.e., the 5, 6, and 7 o'clock positions — is 100% BLANK matte slate-blue plastic with ZERO tick marks. CRITICAL HANDS: Strictly 2 burnt-orange pointer hands total on the entire clock (1 long burnt-orange hand on the upper beach dial, 1 short burnt-orange hand on the lower WORTH IT? semicircular gauge). CRITICAL TEXTURE & SCALE: Authentic VDI-24 micro-bead injection-molded matte slate-blue plastic surface texture, open matte dial face with ZERO glass cover and ZERO blue LED glow, physical dimensions 184mm wide x 230mm tall x 52mm deep (the exact size of a large hardcover art monograph book)."
    ),
    (
        "A08_STILL_04_FlannelFlowers_And_BillyButtons_Tabletop_4K.jpg",
        "Warm sunlit Australian morning architectural tabletop photograph — reproduce the exact matte slate-blue Braun/Orchid Surf Forecast Instrument from the reference images with 100% geometric and typographic fidelity, standing on a honed travertine and warm timber morning table beside a handmade matte stoneware vessel holding native velvety white Australian Flannel Flowers (Actinotus helianthi) with soft grey-green tips and golden yellow Billy Buttons (Craspedia globosa). Soft morning light streams through sheer linen curtains, casting gentle botanical shadows. Shot on 16mm Kodak Vision3 250D film with rich tonal latitude and fine organic film texture. CRITICAL DIAL GEOMETRY: The upper beach dial has STRICTLY 9 white radial tick marks arranged in an upper horseshoe arc from 8 o'clock (FRESHIE) through 12 o'clock (LONG REEF) to 4 o'clock (CURL CURL). The bottom section of the upper circle between FRESHIE (8 o'clock) and CURL CURL (4 o'clock) — i.e., the 5, 6, and 7 o'clock positions — is 100% BLANK matte slate-blue plastic with ZERO tick marks. CRITICAL HANDS: Strictly 2 burnt-orange pointer hands total on the entire clock (1 long burnt-orange hand on the upper beach dial, 1 short burnt-orange hand on the lower WORTH IT? semicircular gauge). CRITICAL TEXTURE & SCALE: Authentic VDI-24 micro-bead injection-molded matte slate-blue plastic surface texture, open matte dial face with ZERO glass cover and ZERO blue LED glow, physical dimensions 184mm wide x 230mm tall x 52mm deep (the exact size of a large hardcover art monograph book)."
    ),
]

def main():
    report = {"stills": {}, "videos": {}}

    for fname, prompt in STILLS:
        out_path = os.path.join(OUT_DIR, fname)
        print(f"\n=== Generating Still: {fname} ===")
        ok = generate_4k_still(
            prompt=prompt,
            out_path=out_path,
            ref_image_paths=REFS,
            aspect_ratio="16:9",
            max_retries=6,
            model_name="gemini-3-pro-image-preview",
        )
        audit = self_audit_still(out_path) if os.path.exists(out_path) else {"pass": False, "score": 0.0}
        report["stills"][fname] = {
            "path": out_path,
            "exists": os.path.exists(out_path),
            "passed_on_gen": ok,
            "audit": audit,
        }

    still_01_path = os.path.join(OUT_DIR, "A08_STILL_01_BillyButtons_Craspedia_Sandstone_16mm_4K.jpg")
    still_03_path = os.path.join(OUT_DIR, "A08_STILL_03_NativeKangarooGrass_CoastalHeadland_16mm_4K.jpg")

    VIDEOS = [
        (
            "A08_VIDEO_01_BillyButtons_And_NativeGrasses_16mm_Film_4K60.mp4",
            still_01_path,
            "Poetic Arriflex 16mm Kodak Vision3 250D film cinematography: golden spherical Australian Billy Buttons (Craspedia globosa) and wispy native Kangaroo Grass sway gently in the warm afternoon coastal breeze beside the stationary matte slate-blue 9-tick Surf Forecast Instrument resting on weathered Hawkesbury sandstone. Subtle camera dolly push-in with warm dappled sunlight shifting softly across the sandstone and VDI-24 matte slate-blue housing. Keep the instrument rock-solid with strictly 9 upper white ticks (zero ticks at 5, 6, 7 o'clock) and strictly 2 burnt-orange pointer needles."
        ),
        (
            "A08_VIDEO_02_CoastalHeadland_NativeGrass_Bokeh_4K60.mp4",
            still_03_path,
            "Sunlit Arriflex 16mm Kodak Vision3 50D coastal headland film shot: feathery Australian Kangaroo Grass and coastal Spinifex move gently in the foreground breeze while out-of-focus deep blue Pacific Ocean bokeh shimmers softly in the background behind the stationary matte slate-blue 9-tick Surf Forecast Instrument resting on a sun-bleached coastal timber post. Gentle breathing prime lens focus and natural golden sunlight. Keep the instrument rock-solid with strictly 9 upper white ticks (zero ticks at 5, 6, 7 o'clock) and strictly 2 burnt-orange pointer needles."
        ),
    ]

    for vname, start_img, vprompt in VIDEOS:
        out_vpath = os.path.join(OUT_DIR, vname)
        print(f"\n=== Generating Video: {vname} ===")
        ok = generate_omni_flash_4k60_video(
            prompt=vprompt,
            start_image_path=start_img,
            out_mp4_4k60_path=out_vpath,
            aspect_ratio="16:9",
            extra_ref_paths=REFS,
            max_retries=4,
        )
        grid_jpg = out_vpath.replace(".mp4", "_audit_grid.jpg")
        audit = self_audit_video_grid(grid_jpg) if os.path.exists(grid_jpg) else {"pass": False, "score": 0.0}
        report["videos"][vname] = {
            "path": out_vpath,
            "exists": os.path.exists(out_vpath),
            "passed_on_gen": ok,
            "audit": audit,
        }

    report_path = os.path.join(OUT_DIR, "agent_08_audit_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print("\n=== FINAL AGENT 08 REPORT ===")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
