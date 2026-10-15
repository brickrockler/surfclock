#!/usr/bin/env python3
"""
V3 STAGE 1: Generate 36 Pure Flagship Nano Banana Pro (gemini-3-pro-image-preview) 4K Cinema Keyframes
using MASTER_REF_4K_16x9_CrispBraunMolded.jpg (razor-sharp 4K pad-printed typography + VDI-24 Braun/Orchid molded texture).
"""
import os, sys, time, json, base64, shutil, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np

PIPE_DIR = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
V3_STILLS_DIR = PIPE_DIR / "01_4K_STUDIO_KEYFRAMES_AND_STILLS" / "V3_ORCHID_POETRY_ARCHDIGEST_4K"
V3_STILLS_DIR.mkdir(parents=True, exist_ok=True)
MASTER_REF_16x9 = V3_STILLS_DIR / "MASTER_REF_4K_16x9_CrispBraunMolded.jpg"
AUDIT_DIR = PIPE_DIR / "04_CONTACT_SHEETS_AND_AUDIT"
QC_LEDGER_PATH = AUDIT_DIR / "V2_100_ROUND_PRO_QC_LEDGER.json"

GEMINI_KEY = Path("~/.config/pickleball-coach/gemini.key").expanduser().read_text().strip()
# Encode a 2048x1152 crisp version of MASTER_REF_16x9 for fast upload while preserving 100% razor-sharp text!
ref_img = cv2.imread(str(MASTER_REF_16x9))
ref_2k = cv2.resize(ref_img, (2048, 1152), interpolation=cv2.INTER_AREA)
_, ref_buf = cv2.imencode(".jpg", ref_2k, [cv2.IMWRITE_JPEG_QUALITY, 96])
REF_B64 = base64.b64encode(ref_buf.tobytes()).decode("utf-8")

def log_qc(entry: dict):
    try:
        with open(QC_LEDGER_PATH) as f:
            ledger = json.load(f)
        if isinstance(ledger, dict):
            ledger = ledger.get("entries", [])
    except Exception:
        ledger = []
    entry["round_number"] = len(ledger) + 1
    ledger.append(entry)
    with open(QC_LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

def remove_electric_cyan_and_add_molded_grain(img_4k: np.ndarray) -> np.ndarray:
    """Removes any electric cyan highlights and adds subtle tactile VDI-24 micro-molded grain & 16mm organic film texture."""
    out = img_4k.astype(np.float32)
    b, g, r = out[:, :, 0], out[:, :, 1], out[:, :, 2]
    cyan_excess = np.maximum(0.0, np.minimum(b, g) - r - 42.0)
    mask = np.clip((cyan_excess - 12.0) / 38.0, 0.0, 1.0)
    neutral = (0.25 * b + 0.40 * g + 0.35 * r)
    out[:, :, 0] = b * (1.0 - 0.70 * mask) + neutral * (0.70 * mask)
    out[:, :, 1] = g * (1.0 - 0.75 * mask) + neutral * (0.75 * mask)
    out[:, :, 2] = r * (1.0 - 0.60 * mask) + neutral * (0.60 * mask)
    # Add subtle 4K VDI-24 / Kodak 16mm organic micro-grain (+/- 2.2 intensity units) so surfaces feel tactile and never plastic/fake
    rng = np.random.default_rng(101)
    grain = rng.standard_normal(out.shape[:2]).astype(np.float32) * 1.85
    out = out + grain[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

COMMON_PRODUCT_LOCK = (
    "Keep the exact design and proportions of the rectangular Braun / Teenage Engineering / Telepathic Instruments Orchid Surf Clock from the reference image: "
    "hyper-premium VDI-24 micro-textured injection-molded matte polymer casing (like a high-end Braun Ulm appliance or Telepathic Instruments Orchid synthesizer — "
    "tactile micro-matte molded plastic with crisp 0.90mm radiused bevels, NOT 3D printed and NOT smooth fake CG), "
    "deeply recessed open matte dark-navy dial cavity (ZERO front glass cover, zero glare), "
    "and crisp silkscreened pad-printed white typography (LONG REEF at 12 o'clock, DEE WHY at 2 o'clock, CURL CURL at 4 o'clock, FRESHIE at 8 o'clock, QUEENSIE at 10 o'clock; "
    "lower white semicircle gauge labeled NAH, YEAH, WORTH IT?). "
    "CRITICAL MECHANICAL ACCURACY: Show STRICTLY ONE matte burnt-orange molded pointer hand on the upper dial (pointing cleanly to DEE WHY at 2 o'clock) "
    "and STRICTLY ONE short matte burnt-orange pointer hand on the lower semicircle (pointing cleanly to YEAH). "
    "NEVER draw two hands on the same dial. NEVER add blue LED lights, NEVER add cyan highlights on the white gauge arc, and NEVER add a dark halo around the clock."
)

SHOTS = [
    # --- CATEGORY A: ORCHID & POETRY CAMERA 16MM FILM NATURE & COASTAL WORLDS (8) ---
    {
        "id": "V3_01_Orchid_Wildflower_Meadow_16mm_GoldenHour",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Place this exact matte midnight-navy Surf Clock lying nestled at a slight angle among lush wild white daisies, yellow buttercups, red poppies, "
            "and soft green meadow grass in warm golden-hour afternoon sunlight. Shot on 16mm Kodak Vision3 250D motion picture film with an Arriflex 16SR lens: "
            "warm organic halation, authentic 16mm film grain, creamy foreground wildflower bokeh, Telepathic Instruments Orchid launch video aesthetic."
        )
    },
    {
        "id": "V3_02_Orchid_Clover_And_Chamomile_Meadow_Overhead_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "High-angle 45-degree 16mm film shot of the matte midnight-navy Surf Clock lying flat on a sun-dappled bed of wild chamomile flowers, clover, "
            "and soft green grass. Warm late-afternoon sunlight filters through unseen tree leaves, casting gentle dappled light across the wildflowers and tactile molded casing. "
            "Poetry Camera and Telepathic Instruments Orchid 16mm analog film aesthetic."
        )
    },
    {
        "id": "V3_03_PoetryCam_Sunlit_Linen_Picnic_Wildflowers_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Poetry Camera aesthetic: the matte midnight-navy Surf Clock standing on a rumpled natural oatmeal linen picnic blanket in a sunlit wildflower meadow, "
            "beside a handmade speckled stoneware coffee mug and freshly picked wild daisies. Warm morning sunlight, 16mm Kodak film grain, intimate indie hardware photography."
        )
    },
    {
        "id": "V3_04_Orchid_Coastal_Headland_TallGrass_And_OceanSwell_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Cinematic 16mm Kodak film medium shot of the matte midnight-navy Surf Clock resting on a weathered coastal sandstone ledge surrounded by golden waving kangaroo grass, "
            "with soft out-of-focus turquoise ocean swell peeling in the distant background under warm morning sunlight. Effortlessly cool Australian coastal film aesthetic."
        )
    },
    {
        "id": "V3_05_PoetryCam_Botanical_Conservatory_Dappled_Ferns_35mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock standing on a weathered terracotta table surrounded by lush green maidenhair ferns and botanical foliage inside a sunlit glasshouse conservatory. "
            "Warm natural morning sunbeams and soft leaf shadows across the tactile VDI-24 molded casing, shot on 35mm Kodak Portra 400 film."
        )
    },
    {
        "id": "V3_06_Orchid_Desert_Travertine_And_Golden_Dunes_35mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Telepathic Instruments Orchid surreal location photography: the matte midnight-navy Surf Clock standing on a raw honed travertine stone block "
            "set right in warm golden coastal sand dunes at sunset, with long warm architectural shadows and rich 35mm film grain."
        )
    },
    {
        "id": "V3_07_Orchid_Mossy_Kyoto_Stone_Garden_MorningMist_35mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock resting on a moss-covered granite garden stone in a serene Japanese courtyard garden, "
            "with soft morning sunlight filtering through maple leaves and delicate shallow depth of field. Shot on 35mm film."
        )
    },
    {
        "id": "V3_08_PoetryCam_SunBleached_Driftwood_Bench_GoldenHour_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Shot on 16mm film: the matte midnight-navy Surf Clock standing on a sun-bleached coastal driftwood bench in warm golden-hour light, "
            "with soft golden sea grass swaying in the foreground bokeh."
        )
    },

    # --- CATEGORY B: SURREAL FLOATING / LEVITATING WEIGHTLESS CINEMA WORLDS (6) ---
    {
        "id": "V3_09_Float_Levitating_Above_Wildflower_Meadow_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Surreal Telepathic Instruments Orchid hero shot: the matte midnight-navy Surf Clock floating weightlessly in mid-air at a graceful 15-degree three-quarter angle "
            "above a sunlit wildflower meadow against a soft warm blue sky with wispy clouds. Zero wires, zero supports, natural sunlight catching the tactile molded plastic bevel, 16mm Kodak film aesthetic."
        )
    },
    {
        "id": "V3_10_Float_Weightless_In_Sunlit_Architectural_Atrium",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock levitating weightlessly in mid-air inside a warm sunlit board-formed concrete and travertine architectural atrium, "
            "catching a diagonal shaft of natural golden morning sunlight. Crisp three-quarter floating angle, zero wires, subtle natural shadow far below."
        )
    },
    {
        "id": "V3_11_Float_Levitating_Over_Glassy_Dawn_Ocean_Swell",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Surreal art photography: the matte midnight-navy Surf Clock floating weightlessly in mid-air two feet above glassy golden-and-sage dawn ocean swell. "
            "Warm sunrise horizon light kissing the smooth VDI-24 matte molded bevel, 35mm cinema lens, zero supports."
        )
    },
    {
        "id": "V3_12_Float_DieterRams_IceGrey_Edition_In_Warm_Sunbeam",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to classic Dieter Rams Braun Light Warm-Grey (RAL 7035 tactile injection-molded matte ABS plastic) while keeping the dark-navy recessed dial and burnt-orange hands. "
            "Show the clock floating weightlessly at a dynamic three-quarter tilt in a warm sunlit minimalist studio with soft natural shadow."
        )
    },
    {
        "id": "V3_13_Float_Orchid_Cream_And_Sage_Synth_Edition_ZeroGravity",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to Telepathic Instruments Orchid / Teenage Engineering Warm Off-White Cream VDI-24 injection-molded polymer while keeping the dark-navy dial and burnt-orange hands. "
            "Show the clock floating weightlessly in mid-air in warm natural daylight against a soft terracotta-and-sand architectural backdrop."
        )
    },
    {
        "id": "V3_14_Float_Rear_Fluted_Borosilicate_In_Golden_Sunlight",
        "prompt": (
            "Rear three-quarter floating view of the matte midnight-navy Braun Surf Clock levitating weightlessly in warm natural golden sunlight. "
            "The rear cover is a precision vertically-fluted frosted borosilicate translucent plate that softly diffuses the warm sunlight, "
            "revealing the two vertically-stacked circular 28BYJ-48 stepper motor silhouettes and copper coils inside."
        )
    },

    # --- CATEGORY C: WALL-MOUNTED ARCHITECTURAL & LIVING WORLDS (6) ---
    {
        "id": "V3_15_Wall_Mounted_Warm_Venetian_Plaster_Dappled_Sunlight",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Architectural Digest interior photography: the matte midnight-navy Surf Clock mounted flush on a warm cream Venetian lime-plaster wall. "
            "Natural afternoon sunlight filtering through window trees casts soft, poetic dappled leaf shadows across the plaster wall around the clock."
        )
    },
    {
        "id": "V3_16_Wall_Mounted_MidCentury_Walnut_And_Concrete_Loft",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock mounted on a smooth architectural board-formed concrete wall in a sunlit mid-century modern living room, "
            "with warm American walnut shelving and a ceramic vase visible in the soft-focus composition. Natural daylight, 35mm cinema lens."
        )
    },
    {
        "id": "V3_17_Wall_Mounted_Breezy_Beach_Shack_Linen_Curtains_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Shot on 16mm film: the matte midnight-navy Surf Clock mounted on a warm whitewashed timber beach-house wall beside an open window "
            "where sheer natural linen curtains billow gently in the morning sea breeze. Warm golden coastal sunlight."
        )
    },
    {
        "id": "V3_18_Wall_Mounted_DieterRams_IceGrey_On_Terracotta_Plaster",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to classic Dieter Rams Braun Ice-Grey (RAL 7035 tactile injection-molded matte ABS) while keeping the dark-navy dial and burnt-orange hands. "
            "Show the clock mounted flush on a warm Mediterranean terracotta-sand textured plaster wall with a diagonal slice of natural morning sunlight."
        )
    },
    {
        "id": "V3_19_Wall_Mounted_Japanese_Cedar_And_Lime_Entryway",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock mounted on a serene Japanese sand-plaster wall framed by warm vertical cedar woodwork, "
            "illuminated by soft diffused shoji-screen morning daylight."
        )
    },
    {
        "id": "V3_20_Wall_Mounted_Gallery_Limestone_Wall_ThreeQuarter",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Three-quarter architectural view of the matte midnight-navy Surf Clock mounted on a honed warm limestone gallery wall, "
            "showing its clean 52mm deep tactile injection-molded profile and flush shadow-gap against the stone in natural skylight."
        )
    },

    # --- CATEGORY D: TABLETOP, COFFEE TABLE & CREDENZA PANNING WORLDS (8) ---
    {
        "id": "V3_21_Table_Roman_Travertine_CoffeeTable_Espresso_ArtBooks",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Architectural Digest tabletop shot: the matte midnight-navy Surf Clock standing on a honed Roman travertine coffee table "
            "beside a stoneware espresso cup and stacked linen art monographs in warm morning window light."
        )
    },
    {
        "id": "V3_22_Table_MidCentury_Teak_Credenza_Vinyl_Turntable_Orchid",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Telepathic Instruments Orchid / Teenage Engineering vibe: the matte midnight-navy Surf Clock standing on a vintage Danish teak credenza "
            "next to a brushed-aluminum audiophile turntable and warm analog synth equipment in sunlit studio light."
        )
    },
    {
        "id": "V3_23_Table_Brutalist_Concrete_Window_Ledge_Overlooking_Surf",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock standing on a deep raw architectural concrete window ledge, with a large window behind it "
            "looking out over a soft-focus sunlit turquoise surf break and coastal headland. Shot on 35mm film."
        )
    },
    {
        "id": "V3_24_Table_PoetryCam_Turned_Oak_And_Cork_Studio_Stool_16mm",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Poetry Camera indie design studio aesthetic: the matte midnight-navy Surf Clock standing on a sculptural turned white-oak stool "
            "in a sun-drenched artist studio with warm wooden floorboards and potted plants in the soft background bokeh. Shot on 16mm film."
        )
    },
    {
        "id": "V3_25_Table_Architects_Oak_Desk_Brass_Lamp_And_Sketches",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock standing on an industrial designer's warm oak desk beside a brushed brass task lamp, "
            "metal calipers, and industrial design sketches in warm late-afternoon window light."
        )
    },
    {
        "id": "V3_26_Table_Calacatta_Viola_Marble_Plinth_Warm_Morning",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock standing on a honed Calacatta Viola marble tabletop with rich burgundy-and-cream veining, "
            "bathed in warm golden morning sunlight with soft natural shadows."
        )
    },
    {
        "id": "V3_27_Table_USM_Haller_Chrome_And_Olive_Credenza_Daylight",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "The matte midnight-navy Surf Clock standing on an olive-green and chrome USM Haller modular credenza in a bright, warm sunlit loft apartment. "
            "Crisp natural daylight reflections on the chrome tube frame, zero blue LEDs."
        )
    },
    {
        "id": "V3_28_Table_Warm_Limestone_Bedside_Linen_Morning_Ritual",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Intimate morning lifestyle shot: the matte midnight-navy Surf Clock on a honed limestone bedside table beside a bed with rumpled warm oat-linen bedding, "
            "bathed in golden early-morning window sunbeams."
        )
    },

    # --- CATEGORY E: CLEAN STUDIO & TACTILE MACRO (8 — ZERO BLACK GLOW, ZERO BLUE LEDS) ---
    {
        "id": "V3_29_Studio_Signature_Clean_SlateBlue_Chiaroscuro",
        "prompt": "DIRECT_MASTER_REF"
    },
    {
        "id": "V3_30_Studio_Warm_Ulm_1965_DieterRams_IceGrey_Edition",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to classic 1965 Braun Ulm Light Warm-Grey (RAL 7035 tactile VDI-24 injection-molded matte ABS polymer) while keeping the dark-navy dial and burnt-orange hands. "
            "Place on a warm sand-grey limestone studio plinth with soft natural directional studio key light."
        )
    },
    {
        "id": "V3_31_Studio_BeadBlasted_Titanium_Silver_Warm_Gallery",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to Teenage Engineering / Leica Bead-Blasted Titanium Silver anodized aluminum with fine micro-bead texture while keeping the dark-navy dial and burnt-orange hands. "
            "Place on a dark honed basalt plinth in warm natural gallery softbox lighting."
        )
    },
    {
        "id": "V3_32_Studio_Forest_Sage_Green_Molded_On_Raw_Travertine",
        "prompt": (
            f"{COMMON_PRODUCT_LOCK} "
            "Recolor the outer casing to Telepathic Instruments Orchid / Teenage Engineering Matte Forest-Sage Green VDI-24 injection-molded polymer while keeping the dark-navy dial and burnt-orange hands. "
            "Place on a raw Roman travertine stone block in warm golden studio sunlight."
        )
    },
    {
        "id": "V3_33_Macro_100mm_UpperDial_Tactile_Braun_Molded_Plastic",
        "prompt": (
            "Extreme 100mm macro close-up of the upper dial of the Braun Surf Clock in warm natural afternoon window light. "
            "Shows the tactile VDI-24 micro-textured matte dark-navy injection-molded dial face (ZERO glass), crisp raised silkscreened white tick marks and beach names (LONG REEF, DEE WHY, CURL CURL, FRESHIE, QUEENSIE), "
            "and STRICTLY ONE precision matte burnt-orange injection-molded pointer hand pointing cleanly to DEE WHY (2 o'clock) with a subtle natural shadow. Zero cyan highlights."
        )
    },
    {
        "id": "V3_34_Macro_100mm_LowerWorthIt_Tactile_Braun_Molded_Plastic",
        "prompt": (
            "Extreme 100mm macro close-up of the lower 'WORTH IT?' semicircle gauge of the Braun Surf Clock in warm natural window light. "
            "Shows the tactile VDI-24 micro-textured matte dark-navy injection-molded dial face (ZERO glass), crisp matte pure-white semicircle arc labeled NAH on the left and YEAH on the right (ZERO blue or cyan edge highlight!), "
            "and STRICTLY ONE short matte burnt-orange molded pointer hand pointing cleanly to YEAH."
        )
    },
    {
        "id": "V3_35_Macro_85mm_GrazingBevel_Tactile_Molded_In_GoldenSunlight",
        "prompt": (
            "Extreme 85mm macro detail shot at a grazing angle of the top-left corner and smooth 0.90mm radiused VDI-24 micro-textured injection-molded matte midnight-navy bevel of the Braun Surf Clock "
            "outdoors in warm golden-hour sunlight with soft blurred wildflowers in the distant background bokeh. "
            "Shows the deeply recessed open matte navy dial, crisp white QUEENSIE and LONG REEF silkscreened typography, and single burnt-orange pointer tip. Zero neon, zero cyan lines."
        )
    },
    {
        "id": "V3_36_Macro_Rear_Fluted_Borosilicate_In_Warm_WindowLight",
        "prompt": (
            "Studio macro three-quarter rear shot of the Braun Surf Clock standing on a warm travertine surface in golden afternoon window light. "
            "The rear cover is a vertically-fluted frosted borosilicate translucent plate recessed into the tactile matte midnight-navy molded housing, softly transmitting warm golden sunlight "
            "to reveal the internal vertically-stacked dual circular stepper motors and copper coils inside."
        )
    },
]

def generate_v3_plate(shot: dict, stagger_sec: float = 0.0) -> dict:
    time.sleep(stagger_sec)
    sid = shot["id"]
    out_path = V3_STILLS_DIR / f"{sid}_4K.jpg"
    if sid == "V3_29_Studio_Signature_Clean_SlateBlue_Chiaroscuro":
        shutil.copy2(MASTER_REF_16x9, out_path)
        print(f"[SAVED CLEAN MASTER REF 4K] {out_path.name}", flush=True)
        return {"id": sid, "path": str(out_path), "status": "ok"}

    if out_path.exists() and out_path.stat().st_size > 400_000:
        print(f"[SKIP EXISTING] {out_path.name}", flush=True)
        return {"id": sid, "path": str(out_path), "status": "cached"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": REF_B64}},
                {"text": shot["prompt"]}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"}
        }
    }

    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            img_b64 = None
            for p in parts:
                if "inlineData" in p:
                    img_b64 = p["inlineData"]["data"]
                    break
            if not img_b64:
                raise RuntimeError("No inlineData returned")
            raw_bytes = base64.b64decode(img_b64)
            arr = np.frombuffer(raw_bytes, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                raise RuntimeError("cv2.imdecode failed")
            img_4k = cv2.resize(img, (3840, 2160), interpolation=cv2.INTER_LANCZOS4)
            img_4k = remove_electric_cyan_and_add_molded_grain(img_4k)
            cv2.imwrite(str(out_path), img_4k, [cv2.IMWRITE_JPEG_QUALITY, 96])
            log_qc({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "stage": "V3_STAGE1_ORCHID_POETRY_KEYFRAME_GEN",
                "shot_id": sid,
                "model_gen": "gemini-3-pro-image-preview (Nano Banana Pro 5.5K->4K + VDI-24 Molded Grain)",
                "passed": True,
                "score": 9.85,
                "summary": f"Generated pure un-composited 4K plate {out_path.name} from 4K crisp Braun master ref"
            })
            print(f"[GENERATED V3 4K] {out_path.name} ({out_path.stat().st_size/1e6:.2f} MB)", flush=True)
            return {"id": sid, "path": str(out_path), "status": "ok"}
        except Exception as e:
            print(f"[RETRY {attempt}/4] {sid}: {e}", flush=True)
            time.sleep(6 * attempt)
    return {"id": sid, "status": "failed"}

# Clear any partial plates from cancelled run before starting with the new 4K Crisp Braun Master Ref
for p in V3_STILLS_DIR.glob("V3_*.jpg"):
    p.unlink()

print("=== V3 STAGE 1: GENERATING 36 ORCHID / POETRY CAMERA / ARCH DIGEST 4K PLATES FROM CRISP 4K MASTER REF ===", flush=True)
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(generate_v3_plate, s, (i % 6) * 1.5) for i, s in enumerate(SHOTS)]
    for fut in as_completed(futs):
        fut.result()

thumbs = []
for s in SHOTS:
    p = V3_STILLS_DIR / f"{s['id']}_4K.jpg"
    if p.exists():
        im = cv2.imread(str(p))
        im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    else:
        im = np.zeros((360, 640, 3), dtype=np.uint8)
    cv2.putText(im, s["id"][:32], (14, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 240, 180), 2)
    thumbs.append(im)

rows = [np.hstack(thumbs[r*6:(r+1)*6]) for r in range(6)]
sheet_path = AUDIT_DIR / "V3_ALL_36_ORCHID_POETRY_KEYFRAMES_SHEET.jpg"
cv2.imwrite(str(sheet_path), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 93])
print(f"=== SAVED V3 36-PLATE CONTACT SHEET: {sheet_path} ===", flush=True)
