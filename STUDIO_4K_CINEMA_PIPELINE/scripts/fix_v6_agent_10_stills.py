#!/usr/bin/env python3
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor

sys.path.append('/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts')
from omni_pro_client import (
    generate_4k_still,
    self_audit_still,
    GOLDEN_DIR,
    USER_REF_DIR,
)
import importlib.util
spec_m = importlib.util.spec_from_file_location(
    "film_mastering",
    "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/49_world_class_film_mastering.py"
)
film_mastering = importlib.util.module_from_spec(spec_m)
spec_m.loader.exec_module(film_mastering)

OUT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/raw_renders/v6_film_explorations/v6_agent_10"
ING_07 = os.path.join(GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_05_UPPER = os.path.join(GOLDEN_DIR, "INGREDIENT_05_MACRO_UPPER_DIAL_9TICK_4K.jpg")
USER_REF_05 = os.path.join(USER_REF_DIR, "USER_REF_05_Tactile_VDI24_Molded_Plastic_Macro_LowerWorthIt_4K.jpg")

STILL_SPECS = [
    {
        "filename": "V6_A10_STILL_01_Bolex16mm_Macro_SunlitCream_Bezel_4K.jpg",
        "refs": [ING_07, ING_05_UPPER, USER_REF_05],
        "prompt": (
            "16:9 widescreen 4K photochemical 16mm close-up product photograph of the exact deep matte slate-blue (#2D3E5E) Braun / Dieter Rams rectangular Surf Forecast Instrument "
            "from Reference Image 1 (INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg). "
            "CRITICAL GEOMETRY (MATCH REFERENCE IMAGE 1 EXACTLY): Sharp 90-degree rectangular outer stepped bezel (184 x 230 x 52 mm vertical book-sized monolith) enclosing ONE SINGLE FLAT CONTINUOUS RECESSED RECTANGULAR DIAL FACE from top to bottom. "
            "NEVER add any semicircular or arched cutout/recess around the upper dial — the 9 upper white radial ticks and 5 beach labels sit directly on the flat continuous matte slate-blue rectangular dial plane! "
            "Shot on a spring-wound Bolex H16 16mm camera with a Kern Macro-Switar 75mm f/1.9 lens on Kodak Vision3 50D (7203): "
            "the rectangular Surf Clock rests cleanly against a bright, airy, sun-drenched warm cream / chalk-ivory plaster wall with soft out-of-focus dappled eucalyptus leaf shadows and a softly blurred golden sunlit eucalyptus leaf tip in the foreground edge. "
            "Extreme shallow depth of field across the sharp rectangular stepped bezel, with razor-sharp focus on the tactile VDI-24 micro-bead matte slate-blue plastic grain, "
            "strictly 9 raised white radial tick marks along the top arc ONLY (8, 9, 10, 11, 12, 1, 2, 3, and 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
            "100% BLANK smooth flat matte slate-blue plastic at the bottom of the upper circle (5, 6, and 7 o'clock), the lower WORTH IT? (NAH / YEAH) semicircular arc gauge with 3 ticks, "
            "and strictly 2 skinny burnt-orange pointer needles glowing with warm +1.3 EV 16mm halation."
        ),
    },
    {
        "filename": "V6_A10_STILL_02_SplitDiopter_16mm_ForegroundShell_4K.jpg",
        "refs": [ING_07, ING_05_UPPER, USER_REF_05],
        "prompt": (
            "16:9 widescreen 4K art-house split-diopter 16mm cinema photograph shot on Bolex H16 with a 50mm lens and +2 optical split-field diopter on Kodak Vision3 50D (7203). "
            "CRITICAL PRODUCT SHAPE (NON-NEGOTIABLE): The Surf Clock in the center-right background MUST be the exact SHARP 90-DEGREE VERTICAL RECTANGULAR STEPPED-BEZEL MONOLITH (184 x 230 x 52 mm hardcover-book rectangle) "
            "shown in Reference Image 1 (INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg) with ONE SINGLE FLAT CONTINUOUS RECTANGULAR RECESSED DIAL FACE. NEVER render a circular/round clock housing and NEVER render arched cutouts! "
            "SPLIT-DIOPTER COMPOSITION: On the left side in the near foreground (left 28% of frame), a sun-bleached Australian Nautilus shell rests on a warm cream woven linen table in crisp macro focus. "
            "A soft vertical optical split-diopter blur line runs vertically at 32% from the left edge. "
            "On the center-right side (occupying the central focal zone), the sharp rectangular matte slate-blue Surf Clock stands upright on the warm cream architectural surface against a bright, airy, sun-drenched warm cream plaster wall with soft dappled golden afternoon light, "
            "ALSO in simultaneous razor-sharp optical focus! "
            "On its single flat rectangular matte blue dial face: strictly 9 raised white radial tick marks on the top semicircle ONLY (8 to 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
            "100% blank smooth matte slate-blue bottom arc at 5, 6, and 7 o'clock, lower WORTH IT? (NAH / YEAH) arc gauge, and strictly 2 skinny burnt-orange pointer hands total."
        ),
    },
]

def run_still(spec):
    out_path = os.path.join(OUT_DIR, spec["filename"])
    raw_ungraded_path = out_path.replace("_4K.jpg", "_4K_raw_ungraded.jpg")
    graded_copy_path = out_path.replace("_4K.jpg", "_4K_poetry_camera_16mm_50D.jpg")
    if os.path.exists(out_path):
        os.remove(out_path)
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
    print(f"=== Finished Still: {spec['filename']} (ok={ok}, score={audit.get('score')}, pass={audit.get('pass')}) ===", flush=True)
    return spec["filename"], out_path, raw_ungraded_path, audit

with ThreadPoolExecutor(max_workers=2) as ex:
    futures = [ex.submit(run_still, s) for s in STILL_SPECS]
    for f in futures:
        f.result()
