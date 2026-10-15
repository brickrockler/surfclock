import os, sys, json, time, base64, urllib.request
import numpy as np
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
from omni_pro_client import get_api_key, get_vertex_token, _b64_image_part, master_raw_video_to_4k60, VERTEX_PROJECT, VERTEX_LOCATION
from sift_4k_video_mastering import fast_master_shot

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
STILLS_DIR = f"{BASE}/01_4K_STUDIO_KEYFRAMES_AND_STILLS"
CLIPS_DIR = f"{BASE}/02_INDIVIDUAL_4K_CLIPS_16x9"
RAW_DIR = f"{BASE}/raw_renders"
os.makedirs(RAW_DIR, exist_ok=True)

def detect_front_bezel_polygon_4k(still_path: str):
    """
    Uses Gemini Vision to return the exact 4 corners of the Surf Clock's front rectangular bezel
    in [x, y] pixel coordinates for a 3840x2160 frame.
    """
    api_key = get_api_key()
    prompt = """Return ONLY valid JSON with the 4 corners of the Surf Clock's front rectangular outer bezel face (top-left, top-right, bottom-right, bottom-left) in normalized 0..1000 coordinates [x, y] (where x is horizontal 0..1000 and y is vertical 0..1000):
{
  "corners_1000": [[x_tl, y_tl], [x_tr, y_tr], [x_br, y_br], [x_bl, y_bl]]
}"""
    for model in ["gemini-3.1-pro-preview"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [_b64_image_part(still_path), {"text": prompt}]}],
                "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            txt = data["candidates"][0]["content"]["parts"][0]["text"]
            pts = json.loads(txt)["corners_1000"]
            poly_4k = np.array([[p[0] * 3.84, p[1] * 2.16] for p in pts], dtype=np.float32)
            x1 = max(0, int(np.min(poly_4k[:, 0])) - 80)
            y1 = max(0, int(np.min(poly_4k[:, 1])) - 80)
            x2 = min(3840, int(np.max(poly_4k[:, 0])) + 80)
            y2 = min(2160, int(np.max(poly_4k[:, 1])) + 80)
            return (x1, y1, x2, y2), poly_4k
        except Exception as e:
            print(f"  [Polygon detect warn {model}]: {e}", flush=True)
    poly_4k = np.array([[1420, 320], [2420, 320], [2420, 1780], [1420, 1780]], dtype=np.float32)
    return (1340, 240, 2500, 1860), poly_4k

def generate_clean_veo31_pushin(still_path: str, out_raw_4k60: str, motion_desc: str) -> bool:
    """
    Generates an 8s 1080p clip on Vertex AI Veo 3.1 with a subtle 2.6% centered push-in lastFrame
    so Veo NEVER zooms out or hallucinates frame borders, then scales cleanly (NO unsharp) to 4K60.
    """
    src_b64 = base64.b64encode(Path(still_path).read_bytes()).decode("utf-8")
    im = Image.open(still_path).convert("RGB")
    w_im, h_im = im.size
    cw, ch = int(w_im * 0.974), int(h_im * 0.974)
    lx, ly = (w_im - cw) // 2, (h_im - ch) // 2
    lf_tmp = out_raw_4k60 + "_lf.jpg"
    im.crop((lx, ly, lx + cw, ly + ch)).resize((w_im, h_im), Image.Resampling.LANCZOS).save(lf_tmp, quality=96)
    lf_b64 = base64.b64encode(Path(lf_tmp).read_bytes()).decode("utf-8")

    for model in ["veo-3.1-generate-001", "veo-3.1-generate-preview", "veo-3.1-fast-generate-001"]:
        try:
            token = get_vertex_token()
            url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:predictLongRunning"
            instance = {
                "prompt": motion_desc,
                "image": {"bytesBase64Encoded": src_b64, "mimeType": "image/jpeg"},
                "lastFrame": {"bytesBase64Encoded": lf_b64, "mimeType": "image/jpeg"}
            }
            payload = {
                "instances": [instance],
                "parameters": {"aspectRatio": "16:9", "durationSeconds": 8, "resolution": "1080p"}
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                op_name = json.loads(resp.read().decode("utf-8"))["name"]
            poll_url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:fetchPredictOperation"
            for _ in range(80):
                time.sleep(6)
                tk = get_vertex_token()
                preq = urllib.request.Request(poll_url, data=json.dumps({"operationName": op_name}).encode("utf-8"), headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(preq, timeout=45) as presp:
                    pdata = json.loads(presp.read().decode("utf-8"))
                if pdata.get("done"):
                    vids = pdata.get("response", {}).get("videos", [])
                    if vids and "bytesBase64Encoded" in vids[0]:
                        veo_1080 = out_raw_4k60 + "_1080.mp4"
                        Path(veo_1080).write_bytes(base64.b64decode(vids[0]["bytesBase64Encoded"]))
                        ok = master_raw_video_to_4k60(veo_1080, out_raw_4k60, "16:9")
                        for f in (veo_1080, lf_tmp):
                            if os.path.exists(f): os.remove(f)
                        if ok:
                            return True
                    break
        except Exception as e:
            print(f"  [Veo 3.1 warn {model}]: {e}", flush=True)
    return False

BESPOKE_VIDEOS = [
    ("CS_02_SAN_FRANCISCO_OCEAN_BEACH_SeaKelp_Dark_Tonal_Slate_Stone",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the matte sea-kelp green Surf Clock on dark slate stone while a soft museum rim-light glides smoothly across the dark tonal backdrop. Strictly slow forward push-in ONLY."),
    ("CS_03_PORTUGAL_ERICEIRA_Warm_Sand_Travertine_and_Belgian_Linen",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the warm sand Surf Clock on Roman travertine stone and raw Belgian linen as warm morning gallery light softly shifts across the sand plaster wall. Strictly slow forward push-in ONLY."),
    ("CS_04_HAWAII_NORTH_SHORE_Pure_Gallery_White_and_Alabaster",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the two-tone chalk-white and Pacific navy Surf Clock on honed white alabaster in a pure white gallery cyclorama as soft museum light drifts gently. Strictly slow forward push-in ONLY."),
    ("CS_05_SOCAL_MALIBU_TRESTLES_Terracotta_Clay_on_Sand_Plaster",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the desert terracotta Surf Clock on warm sand Venetian plaster as a soft golden-hour studio shadow glides subtly across the backdrop. Strictly slow forward push-in ONLY."),
    ("CS_06_BYRON_GOLD_COAST_Pebble_Putty_on_Raw_Belgian_Linen",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the pebble-putty and charcoal Surf Clock on pale limestone and oat Belgian linen as diffused daylight gently shifts. Strictly slow forward push-in ONLY."),
    ("CS_07_FRANCE_BIARRITZ_HOSSEGOR_Oxblood_on_Dark_Tonal_Basalt",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the deep Bordeaux oxblood Surf Clock on dark basalt stone as a dramatic warm rim-light glides across the matching dark tonal burgundy backdrop. Strictly slow forward push-in ONLY."),
    ("CS_08_SANTA_CRUZ_Matte_Obsidian_Black_on_Honed_Limestone",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the matte obsidian black Surf Clock on honed sand-beige limestone as soft architectural side light moves gently across the white gallery wall. Strictly slow forward push-in ONLY."),
    ("CS_09_MONTAUK_EAST_END_Dune_Sand_on_Bleached_Linen_and_Stone",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the coastal dune-sand and slate Surf Clock on travertine stone and bleached Belgian linen in soft coastal studio light. Strictly slow forward push-in ONLY."),
    ("CS_10_SYDNEY_BONDI_EAST_Pure_White_Monochrome_on_Carrara_Marble",
     "ARRI Alexa 65 85mm Master Prime studio shot: slow, buttery 2.5% forward camera dolly push-in toward the pure matte white Surf Clock on honed white Carrara marble as soft museum shadow sculpts the white-on-white gallery set. Strictly slow forward push-in ONLY."),
]

def process_one_video(tag, prompt):
    still_path = f"{STILLS_DIR}/{tag}_4K.jpg"
    final_4k60 = f"{CLIPS_DIR}/{tag}_4K60.mp4"
    if os.path.exists(final_4k60) and os.path.getmtime(final_4k60) > os.path.getmtime(still_path) and os.path.getsize(final_4k60) > 5_000_000:
        print(f"[{tag}] Already mastered & up-to-date ({round(os.path.getsize(final_4k60)/1e6, 1)} MB), skipping!", flush=True)
        return tag, True

    raw_veo_4k60 = f"{RAW_DIR}/{tag}_VEO_RAW_4K60.mp4"
    print(f"[{tag}] 1/3 Generating Veo 3.1 studio clip...", flush=True)
    ok = generate_clean_veo31_pushin(still_path, raw_veo_4k60, prompt)
    if not ok:
        print(f"[{tag}] Veo 3.1 failed!", flush=True)
        return tag, False
    print(f"[{tag}] 2/3 Detecting front bezel 4K polygon...", flush=True)
    roi_4k, poly_4k = detect_front_bezel_polygon_4k(still_path)
    print(f"[{tag}] 3/3 Running SIFT Sub-Pixel Homography Relit 4K60 Mastering...", flush=True)
    fast_master_shot(tag, [(roi_4k, poly_4k)], src_vid_override=raw_veo_4k60)
    return tag, True

if __name__ == "__main__":
    print("[V8_050] Mastering 3-Up Global Constellation on clean Veo motion...", flush=True)
    orig_v8_050_veo = f"{RAW_DIR}/V8_050_ZERO_GRAVITY_Three_Colorways_Floating_ZeroG_Constellation_ORIGINAL_VEO_BACKUP.mp4"
    fast_master_shot(
        "V8_050_ZERO_GRAVITY_Three_Colorways_Floating_ZeroG_Constellation",
        [
            ((340, 420, 1340, 1530), np.array([[358, 605], [418, 530], [1048, 442], [1322, 1368], [685, 1498], [612, 1518]], dtype=np.float32)),
            ((1360, 420, 2450, 1700), np.array([[1525, 480], [2385, 515], [2265, 1650], [1400, 1585]], dtype=np.float32)),
            ((2620, 460, 3480, 1510), np.array([[2665, 595], [3290, 490], [3430, 1385], [2785, 1475]], dtype=np.float32)),
        ],
        src_vid_override=orig_v8_050_veo
    )
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(process_one_video, t, p) for t, p in BESPOKE_VIDEOS]
        for f in as_completed(futs):
            t, ok = f.result()
            print(f"[{t}] DONE: {ok}", flush=True)
    os.system("python3 /Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/build_bespoke_lookbook.py")
    os.system("python3 /Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts/build_interactive_lookbook.py")
    print("ALL BESPOKE STUDIO 4K60 VIDEOS & LOOKBOOKS MASTERED!", flush=True)
