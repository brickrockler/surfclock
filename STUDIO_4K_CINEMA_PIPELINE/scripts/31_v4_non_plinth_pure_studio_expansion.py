#!/usr/bin/env python3
"""
V4 STAGE 2 ARTFUL NON-PLINTH STUDIO & EDITORIAL DESIGN FILM EXPANSION
(Teenage Engineering / Telepathic Instruments Orchid / Braun 1968 Kronberg / Apartamento / Donald Judd Aesthetic)
- Zero cliché ad packshots, zero plinth blocks, zero AI slop tells.
- 24 brand-new Native 4K Non-Plinth Studio & Editorial Keyframes (16 in 16:9 widescreen + 8 in 9:16 vertical)
  shot on simulated medium-format Kodak Portra 400 / 35mm cinema lenses with real physical craft, tactile surfaces,
  asymmetric compositions, and rich chiaroscuro / dappled natural light.
- 16 brand-new Native 1080p First+Last-Frame Locked Veo 3.1 Pro (`veo-3.1-generate-001`) cinema clips
  mastered to 4K 60fps with 100% accurate 9-tick, 2-hand, razor-sharp pad-printed dial lock.
"""

import os
import sys
import time
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
import importlib.util

BASE = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
spec = importlib.util.spec_from_file_location("v4_suite", str(BASE / "scripts" / "30_v4_veo31_locked_studio_and_aussie_cinema_suite.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

GEMINI_KEY = Path("~/.config/pickleball-coach/gemini.key").expanduser().read_text().strip()
MASTER_16x9_PATH = m.REF_DIR / "MASTER_REF_4K_16x9_CrispBraunMolded.jpg"
MASTER_9x16_PATH = m.REF_DIR / "MASTER_REF_4K_9x16_CrispBraunMolded.jpg"

B64_MASTER_16x9 = base64.b64encode(MASTER_16x9_PATH.read_bytes()).decode("utf-8")
B64_MASTER_9x16 = base64.b64encode(MASTER_9x16_PATH.read_bytes()).decode("utf-8")

ACCURATE_PRODUCT_LOCK = (
    "CRITICAL PRODUCT ACCURACY RULES (DO NOT VIOLATE): "
    "Keep the EXACT upright 3:4 rectangular matte slate-blue/midnight-navy Braun/Orchid molded Surf Instrument from the reference image. "
    "1. NO PLINTH / NO PEDESTAL BLOCK: Never place the clock on a small cube or plinth; rest it directly on the continuous tabletop, workbench, floor, or wall described. "
    "2. STRICTLY TWO HANDS TOTAL: ONE single burnt-orange pointer hand on the upper beach dial (pointing to DEE WHY at 2 o'clock), "
    "and ONE single short burnt-orange pointer hand on the lower WORTH IT? semicircle gauge (pointing to YEAH). NEVER add a second hand on the upper dial! "
    "3. DIAL MARKS STOP AT FRESHIE (8 o'clock) AND CURL CURL (4 o'clock): The upper dial has ONLY 9 white radial tick marks in the upper arc "
    "(8, 9, 10, 11, 12, 1, 2, 3, 4 o'clock). There are ZERO tick marks at 5 o'clock, 6 o'clock, or 7 o'clock — the bottom third of the upper dial "
    "between FRESHIE and CURL CURL is 100% blank matte navy dial surface! "
    "4. OPEN MATTE STEPPED BEZEL: ZERO glass cover over the front face, ZERO glowing blue LEDs, ZERO electric cyan highlights. "
    "Tactile VDI-24 micro-bead matte injection-molded Braun / Teenage Engineering finish with razor-sharp white pad-printed typography "
    "(LONG REEF, QUEENSIE, DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT?)."
)

NON_PLINTH_STUDIO_KEYFRAME_JOBS = [
    # --- 16 ARTFUL NON-PLINTH STUDIO, DESIGN LAB & EDITORIAL TABLETOP SHOTS (16:9) ---
    ("V4_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_16x9_4K.jpg", "16:9",
     "Artful industrial design film frame shot on 35mm Kodak Vision3 250D (Teenage Engineering Stockholm lab / Braun 1968 Kronberg workshop vibe, NOT a generic ad). "
     "The matte slate-blue rectangular Surf Instrument rests directly on a worn, matte sage-grey self-healing engineering cutting mat with faint printed millimeter grid lines on a designer's workbench (NO plinth). "
     "In the soft out-of-focus foreground/side lie a pair of brushed stainless-steel Mitutoyo vernier calipers and a coiled grey braided cloth USB-C cable; raking natural studio window light from the side cuts across the tactile VDI-24 matte molded bezel. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_12_Raw_Galvanized_Steel_Worktable_DarkBlue_Backdrop_16x9_4K.jpg", "16:9",
     "Editorial industrial design photography shot on medium-format Hasselblad 80mm Planar lens (Kodak Portra 400 grain, rich tonal depth). "
     "The matte slate-blue rectangular Surf Instrument rests directly on a wide, continuous raw mill-finish galvanized sheet-steel studio worktable with subtle brushed fabrication marks (NO plinth) against a deep, moody matte midnight-blue painted studio backdrop. "
     "A single warm-tungsten key light from the left creates a soft, muted reflection of the blue housing on the raw steel surface and long dramatic shadow falloff. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_13_Crumpled_Unbleached_Painter_Canvas_WhiteStudio_Sunlight_16x9_4K.jpg", "16:9",
     "Art-house studio photography (Poetry Camera / Apartamento magazine aesthetic, shot on 35mm film). "
     "The matte slate-blue rectangular Surf Instrument stands directly on a heavy, loosely draped unbleached raw cotton painter's drop-cloth covering a wide studio table against a sunlit chalk-white studio wall (NO plinth). "
     "Hard, low-angle late-afternoon sunlight streams through an unseen studio window, casting organic folds of shadow across the raw canvas and illuminating the crisp matte slate-blue dial. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_14_Monochrome_SlateBlue_Seamless_Floor_Hard_SlitLight_16x9_4K.jpg", "16:9",
     "Cinematic monochromatic industrial design film still in a deep slate-blue studio cyclorama (NO plinth). "
     "The matte slate-blue rectangular Surf Instrument stands directly on the continuous matte slate-blue studio floor, framed slightly off-center, while a single narrow diagonal blade of warm sunlight cuts across the floor and illuminates the face of the instrument, leaving the rest of the deep blue studio in velvety shadow. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_16x9_4K.jpg", "16:9",
     "Telepathic Instruments Orchid / Kevin Parker analog synth studio aesthetic shot on 35mm film. "
     "The matte slate-blue rectangular Surf Instrument rests directly on a warm matte-oiled Baltic birch plywood studio desk against a warm cream acoustic plaster wall (NO plinth). "
     "Beside it in the soft shallow depth-of-field bokeh sit a tangled loop of burnt-orange and grey 3.5mm braided synth patch cables and a brushed aluminum rotary knob module in warm afternoon sunbeams. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_16x9_4K.jpg", "16:9",
     "Architectural minimalism photography (Donald Judd Marfa / Axel Vervoordt gallery vibe, shot on medium format film). "
     "The matte slate-blue rectangular Surf Instrument hangs flush-mounted directly on a textured, mineral bone-white lime-washed studio wall near a quiet architectural corner reveal (NO plinth, NO shelf). "
     "Grazing natural skylight from above washes down the lime-washed plaster texture and casts a soft, elongated shadow below the matte slate-blue housing. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_17_SunWarmed_Terracotta_QuarryTiles_Studio_Floor_16x9_4K.jpg", "16:9",
     "Warm Mediterranean / Australian modernist studio floor photography shot on Kodak Portra 400 film. "
     "The matte slate-blue rectangular Surf Instrument rests directly on a continuous floor of raw, matte sun-warmed ochre-terracotta clay quarry tiles against a clean warm-white studio wall (NO plinth). "
     "Long, slanted afternoon window-mullion shadows stretch across the terracotta tiles and warm white wall, creating a striking color contrast with the matte slate-blue Braun housing. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_18_PureWhite_Cyc_Floor_WideAngle_LongShadow_Hero_16x9_4K.jpg", "16:9",
     "Iconic 1968 Braun archival industrial design film frame in a pure white infinity cyclorama studio (NO plinth). "
     "Shot from a low tabletop/floor angle on a 35mm cinema prime lens: the matte slate-blue rectangular Surf Instrument stands directly on the continuous matte white cyclorama floor, casting a long, dramatic, razor-clean architectural shadow stretching across the white floor toward the right edge of the frame. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_19_Wet_Cleft_Bluestone_Slab_DarkBlue_Studio_Mist_16x9_4K.jpg", "16:9",
     "Tactile material-contrast studio photography in a dark slate-blue studio (NO plinth). "
     "The matte slate-blue rectangular Surf Instrument rests directly on a wide, continuous flat slab of dark Australian cleft basalt/bluestone table surface with a few natural droplets of water on the stone, set against a deep midnight-blue studio backdrop with soft side key light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_20_Unrolled_WarmPutty_CottonRag_Paper_On_Worktable_16x9_4K.jpg", "16:9",
     "Artful studio still-life shot on 35mm film. The matte slate-blue rectangular Surf Instrument stands directly on a wide roll of heavy, deckle-edged warm putty/sand cotton rag art paper unrolled across a dark studio worktable against a soft off-white studio wall (NO plinth). "
     "Dappled natural window light filters across the textured paper and matte slate-blue housing. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_21_WallMounted_DeepNavy_Panel_Raking_Skylight_16x9_4K.jpg", "16:9",
     "Quiet, hyper-minimalist monochrome architectural studio shot. The matte slate-blue rectangular Surf Instrument is mounted flush directly on a continuous matte midnight-navy architectural wall panel (NO plinth, NO table). "
     "A raking shaft of warm golden skylight from the upper right grazes the stepped bezel, white pad-printed typography, and burnt-orange hands so they pop with extraordinary clarity against the deep navy wall. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_22_Raw_Concrete_Studio_Floor_And_GafferTape_Marks_16x9_4K.jpg", "16:9",
     "Behind-the-scenes industrial design film studio aesthetic shot on 35mm Kodak film. "
     "The matte slate-blue rectangular Surf Instrument rests directly on a smooth, matte power-troweled grey concrete photography studio floor (NO plinth) in a pool of warm tungsten-balanced studio key light, with the soft out-of-focus curve of a white cyclorama wall in the background. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_23_Bleached_DouglasFir_Table_Against_SlateBlue_Cyc_16x9_4K.jpg", "16:9",
     "Editorial studio tabletop photography with rich color contrast (NO plinth). "
     "The matte slate-blue rectangular Surf Instrument rests directly on a wide, continuous flat table of pale soap-finished Douglas Fir timber with linear grain, set in front of a deep matte slate-blue seamless studio backdrop illuminated by a soft diagonal shaft of warm light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_24_Warm_Cork_Pinboard_Desk_And_Braun_Sketches_16x9_4K.jpg", "16:9",
     "Industrial designer's studio desk photography shot on 35mm film (Dieter Rams / Vitsoe studio vibe). "
     "The matte slate-blue rectangular Surf Instrument rests directly on a continuous flat desktop of warm natural cork against a clean warm-white studio wall (NO plinth), with the corner of a cream grid notebook and a black technical drafting pen resting out-of-focus on the cork table beside it. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_25_Charcoal_Linen_Bookcloth_Table_Warm_WindowBeam_16x9_4K.jpg", "16:9",
     "Refined editorial tabletop photography in a quiet studio setting. "
     "The matte slate-blue rectangular Surf Instrument rests directly on a continuous flat surface covered in woven charcoal-slate bookcloth linen against a warm cream plaster studio wall (NO plinth), caught in a soft golden beam of afternoon window light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_26_WallMounted_Sunlit_White_Plaster_Dappled_Eucalyptus_16x9_4K.jpg", "16:9",
     "Sun-drenched Australian architectural studio photography. The matte slate-blue rectangular Surf Instrument is mounted flush directly on a smooth matte white plaster studio wall (NO plinth, NO shelf) while real moving dappled eucalyptus tree shadows dance across the white wall around the clock. " + ACCURATE_PRODUCT_LOCK),

    # --- 8 NATIVE 9:16 VERTICAL ARTFUL NON-PLINTH STUDIO SHOTS ---
    ("V4_9x16_13_PureWhite_Cyc_Floor_LongShadow_Hero_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical 1968 Braun archival studio photography. The matte slate-blue rectangular Surf Instrument stands directly on the continuous flat floor of a pure matte white infinity cyclorama (NO plinth), casting a long, dramatic diagonal shadow across the white floor in warm angled studio light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_14_Monochrome_SlateBlue_Cyc_Floor_SlitLight_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical monochromatic dark studio photography. The matte slate-blue rectangular Surf Instrument stands directly on the continuous flat floor of a deep midnight slate-blue studio cyclorama (NO plinth), illuminated by a single dramatic diagonal blade of warm sunlight cutting across the floor. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical Teenage Engineering / Braun workshop photography shot on 35mm film. The matte slate-blue rectangular Surf Instrument rests directly on a matte sage-grey engineering cutting mat with faint grid lines on a studio workbench (NO plinth), with steel vernier calipers in the soft foreground bokeh. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_16_WallMounted_Limewash_Gallery_Wall_Shadow_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical architectural studio photography. The matte slate-blue rectangular Surf Instrument hangs flush-mounted directly on a textured bone-white lime-washed studio wall (NO plinth, NO shelf) with directional sunlight casting a crisp geometric drop shadow onto the wall. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_17_Crumpled_Unbleached_Canvas_Table_Sunbeam_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical art-house studio photography (Poetry Camera / Apartamento vibe). The matte slate-blue rectangular Surf Instrument rests directly on heavy unbleached raw cotton painter's canvas draped over a studio table against a warm white wall (NO plinth) in a hard beam of golden afternoon sun. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_18_Raw_Galvanized_Steel_Worktable_DarkBlue_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical industrial design studio photography. The matte slate-blue rectangular Surf Instrument rests directly on a continuous raw mill-finish galvanized steel workbench (NO plinth) against a deep matte slate-blue studio backdrop with warm tungsten key lighting. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_19_Orchid_Synth_Desk_BirchPlywood_PatchCables_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical Telepathic Instruments Orchid studio aesthetic shot on 35mm film. The matte slate-blue rectangular Surf Instrument rests directly on a warm birch plywood studio desk beside braided synth patch cables against a warm cream studio wall in golden afternoon light (NO plinth). " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_20_SunWarmed_Terracotta_Tiles_Studio_Floor_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical modernist studio photography on Kodak Portra 400 film. The matte slate-blue rectangular Surf Instrument rests directly on a continuous floor of matte sun-warmed terracotta quarry tiles against a warm white studio wall with slanted window shadows (NO plinth). " + ACCURATE_PRODUCT_LOCK),
]


def generate_and_lock_one_non_plinth_keyframe(idx: int, job_tuple: tuple) -> Path:
    out_name, aspect, prompt = job_tuple
    out_dir = m.V4_16x9_STILLS if aspect == "16:9" else m.V4_9x16_STILLS
    out_path = out_dir / out_name
    if out_path.exists() and out_path.stat().st_size > 400_000:
        print(f"[SKIP EXISTING 4K NON-PLINTH] {out_name}", flush=True)
        return out_path

    time.sleep((idx % 6) * 1.1)
    ref_b64 = B64_MASTER_16x9 if aspect == "16:9" else B64_MASTER_9x16
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": ref_b64}},
                {"text": prompt},
            ],
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "temperature": 0.38,
            "imageConfig": {
                "aspectRatio": aspect,
                "imageSize": "4K",
            },
        },
    }

    data = json.dumps(payload).encode("utf-8")
    ink_layers = m.render_ink_and_hands_4k(0.0, 0.0)

    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                res = json.loads(resp.read().decode("utf-8"))
            b64_out = None
            for cand in res.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    if "inlineData" in part and part["inlineData"].get("data"):
                        b64_out = part["inlineData"]["data"]
                        break
            if not b64_out:
                raise RuntimeError("No image returned")
            raw_bytes = base64.b64decode(b64_out)
            arr = np.frombuffer(raw_bytes, dtype=np.uint8)
            im = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            im = m.remove_electric_cyan_highlights(im)
            H = m.find_initial_homography_from_4k_ref(im, None)
            if H is not None:
                im = m.clean_frame_chimney_and_dial_v14(im, H, ink_layers, erase_chimney=False)
            cv2.imwrite(str(out_path), im, [cv2.IMWRITE_JPEG_QUALITY, 97])
            print(f"[GENERATED & DIAL-LOCKED 4K NON-PLINTH] {out_name} ({out_path.stat().st_size/1e6:.2f} MB)", flush=True)
            return out_path
        except Exception as e:
            print(f"[RETRY {attempt}/4] {out_name}: {e}", flush=True)
            time.sleep(4 * attempt)

    raise RuntimeError(f"Failed to generate {out_name}")


NON_PLINTH_VEO_JOBS = [
    # --- 12 WIDESCREEN 16:9 ARTFUL NON-PLINTH STUDIO & DESIGN LAB CINEMA CLIPS ---
    {
        "id": "V4_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers",
        "out_mp4": "V4_28_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "16mm",
        "prompt": (
            "Artful 35mm industrial design film shot in a Teenage Engineering / Braun Kronberg prototype workshop (no plinth). "
            "Slow, smooth camera slider push-in across a matte grid cutting mat with steel vernier calipers in the soft foreground bokeh while natural window light shifts across the matte slate-blue rectangular Braun instrument."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_12_Raw_Galvanized_Steel_Worktable_DarkBlue_Backdrop",
        "out_mp4": "V4_29_STUDIO_12_Raw_Galvanized_Steel_Worktable_DarkBlue_Backdrop_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_12_Raw_Galvanized_Steel_Worktable_DarkBlue_Backdrop_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Medium-format editorial studio cinema shot. Slow, smooth camera push-in across a raw mill-finish galvanized sheet-steel worktable against a deep midnight-blue studio backdrop as warm tungsten key light glides across the brushed steel and matte slate-blue housing."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_13_Crumpled_Unbleached_Painter_Canvas_WhiteStudio_Sunlight",
        "out_mp4": "V4_30_STUDIO_13_Crumpled_Unbleached_Painter_Canvas_WhiteStudio_Sunlight_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_13_Crumpled_Unbleached_Painter_Canvas_WhiteStudio_Sunlight_16x9_4K.jpg",
        "sweep_beaches": False,
        "grain": "16mm",
        "prompt": (
            "Art-house 35mm film studio shot (Poetry Camera / Apartamento vibe). Subtle camera push-in across heavy unbleached painter's canvas on a studio table against a sunlit chalk-white wall while warm afternoon sunbeams and dust motes drift gently."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_14_Monochrome_SlateBlue_Seamless_Floor_Hard_SlitLight",
        "out_mp4": "V4_31_STUDIO_14_Monochrome_SlateBlue_Seamless_Floor_Hard_SlitLight_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_14_Monochrome_SlateBlue_Seamless_Floor_Hard_SlitLight_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Cinematic monochromatic studio shot on a continuous deep slate-blue cyclorama floor (no plinth). "
            "Slow, smooth camera push-in while a narrow diagonal blade of warm sunlight slowly sweeps across the deep slate-blue floor and matte slate-blue Braun instrument."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables",
        "out_mp4": "V4_32_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_16x9_4K.jpg",
        "sweep_beaches": False,
        "grain": "16mm",
        "prompt": (
            "Telepathic Instruments Orchid analog synth studio cinema shot on 35mm film. "
            "Slow, smooth camera slider push-in across a birch plywood studio desk with braided synth patch cables in the foreground bokeh while warm afternoon sunbeams shift across the matte slate-blue instrument."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap",
        "out_mp4": "V4_33_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Donald Judd Marfa architectural studio cinema shot of the matte slate-blue rectangular Braun instrument mounted flush on a textured bone-white lime-washed wall. "
            "Slow, smooth camera push-in as grazing natural skylight shifts gently across the mineral plaster wall."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_17_SunWarmed_Terracotta_QuarryTiles_Studio_Floor",
        "out_mp4": "V4_34_STUDIO_17_SunWarmed_Terracotta_QuarryTiles_Studio_Floor_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_17_SunWarmed_Terracotta_QuarryTiles_Studio_Floor_16x9_4K.jpg",
        "sweep_beaches": False,
        "grain": "16mm",
        "prompt": (
            "Modernist studio cinema shot on Kodak Portra 35mm film. Slow, smooth camera push-in across a continuous floor of sun-warmed terracotta quarry tiles as slanted afternoon window shadows glide gently across the tiles."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_18_PureWhite_Cyc_Floor_WideAngle_LongShadow_Hero",
        "out_mp4": "V4_35_STUDIO_18_PureWhite_Cyc_Floor_WideAngle_LongShadow_Hero_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_18_PureWhite_Cyc_Floor_WideAngle_LongShadow_Hero_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Iconic 1968 Braun archival industrial design cinema shot on a continuous pure white cyclorama floor (no plinth). "
            "Slow, low-angle camera dolly push-in toward the matte slate-blue rectangular Braun instrument casting a long architectural shadow across the white floor."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_19_Wet_Cleft_Bluestone_Slab_DarkBlue_Studio_Mist",
        "out_mp4": "V4_36_STUDIO_19_Wet_Cleft_Bluestone_Slab_DarkBlue_Studio_Mist_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_19_Wet_Cleft_Bluestone_Slab_DarkBlue_Studio_Mist_16x9_4K.jpg",
        "sweep_beaches": False,
        "grain": "studio",
        "prompt": (
            "Tactile dark studio cinema shot. Slow, smooth camera push-in across a wet cleft bluestone slab in a deep midnight-blue studio as raking side light glints off water droplets on the stone."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_20_Unrolled_WarmPutty_CottonRag_Paper_On_Worktable",
        "out_mp4": "V4_37_STUDIO_20_Unrolled_WarmPutty_CottonRag_Paper_On_Worktable_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_20_Unrolled_WarmPutty_CottonRag_Paper_On_Worktable_16x9_4K.jpg",
        "sweep_beaches": False,
        "grain": "16mm",
        "prompt": (
            "Artful studio still-life cinema shot on 35mm film. Slow, smooth camera push-in across deckle-edged warm putty cotton rag paper unrolled on a studio worktable while dappled window light sways gently."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_23_Bleached_DouglasFir_Table_Against_SlateBlue_Cyc",
        "out_mp4": "V4_38_STUDIO_23_Bleached_DouglasFir_Table_Against_SlateBlue_Cyc_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_23_Bleached_DouglasFir_Table_Against_SlateBlue_Cyc_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Editorial studio tabletop cinema shot. Slow, smooth camera push-in across a pale soap-finished Douglas Fir timber table set against a deep matte slate-blue studio backdrop."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_STUDIO_26_WallMounted_Sunlit_White_Plaster_Dappled_Eucalyptus",
        "out_mp4": "V4_39_STUDIO_26_WallMounted_Sunlit_White_Plaster_Dappled_Eucalyptus_4K.mp4",
        "aspect": "16:9",
        "kf": m.V4_16x9_STILLS / "V4_STUDIO_26_WallMounted_Sunlit_White_Plaster_Dappled_Eucalyptus_16x9_4K.jpg",
        "sweep_beaches": True,
        "grain": "16mm",
        "prompt": (
            "Sun-drenched Australian architectural studio cinema shot. The matte slate-blue rectangular Braun instrument hangs flush on a smooth white plaster wall while real dappled eucalyptus tree shadows sway in the breeze across the wall."
            + m.NO_CLOCK_WORD_RULE
        ),
    },

    # --- 4 NATIVE 9:16 VERTICAL ARTFUL NON-PLINTH STUDIO CINEMA CLIPS ---
    {
        "id": "V4_9x16_13_PureWhite_Cyc_Floor_LongShadow_Hero_Vertical",
        "out_mp4": "V4_9x16_13_PureWhite_Cyc_Floor_LongShadow_Hero_Vertical_4K.mp4",
        "aspect": "9:16",
        "kf": m.V4_9x16_STILLS / "V4_9x16_13_PureWhite_Cyc_Floor_LongShadow_Hero_Vertical_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Native 9:16 vertical 1968 Braun studio cinema shot on a continuous pure white cyclorama floor (no plinth). "
            "Slow, smooth camera push-in toward the matte slate-blue rectangular Braun instrument casting a long diagonal shadow across the floor."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_9x16_14_Monochrome_SlateBlue_Cyc_Floor_SlitLight_Vertical",
        "out_mp4": "V4_9x16_14_Monochrome_SlateBlue_Cyc_Floor_SlitLight_Vertical_4K.mp4",
        "aspect": "9:16",
        "kf": m.V4_9x16_STILLS / "V4_9x16_14_Monochrome_SlateBlue_Cyc_Floor_SlitLight_Vertical_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Native 9:16 vertical monochromatic dark studio cinema shot on a deep midnight slate-blue cyclorama floor (no plinth). "
            "Slow, smooth camera push-in while a diagonal blade of warm sunlight sweeps gently across the floor."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical",
        "out_mp4": "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_4K.mp4",
        "aspect": "9:16",
        "kf": m.V4_9x16_STILLS / "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_4K.jpg",
        "sweep_beaches": False,
        "grain": "16mm",
        "prompt": (
            "Native 9:16 vertical Teenage Engineering / Braun workshop cinema shot on 35mm film. "
            "Slow, smooth camera push-in across a matte grid cutting mat with steel vernier calipers in the soft foreground bokeh."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
    {
        "id": "V4_9x16_16_WallMounted_Limewash_Gallery_Wall_Shadow_Vertical",
        "out_mp4": "V4_9x16_16_WallMounted_Limewash_Gallery_Wall_Shadow_Vertical_4K.mp4",
        "aspect": "9:16",
        "kf": m.V4_9x16_STILLS / "V4_9x16_16_WallMounted_Limewash_Gallery_Wall_Shadow_Vertical_4K.jpg",
        "sweep_beaches": True,
        "grain": "studio",
        "prompt": (
            "Native 9:16 vertical architectural studio cinema shot of the matte slate-blue rectangular Braun instrument mounted flush on a textured lime-washed wall (no plinth). "
            "Slow, smooth camera push-in while directional sunlight shifts the geometric drop shadow across the wall."
            + m.NO_CLOCK_WORD_RULE
        ),
    },
]


def main():
    print(f"=== STEP 1: GENERATING & DIAL-LOCKING {len(NON_PLINTH_STUDIO_KEYFRAME_JOBS)} ARTFUL NON-PLINTH STUDIO 4K STILLS ===", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(generate_and_lock_one_non_plinth_keyframe, i, job) for i, job in enumerate(NON_PLINTH_STUDIO_KEYFRAME_JOBS)]
        for f in as_completed(futs):
            f.result()

    tiles = []
    for out_name, aspect, _ in NON_PLINTH_STUDIO_KEYFRAME_JOBS:
        p = (m.V4_16x9_STILLS if aspect == "16:9" else m.V4_9x16_STILLS) / out_name
        im = cv2.imread(str(p))
        if im is not None:
            tile = cv2.resize(im, (480, 270))
            cv2.putText(tile, out_name[:34], (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 0, 0), 3)
            cv2.putText(tile, out_name[:34], (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 1)
            tiles.append(tile)
    while len(tiles) % 4 != 0:
        tiles.append(np.zeros((270, 480, 3), dtype=np.uint8))
    grid = np.vstack([np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)])
    cv2.imwrite(str(m.AUDIT_DIR / "AUDIT_V4_NON_PLINTH_PURE_STUDIO_24_STILLS.jpg"), grid, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print("[SAVED AUDIT] AUDIT_V4_NON_PLINTH_PURE_STUDIO_24_STILLS.jpg", flush=True)

    print(f"=== STEP 2: GENERATING {len(NON_PLINTH_VEO_JOBS)} ARTFUL NON-PLINTH STUDIO 1080P VEO 3.1 PRO VIDEOS ===", flush=True)
    raw_map = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        fut_map = {ex.submit(m.generate_veo_1080p_first_last_locked, i, job): job for i, job in enumerate(NON_PLINTH_VEO_JOBS)}
        for fut in as_completed(fut_map):
            job = fut_map[fut]
            raw_mp4 = fut.result()
            raw_map[job["id"]] = raw_mp4

    print("=== STEP 3: MASTERING ALL 16 ARTFUL NON-PLINTH STUDIO VIDEOS TO 4K 60FPS ===", flush=True)
    for job in NON_PLINTH_VEO_JOBS:
        raw_mp4 = raw_map[job["id"]]
        out_dir = m.CLIPS_16x9_DIR if job["aspect"] == "16:9" else m.CLIPS_9x16_DIR
        m.master_clip_v4_perfect(
            raw_mp4=raw_mp4,
            out_mp4=out_dir / job["out_mp4"],
            aspect=job["aspect"],
            kf_4k_path=job["kf"],
            sweep_beaches=job["sweep_beaches"],
            grain_mode=job["grain"],
            erase_chimney=False,
        )

    m.build_video_audit_sheet(sorted(m.CLIPS_16x9_DIR.glob("V4_*.mp4")), m.AUDIT_DIR / "AUDIT_V4_ALL_16x9_VIDEOS_DIAL_ZOOM.jpg")
    m.build_video_audit_sheet(sorted(m.CLIPS_9x16_DIR.glob("V4_*.mp4")), m.AUDIT_DIR / "AUDIT_V4_ALL_9x16_VIDEOS_DIAL_ZOOM.jpg")

    clips_16 = sorted(m.CLIPS_16x9_DIR.glob("V4_*.mp4"))
    clips_9  = sorted(m.CLIPS_9x16_DIR.glob("V4_*.mp4"))
    studio_16 = [c for c in clips_16 if "_STUDIO_" in c.name or "_CREAM_" in c.name or "_MACRO_" in c.name]
    aussie_16 = [c for c in clips_16 if "_AUSSIE_" in c.name or "_CREAM_" in c.name]

    m.concat_videos(clips_16,  m.SHOWREELS_DIR / "01_SURF_CLOCK_MASTER_4K_60FPS_16x9_WIDESCREEN_SHOWREEL.mp4")
    m.concat_videos(clips_9,   m.SHOWREELS_DIR / "02_SURF_CLOCK_MASTER_4K_60FPS_9x16_VERTICAL_SOCIAL_REEL.mp4")
    m.concat_videos(studio_16, m.SHOWREELS_DIR / "03_SURF_CLOCK_CLEAN_STUDIO_PLINTHS_AND_DAPPLED_CREAM_4K_REEL.mp4")
    m.concat_videos(aussie_16, m.SHOWREELS_DIR / "04_SURF_CLOCK_AUSSIE_SURF_CULTURE_16MM_AND_CAMCORDER_4K_REEL.mp4")
    print("ARTFUL NON-PLINTH STUDIO EXPANSION COMPLETE!", flush=True)


if __name__ == "__main__":
    main()
