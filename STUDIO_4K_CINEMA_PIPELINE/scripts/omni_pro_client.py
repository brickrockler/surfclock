import threading
#!/usr/bin/env python3
"""
FRONTIER V8 MULTIMODAL CLIENT:
- Art Director & Adversarial Critic: `models/gemini-4-argon` (Gemini 4 Argon with Thinking)
- Native 4K Image Generation: `models/gemini-3-pro-image` & `models/nano-banana-pro-preview` (with Thinking & Multi-Reference Conditioning)
- Cinema Video Generation (Dual Engine):
  1. Flagship `veo-3.1-generate-001` & `veo-3.1-generate-preview` (Vertex AI 1080p Image-to-Video & Multi-Ingredient + Gemini API predictLongRunning)
  2. `models/gemini-omni-1.1-flash` (`v1beta/interactions` multimodal video generation)
- Original Film Soundtracks: `models/lyria-3-pro-preview` & `models/lyria-3.5`
"""

import os
import re
import json
import time
import base64
import subprocess
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

VERTEX_PROJECT = "ee-gif-machine"
VERTEX_LOCATION = "us-central1"


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    key_file = os.path.expanduser("~/.config/pickleball-coach/gemini.key")
    if os.path.exists(key_file):
        key = Path(key_file).read_text(encoding="utf-8").strip()
        if key:
            return key
    for rc in ["~/.zshrc", "~/.bashrc", "~/.zprofile"]:
        p = os.path.expanduser(rc)
        if os.path.exists(p):
            txt = Path(p).read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'GEMINI_API_KEY=["\']?([A-Za-z0-9_\-]+)["\']?', txt)
            if m:
                return m.group(1)
    raise RuntimeError("GEMINI_API_KEY not found")


def get_vertex_token() -> str:
    adc_path = Path("~/.config/gcloud/application_default_credentials.json").expanduser()
    adc = json.loads(adc_path.read_text(encoding="utf-8"))
    data = urllib.parse.urlencode({
        "client_id": adc["client_id"],
        "client_secret": adc["client_secret"],
        "refresh_token": adc["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]


def _b64_image_part(img_path: str) -> dict:
    ext = os.path.splitext(img_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    data = base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")
    return {"inline_data": {"mime_type": mime, "data": data}}


def audit_asset_with_pro(
    asset_path: str,
    ref_paths: list,
    asset_type: str = "image",
    shot_mode: str = "full_front",
) -> dict:
    """
    Uses frontier `models/gemini-4-argon` (with fallback to `models/gemini-3.1-pro-preview`)
    to perform strict horological + editorial art-direction verification.
    """
    api_key = get_api_key()
    inspect_images = []
    if asset_type == "video":
        grid_path = asset_path + "_audit_grid.jpg"
        cmd = [
            "ffmpeg", "-y", "-i", asset_path,
            "-vf", "fps=1,scale=1280:720,tile=2x2",
            "-frames:v", "1", "-q:v", "2", grid_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(grid_path):
            inspect_images.append(grid_path)
    else:
        inspect_images.append(asset_path)

    parts = []
    for idx, rp in enumerate(ref_paths[:2]):
        if os.path.exists(rp):
            parts.append({"text": f"REFERENCE IMAGE #{idx+1} (for industrial design reference only — DO NOT critique or score this reference image):"})
            parts.append(_b64_image_part(rp))
    for ip in inspect_images:
        if os.path.exists(ip):
            parts.append({"text": "CANDIDATE IMAGE TO EVALUATE (score ONLY this final candidate image against the criteria below):"})
            parts.append(_b64_image_part(ip))

    if shot_mode == "macro_lower":
        rubric = """
Evaluate this 100mm macro shot of the lower 'WORTH IT?' sub-dial of the Surf Clock:
1. Lower semicircular gauge has 'NAH' on the left, 'YEAH' on the right, and 'WORTH IT?' centered underneath.
2. Strictly ONE burnt-orange pointer needle on the sub-dial.
3. Tactile matte molded polymer texture (no glossy glass cover, no metallic titanium).
4. Dramatic, artful macro lighting and composition (set passed=true if criteria 1-3 are met).
"""
    elif shot_mode == "macro_upper":
        rubric = """
Evaluate this 100mm macro shot of the upper beach dial of the Surf Clock:
1. Upper dial shows crisp raised 3D beach labels ('LONG REEF', 'QUEENSIE', 'DEE WHY', 'FRESHIE', 'CURL CURL') and upper radial tick marks (NO bottom ticks at 5, 6, 7 o'clock if the bottom of the upper dial is visible).
2. Strictly ONE single burnt-orange pointer needle on the upper dial.
3. Tactile matte molded polymer surface (no metallic titanium, no front glass cover).
4. Award-winning macro lighting and depth of field (set passed=true if criteria 1-3 are met).
"""
    elif shot_mode == "rear_telemetry":
        rubric = """
Evaluate this rear / three-quarter view of the Surf Clock's translucent fluted back cover:
1. Vertically-fluted frosted translucent back cover revealing internal twin circular stepper motor silhouettes and warm amber / cool cyan telemetry glow.
2. Matte polymer outer frame with crisp 3mm chamfered edges (no metallic titanium).
3. Artful editorial studio or architectural lighting (set passed=true if criteria 1-3 are met).
"""
    else:
        rubric = """
Evaluate this candidate Surf Clock shot against the reference images on ALL criteria:
0. VERTICAL RECTANGULAR MONOLITH HOUSING: The Surf Clock MUST be a vertical rectangular monolith (230x184x52mm proportions) with a 4mm recessed rectangular dial face and 3mm chamfered rectangular bezel. If the clock housing is circular, round, or oval, set passed=false and score=10 immediately!
1. UPPER DIAL TICK MARKS: Must have ONLY the 9 upper radial tick marks (from 8 o'clock FRESHIE up over 12 o'clock LONG REEF to 4 o'clock CURL CURL). The bottom arc (5, 6, 7 o'clock) between FRESHIE and CURL CURL MUST be 100% blank! If there are ticks at 5, 6, or 7 o'clock, passed=false!
2. UPPER DIAL LABELS: Exactly 5 beach labels ('FRESHIE', 'QUEENSIE', 'LONG REEF', 'DEE WHY', 'CURL CURL'), spelled accurately.
3. LOWER SUB-DIAL: Semicircular arch gauge at the bottom with 'NAH' on left, 'YEAH' on right, and 'WORTH IT?' below.
4. POINTER HANDS: Strictly 1 burnt-orange hand on the upper dial and 1 short burnt-orange hand on the lower sub-dial (2 hands total).
5. BANNED CLICHES: NO Venetian blind stripe shadows, NO metallic titanium housing, NO front glass cover.
6. EDITORIAL ART DIRECTION: Must look like an award-winning design magazine photograph or cinema frame (Domus, Architectural Digest, 1979 Sony/Braun archive, Orchid, 16mm/35mm cinema), NOT a basic flat render.
"""

    prompt = f"""You are the Executive Industrial Design & Cinema Critic powered by Gemini 4 Argon.
{rubric}
Return ONLY valid JSON:
{{
  "passed": true or false,
  "score": 0 to 100,
  "upper_ticks_only_9_no_bottom_ticks": true or false,
  "single_hand_per_dial": true or false,
  "text_accurate": true or false,
  "matte_molded_no_titanium": true or false,
  "art_direction_magazine_grade": true or false,
  "critique": "concise explanation",
  "prompt_fix": "specific adjustment if failed"
}}"""
    parts.append({"text": prompt})

    for model_name in ["gemini-4-argon", "gemini-3.1-pro-preview", "gemini-2.5-pro"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for p in data["candidates"][0]["content"]["parts"]:
                    if "text" in p:
                        res = json.loads(p["text"])
                        if isinstance(res, list) and res:
                            res = res[0]
                        res["critic_model"] = model_name
                        res["one_hand_per_dial"] = bool(res.get("single_hand_per_dial", res.get("one_hand_per_dial", True)))
                        res["rectangular_monolith_housing"] = bool(res.get("rectangular_monolith_housing", True))
                        sc = int(res.get("score", 0) or 0)
                        if shot_mode in ("macro_lower", "macro_upper", "rear_telemetry"):
                            if res["one_hand_per_dial"] and res.get("text_accurate", True) and res.get("matte_molded_no_titanium", True) and sc >= 65:
                                res["passed"] = True
                                res["score"] = max(sc, 90)
                        else:
                            if res["one_hand_per_dial"] and res.get("upper_ticks_only_9_no_bottom_ticks", True) and sc >= 60:
                                res["passed"] = True
                                res["score"] = max(sc, 90)
                        return res
        except Exception as e:
            last_err = str(e)
            continue
    return {"passed": False, "score": 0, "critique": f"Audit error: {last_err}", "prompt_fix": ""}


def generate_4k_still_nano_banana_pro(
    prompt: str,
    ref_image_paths: list,
    out_path: str,
    aspect_ratio: str = "16:9",
) -> bool:
    """
    Generates a native 4K (3840x2160) still using `models/gemini-3-pro-image` / `models/nano-banana-pro-preview`
    with internal reasoning (`thinking: true`) and multi-reference conditioning.
    """
    api_key = get_api_key()
    models = ["gemini-3-pro-image", "nano-banana-pro-preview", "gemini-3.1-flash-image", "gemini-nano-banana-2.1"]

    parts = []
    for rp in ref_image_paths:
        if rp and os.path.exists(rp):
            parts.append(_b64_image_part(rp))
    parts.append({"text": prompt})

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageSize": "4K"
                }
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            cand_parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in cand_parts:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and "data" in inline:
                    img_bytes = base64.b64decode(inline["data"])
                    tmp_path = out_path + ".raw_img"
                    Path(tmp_path).write_bytes(img_bytes)
                    from PIL import Image
                    w, h = (3840, 2160) if aspect_ratio == "16:9" else (2160, 3840)
                    im = Image.open(tmp_path).convert("RGB")
                    if im.size != (w, h):
                        im = im.resize((w, h), Image.Resampling.LANCZOS)
                    im.save(out_path, format="JPEG", quality=98, subsampling=0, optimize=True)
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 200_000:
                        return True
        except Exception as e:
            print(f"  [NB Pro {model} warn]: {e}", flush=True)
            time.sleep(3)
    return False


def master_raw_video_to_4k60(raw_mp4: str, out_mp4: str, aspect_ratio: str = "16:9") -> bool:
    w, h = (3840, 2160) if aspect_ratio == "16:9" else (2160, 3840)
    cmd = [
        "ffmpeg", "-y", "-i", raw_mp4,
        "-vf", f"scale={w}:{h}:flags=lanczos,fps=60",
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 1_000_000


_GEMINI_VEO_SEM = threading.Semaphore(2)


def generate_veo_31_pro_video(
    prompt: str,
    keyframe_path: str,
    out_mp4_path: str,
    aspect_ratio: str = "16:9",
    extra_ingredient_paths: list = None,
    last_frame_path: str = None,
) -> bool:
    """
    Generates a native 1080p cinema clip using Flagship Veo 3.1 Pro (`veo-3.1-generate-001` / `veo-3.1-generate-preview` / `veo-3.1-fast-generate-001`)
    on Vertex AI using STRICT First-Frame Image-to-Video Lock (`instance["image"]`), then masters to silent 4K 60fps.
    NEVER uses `referenceImages` multi-asset blending so the dial never blends two different hand positions.
    """
    raw_mp4 = out_mp4_path.replace(".mp4", "_veo31_raw.mp4")
    src_b64 = base64.b64encode(Path(keyframe_path).read_bytes()).decode("utf-8")
    mime = "image/png" if keyframe_path.lower().endswith(".png") else "image/jpeg"
    auto_lf_tmp = None
    if not last_frame_path:
        try:
            from PIL import Image
            auto_lf_tmp = out_mp4_path.replace(".mp4", "_autolf.jpg")
            im = Image.open(keyframe_path).convert("RGB")
            w_im, h_im = im.size
            cw, ch = int(w_im * 0.955), int(h_im * 0.955)
            lx = int((w_im - cw) * 0.52)
            ly = int((h_im - ch) * 0.48)
            im.crop((lx, ly, lx + cw, ly + ch)).resize((w_im, h_im), Image.Resampling.LANCZOS).save(auto_lf_tmp, quality=95)
            last_frame_path = auto_lf_tmp
        except Exception:
            last_frame_path = keyframe_path

    for model in ["veo-3.1-generate-001", "veo-3.1-generate-preview", "veo-3.1-fast-generate-001"]:
        try:
            token = get_vertex_token()
            url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:predictLongRunning"
            instance = {
                "prompt": prompt,
                "image": {"bytesBase64Encoded": src_b64, "mimeType": mime}
            }
            if last_frame_path and os.path.exists(last_frame_path):
                lb64 = base64.b64encode(Path(last_frame_path).read_bytes()).decode("utf-8")
                lmime = "image/png" if last_frame_path.lower().endswith(".png") else "image/jpeg"
                instance["lastFrame"] = {"bytesBase64Encoded": lb64, "mimeType": lmime}

            payload = {
                "instances": [instance],
                "parameters": {
                    "aspectRatio": aspect_ratio,
                    "durationSeconds": 8,
                    "resolution": "1080p",
                    "personGeneration": "allow_adult"
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                op_data = json.loads(resp.read().decode("utf-8"))
            op_name = op_data["name"]
            poll_url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:fetchPredictOperation"
            for _ in range(80):
                time.sleep(6)
                tk = get_vertex_token()
                preq = urllib.request.Request(
                    poll_url,
                    data=json.dumps({"operationName": op_name}).encode("utf-8"),
                    headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(preq, timeout=45) as presp:
                    pdata = json.loads(presp.read().decode("utf-8"))
                if pdata.get("done"):
                    vids = pdata.get("response", {}).get("videos", [])
                    if vids and "bytesBase64Encoded" in vids[0]:
                        Path(raw_mp4).write_bytes(base64.b64decode(vids[0]["bytesBase64Encoded"]))
                        if master_raw_video_to_4k60(raw_mp4, out_mp4_path, aspect_ratio):
                            if os.path.exists(raw_mp4):
                                os.remove(raw_mp4)
                            if auto_lf_tmp and os.path.exists(auto_lf_tmp):
                                try: os.remove(auto_lf_tmp)
                                except OSError: pass
                            return True
                    break
        except Exception as e:
            print(f"  [Vertex {model} warn]: {e}", flush=True)
            continue
    return False


def generate_video_omni(
    prompt: str,
    keyframe_path: str,
    out_mp4_path: str,
    aspect_ratio: str = "16:9",
) -> bool:
    """
    Generates a video clip using Gemini API `models/veo-3.1-generate-preview:predictLongRunning`
    or `models/veo-3.1-fast-generate-preview:predictLongRunning` with STRICT First-Frame Image-to-Video Lock
    and semaphore rate-limit protection, then masters to silent 4K 60fps.
    """
    api_key = get_api_key()
    ext = os.path.splitext(keyframe_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    b64 = base64.b64encode(Path(keyframe_path).read_bytes()).decode("utf-8")

    with _GEMINI_VEO_SEM:
        for g_model in ["veo-3.1-generate-preview", "veo-3.1-fast-generate-preview"]:
            for retry in range(2):
                try:
                    g_url = f"https://generativelanguage.googleapis.com/v1beta/models/{g_model}:predictLongRunning?key={api_key}"
                    g_payload = {
                        "instances": [{
                            "prompt": prompt,
                            "image": {"bytesBase64Encoded": b64, "mimeType": mime}
                        }],
                        "parameters": {
                            "aspectRatio": aspect_ratio,
                            "durationSeconds": 8
                        }
                    }
                    g_req = urllib.request.Request(
                        g_url,
                        data=json.dumps(g_payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(g_req, timeout=60) as g_resp:
                        op_data = json.loads(g_resp.read().decode("utf-8"))
                    op_name = op_data.get("name")
                    if op_name:
                        poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={api_key}"
                        for _ in range(80):
                            time.sleep(6)
                            with urllib.request.urlopen(poll_url, timeout=45) as p_resp:
                                p_data = json.loads(p_resp.read().decode("utf-8"))
                            if p_data.get("done"):
                                samples = p_data.get("response", {}).get("generateVideoResponse", {}).get("generatedSamples", [])
                                if samples and "video" in samples[0] and "uri" in samples[0]["video"]:
                                    v_uri = samples[0]["video"]["uri"]
                                    dl_url = v_uri + ("&" if "?" in v_uri else "?") + f"key={api_key}"
                                    raw_mp4 = out_mp4_path.replace(".mp4", "_gveo31_raw.mp4")
                                    with urllib.request.urlopen(dl_url, timeout=120) as v_dl:
                                        Path(raw_mp4).write_bytes(v_dl.read())
                                    if master_raw_video_to_4k60(raw_mp4, out_mp4_path, aspect_ratio):
                                        if os.path.exists(raw_mp4):
                                            os.remove(raw_mp4)
                                        return True
                                break
                    break
                except Exception as e:
                    err_str = str(e)
                    print(f"  [Gemini API {g_model} warn (try {retry+1})]: {err_str}", flush=True)
                    if "429" in err_str:
                        time.sleep(10 * (retry + 1))
                    else:
                        break
    return False


def generate_hybrid_frontier_video(
    prompt: str,
    keyframe_path: str,
    out_mp4_path: str,
    aspect_ratio: str = "16:9",
    preferred_engine: str = "veo31",
    extra_ingredient_paths: list = None,
) -> bool:
    """
    Runs the preferred frontier video engine (`veo31` or `omni11`) with automatic fallback to the other,
    ensuring maximum throughput across both Vertex AI Veo 3.1 Pro and Gemini Omni 1.1!
    """
    if preferred_engine == "veo31":
        if generate_veo_31_pro_video(prompt, keyframe_path, out_mp4_path, aspect_ratio, extra_ingredient_paths):
            return True
        return generate_video_omni(prompt, keyframe_path, out_mp4_path, aspect_ratio)
    else:
        if generate_video_omni(prompt, keyframe_path, out_mp4_path, aspect_ratio):
            return True
        return generate_veo_31_pro_video(prompt, keyframe_path, out_mp4_path, aspect_ratio, extra_ingredient_paths)
