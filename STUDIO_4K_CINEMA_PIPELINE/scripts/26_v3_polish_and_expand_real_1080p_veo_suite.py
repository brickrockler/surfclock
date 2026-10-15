#!/usr/bin/env python3
"""
V3 STAGE 6: POLISH FLAGGED CLIPS & EXPAND REAL 1080P + 3 CLOSE-UP INGREDIENTS VEO 3.1 PRO SUITE
1. Fixes V3_REAL_10 by trimming to t=3.8..8.0s + cyan suppression so zero ocean cyan reflection ever touches the arc.
2. Regenerates the flagged 16:9 clips (V3_REAL_04, V3_REAL_08, V3_REAL_11, V3_REAL_15, V3_REAL_18, V3_REAL_20)
   and flagged 9:16 clips (V3_9x16_REAL_01, V3_9x16_REAL_02, V3_9x16_REAL_06, V3_9x16_REAL_08) using the
   "Single-Needle Analog Surf Gauge Instrument (strictly ONE stationary orange needle per dial, NEVER two hands,
   NEVER spinning edge-on)" prompt at native 1080p + 3 Close-Up Ingredients on Vertex AI veo-3.1-generate-001.
3. Expands the suite with 8 brand-new 1080p + 3 Close-Up Ingredients Real 3D Veo 3.1 Pro shots
   (V3_REAL_21..26 in 16:9 and V3_9x16_REAL_11..12 in 9:16).
4. Masters all clips to 4K 60fps, rebuilds the 4 Master Showreels, and generates updated 1:1 dial audit sheets.
"""

import os
import json
import time
import base64
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PIPELINE_ROOT = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
STILLS_16x9_DIR = PIPELINE_ROOT / "01_4K_STUDIO_KEYFRAMES_AND_STILLS" / "V3_ORCHID_POETRY_ARCHDIGEST_4K"
STILLS_9x16_DIR = PIPELINE_ROOT / "01_4K_STUDIO_KEYFRAMES_AND_STILLS" / "V3_9x16_VERTICAL_STUDIO_AND_ORCHID_4K"
RAW_VEO_DIR = PIPELINE_ROOT / "raw_renders" / "v3_veo31_pro_1080p_ingredients_raw"
CLIPS_16x9_DIR = PIPELINE_ROOT / "02_INDIVIDUAL_4K_CLIPS_16x9"
CLIPS_9x16_DIR = PIPELINE_ROOT / "03_INDIVIDUAL_4K_CLIPS_9x16"
SHOWREELS_DIR = PIPELINE_ROOT / "00_MASTER_SHOWREELS"
AUDIT_DIR = PIPELINE_ROOT / "04_CONTACT_SHEETS_AND_AUDIT"

ING_WHOLE_4K = STILLS_16x9_DIR / "INGREDIENT_WHOLE_CLOCK_CLOSEUP_4K.jpg"
ING_DIAL_4K = STILLS_16x9_DIR / "INGREDIENT_CLOSEUP_FULL_DIAL_4K.jpg"

VERTEX_PROJECT = "ee-gif-machine"
VERTEX_LOCATION = "us-central1"
VEO_PRO_MODEL = "veo-3.1-generate-001"


def get_access_token() -> str:
    adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    with open(adc_path, "r") as f:
        creds = json.load(f)
    data = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]



def resolve_kf(base_dir: Path, prefix: str) -> Path:
    matches = sorted(base_dir.glob(f"{prefix}_*.jpg"))
    if not matches:
        raise FileNotFoundError(f"No keyframe matching {prefix}_*.jpg in {base_dir}")
    return matches[0]

SINGLE_NEEDLE_GAUGE_RULE = (
    "CRITICAL INSTRUMENT ACCURACY: This is a Single-Needle Analog Surf Gauge Instrument (like a single-needle Braun meter, "
    "NOT a two-hand clock). The top dial has STRICTLY ONE SINGLE STATIONARY ORANGE POINTER NEEDLE fixed rigidly at DEE WHY "
    "(2 o'clock). The bottom white semicircle arc has STRICTLY ONE SINGLE STATIONARY ORANGE POINTER NEEDLE fixed rigidly at "
    "YEAH (4 o'clock). Both orange needles are 100% stationary and locked in place; they NEVER move, NEVER rotate, and NEVER "
    "split into two hands. The gauge housing stays facing toward the camera so the front dial typography (LONG REEF, QUEENSIE, "
    "DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT?) remains 100% visible, razor-sharp, and legible throughout the entire shot. "
    "Zero glowing lights, zero cyan or blue highlights."
)


# 1. Regenerate flagged clips (force_regenerate=True)
REGEN_AND_NEW_JOBS = [
    # --- FLAGGED 16:9 CLIPS TO REGENERATE CLEANLY ---
    {
        "id": "V3_REAL_04_Handycam_Botanical_Greenhouse_Dappled_Ferns",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_05"),
        "force": True,
        "prompt": (
            "Real 1990s Sony Hi8 Handycam camcorder video in a sunlit glasshouse conservatory. "
            "Gentle handheld camcorder movement with real 3D parallax between foreground maidenhair fern fronds and the matte "
            "slate-blue Single-Needle Surf Gauge resting on a weathered cedar potting bench. Real water droplets glisten on fern leaves "
            "while warm sunlight filters through the glass roof. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_08_Float_ZeroGravity_Above_Wildflower_Meadow_16mm",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_11"),
        "force": True,
        "prompt": (
            "Real Arriflex 16mm film cinema shot. The matte slate-blue Single-Needle Surf Gauge levitates weightlessly in mid-air "
            "above a coastal wildflower meadow at golden hour. The gauge bobs gently up and down by 2 centimeters in zero gravity "
            "while ALWAYS facing the camera (it NEVER spins or turns sideways). Red poppies and white daisies sway in the warm sea "
            "breeze beneath the floating gauge as the 16mm camera glides forward with real 3D parallax. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_11_Float_DieterRams_IceGrey_Weightless_In_Sunbeam",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_16"),
        "force": True,
        "prompt": (
            "Real 35mm cinema shot of a 1965 Dieter Rams Braun Edition (Matte Ice-Grey RAL 7035 outer frame, charcoal-black dial) "
            "Single-Needle Surf Gauge levitating weightlessly in mid-air inside a warm mid-century architectural studio. "
            "The gauge hovers steadily facing the camera (it NEVER spins edge-on and has zero glowing edges) while natural tree-leaf "
            "shadows dance softly across the plaster wall behind it and the camera performs a smooth 3D slider glide. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_15_Table_Travertine_CoffeeTable_SteamingEspresso",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_24"),
        "force": True,
        "prompt": (
            "Real 35mm cinema lateral slider shot across a Roman travertine stone coffee table in a sunlit coastal apartment. "
            "Delicate real wisps of hot steam rise from a ceramic espresso cup in the foreground while the camera glides smoothly "
            "sideways (no extreme zoom-in) past the matte slate-blue Single-Needle Surf Gauge. Warm morning sunlight casts crisp "
            "natural shadows across the porous travertine stone. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_18_Studio_Clean_SlateBlue_Chiaroscuro_3D_Orbit",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_31"),
        "force": True,
        "prompt": (
            "High-end real commercial studio cinema shot on Arri Alexa 65 with 85mm Master Prime lens. "
            "The camera executes a subtle 12-degree front-three-quarter slider glide across the matte slate-blue Single-Needle "
            "Surf Gauge on a dark cleft slate plinth. The gauge remains facing the camera 100% of the shot (it NEVER rotates edge-on "
            "or backwards) as soft warm tungsten key light reveals the tactile VDI-24 micro-bead polymer texture and stepped bezel. "
            + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_20_Studio_Rear_Fluted_Borosilicate_WarmLight_Orbit",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_36"),
        "force": True,
        "prompt": (
            "High-end real commercial studio cinema shot of the rear of the Surf Gauge resting on a travertine plinth. "
            "The camera performs a slow, subtle 10-degree lateral slider movement across the vertical-ribbed fluted borosilicate glass "
            "backplate, creating real optical refraction over the internal copper stepper coils and matte orange structural bridge inside, "
            "with the single knurled solid-brass thumbscrew latch fixed cleanly at top-center (no side knobs). Zero blue or cyan light."
        ),
    },

    # --- FLAGGED 9:16 VERTICAL CLIPS TO REGENERATE CLEANLY ---
    {
        "id": "V3_9x16_REAL_01_Studio_SlateBlue_Chiaroscuro_3D_Dolly",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_01"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real studio cinema shot on Arri Alexa 65. Smooth, slow 3D camera slider movement across the "
            "matte slate-blue Single-Needle Surf Gauge on a dark cleft slate plinth. Soft warm key lighting moves gently across "
            "the VDI-24 micro-bead polymer bezel and recessed matte dial cavity. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_02_Studio_Braun_IceGrey_RAL7035_3D_Orbit",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_02"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real studio cinema shot of the 1965 Dieter Rams Braun Edition (Matte Ice-Grey RAL 7035 housing, "
            "charcoal-black dial) Single-Needle Surf Gauge on a Roman travertine stone plinth. Subtle 10-degree 3D studio slider "
            "glide with natural perspective parallax and warm tungsten studio lighting. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_06_Orchid_Wildflower_Meadow_16mm_Handheld",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_09"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real Arriflex 16mm film cinema shot in a coastal wildflower meadow at golden hour. "
            "Red poppies and white daisies sway in the warm ocean breeze in the foreground while the 16mm camera glides smoothly "
            "past the matte slate-blue Single-Needle Surf Gauge with real 3D parallax and Kodak Vision3 250D film grain. "
            + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_08_Float_Weightless_Above_Wildflowers_16mm",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_12"),
        "force": True,
        "prompt": (
            "Native 9:16 vertical real 16mm cinema shot. The matte slate-blue Single-Needle Surf Gauge floats weightlessly in mid-air "
            "above a golden-hour wildflower meadow. The gauge bobs gently up and down by 2 centimeters while ALWAYS facing the camera "
            "(it NEVER spins edge-on or rotates sideways) as red poppies and daisies sway in the breeze below. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },

    # --- 8 BRAND-NEW BONUS REAL 1080P VEO 3.1 PRO SHOTS (16:9 & 9:16) ---
    {
        "id": "V3_REAL_21_Handycam_90s_Hi8_Surfer_Waxing_Board_Beside_Clock",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_04"),
        "force": False,
        "prompt": (
            "Real 1990s Sony Hi8 Handycam camcorder video in a sunlit coastal meadow. The matte slate-blue Single-Needle Surf Gauge "
            "sits sharply in the foreground on a woven blanket while out-of-focus coastal grasses sway in the warm breeze and soft "
            "natural sunlight shifts across the tactile VDI-24 molded bezel. Authentic handheld camcorder breathing and 3D parallax. "
            + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_22_Orchid_Coastal_Dune_Spinifex_GoldenHour_16mm",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_08"),
        "force": False,
        "prompt": (
            "Real Arriflex 16SR3 16mm film cinema shot on a golden sand dune overlooking the ocean at sunset. Silvery spinifex grass "
            "and dry marram reeds blow gently in the offshore breeze around the matte slate-blue Single-Needle Surf Gauge as the 16mm "
            "camera performs a slow low-angle 3D dolly glide. Warm Kodak 250D halation and organic film grain. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_23_PoetryCam_Sunlit_Travertine_Courtyard_Jasmine_16mm",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_10"),
        "force": False,
        "prompt": (
            "Real 16mm film cinema shot in a sunlit Mediterranean courtyard. Dappled shadows of star-jasmine vines sway gently across "
            "a warm travertine stone table and the matte slate-blue Single-Needle Surf Gauge as the handheld 16mm camera glides "
            "with real 3D parallax. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_24_Table_Collector_Concrete_Desk_Leica_And_Coffee_35mm",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_26"),
        "force": False,
        "prompt": (
            "Architectural Digest 35mm cinema slider shot across an architect's cast-concrete desk alongside a silver rangefinder camera "
            "and open linen sketchbook. Soft morning window light and natural tree shadows shift across the desk as the camera glides "
            "with real 3D parallax past the matte slate-blue Single-Needle Surf Gauge. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_25_Studio_Orchid_ForestSage_VDI24_Macro_3D_Slider",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_33"),
        "force": False,
        "prompt": (
            "High-end real studio cinema shot of the Teenage Engineering Orchid Edition (Matte Forest-Sage Green VDI-24 molded polymer "
            "housing, deep forest-green dial) Single-Needle Surf Gauge on a travertine plinth. Smooth 12-degree front 3D slider glide "
            "with warm tungsten key lighting sweeping across the tactile polymer grain. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_REAL_26_Studio_BeadBlasted_Titanium_Pro_3D_Slider",
        "aspect": "16:9",
        "keyframe": resolve_kf(STILLS_16x9_DIR, "V3_35"),
        "force": False,
        "prompt": (
            "High-end real studio cinema shot of the Bead-Blasted Grade-5 Titanium CNC Pro Edition Single-Needle Surf Gauge on a dark "
            "basalt plinth. Smooth 12-degree front 3D camera slider glide as soft warm studio light rolls across the satin bead-blasted "
            "titanium chamfers and matte slate-blue dial. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_11_Handycam_90s_Hi8_Coastal_Headland_SurfCheck",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_10"),
        "force": False,
        "prompt": (
            "Native 9:16 vertical real 1990s Sony Hi8 Handycam video on a sandstone ledge overlooking a coastal headland. "
            "Real turquoise ocean waves roll toward the beach in the background while coastal grass sways in the sea breeze and "
            "the camcorder frames the matte slate-blue Single-Needle Surf Gauge with subtle handheld breathing. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
    {
        "id": "V3_9x16_REAL_12_Tabletop_Travertine_Steaming_Espresso_Morning_Sun",
        "aspect": "9:16",
        "keyframe": resolve_kf(STILLS_9x16_DIR, "V3_9x16_16"),
        "force": False,
        "prompt": (
            "Native 9:16 vertical real 35mm cinema slider shot across a sunlit Roman travertine coffee table. Delicate real wisps "
            "of steam rise from a ceramic espresso cup beside the matte slate-blue Single-Needle Surf Gauge as the camera glides "
            "smoothly with real 3D parallax. " + SINGLE_NEEDLE_GAUGE_RULE
        ),
    },
]


def submit_veo_1080p_with_ingredients(job: dict) -> str:
    cid = job["id"]
    aspect = job["aspect"]
    kf_path = job["keyframe"]
    prompt = job["prompt"]

    kf_b64 = base64.b64encode(kf_path.read_bytes()).decode("utf-8")
    ing1_b64 = base64.b64encode(ING_WHOLE_4K.read_bytes()).decode("utf-8")
    ing2_b64 = base64.b64encode(ING_DIAL_4K.read_bytes()).decode("utf-8")

    payload = {
        "instances": [
            {
                "prompt": prompt,
                "referenceImages": [
                    {
                        "image": {"bytesBase64Encoded": kf_b64, "mimeType": "image/jpeg"},
                        "referenceType": "asset",
                    },
                    {
                        "image": {"bytesBase64Encoded": ing1_b64, "mimeType": "image/jpeg"},
                        "referenceType": "asset",
                    },
                    {
                        "image": {"bytesBase64Encoded": ing2_b64, "mimeType": "image/jpeg"},
                        "referenceType": "asset",
                    },
                ],
            }
        ],
        "parameters": {
            "aspectRatio": aspect,
            "durationSeconds": 8,
            "resolution": "1080p",
            "sampleCount": 1,
            "personGeneration": "allow_adult",
            
        },
    }

    url = (
        f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/"
        f"{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/"
        f"{VEO_PRO_MODEL}:predictLongRunning"
    )
    for attempt in range(1, 5):
        try:
            token = get_access_token()
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                op_name = data["name"]
                print(f"[STARTED 1080P+INGREDIENTS] {cid} -> {op_name.split('/')[-1]}", flush=True)
                return op_name
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[HTTP WARN {cid}] attempt {attempt} code={e.code}: {err_body[:200]}", flush=True)
            time.sleep(6 * attempt)
        except Exception as e:
            print(f"[WARN {cid}] attempt {attempt}: {e}", flush=True)
            time.sleep(6 * attempt)
    raise RuntimeError(f"Failed to start {cid}")


def poll_veo_operation(cid: str, op_name: str, out_mp4: Path) -> bool:
    poll_url = (
        f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/"
        f"{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/"
        f"{VEO_PRO_MODEL}:fetchPredictOperation"
    )
    for step in range(1, 90):
        time.sleep(8)
        try:
            token = get_access_token()
            req = urllib.request.Request(
                poll_url,
                data=json.dumps({"operationName": op_name}).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if not data.get("done"):
                continue
            if "error" in data:
                print(f"[OP ERROR {cid}] {data['error']}", flush=True)
                return False
            videos = data.get("response", {}).get("videos", [])
            if not videos:
                print(f"[NO VIDEO {cid}] {data}", flush=True)
                return False
            b64_vid = videos[0].get("bytesBase64Encoded")
            if b64_vid:
                out_mp4.write_bytes(base64.b64decode(b64_vid))
                mb = out_mp4.stat().st_size / (1024 * 1024)
                print(f"[DONE 1080P+INGREDIENTS] {cid} ({mb:.2f} MB)", flush=True)
                return True
        except Exception as e:
            print(f"[POLL WARN {cid}] step {step}: {e}", flush=True)
    return False


def generate_and_wait(job: dict) -> Path:
    RAW_VEO_DIR.mkdir(parents=True, exist_ok=True)
    cid = job["id"]
    out_raw = RAW_VEO_DIR / f"{cid}_1080p_raw.mp4"
    if not job.get("force", False) and out_raw.exists() and out_raw.stat().st_size > 1_000_000:
        print(f"[CACHED 1080P VEO] {cid}", flush=True)
        return out_raw

    for retry in range(1, 4):
        try:
            op_name = submit_veo_1080p_with_ingredients(job)
            if poll_veo_operation(cid, op_name, out_raw):
                return out_raw
        except Exception as e:
            print(f"[RETRY {retry} {cid}] {e}", flush=True)
            time.sleep(8)
    raise RuntimeError(f"Exhausted retries for {cid}")


def suppress_cyan_on_video(in_mp4: Path, out_mp4: Path):
    cap = cv2.VideoCapture(str(in_mp4))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    tmp_avi = out_mp4.with_suffix(".nocyan.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(tmp_avi), fourcc, fps, (w, h))

    modified = 0
    while True:
        ret, bgr = cap.read()
        if not ret:
            break
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
        H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
        # Suppress any electric cyan/teal on the clock dial/arc area (center 60% of frame)
        cy_mask = np.zeros_like(H, dtype=bool)
        cy_mask[int(h*0.18):int(h*0.85), int(w*0.25):int(w*0.75)] = True
        cyan_arc = cy_mask & (H >= 80) & (H <= 108) & (S > 55) & (V > 120)
        if np.any(cyan_arc):
            modified += 1
            S[cyan_arc] *= 0.08
            V[cyan_arc] = np.clip(V[cyan_arc] * 1.08, 0, 255)
            hsv[:, :, 1] = S
            hsv[:, :, 2] = V
            bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        writer.write(bgr)
    cap.release()
    writer.release()

    if modified > 0:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(tmp_avi), "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out_mp4)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"[CYAN SUPPRESSED] {out_mp4.name} ({modified} frames cleaned)", flush=True)
    else:
        if in_mp4 != out_mp4:
            out_mp4.write_bytes(in_mp4.read_bytes())
    tmp_avi.unlink(missing_ok=True)


def auto_trim_best_window(in_mp4: Path, out_mp4: Path):
    """
    Checks if the first half or second half has any unwanted second orange arm at 4 o'clock or edge-on spin,
    and trims to the cleanest continuous window if needed.
    """
    cap = cv2.VideoCapture(str(in_mp4))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if total_frames < 48:
        cap.release()
        if in_mp4 != out_mp4:
            out_mp4.write_bytes(in_mp4.read_bytes())
        return

    orange_counts = []
    idx = 0
    while True:
        ret, bgr = cap.read()
        if not ret:
            break
        if idx % 4 == 0:
            roi = bgr[int(h * 0.22):int(h * 0.72), int(w * 0.22):int(w * 0.78)]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (5, 130, 120), (24, 255, 255))
            orange_counts.append((idx / fps, int(np.sum(mask > 0))))
        idx += 1
    cap.release()

    if len(orange_counts) >= 6:
        first_q = np.median([c for t, c in orange_counts if t <= 2.4])
        last_h = np.median([c for t, c in orange_counts if t >= 3.6])
        # Case A: early split needle that resolves to single needle in second half
        if first_q > 120 and last_h > 80 and first_q > last_h * 1.42:
            tmp_trim = out_mp4.with_suffix(".trim.mp4")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-ss", "3.2", "-i", str(in_mp4),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(tmp_trim)
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            tmp_trim.replace(out_mp4)
            print(f"[AUTO TRIM SECOND HALF] {out_mp4.name}: using pristine 3.2s..8.0s!", flush=True)
            return
        # Case B: pristine single needle in first 3.6s before a second hand sprouts later
        if first_q > 80 and last_h > first_q * 1.42:
            tmp_trim = out_mp4.with_suffix(".trim.mp4")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-ss", "0.0", "-t", "3.6", "-i", str(in_mp4),
                    "-vf", "setpts=1.5*PTS",
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(tmp_trim)
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            tmp_trim.replace(out_mp4)
            print(f"[AUTO TRIM FIRST HALF] {out_mp4.name}: using pristine 0.0s..3.6s (slowed 1.5x)!", flush=True)
            return

    if in_mp4 != out_mp4:
        out_mp4.write_bytes(in_mp4.read_bytes())


def master_clip_to_4k_60fps(raw_mp4: Path, aspect: str, cid: str, start_ss: float = None) -> Path:
    CLIPS_16x9_DIR.mkdir(parents=True, exist_ok=True)
    CLIPS_9x16_DIR.mkdir(parents=True, exist_ok=True)
    out_dir = CLIPS_16x9_DIR if aspect == "16:9" else CLIPS_9x16_DIR
    out_4k = out_dir / f"{cid}_4K_60fps.mp4"

    tmp_clean = raw_mp4.with_suffix(".clean.mp4")
    if start_ss is not None:
        tmp_ss = raw_mp4.with_suffix(".ss.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(start_ss), "-i", str(raw_mp4), "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(tmp_ss)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        suppress_cyan_on_video(tmp_ss, tmp_clean)
        tmp_ss.unlink(missing_ok=True)
    else:
        suppress_cyan_on_video(raw_mp4, tmp_clean)
        auto_trim_best_window(tmp_clean, tmp_clean)

    target_w, target_h = (3840, 2160) if aspect == "16:9" else (2160, 3840)
    vf = (
        f"scale={target_w}:{target_h}:flags=lanczos+accurate_rnd+full_chroma_int,"
        f"unsharp=5:5:0.45:3:3:0.0,"
        f"fps=60"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(tmp_clean),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "15",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_4k),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_clean.unlink(missing_ok=True)
    mb = out_4k.stat().st_size / (1024 * 1024)
    print(f"[MASTERED 4K 60FPS] {out_4k.name} ({mb:.2f} MB)", flush=True)
    return out_4k


def concat_mp4s(clips: list[Path], out_path: Path):
    SHOWREELS_DIR.mkdir(parents=True, exist_ok=True)
    list_txt = SHOWREELS_DIR / f".concat_{out_path.stem}.txt"
    with open(list_txt, "w") as f:
        for c in clips:
            if c.exists():
                f.write(f"file '{c.resolve()}'\n")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_txt),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    list_txt.unlink(missing_ok=True)
    dur_out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_path)]
    ).decode().strip()
    dur = float(dur_out) if dur_out else 0.0
    mb = out_path.stat().st_size / (1024 * 1024)
    print(f"[SHOWREEL BUILT] {out_path.name} | Duration: {dur:.1f}s ({dur/60:.2f} min) | Size: {mb:.1f} MB", flush=True)


def build_real_veo_audit_sheet(clips: list[Path], out_jpg: Path, is_vertical: bool = False):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    cols = 4
    rows = len(clips)
    cw = 480 if not is_vertical else 360
    ch = 270 if not is_vertical else 520
    sheet = Image.new("RGB", (cols * cw, rows * ch), (14, 14, 16))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 16)
    except Exception:
        font = ImageFont.load_default()

    for r_idx, mp4 in enumerate(clips):
        dur_str = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(mp4)]
        ).decode().strip()
        dur = float(dur_str) if dur_str else 5.0
        for c_idx, frac in enumerate([0.18, 0.50, 0.82]):
            t = max(0.2, min(dur - 0.2, dur * frac))
            tmp_jpg = AUDIT_DIR / f".tmp_{mp4.stem}_{c_idx}.jpg"
            subprocess.run(
                ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(tmp_jpg)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if tmp_jpg.exists():
                im = Image.open(tmp_jpg).convert("RGB")
                im_thumb = im.resize((cw - 6, ch - 6), Image.Resampling.LANCZOS)
                draw = ImageDraw.Draw(im_thumb)
                if c_idx == 0:
                    draw.text((10, 8), mp4.stem[:32], fill=(80, 255, 140), font=font)
                sheet.paste(im_thumb, (c_idx * cw + 3, r_idx * ch + 3))
                if c_idx == 1:
                    w, h = im.size
                    if not is_vertical:
                        crop = im.crop((int(w * 0.28), int(h * 0.14), int(w * 0.72), int(h * 0.86)))
                    else:
                        crop = im.crop((int(w * 0.10), int(h * 0.20), int(w * 0.90), int(h * 0.78)))
                    crop_thumb = crop.resize((cw - 6, ch - 6), Image.Resampling.LANCZOS)
                    d2 = ImageDraw.Draw(crop_thumb)
                    d2.text((10, 8), "1:1 DIAL ZOOM", fill=(255, 220, 80), font=font)
                    sheet.paste(crop_thumb, (3 * cw + 3, r_idx * ch + 3))
                tmp_jpg.unlink(missing_ok=True)

    sheet.save(out_jpg, quality=92)
    print(f"[SAVED REAL VEO AUDIT SHEET] {out_jpg}", flush=True)


def main():
    print("=== V3 STAGE 6: POLISHING FLAGGED CLIPS & EXPANDING REAL 1080P VEO 3.1 PRO SUITE ===", flush=True)

    # First: fix V3_REAL_10 immediately from its existing 1080p raw file by trimming t=3.8..8.0s + cyan suppression
    raw_10 = RAW_VEO_DIR / "V3_REAL_10_Float_Levitating_Over_Rolling_Dawn_Ocean_Swell_1080p_raw.mp4"
    if raw_10.exists():
        master_clip_to_4k_60fps(
            raw_10, "16:9", "V3_REAL_10_Float_Levitating_Over_Rolling_Dawn_Ocean_Swell", start_ss=3.8
        )

    # Second: submit & poll the 18 jobs (10 fixes + 8 brand-new real 1080p Veo clips)
    completed = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(generate_and_wait, job): job for job in REGEN_AND_NEW_JOBS}
        for fut in as_completed(futs):
            job = futs[fut]
            raw_mp4 = fut.result()
            completed.append((job, raw_mp4))

    # Third: master all 18 newly generated 1080p clips to 4K 60fps
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = [
            pool.submit(master_clip_to_4k_60fps, raw_mp4, job["aspect"], job["id"])
            for job, raw_mp4 in completed
        ]
        for fut in as_completed(futs):
            fut.result()

    # Fourth: rebuild all 4 Master Showreels with 100% Real 3D Video
    real_16x9 = sorted(CLIPS_16x9_DIR.glob("V3_REAL_*_4K_60fps.mp4"))
    v1_v2_16x9 = sorted(
        [p for p in CLIPS_16x9_DIR.glob("*_4K_60fps.mp4") if not p.name.startswith("V3_")]
    )
    match_cuts = sorted(CLIPS_16x9_DIR.glob("V3_MATCHCUT_*_4K_60fps.mp4"))
    real_9x16 = sorted(CLIPS_9x16_DIR.glob("V3_9x16_REAL_*_4K_60fps.mp4"))
    v2_9x16 = sorted(
        [p for p in CLIPS_9x16_DIR.glob("*_4K_60fps.mp4") if not p.name.startswith("V3_")]
    )

    concat_mp4s(
        real_16x9 + match_cuts[:2] + v1_v2_16x9,
        SHOWREELS_DIR / "SURF_CLOCK_4K_60FPS_MASTER_COMMERCIAL_16x9.mp4",
    )
    concat_mp4s(
        real_16x9,
        SHOWREELS_DIR / "SURF_CLOCK_4K_60FPS_ORCHID_AND_POETRY_16MM_SHOWCASE_16x9.mp4",
    )
    if match_cuts:
        concat_mp4s(
            match_cuts,
            SHOWREELS_DIR / "SURF_CLOCK_4K_60FPS_MATCH_CUT_SHOWCASE_16x9.mp4",
        )
    concat_mp4s(
        real_9x16 + v2_9x16,
        SHOWREELS_DIR / "SURF_CLOCK_4K_60FPS_VERTICAL_REEL_9x16.mp4",
    )

    # Fifth: build updated audit sheets
    build_real_veo_audit_sheet(
        real_16x9, AUDIT_DIR / "V3_REAL_VEO_16x9_MIDFRAME_AND_DIAL_AUDIT.jpg", is_vertical=False
    )
    build_real_veo_audit_sheet(
        real_9x16, AUDIT_DIR / "V3_REAL_VEO_9x16_MIDFRAME_AND_DIAL_AUDIT.jpg", is_vertical=True
    )
    print("=== V3 STAGE 6 COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
