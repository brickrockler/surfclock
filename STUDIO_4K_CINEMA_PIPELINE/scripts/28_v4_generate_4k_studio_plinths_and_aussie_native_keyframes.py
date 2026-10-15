#!/usr/bin/env python3
"""
V4 STAGE 1:
1. Cleans the 3 false bottom ticks (5, 6, 7 o'clock) across all retained studio/cream/tabletop 4K keyframes
   so the dial marks strictly stop at FRESHIE (8 o'clock) and CURL CURL (4 o'clock) (9 ticks total on upper dial).
2. Generates 24 brand-new native 4K keyframes with gemini-3-pro-image-preview (Nano Banana Pro):
   - 10 Clean Industrial Design Studio & Plinth shots (White Studio Plinths, Raw Travertine Block, Aluminum Cube,
     Fluted Concrete, Blackbutt Timber Tabletop, Dappled Cream Limestone, and Dark Slate-Blue Studio Plinths)
   - 8 Authentic Australian Surf Culture & Native Flora Outdoor shots (Golden Billy Buttons / Craspedia,
     Native Kangaroo Grass, Coastal Spinifex & Pigface on Northern Beaches sand dunes, Banksia serrata cones on
     Hawkesbury sandstone, Vintage Twin-Fin Surfboard in coastal tussock grass, 80s Aussie Troopy tailgate, etc.)
   - 6 Native 9:16 Vertical Studio Plinth & Australian Native Flora 4K keyframes.
3. Automatically runs clean_bottom_3_ticks_auto() and remove_electric_cyan_highlights() on every 4K keyframe.
"""

import os
import json
import time
import base64
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np

PIPE_DIR = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
STILLS_ROOT = PIPE_DIR / "01_4K_STUDIO_KEYFRAMES_AND_STILLS"
V3_16x9_DIR = STILLS_ROOT / "V3_ORCHID_POETRY_ARCHDIGEST_4K"
V3_9x16_DIR = STILLS_ROOT / "V3_9x16_VERTICAL_STUDIO_AND_ORCHID_4K"
V4_16x9_DIR = STILLS_ROOT / "V4_ACCURATE_STUDIO_AND_AUSSIE_4K_16x9"
V4_9x16_DIR = STILLS_ROOT / "V4_ACCURATE_STUDIO_AND_AUSSIE_4K_9x16"
AUDIT_DIR   = PIPE_DIR / "04_CONTACT_SHEETS_AND_AUDIT"

for d in [V4_16x9_DIR, V4_9x16_DIR, AUDIT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

GEMINI_KEY = Path("~/.config/pickleball-coach/gemini.key").expanduser().read_text().strip()
MASTER_16x9_PATH = V3_16x9_DIR / "MASTER_REF_4K_16x9_CrispBraunMolded.jpg"
MASTER_9x16_PATH = V3_16x9_DIR / "MASTER_REF_4K_9x16_CrispBraunMolded.jpg"


def remove_electric_cyan_highlights(img: np.ndarray) -> np.ndarray:
    out = img.astype(np.float32)
    b, g, r = out[:, :, 0], out[:, :, 1], out[:, :, 2]
    cyan_excess = np.maximum(0.0, np.minimum(b, g) - r - 38.0)
    mask = np.clip((cyan_excess - 10.0) / 35.0, 0.0, 1.0)
    neutral = (0.25 * b + 0.40 * g + 0.35 * r)
    out[:, :, 0] = b * (1.0 - 0.75 * mask) + neutral * (0.75 * mask)
    out[:, :, 1] = g * (1.0 - 0.80 * mask) + neutral * (0.80 * mask)
    out[:, :, 2] = r * (1.0 - 0.65 * mask) + neutral * (0.65 * mask)
    return np.clip(out, 0, 255).astype(np.uint8)


def clean_bottom_3_ticks_auto(img_bgr: np.ndarray) -> np.ndarray:
    """
    Locates the upper orange pointer hand sitting on the dark slate-blue dial and automatically removes
    any false tick marks in the bottom 5, 6, and 7 o'clock zone below FRESHIE and CURL CURL.
    """
    out = img_bgr.copy()
    h, w = out.shape[:2]
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV)
    y_lo, y_hi = int(h * 0.10), int(h * 0.65)
    x_lo, x_hi = int(w * 0.15), int(w * 0.85)
    roi_hsv = hsv[y_lo:y_hi, x_lo:x_hi]
    omask = cv2.inRange(roi_hsv, np.array([3, 120, 95]), np.array([22, 255, 255]))
    n_lbl, lbls, stats, _ = cv2.connectedComponentsWithStats(omask)
    if n_lbl <= 1:
        return out

    best_i = -1
    best_area = 0
    for i in range(1, n_lbl):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < 160 or area > 45000:
            continue
        cx_box = x_lo + stats[i, cv2.CC_STAT_LEFT]
        cy_box = y_lo + stats[i, cv2.CC_STAT_TOP]
        cw_box = stats[i, cv2.CC_STAT_WIDTH]
        ch_box = stats[i, cv2.CC_STAT_HEIGHT]
        pad_b = out[max(0, cy_box - 25):min(h, cy_box + ch_box + 25), max(0, cx_box - 25):min(w, cx_box + cw_box + 25)]
        med_b = float(np.median(pad_b[:, :, 0]))
        med_r = float(np.median(pad_b[:, :, 2]))
        if med_b > med_r + 4.0 and med_r < 105.0 and area > best_area:
            best_area = area
            best_i = i

    if best_i < 0:
        return out

    hand_mask = (lbls == best_i).astype(np.uint8) * 255
    dist = cv2.distanceTransform(hand_mask, cv2.DIST_L2, 5)
    _, _, _, max_loc = cv2.minMaxLoc(dist)
    hub_cx = x_lo + max_loc[0]
    hub_cy = y_lo + max_loc[1]

    ys, xs = np.where(hand_mask > 0)
    pts_x = x_lo + xs
    pts_y = y_lo + ys
    needle_len = float(np.percentile(np.hypot(pts_x - hub_cx, pts_y - hub_cy), 99.0))
    if needle_len > 380.0 or hub_cy + 1.35 * needle_len >= h - 20:
        return out

    bx1 = max(20, int(round(hub_cx - 0.72 * needle_len)))
    bx2 = min(w - 20, int(round(hub_cx + 0.72 * needle_len)))
    by1 = max(20, int(round(hub_cy + 0.45 * needle_len)))
    by2 = min(h - 20, int(round(hub_cy + 1.25 * needle_len)))
    if bx2 <= bx1 + 20 or by2 <= by1 + 20:
        return out

    sub = out[by1:by2, bx1:bx2]
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.medianBlur(gray.astype(np.uint8), 31).astype(np.float32)
    tick_cand = ((gray - bg > 16.0) & (bg < 125.0)).astype(np.uint8) * 255
    nt, tlbl, tstats, _ = cv2.connectedComponentsWithStats(tick_cand)
    clean_mask = np.zeros_like(tick_cand)
    for ti in range(1, nt):
        area = tstats[ti, cv2.CC_STAT_AREA]
        tw = tstats[ti, cv2.CC_STAT_WIDTH]
        th = tstats[ti, cv2.CC_STAT_HEIGHT]
        if 8 <= area <= 950 and tw < 42 and th < 55:
            clean_mask[tlbl == ti] = 255

    if np.count_nonzero(clean_mask) == 0:
        return out

    clean_mask = cv2.dilate(clean_mask, np.ones((9, 9), np.uint8), iterations=1)
    inp = cv2.inpaint(sub, clean_mask, 9, cv2.INPAINT_TELEA)
    inp_blur = cv2.GaussianBlur(inp, (7, 7), 1.6)
    rng = np.random.default_rng(hub_cx + hub_cy)
    grain = rng.standard_normal(sub.shape[:2]).astype(np.float32) * 1.8
    patched = np.clip(inp_blur.astype(np.float32) + grain[..., None], 0, 255)
    mf = cv2.GaussianBlur(clean_mask.astype(np.float32) / 255.0, (7, 7), 1.5)[..., None]
    out[by1:by2, bx1:bx2] = np.clip(sub.astype(np.float32) * (1.0 - mf) + patched * mf, 0, 255).astype(np.uint8)
    return out


# Step 1: Curate & clean the best existing Studio / Sunlit Cream / Tabletop / Macro keyframes into V4_16x9_DIR & V4_9x16_DIR
CURATED_V3_16x9 = [
    ("V3_15_Wall_Mounted_Warm_Venetian_Plaster_Dappled_Sunlight_4K.jpg", "V4_CREAM_01_Venetian_Plaster_Wall_Dappled_Sunlight_4K.jpg"),
    ("V3_17_Wall_Mounted_Breezy_Beach_Shack_Linen_Curtains_16mm_4K.jpg", "V4_CREAM_02_Beach_House_Wall_Billowing_Linen_Curtains_4K.jpg"),
    ("V3_20_Wall_Mounted_Gallery_Limestone_Wall_ThreeQuarter_4K.jpg",    "V4_CREAM_03_Warm_Limestone_Gallery_Wall_ThreeQuarter_4K.jpg"),
    ("V3_21_Table_Roman_Travertine_CoffeeTable_Espresso_ArtBooks_4K.jpg","V4_CREAM_04_Roman_Travertine_CoffeeTable_Espresso_Monographs_4K.jpg"),
    ("V3_25_Table_Architects_Oak_Desk_Brass_Lamp_And_Sketches_4K.jpg",   "V4_CREAM_05_Architects_Oak_Workbench_Warm_Morning_4K.jpg"),
    ("V3_26_Table_Calacatta_Viola_Marble_Plinth_Warm_Morning_4K.jpg",    "V4_CREAM_06_Calacatta_Marble_Studio_Plinth_Morning_4K.jpg"),
    ("V3_28_Table_Warm_Limestone_Bedside_Linen_Morning_Ritual_4K.jpg",   "V4_CREAM_07_Warm_Limestone_Tabletop_Morning_Light_4K.jpg"),
    ("V3_29_Studio_Signature_Clean_SlateBlue_Chiaroscuro_4K.jpg",        "V4_STUDIO_00_Signature_SlateBlue_Cyclorama_Hero_4K.jpg"),
    ("V3_33_Macro_100mm_UpperDial_Tactile_Braun_Molded_Plastic_4K.jpg",  "V4_MACRO_01_100mm_Upper_9Tick_BeachDial_BraunMolded_4K.jpg"),
    ("V3_34_Macro_100mm_LowerWorthIt_Tactile_Braun_Molded_Plastic_4K.jpg","V4_MACRO_02_100mm_Lower_WorthIt_Semicircle_BraunMolded_4K.jpg"),
    ("V3_35_Macro_85mm_GrazingBevel_Tactile_Molded_In_GoldenSunlight_4K.jpg","V4_MACRO_03_85mm_Grazing_Bevel_And_Typography_4K.jpg"),
    ("V3_36_Macro_Rear_Fluted_Borosilicate_In_Warm_WindowLight_4K.jpg",  "V4_MACRO_04_Rear_Fluted_Translucent_BackCover_4K.jpg"),
]

CURATED_V3_9x16 = [
    ("V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg",     "V4_9x16_00_Studio_SlateBlue_Cyclorama_Hero_Vertical_4K.jpg"),
    ("V3_9x16_05_Studio_100mm_Macro_UpperDial_CrispPadPrint_4K.jpg",   "V4_9x16_07_Macro_100mm_Upper_9Tick_Dial_Vertical_4K.jpg"),
    ("V3_9x16_06_Studio_100mm_Macro_WorthIt_SubDial_4K.jpg",           "V4_9x16_08_Macro_100mm_Lower_WorthIt_Vertical_4K.jpg"),
    ("V3_9x16_08_Studio_Rear_Fluted_Borosilicate_WarmDaylight_4K.jpg", "V4_9x16_09_Studio_Rear_Fluted_Translucent_Vertical_4K.jpg"),
    ("V3_9x16_13_Wall_Venetian_Plaster_DappledLeaves_Vertical_4K.jpg", "V4_9x16_10_Cream_Venetian_Plaster_DappledLeaves_Vertical_4K.jpg"),
    ("V3_9x16_14_Wall_Whitewashed_BeachShack_Timber_Vertical_4K.jpg",  "V4_9x16_11_Cream_BeachHouse_Wall_Linen_Vertical_4K.jpg"),
    ("V3_9x16_15_Tabletop_Travertine_CoffeeTable_Vertical_4K.jpg",     "V4_9x16_12_Cream_Travertine_CoffeeTable_Vertical_4K.jpg"),
]

for src_name, dst_name in CURATED_V3_16x9:
    sp = V3_16x9_DIR / src_name
    dp = V4_16x9_DIR / dst_name
    if sp.exists():
        im = cv2.imread(str(sp))
        im_clean = clean_bottom_3_ticks_auto(remove_electric_cyan_highlights(im))
        cv2.imwrite(str(dp), im_clean, [cv2.IMWRITE_JPEG_QUALITY, 97])
        # Also update V3 in-place so all references are 9-tick clean
        cv2.imwrite(str(sp), im_clean, [cv2.IMWRITE_JPEG_QUALITY, 97])

for src_name, dst_name in CURATED_V3_9x16:
    sp = V3_9x16_DIR / src_name
    dp = V4_9x16_DIR / dst_name
    if sp.exists():
        im = cv2.imread(str(sp))
        im_clean = clean_bottom_3_ticks_auto(remove_electric_cyan_highlights(im))
        cv2.imwrite(str(dp), im_clean, [cv2.IMWRITE_JPEG_QUALITY, 97])
        cv2.imwrite(str(sp), im_clean, [cv2.IMWRITE_JPEG_QUALITY, 97])

print(f"[CURATED & 9-TICK CLEANED] {len(CURATED_V3_16x9)} 16:9 and {len(CURATED_V3_9x16)} 9:16 existing keyframes.")

# Step 2: Generate the 24 Brand-New 4K Keyframes (Clean White/Dark-Blue Studio Plinths + Australian Native Flora Surf Culture)
ACCURATE_PRODUCT_LOCK = (
    "CRITICAL PRODUCT ACCURACY RULES (DO NOT VIOLATE): "
    "Keep the EXACT upright 3:4 rectangular matte slate-blue/midnight-navy Braun/Orchid molded Surf Instrument from the reference image. "
    "1. STRICTLY TWO HANDS TOTAL: ONE single burnt-orange pointer hand on the upper beach dial (pointing to DEE WHY at 2 o'clock), "
    "and ONE single short burnt-orange pointer hand on the lower WORTH IT? semicircle gauge (pointing to YEAH). NEVER add a second hand on the upper dial! "
    "2. DIAL MARKS STOP AT FRESHIE (8 o'clock) AND CURL CURL (4 o'clock): The upper dial has ONLY 9 white radial tick marks in the upper arc "
    "(8, 9, 10, 11, 12, 1, 2, 3, 4 o'clock). There are ZERO tick marks at 5 o'clock, 6 o'clock, or 7 o'clock — the bottom third of the upper dial "
    "between FRESHIE and CURL CURL is 100% blank matte navy dial surface! "
    "3. OPEN MATTE STEPPED BEZEL: ZERO glass cover over the front face, ZERO glowing blue LEDs, ZERO electric cyan highlights. "
    "Tactile VDI-24 micro-bead matte injection-molded Braun / Teenage Engineering finish with razor-sharp white pad-printed typography "
    "(LONG REEF, QUEENSIE, DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT?)."
)

NEW_V4_KEYFRAME_JOBS = [
    # --- PILLAR A: CLEAN INDUSTRIAL DESIGN STUDIO PLINTHS & TABLETOPS (MIX OF WHITE STUDIO & DARK BLUE STUDIO) ---
    ("V4_STUDIO_01_WhiteStudio_Monolithic_ChalkPlinth_16x9_4K.jpg", "16:9",
     "Ultra-clean industrial design studio product photography (Dieter Rams Braun / Teenage Engineering / Vitsoe catalog aesthetic). "
     "The matte slate-blue rectangular Surf Instrument stands upright on a monolithic matte chalk-white architectural plinth inside a pure, bright white seamless studio cyclorama. "
     "Soft overhead diffused scrim lighting with a gentle warm-daylight key light from the left casting a clean, soft architectural shadow across the white plinth. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_02_WhiteStudio_Raw_RomanTravertine_Plinth_16x9_4K.jpg", "16:9",
     "Ultra-clean industrial design studio photography in a bright white seamless cyclorama studio. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a raw, porous honed cream Roman travertine stone block plinth set inside a pure white photography studio. "
     "Crisp studio key lighting highlights the contrast between the porous warm travertine stone texture and the ultra-clean matte slate-blue molded Braun housing. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_03_WhiteStudio_BeadBlasted_Aluminum_Cube_16x9_4K.jpg", "16:9",
     "High-end industrial design film still in a pure white studio setting (Teenage Engineering / Leica studio look). "
     "The matte slate-blue rectangular Surf Instrument stands upright on a solid CNC-machined bead-blasted silver anodized aluminum plinth block against a clean white studio backdrop. "
     "Precise studio rim and key lighting with subtle matte metallic reflection on the aluminum block surface. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_04_WhiteStudio_Fluted_Architectural_Concrete_Plinth_16x9_4K.jpg", "16:9",
     "Minimalist industrial design studio photography. The matte slate-blue rectangular Surf Instrument stands upright on a raw fluted pale-grey architectural concrete pedestal inside a bright warm-white studio cyclorama. "
     "Soft angled studio sunlight creates delicate shadow geometry across the fluted concrete plinth and matte slate-blue bezel. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_05_WhiteStudio_Australian_Blackbutt_Timber_Tabletop_16x9_4K.jpg", "16:9",
     "Clean industrial design studio tabletop photography. The matte slate-blue rectangular Surf Instrument rests upright on a smooth, natural matte-oiled Australian Blackbutt timber studio tabletop against a pure warm-white seamless studio backdrop. "
     "Bright, airy studio lighting with natural wood grain texture and crisp product focus. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_06_CreamStudio_Dappled_Eucalyptus_Limestone_Plinth_16x9_4K.jpg", "16:9",
     "Sunlit studio photography on a honed warm cream limestone plinth in front of a warm cream Venetian plaster studio wall. "
     "Natural morning sunlight filters through studio gobos, casting soft, artful dappled tree-leaf shadows across the cream limestone plinth and warm cream background wall while the matte slate-blue Surf Instrument stands crisp and legible in the center. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_07_DarkBlueStudio_Honed_Basalt_Plinth_Chiaroscuro_16x9_4K.jpg", "16:9",
     "Dramatic industrial design studio photography in a dark slate-blue seamless cyclorama studio. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a dark honed charcoal-basalt stone plinth against a deep midnight slate-blue studio backdrop. "
     "A sculpted diagonal shaft of warm-neutral studio key light illuminates the clock face and tactile basalt plinth texture with rich chiaroscuro contrast. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_08_DarkBlueStudio_Cleft_Slate_Tabletop_16x9_4K.jpg", "16:9",
     "High-end studio tabletop gear-porn photography against a dark slate-blue studio background. "
     "The matte slate-blue rectangular Surf Instrument rests upright on a tactile, natural cleft dark-slate stone studio surface with subtle raking side light that reveals the fine VDI-24 molded polymer grain and raised white pad-printed dial markings. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_09_DarkBlueStudio_Brushed_Steel_Plinth_16x9_4K.jpg", "16:9",
     "Luxury industrial design studio photography. The matte slate-blue rectangular Surf Instrument stands upright on a dark brushed gunmetal-steel studio plinth against a deep slate-blue seamless cyclorama with a soft, cinematic pool of overhead studio light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_STUDIO_10_WhiteStudio_Terrazzo_And_Cork_Tabletop_16x9_4K.jpg", "16:9",
     "Clean studio tabletop photography in a bright white industrial design studio. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a matte honed warm limestone-terrazzo slab resting on a natural cork studio block against a clean white cyclorama background. " + ACCURATE_PRODUCT_LOCK),

    # --- PILLAR B: AUTHENTIC AUSTRALIAN SURF CULTURE & NATIVE AUSTRALIAN FLORA (16MM FILM & CAMCORDER VIBE) ---
    ("V4_AUSSIE_01_Golden_BillyButtons_And_KangarooGrass_Headland_16mm_16x9_4K.jpg", "16:9",
     "Authentic Australian coastal surf-culture cinematography shot on Kodak Vision3 250D 16mm film (Poetry Camera / Telepathic Instruments Orchid Australian aesthetic, natural 16mm film grain and subtle halation). "
     "The matte slate-blue rectangular Surf Instrument rests naturally on weathered Sydney Hawkesbury sandstone among vibrant golden-yellow spherical Australian Billy Buttons wildflowers (Craspedia / Pycnosorus globosus) and bronze-green Native Kangaroo Grass (Themeda triandra) on a sunlit Northern Beaches headland, with soft out-of-focus turquoise ocean swell lines breaking in the background. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_02_NorthernBeaches_Dune_Spinifex_And_Pigface_Camcorder_16x9_4K.jpg", "16:9",
     "Authentic Australian surf-culture photography shot on 16mm film / vintage camcorder optics at dawn patrol. "
     "The matte slate-blue rectangular Surf Instrument rests naturally on pale golden Australian coastal sand dunes among silvery-green coastal Spinifex grass runners (Spinifex sericeus) and succulent Australian coastal Pigface (Carpobrotus glaucescens) with magenta-pink native blooms, backlit by warm early-morning golden surf-check sunlight. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_03_BanksiaSerrata_And_Lomandra_HawkesburySandstone_16mm_16x9_4K.jpg", "16:9",
     "Artful Australian bush-meets-surf photography shot on 16mm Kodak film with organic grain and dappled morning light. "
     "The matte slate-blue rectangular Surf Instrument rests on a warm ochre Hawkesbury sandstone rock shelf surrounded by sculptural native Australian coastal Banksia serrata seed cones, spiky green Lomandra longifolia mat-rush grass, and fallen eucalyptus gum leaves overlooking the coast. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_04_TwinFin_Surfboard_And_BillyButtons_In_TussockGrass_16mm_16x9_4K.jpg", "16:9",
     "Nostalgic Australian surf culture 16mm film frame at golden hour. "
     "The matte slate-blue rectangular Surf Instrument rests on a sun-faded oatmeal canvas surf towel in native Australian coastal tussock grass (Poa poiformis) and yellow spherical Billy Buttons (Craspedia), right beside the waxed nose of a vintage cream fiberglass twin-fin surfboard and a block of surf wax. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_05_80s_Aussie_Troopy_SurfWagon_Tailgate_Headland_Camcorder_16x9_4K.jpg", "16:9",
     "Authentic Australian surf culture 16mm film / camcorder frame. "
     "The matte slate-blue rectangular Surf Instrument sits upright on the weathered timber-and-steel tailgate of a classic sand-beige 1980s Australian 4WD Troopy surf wagon parked at a Northern Beaches headland look-out, beside a battered stainless-steel thermos and surf wax, with native golden Billy Buttons and coastal tea-tree (Leptospermum) in the sunlit background bokeh. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_06_Paperbark_And_CoastalWattle_BushTrack_16mm_16x9_4K.jpg", "16:9",
     "Australian coastal bush-track surf check shot on 16mm Kodak Vision3 film. "
     "The matte slate-blue rectangular Surf Instrument rests on a sun-bleached grey hardwood fence post along a sandy beach-access track, framed by peeling papery white Melaleuca paperbark trees, native golden Australian coastal wattle (Acacia sophorae), and native grasses in dappled morning sun. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_07_Sandstone_Rockpool_Shelf_And_Pandanus_16mm_16x9_4K.jpg", "16:9",
     "Australian East Coast surf culture 16mm film photography. "
     "The matte slate-blue rectangular Surf Instrument rests on a dry, warm honey-toned sandstone rock ledge above an Australian ocean rockpool at low tide, with native coastal Pandanus leaves and golden Billy Buttons swaying in the sunlit foreground bokeh. " + ACCURATE_PRODUCT_LOCK),

    ("V4_AUSSIE_08_Fibro_BeachShack_Verandah_Eucalyptus_Dappled_16mm_16x9_4K.jpg", "16:9",
     "Nostalgic Australian coastal fibro beach-shack verandah shot on 16mm film at morning surf check. "
     "The matte slate-blue rectangular Surf Instrument rests on a weathered tallowwood timber verandah rail in warm dappled eucalyptus leaf sunlight, with a vintage fiberglass surfboard tail leaning against cream weatherboards in the soft background bokeh. " + ACCURATE_PRODUCT_LOCK),

    # --- NATIVE 9:16 VERTICAL STUDIO PLINTHS & AUSTRALIAN NATIVE FLORA ---
    ("V4_9x16_01_WhiteStudio_Monolithic_ChalkPlinth_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical ultra-clean industrial design studio photography. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a monolithic matte chalk-white gallery plinth inside a pure bright-white studio cyclorama with soft overhead scrim light and crisp shadow falloff. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_02_WhiteStudio_Raw_Travertine_Plinth_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical industrial design studio photography. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a raw porous cream Roman travertine stone plinth block inside a pure white photography studio with warm angled key light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_03_DarkBlueStudio_Honed_Basalt_Plinth_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical dark studio photography. "
     "The matte slate-blue rectangular Surf Instrument stands upright on a dark honed charcoal-basalt stone plinth against a deep slate-blue seamless studio cyclorama with a sculpted diagonal shaft of studio key light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_04_Aussie_Golden_BillyButtons_And_KangarooGrass_16mm_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical Australian coastal surf-culture 16mm film frame. "
     "The matte slate-blue rectangular Surf Instrument rests on weathered Hawkesbury sandstone among golden-yellow spherical Australian Billy Buttons wildflowers (Craspedia) and bronze-green Native Kangaroo Grass on a sunlit headland overlooking the surf. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_05_Aussie_NorthernBeaches_Spinifex_Dune_Camcorder_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical Australian surf-culture 16mm / camcorder frame. "
     "The matte slate-blue rectangular Surf Instrument rests on pale golden Northern Beaches sand dunes among silvery-green coastal Spinifex grass runners and native Australian coastal Pigface in golden morning light. " + ACCURATE_PRODUCT_LOCK),

    ("V4_9x16_06_Aussie_Banksia_And_Sandstone_Headland_16mm_Vertical_4K.jpg", "9:16",
     "Native 9:16 vertical Australian coastal 16mm film photography. "
     "The matte slate-blue rectangular Surf Instrument rests on a warm sandstone rock ledge surrounded by sculptural native Australian Banksia serrata cones, Lomandra grass, and dappled eucalyptus shade. " + ACCURATE_PRODUCT_LOCK),
]

B64_MASTER_16x9 = base64.b64encode(MASTER_16x9_PATH.read_bytes()).decode("utf-8")
B64_MASTER_9x16 = base64.b64encode(MASTER_9x16_PATH.read_bytes()).decode("utf-8")


def generate_one_v4_keyframe(idx: int, job_tuple: tuple) -> str:
    out_name, aspect, prompt = job_tuple
    out_dir = V4_16x9_DIR if aspect == "16:9" else V4_9x16_DIR
    out_path = out_dir / out_name
    if out_path.exists() and out_path.stat().st_size > 400_000:
        print(f"[SKIP EXISTING 4K] {out_name}", flush=True)
        return str(out_path)

    time.sleep((idx % 6) * 1.2)
    ref_b64 = B64_MASTER_16x9 if aspect == "16:9" else B64_MASTER_9x16
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": ref_b64}},
                {"text": prompt},
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect,
                "imageSize": "4K",
            }
        }
    }

    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=150) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in parts:
                if "inlineData" in p and "data" in p["inlineData"]:
                    raw_bytes = base64.b64decode(p["inlineData"]["data"])
                    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
                    im = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    if im is not None:
                        target_wh = (3840, 2160) if aspect == "16:9" else (2160, 3840)
                        if (im.shape[1], im.shape[0]) != target_wh:
                            im = cv2.resize(im, target_wh, interpolation=cv2.INTER_LANCZOS4)
                        im = remove_electric_cyan_highlights(im)
                        im = clean_bottom_3_ticks_auto(im)
                        cv2.imwrite(str(out_path), im, [cv2.IMWRITE_JPEG_QUALITY, 97])
                        print(f"[GENERATED V4 4K] {out_name} ({out_path.stat().st_size/1e6:.2f} MB)", flush=True)
                        return str(out_path)
        except Exception as e:
            print(f"[WARN {out_name}] attempt {attempt+1}: {e}", flush=True)
            time.sleep(4 * (attempt + 1))
    raise RuntimeError(f"Failed to generate {out_name}")


if __name__ == "__main__":
    print(f"Launching parallel generation of {len(NEW_V4_KEYFRAME_JOBS)} V4 4K Studio Plinth & Australian Native Surf Culture Keyframes...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(generate_one_v4_keyframe, i, job): job[0] for i, job in enumerate(NEW_V4_KEYFRAME_JOBS)}
        for f in as_completed(futs):
            name = futs[f]
            try:
                f.result()
            except Exception as exc:
                print(f"[ERR {name}] {exc}", flush=True)
    print("ALL V4 4K KEYFRAMES COMPLETE!")
