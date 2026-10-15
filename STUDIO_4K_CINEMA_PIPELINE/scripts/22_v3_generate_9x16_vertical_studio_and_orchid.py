#!/usr/bin/env python3
"""
V3 STAGE 2:
1. Regenerates V3_02, V3_04, and V3_20 (16:9) so 36/36 16:9 plates have 100% identical upright rectangular 3:4 frame + white semicircle arc geometry.
2. Generates 16 Native 9:16 Vertical (2160x3840 4K) Studio & Orchid / Poetry Camera plates from MASTER_REF_4K_9x16_CrispBraunMolded.jpg.
"""

import os
import time
import base64
from pathlib import Path
import requests
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
V3_16x9_DIR = os.path.join(BASE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS/V3_ORCHID_POETRY_ARCHDIGEST_4K")
V3_9x16_DIR = os.path.join(BASE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS/V3_9x16_VERTICAL_STUDIO_AND_ORCHID_4K")
AUDIT_DIR = os.path.join(BASE_DIR, "04_CONTACT_SHEETS_AND_AUDIT")
os.makedirs(V3_9x16_DIR, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)

API_KEY = Path("~/.config/pickleball-coach/gemini.key").expanduser().read_text().strip()

MASTER_REF_16x9 = os.path.join(V3_16x9_DIR, "MASTER_REF_4K_16x9_CrispBraunMolded.jpg")
MASTER_REF_9x16 = os.path.join(V3_16x9_DIR, "MASTER_REF_4K_9x16_CrispBraunMolded.jpg")

ref16_img = cv2.imread(MASTER_REF_16x9)
ref16_2k = cv2.resize(ref16_img, (2048, 1152), interpolation=cv2.INTER_AREA)
_, buf16 = cv2.imencode(".jpg", ref16_2k, [cv2.IMWRITE_JPEG_QUALITY, 96])
REF16_B64 = base64.b64encode(buf16.tobytes()).decode("utf-8")

ref9_img = cv2.imread(MASTER_REF_9x16)
ref9_2k = cv2.resize(ref9_img, (1152, 2048), interpolation=cv2.INTER_AREA)
_, buf9 = cv2.imencode(".jpg", ref9_2k, [cv2.IMWRITE_JPEG_QUALITY, 96])
REF9_B64 = base64.b64encode(buf9.tobytes()).decode("utf-8")

STRICT_CLOCK_RULES = """
CRITICAL INDUSTRIAL DESIGN & ACCURACY RULES (100% MANDATORY):
1. EXACT GEOMETRY & PROPORTIONS: Keep the exact upright rectangular 3:4 proportions, deep chamfered outer bezel, and rectangular recessed dial cavity of the Surf Clock shown in the reference image. NEVER make the clock square and NEVER use a circular recess.
2. TACTILE BRAUN / TELEPATHIC INSTRUMENTS 'ORCHID' / TEENAGE ENGINEERING MOLDED FINISH: The housing and recessed dial cavity must look like an ultra-expensive injection-molded VDI-24 micro-bead matte ABS/PBT synthesizer/instrument housing with subtle physical micro-grain texture and razor-sharp pad-printed white typography.
3. EXACT 2 HANDS ONLY (DEE WHY & YEAH):
   - Upper dial has 12 radial tick marks and 5 crisp white pad-printed labels ('LONG REEF' at 12 o'clock, 'QUEENSIE' at 10 o'clock, 'DEE WHY' at 2 o'clock, 'FRESHIE' at 8 o'clock, 'CURL CURL' at 4 o'clock) with EXACTLY ONE matte burnt-orange pointer hand pointing to 'DEE WHY' (2 o'clock).
   - Lower sub-dial has a clean matte-white painted semicircle arc with 5 tick marks, 'NAH' on the left, 'YEAH' on the right, 'WORTH IT?' centered below, and EXACTLY ONE short matte burnt-orange pointer hand pointing to 'YEAH'.
4. NO WEIRD BLUE HIGHLIGHTS OR GLOWS: Never put any electric cyan or glowing blue highlight on the white 'WORTH IT?' semicircle arc. No neon LEDs, no black glow, no front glass cover.
"""

FIX_16x9_SHOTS = [
    ("V3_02_Orchid_Clover_And_Chamomile_Meadow_Overhead_16mm_4K.jpg",
     "Artful 16mm Kodak Vision3 film photograph inspired by Telepathic Instruments Orchid: this exact upright rectangular 3:4 matte midnight-navy Surf Clock stands at a 14-degree angle nestled in a lush green clover and wild white chamomile flower meadow in warm morning sunlight. Keep the exact upright rectangular 3:4 frame, rectangular recessed dial cavity, and white semicircle 'WORTH IT?' arc at the bottom."),
    ("V3_04_Orchid_Coastal_Headland_TallGrass_And_OceanSwell_16mm_4K.jpg",
     "Artful 16mm film photograph inspired by Telepathic Instruments Orchid: this exact upright rectangular 3:4 matte midnight-navy Surf Clock stands on a sun-warmed sandstone boulder surrounded by golden swaying coastal kangaroo grass overlooking turquoise ocean swell Lines in soft out-of-focus bokeh. Keep the exact upright rectangular 3:4 frame, rectangular recessed dial cavity, and white semicircle 'WORTH IT?' arc at the bottom."),
    ("V3_20_Wall_Mounted_Gallery_Limestone_Wall_ThreeQuarter_4K.jpg",
     "Architectural Digest photograph: this exact upright rectangular 3:4 matte midnight-navy Surf Clock is mounted flush on a honed cream limestone gallery wall viewed from a 15-degree three-quarter angle in warm afternoon skylight. Keep the exact upright rectangular 3:4 frame, rectangular recessed dial cavity, and white semicircle 'WORTH IT?' arc at the bottom.")
]

VERTICAL_SHOTS = [
    # --- 8 CLEAN STUDIO & MACRO 9:16 VERTICAL PLATES ---
    ("V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg",
     "Clean 9:16 vertical studio hero photograph of this exact matte midnight-navy Surf Clock standing at a 14-degree three-quarter angle on a honed dark slate-blue architectural monolith. Soft warm-white north-facing window light from camera-left casting gentle diagonal shadow bands across the slate background, revealing the tactile VDI-24 micro-bead injection-molded polymer grain and razor-sharp white pad-printed typography ('LONG REEF', 'QUEENSIE', 'DEE WHY', 'FRESHIE', 'CURL CURL', 'NAH', 'YEAH', 'WORTH IT?'). Shot on Hasselblad X2D 100C 80mm f/4."),

    ("V3_9x16_02_Studio_Braun_1965_IceGrey_RAL7035_Molded_4K.jpg",
     "Clean 9:16 vertical studio photograph of a 1965 Dieter Rams Braun Ulm Edition of this exact rectangular Surf Clock standing at a 14-degree three-quarter angle on a honed warm Roman travertine plinth: the outer chamfered rectangular frame is molded in warm Braun Ice-Grey (RAL 7035) VDI-24 micro-textured matte ABS polymer, while the recessed rectangular dial cavity is deep matte charcoal-black with razor-sharp white pad-printed typography and matte burnt-orange hands pointing to DEE WHY and YEAH. Soft studio daylight, Hasselblad X2D 80mm."),

    ("V3_9x16_03_Studio_Orchid_ForestSage_And_WarmPutty_Molded_4K.jpg",
     "Clean 9:16 vertical studio photograph of a Telepathic Instruments Orchid Edition of this exact rectangular Surf Clock standing at a 14-degree angle on a warm cream limestone studio surface: the outer chamfered rectangular casing is molded in muted forest-sage green VDI-24 micro-bead matte polymer with a deep matte charcoal-black recessed rectangular dial cavity, razor-sharp white pad-printed labels, and burnt-orange hands pointing to DEE WHY and YEAH. Soft natural studio daylight."),

    ("V3_9x16_04_Studio_BeadBlasted_Titanium_And_Navy_4K.jpg",
     "Clean 9:16 vertical studio photograph of a Leica/Teenage Engineering Edition of this exact rectangular Surf Clock standing at a 14-degree angle on a dark basalt studio monolith: the outer chamfered rectangular frame is precision CNC bead-blasted satin titanium-silver aluminum, paired with a deep midnight-navy VDI-24 matte recessed rectangular dial face, crisp white silkscreened labels, and burnt-orange pointer hands at DEE WHY and YEAH. Soft studio chiaroscuro lighting."),

    ("V3_9x16_05_Studio_100mm_Macro_UpperDial_CrispPadPrint_4K.jpg",
     "Clean 9:16 vertical 100mm macro studio photograph focusing tightly on the upper dial of this matte midnight-navy Surf Clock. Extreme close-up showing the physical VDI-24 micro-bead injection-molded polymer surface grain, the thick raised matte-white silkscreened ink of 'LONG REEF', 'QUEENSIE', 'DEE WHY', 'FRESHIE', and 'CURL CURL', and the single matte burnt-orange pointer hand with its stepped cylindrical central cap pointing to 'DEE WHY'. Soft natural raking studio light."),

    ("V3_9x16_06_Studio_100mm_Macro_WorthIt_SubDial_4K.jpg",
     "Clean 9:16 vertical 100mm macro studio photograph focusing on the lower 'WORTH IT?' semicircle gauge of this matte midnight-navy Surf Clock. Shows the fine VDI-24 micro-bead molded polymer grain, the pure matte-white silkscreened semicircle arc (zero blue or cyan tint), the crisp white pad-printed 'NAH', 'YEAH', and 'WORTH IT?' labels, and the single short matte burnt-orange pointer hand pointing to 'YEAH'. Soft warm raking studio light."),

    ("V3_9x16_07_Studio_GoldenHour_VenetianBlinds_SlateMonolith_4K.jpg",
     "Clean 9:16 vertical studio photograph of this exact matte midnight-navy Surf Clock standing on a honed slate monolith as warm 4200K late-afternoon sunlight filters through wooden Venetian blinds, casting crisp diagonal warm sunbeams and shadow bands across the slate surface and the VDI-24 micro-textured matte polymer casing. Razor-sharp white pad-printed typography."),

    ("V3_9x16_08_Studio_Rear_Fluted_Borosilicate_WarmDaylight_4K.jpg",
     "Clean 9:16 vertical three-quarter rear studio photograph of this exact matte midnight-navy Surf Clock standing on a honed warm limestone plinth in natural afternoon window light. Shows the deep 52mm chamfered matte midnight-navy VDI-24 molded polymer housing from behind, with a flush-mounted translucent vertical-ribbed fluted borosilicate glass rear cover and a knurled solid brass thumb-turn latch at the top center. Warm natural daylight refraction only, zero blue LEDs."),

    # --- 8 ARTFUL ORCHID / POETRY CAMERA / FLOATING / WALL / TABLETOP 9:16 VERTICAL PLATES ---
    ("V3_9x16_09_Orchid_Wildflower_Meadow_16mm_Vertical_4K.jpg",
     "Artful 9:16 vertical 16mm Kodak Vision3 250D film photograph inspired by the Telepathic Instruments Orchid launch film: the exact matte midnight-navy rectangular Surf Clock stands upright nestled directly among tall sunlit coastal wildflowers—white oxeye daisies, red poppies, and yellow buttercups—at golden hour. Shallow f/2.0 depth of field with soft foreground wildflower petals and razor-sharp focus on the VDI-24 matte polymer dial face."),

    ("V3_9x16_10_PoetryCam_Sunlit_Linen_Picnic_Vertical_4K.jpg",
     "Artful 9:16 vertical 16mm film photograph inspired by Poetry Camera: the exact matte midnight-navy rectangular Surf Clock stands on a rumpled oatmeal linen blanket spread in a sunlit wildflower meadow beside a handmade speckled ceramic cup and fresh chamomile stems. Warm golden afternoon sunlight, organic 16mm film halation, razor-sharp pad-printed dial typography."),

    ("V3_9x16_11_Float_Weightless_Above_Wildflowers_Vertical_4K.jpg",
     "Surreal 9:16 vertical art-house photograph inspired by Telepathic Instruments Orchid: the exact matte midnight-navy rectangular Surf Clock is floating weightlessly in mid-air at a graceful 12-degree tilt, 18 inches above a sunlit meadow of wild daisies and red poppies against a soft pale-blue coastal sky at golden hour. Shot on 35mm film with razor-sharp focus on the crisp white pad-printed dial."),

    ("V3_9x16_12_Float_Brutalist_Sunbeam_Atrium_Vertical_4K.jpg",
     "Surreal 9:16 vertical architectural photograph: the exact matte midnight-navy rectangular Surf Clock levitates weightlessly in mid-air inside a dramatic vertical shaft of warm morning sunlight inside a minimalist Tadao Ando board-formed concrete atrium. Tiny golden dust motes float in the sunbeam around the VDI-24 micro-textured matte polymer casing."),

    ("V3_9x16_13_Wall_Venetian_Plaster_DappledLeaves_Vertical_4K.jpg",
     "Architectural Digest 9:16 vertical photograph: the exact matte midnight-navy rectangular Surf Clock is mounted flush on a warm hand-troweled oatmeal Venetian lime-plaster wall. Warm late-afternoon sunlight filters through olive tree leaves outside a window, casting soft organic dappled leaf shadows across the plaster wall around the clock."),

    ("V3_9x16_14_Wall_Whitewashed_BeachShack_Timber_Vertical_4K.jpg",
     "Architectural Digest 9:16 vertical coastal photograph: the exact matte midnight-navy rectangular Surf Clock is mounted on a sunlit whitewashed vertical timber board wall inside an architect-designed Palm Beach surf house, with a sheer oatmeal linen curtain billowing gently in the morning sea breeze beside it."),

    ("V3_9x16_15_Tabletop_Travertine_CoffeeTable_Vertical_4K.jpg",
     "Architectural Digest 9:16 vertical interior photograph: the exact matte midnight-navy rectangular Surf Clock stands on a thick honed Roman travertine stone coffee table beside a linen-bound art monograph and a stoneware espresso cup in warm morning sunlight."),

    ("V3_9x16_16_Tabletop_Danish_Teak_HiFi_Credenza_Vertical_4K.jpg",
     "Architectural Digest 9:16 vertical gear-porn photograph inspired by Telepathic Instruments Orchid: the exact matte midnight-navy rectangular Surf Clock stands on a vintage 1960s Danish oiled-teak credenza next to the brushed aluminum platter of an audiophile vinyl turntable in warm afternoon window light.")
]

def remove_electric_cyan_and_add_molded_grain(img_bgr, seed=700):
    out = img_bgr.copy()
    h, w = out.shape[:2]
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    cyan_mask = (hue >= 82) & (hue <= 108) & (sat >= 85) & (val >= 145)
    yy, xx = np.mgrid[0:h, 0:w]
    central_box = (yy > int(h * 0.12)) & (yy < int(h * 0.90)) & (xx > int(w * 0.12)) & (xx < int(w * 0.88))
    target = cyan_mask & central_box
    if np.any(target):
        hsv[:, :, 1][target] *= 0.15
        out = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)

    rng = np.random.default_rng(seed)
    fine = rng.standard_normal((h // 2, w // 2)).astype(np.float32)
    fine = cv2.resize(fine, (w, h), interpolation=cv2.INTER_LINEAR)
    fine = cv2.GaussianBlur(fine, (0, 0), 0.55)
    luma = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    mid_weight = 4.0 * luma * (1.0 - luma)
    delta = fine * 2.2 * mid_weight
    out_f = np.clip(out.astype(np.float32) + delta[:, :, None], 0, 255).astype(np.uint8)
    return out_f

def generate_image(out_path, ref_b64, prompt_body, aspect_ratio, target_wh, seed, force=False):
    if not force and os.path.exists(out_path) and os.path.getsize(out_path) > 300_000:
        print(f"[SKIP] {os.path.basename(out_path)}")
        return out_path

    full_prompt = prompt_body + "\n" + STRICT_CLOCK_RULES
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": ref_b64}},
                {"text": full_prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": "4K"
            }
        }
    }

    for attempt in range(4):
        try:
            resp = requests.post(url, json=payload, timeout=180)
            if resp.status_code == 200:
                data = resp.json()
                for cand in data.get("candidates", []):
                    for part in cand.get("content", {}).get("parts", []):
                        if "inlineData" in part:
                            raw_bytes = base64.b64decode(part["inlineData"]["data"])
                            arr = np.frombuffer(raw_bytes, dtype=np.uint8)
                            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                            if img is not None:
                                img_4k = cv2.resize(img, target_wh, interpolation=cv2.INTER_LANCZOS4)
                                img_4k = remove_electric_cyan_and_add_molded_grain(img_4k, seed=seed)
                                cv2.imwrite(out_path, img_4k, [int(cv2.IMWRITE_JPEG_QUALITY), 96])
                                print(f"[GENERATED {aspect_ratio} 4K] {os.path.basename(out_path)} ({os.path.getsize(out_path)/1e6:.2f} MB)")
                                return out_path
            print(f"[WARN {os.path.basename(out_path)}] attempt {attempt+1} status={resp.status_code}")
        except Exception as e:
            print(f"[ERR {os.path.basename(out_path)}] attempt {attempt+1}: {e}")
        time.sleep(3)
    return None

def build_contact_sheets():
    # 1. Rebuild 36-plate 16:9 sheet
    all_16x9 = sorted([f for f in os.listdir(V3_16x9_DIR) if f.startswith("V3_") and f.endswith(".jpg")])
    cols, rows = 6, 6
    tw, th = 640, 360
    sheet16 = np.zeros((rows * th, cols * tw, 3), dtype=np.uint8)
    for i, fname in enumerate(all_16x9[:36]):
        r, c = divmod(i, cols)
        p = os.path.join(V3_16x9_DIR, fname)
        im = cv2.imread(p)
        if im is not None:
            tile = cv2.resize(im, (tw, th), interpolation=cv2.INTER_AREA)
            cv2.putText(tile, fname[:32], (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 220, 120), 1, cv2.LINE_AA)
            sheet16[r*th:(r+1)*th, c*tw:(c+1)*tw] = tile
    s16_path = os.path.join(AUDIT_DIR, "V3_ALL_36_ORCHID_POETRY_KEYFRAMES_SHEET.jpg")
    cv2.imwrite(s16_path, sheet16, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"[UPDATED 16:9 SHEET] {s16_path}")

    # 2. Build 16-plate 9:16 vertical sheet
    cols, rows = 8, 2
    tw, th = 360, 640
    sheet9 = np.zeros((rows * th, cols * tw, 3), dtype=np.uint8)
    for i, (fname, _) in enumerate(VERTICAL_SHOTS):
        r, c = divmod(i, cols)
        p = os.path.join(V3_9x16_DIR, fname)
        if os.path.exists(p):
            im = cv2.imread(p)
            if im is not None:
                tile = cv2.resize(im, (tw, th), interpolation=cv2.INTER_AREA)
                cv2.rectangle(tile, (0, 0), (tw-1, th-1), (40, 40, 40), 1)
                cv2.putText(tile, fname[:24], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 180), 1, cv2.LINE_AA)
                sheet9[r*th:(r+1)*th, c*tw:(c+1)*tw] = tile
    s9_path = os.path.join(AUDIT_DIR, "V3_ALL_16_VERTICAL_9x16_KEYFRAMES_SHEET.jpg")
    cv2.imwrite(s9_path, sheet9, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"[SAVED 9:16 SHEET] {s9_path}")

if __name__ == "__main__":
    # Save MASTER_REF_4K_9x16_CrispBraunMolded.jpg directly as V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg
    # so the hero 9:16 studio plate is 100% vector-perfect!
    cv2.imwrite(os.path.join(V3_9x16_DIR, "V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg"), ref9_img, [int(cv2.IMWRITE_JPEG_QUALITY), 96])
    print("[SAVED CLEAN MASTER REF 9x16 4K] V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg")

    tasks = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for idx, (fn, pr) in enumerate(FIX_16x9_SHOTS):
            out_p = os.path.join(V3_16x9_DIR, fn)
            tasks.append(ex.submit(generate_image, out_p, REF16_B64, pr, "16:9", (3840, 2160), 750 + idx, True))
        for idx, (fn, pr) in enumerate(VERTICAL_SHOTS[1:], start=1):
            out_p = os.path.join(V3_9x16_DIR, fn)
            tasks.append(ex.submit(generate_image, out_p, REF9_B64, pr, "9:16", (2160, 3840), 800 + idx, False))
        for fut in as_completed(tasks):
            fut.result()

    build_contact_sheets()
