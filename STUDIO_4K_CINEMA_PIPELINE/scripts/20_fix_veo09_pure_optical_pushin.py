#!/usr/bin/env python3
import os, sys, time, json, base64, subprocess, shutil, urllib.request, urllib.parse
from pathlib import Path
import cv2
import numpy as np

PIPE_DIR = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
NB_PRO_DIR = PIPE_DIR / "01_4K_STUDIO_KEYFRAMES_AND_STILLS" / "NANO_BANANA_PRO_BLUE_4K"
VEO_RAW_DIR = PIPE_DIR / "raw_renders" / "v2_veo31_pro_raw"
CLIPS_16x9_DIR = PIPE_DIR / "02_INDIVIDUAL_4K_CLIPS_16x9"
MASTER_DIR = PIPE_DIR / "00_MASTER_SHOWREELS"
AUDIT_DIR = PIPE_DIR / "04_CONTACT_SHEETS_AND_AUDIT"
ART_DIR = Path("/Users/jcolley/.gemini/jetski/brain/47620447-b5c2-401d-af72-8cea98f34b48")

VERTEX_PROJECT = "ee-gif-machine"
VERTEX_LOCATION = "us-central1"

def get_vertex_token() -> str:
    adc = json.loads(Path("~/.config/gcloud/application_default_credentials.json").expanduser().read_text())
    data = urllib.parse.urlencode({
        "client_id": adc["client_id"],
        "client_secret": adc["client_secret"],
        "refresh_token": adc["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]

p09_s = NB_PRO_DIR / "NB_PRO_MACRO_06_SubtleStart_4K.jpg"
p09_e = NB_PRO_DIR / "NB_PRO_MACRO_06_SubtleEnd_4K.jpg"
b64_s = base64.b64encode(p09_s.read_bytes()).decode("utf-8")
b64_e = base64.b64encode(p09_e.read_bytes()).decode("utf-8")

token = get_vertex_token()
model = "veo-3.1-generate-001"
url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:predictLongRunning"
payload = {
    "instances": [{
        "prompt": (
            "Ultra-slow, subtle 85mm macro studio camera push-in at a steep grazing angle onto the smooth 0.90mm radiused rectangular top-left bevel "
            "and deeply recessed open matte navy dial cavity of the Braun Surf Clock. Soft natural cool-blue studio rim light rests gently on the matte bevel "
            "while the burnt-orange pointer hand points cleanly to DEE WHY. Realistic Hasselblad macro photography, zero lasers, zero neon lines."
        ),
        "image": {"bytesBase64Encoded": b64_s, "mimeType": "image/jpeg"},
        "lastFrame": {"bytesBase64Encoded": b64_e, "mimeType": "image/jpeg"},
    }],
    "parameters": {"aspectRatio": "16:9", "durationSeconds": 8, "personGeneration": "allow_adult"}
}
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=60) as resp:
    op_name = json.loads(resp.read().decode("utf-8"))["name"]
print(f"[STARTED VERTEX VEO_PRO_09 OPTICAL PUSH-IN] {op_name.split('/')[-1]}", flush=True)

raw_09 = VEO_RAW_DIR / "VEO_PRO_09_Macro_85mm_GrazingBevel_PureOptical_raw_v3.mp4"
out_09 = CLIPS_16x9_DIR / "VEO_PRO_09_Macro_85mm_GrazingBevel_CyanLaserSweep_4K.mp4"
poll_url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:fetchPredictOperation"
for _ in range(95):
    time.sleep(7)
    token = get_vertex_token()
    preq = urllib.request.Request(poll_url, data=json.dumps({"operationName": op_name}).encode("utf-8"), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(preq, timeout=45) as presp:
        pdata = json.loads(presp.read().decode("utf-8"))
    if pdata.get("done"):
        videos = pdata.get("response", {}).get("videos", [])
        if videos and videos[0].get("bytesBase64Encoded"):
            raw_09.write_bytes(base64.b64decode(videos[0]["bytesBase64Encoded"]))
            subprocess.run([
                "ffmpeg", "-y", "-i", str(raw_09),
                "-vf", "fps=60,scale=3840:2160:flags=lanczos,unsharp=3:3:0.35:3:3:0.0,format=yuv420p",
                "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15",
                str(out_09)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"[FIXED VEO_PRO_09 PURE OPTICAL 4K60] {out_09.name} ({out_09.stat().st_size/1e6:.2f} MB)", flush=True)
            break

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(PIPE_DIR / "raw_renders" / "master_16x9_concat.txt"),
    "-c", "copy", str(MASTER_DIR / "SURF_CLOCK_4K_60FPS_MASTER_COMMERCIAL_16x9.mp4")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(PIPE_DIR / "raw_renders" / "master_veo_concat.txt"),
    "-c", "copy", str(MASTER_DIR / "SURF_CLOCK_4K_60FPS_VEO31_AND_OMNI_AI_SHOWCASE_16x9.mp4")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

all_12_veo = [
    "VEO_PRO_01_Signature_SlateBlue_Caustic_And_HandSweep_4K.mp4",
    "VEO_PRO_02_DarkBasalt_Monolith_PetrolBlue_CausticSweep_4K.mp4",
    "VEO_PRO_03_Brushed_BlueSteel_AudioLab_RimSweep_4K.mp4",
    "VEO_PRO_04_Twilight_Concrete_GlassCaustics_Sweep_4K.mp4",
    "VEO_PRO_05_MidnightIndigo_Marmorino_MoonlightLouvers_4K.mp4",
    "VEO_PRO_06_SmokedSapphire_USM_Credenza_CausticGlint_4K.mp4",
    "VEO_PRO_07_Macro_100mm_UpperDial_SmoothBraun_HandSweep_4K.mp4",
    "VEO_PRO_08_Macro_100mm_LowerWorthIt_NahToYeah_Sweep_4K.mp4",
    "VEO_PRO_09_Macro_85mm_GrazingBevel_CyanLaserSweep_4K.mp4",
    "VEO_PRO_10_RearFrosted_Borosilicate_FlutedCausticSweep_4K.mp4",
    "VEO_PRO_11_LuxuryFinish_Morph_MidnightNavy_To_TitaniumSilver_4K.mp4",
    "VEO_PRO_12_LuxuryFinish_Morph_StealthGraphite_To_PetrolCeramic_4K.mp4",
]
rows = []
for name in all_12_veo:
    cap = cv2.VideoCapture(str(CLIPS_16x9_DIR / name))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    idxs = [int(n*0.08), int(n*0.36), int(n*0.64), int(n*0.92)]
    frames = []
    for idx in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, fr = cap.read()
        fr = cv2.resize(fr, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(fr, f"{name[:20]} f={idx}", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 230, 140), 2)
        frames.append(fr)
    cap.release()
    rows.append(np.hstack(frames))

final_veo_sheet = AUDIT_DIR / "V2_ALL_12_VEO_PRO_FINAL_VERIFIED_SHEET.jpg"
cv2.imwrite(str(final_veo_sheet), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 93])
shutil.copy2(final_veo_sheet, ART_DIR / final_veo_sheet.name)
print("[DONE PURE OPTICAL VEO_PRO_09 & UPDATED SHEET]", flush=True)
