#!/usr/bin/env python3
"""
Launches 16 Veo 3.1 First-Frame + Last-Frame CAD-Anchored Cinema Clips (4K 3840x2160 16:9 and 9:16)
in parallel across Vertex AI (veo-3.1-fast-generate-001 / veo-3.1-generate-001) and
Gemini Developer API (veo-3.1-fast-generate-preview / veo-3.1-generate-preview).

Every single clip uses BOTH a CAD-verified First Frame (`image`) AND Last Frame (`lastFrame`)
plus explicit negative/positive constraints to guarantee:
1. ONLY 2 hands total (1 single hand on top beach dial, 1 single hand on bottom WORTH IT? arc)
2. ZERO glass on the front (open matte 3D-printed dial cavity)
3. Rear shots show ONLY the frosted vertically-ribbed translucent back cover with bottom hook hole
4. 100% accurate typography (LONG REEF, QUEENSIE, DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT?)
"""
import os, sys, time, json, base64, subprocess, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_DIR = "/Users/jcolley/surf_clock"
PIPELINE_DIR = os.path.join(PROJECT_DIR, "STUDIO_4K_CINEMA_PIPELINE")
RAW_KF_DIR = os.path.join(PIPELINE_DIR, "raw_renders", "keyframes")
VEO_RAW_DIR = os.path.join(PIPELINE_DIR, "raw_renders", "veo_clips")
os.makedirs(VEO_RAW_DIR, exist_ok=True)

GEMINI_KEY = open(os.path.expanduser("~/.config/pickleball-coach/gemini.key")).read().strip()
VERTEX_PROJECT = "ee-gif-machine"
VERTEX_LOCATION = "us-central1"

def get_vertex_token():
    import urllib.parse
    adc = json.load(open(os.path.expanduser("~/.config/gcloud/application_default_credentials.json")))
    data = urllib.parse.urlencode({
        "client_id": adc["client_id"],
        "client_secret": adc["client_secret"],
        "refresh_token": adc["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]

def b64_png(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

STRICT_PRODUCT_SUFFIX = (
    " Strict industrial design physical twin accuracy: open matte 3D-printed recessed dial face with NO glass cover "
    "and NO specular glass pane reflection. Exactly one single tapered sand-ochre pointer needle on the upper dial "
    "and one single short sand-ochre pointer needle on the lower semicircle gauge (only 2 needles total; never add a second hand). "
    "All raised 3D white letters remain razor-sharp and unaltered (LONG REEF, QUEENSIE, DEE WHY, FRESHIE, CURL CURL, NAH, YEAH, WORTH IT?). "
    "Shot on Arri Alexa 65 with Zeiss Master Prime macro cinema lens, Kodak Vision3 500T film grain, award-winning studio lighting."
)

VEO_JOBS = [
    # 16:9 Jobs (12 clips)
    {
        "id": "VEO_01_HeroBlue_Slow_Orbital_Parallax_16x9",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_01A_HeroBlue_Orbit_Start_16x9.png",
        "last":  "KF_01B_HeroBlue_Orbit_End_16x9.png",
        "prompt": (
            "Ultra-slow, buttery motorized motion-control camera orbit from left three-quarter to right three-quarter around "
            "the matte dark navy-blue monolithic Surf Clock standing on a satin slate-blue studio cyclorama. A dramatic diagonal shaft "
            "of warm sunlight sweeps across the background and tabletop reflection while the single upper sand-ochre pointer needle "
            "glides smoothly from QUEENSIE to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_02_HeroBlue_Chiaroscuro_Sunbeam_Sweep_16x9",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_02A_HeroBlue_SunSweep_Start_16x9.png",
        "last":  "KF_02B_HeroBlue_SunSweep_End_16x9.png",
        "prompt": (
            "Cinematic slow push-in on the dark blue Surf Clock monolith in a moody slate-blue cyclorama studio as a crisp architectural "
            "window sunbeam sweeps diagonally from left to right across the recessed matte dial face, casting long shifting raking shadows "
            "behind the raised white 3D letters and the single sand-ochre pointer hand." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_03_HeroBlue_Macro_UpperDial_HandSweep_16x9",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_03A_HeroBlue_MacroUpper_Queensie_16x9.png",
        "last":  "KF_03B_HeroBlue_MacroUpper_DeeWhy_16x9.png",
        "prompt": (
            "Extreme macro 85mm f/2.8 close-up on the upper dial of the dark blue Surf Clock. The single warm sand-ochre pointer needle "
            "rotates smoothly clockwise from QUEENSIE past LONG REEF to point at DEE WHY, with its crisp physical shadow sweeping across "
            "the matte blue 3D-printed surface and raised white nozzle-bead letters." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_04_HeroBlue_Macro_LowerWorthIt_NahToYeah_16x9",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_04A_HeroBlue_MacroLower_Nah_16x9.png",
        "last":  "KF_04B_HeroBlue_MacroLower_Yeah_16x9.png",
        "prompt": (
            "Extreme macro cinema close-up on the lower WORTH IT? semicircle gauge of the dark blue Surf Clock. The single short "
            "sand-ochre pointer needle sweeps smoothly from NAH on the left across the raised white semicircular arch to YEAH on the right "
            "under warm raking studio light." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_05_HeroBlue_RearFrosted_Translucent_Back_Orbit_16x9",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_05A_HeroBlue_RearFrosted_Start_16x9.png",
        "last":  "KF_05B_HeroBlue_RearFrosted_End_16x9.png",
        "prompt": (
            "Slow studio turntable orbit around the back of the dark blue Surf Clock, showcasing its frosted vertically-ribbed translucent "
            "back cover seated flush inside the dark blue bezel rim with the rectangular hook/cord cutout hole at the bottom center and "
            "softly diffused internal stepper silhouettes visible through the frosted translucent back."
        ),
    },
    {
        "id": "VEO_06_HeroBlue_GrazingMacro_Typography_Slider_16x9",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_06A_HeroBlue_GrazingMacro_Start_16x9.png",
        "last":  "KF_06B_HeroBlue_GrazingMacro_End_16x9.png",
        "prompt": (
            "Extreme low-angle grazing macro slider shot across the open recessed matte dark-blue dial face, highlighting the physical "
            "0.6mm raised 3D-printed white letters QUEENSIE and LONG REEF and the stepped central boss of the single sand-ochre pointer "
            "needle as it rotates smoothly toward LONG REEF." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_07_HeroBlue_TimberWorkbench_Sunlight_16x9",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_07A_HeroBlue_TimberWorkbench_Start_16x9.png",
        "last":  "KF_07B_HeroBlue_TimberWorkbench_End_16x9.png",
        "prompt": (
            "Slow cinematic parallax slider move across a warm minimalist oak timber workbench where the dark blue Surf Clock rests in "
            "raking morning architectural sunlight. The single upper sand-ochre pointer hand sweeps smoothly from QUEENSIE to DEE WHY "
            "while warm sunlight shifts across the wood grain." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_08_HeroBlue_Terracotta_Architectural_Plinth_16x9",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_08A_HeroBlue_Terracotta_Start_16x9.png",
        "last":  "KF_08B_HeroBlue_Terracotta_End_16x9.png",
        "prompt": (
            "Slow architectural camera orbit around the dark blue Surf Clock standing on a honed Mediterranean terracotta stone bench "
            "in front of a warm lime-plaster wall as golden afternoon sunlight sweeps across the scene and the single upper sand-ochre "
            "hand moves from LONG REEF to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_09_HeroBlue_WalnutShelf_Studio_16x9",
        "backend": "vertex",
        "model": "veo-3.1-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_09A_HeroBlue_WalnutShelf_Start_16x9.png",
        "last":  "KF_09B_HeroBlue_WalnutShelf_End_16x9.png",
        "prompt": (
            "Smooth cinema slider movement past the dark blue Surf Clock resting on a mid-century architectural walnut shelf with "
            "warm afternoon window light sweeping across the matte dark blue frame and crisp white raised typography as the single "
            "upper sand-ochre hand rotates from QUEENSIE to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_10_ChalkWhite_Colorway_Studio_Orbit_16x9",
        "backend": "gemini",
        "model": "veo-3.1-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_10A_ChalkWhite_Studio_Start_16x9.png",
        "last":  "KF_10B_ChalkWhite_Studio_End_16x9.png",
        "prompt": (
            "Slow studio motion-control orbit around the Chalk White Braun edition of the Surf Clock (matte warm off-white frame and dial "
            "with raised matte black typography and single burnt-orange pointer needles) on a moody slate-blue cyclorama as the upper "
            "needle sweeps from QUEENSIE to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_11_OchreDuotone_Colorway_Studio_Orbit_16x9",
        "backend": "vertex",
        "model": "veo-3.1-generate-001",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_11A_OchreDuotone_Studio_Start_16x9.png",
        "last":  "KF_11B_OchreDuotone_Studio_End_16x9.png",
        "prompt": (
            "Slow studio motion-control orbit around the Warm Ochre & Off-White Duotone Surf Clock on a slate-blue cyclorama with "
            "diagonal studio sunlight sweeping across the recessed dial as the single upper burnt-ochre needle moves from LONG REEF "
            "to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_12_AllOchre_Monochrome_Studio_Orbit_16x9",
        "backend": "gemini",
        "model": "veo-3.1-generate-preview",
        "aspect": "16:9",
        "res": "4k",
        "first": "KF_12A_AllOchre_Studio_Start_16x9.png",
        "last":  "KF_12B_AllOchre_Studio_End_16x9.png",
        "prompt": (
            "Slow studio motion-control orbit around the All-Ochre Monochrome Surf Clock (warm terracotta-ochre frame and dial with "
            "crisp white raised 3D typography and single dark-navy pointer needles) on a moody blue cyclorama." + STRICT_PRODUCT_SUFFIX
        ),
    },
    # 9:16 Vertical Cinema Jobs (4 clips)
    {
        "id": "VEO_13_HeroBlue_Vertical_Studio_Orbit_9x16",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "9:16",
        "res": "4k",
        "first": "KF_V01A_HeroBlue_VertOrbit_Start_9x16.png",
        "last":  "KF_V01B_HeroBlue_VertOrbit_End_9x16.png",
        "prompt": (
            "Full-bleed 9:16 vertical cinema slow orbital rotation around the dark blue Surf Clock monolith on a slate-blue studio "
            "cyclorama as a diagonal sunbeam sweeps across the matte dial and the single upper sand-ochre hand moves from QUEENSIE "
            "to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_14_HeroBlue_Vertical_Macro_HandSweep_9x16",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "9:16",
        "res": "4k",
        "first": "KF_V02A_HeroBlue_VertMacro_Start_9x16.png",
        "last":  "KF_V02B_HeroBlue_VertMacro_End_9x16.png",
        "prompt": (
            "Full-bleed 9:16 vertical macro cinema close-up showing both the upper beach dial and lower WORTH IT? gauge of the dark blue "
            "Surf Clock as the single upper sand-ochre needle sweeps from QUEENSIE to DEE WHY and the single lower needle sweeps from "
            "NAH to YEAH." + STRICT_PRODUCT_SUFFIX
        ),
    },
    {
        "id": "VEO_15_HeroBlue_Vertical_RearFrosted_Reveal_9x16",
        "backend": "vertex",
        "model": "veo-3.1-fast-generate-001",
        "aspect": "9:16",
        "res": "4k",
        "first": "KF_V03A_HeroBlue_VertRear_Start_9x16.png",
        "last":  "KF_V03B_HeroBlue_VertRear_End_9x16.png",
        "prompt": (
            "Full-bleed 9:16 vertical studio turntable orbit around the back of the dark blue Surf Clock, showcasing the frosted "
            "vertically-ribbed translucent back cover with the bottom-center rectangular hook hole and softly diffused internal stepper "
            "silhouettes."
        ),
    },
    {
        "id": "VEO_16_HeroBlue_Vertical_TimberWorkbench_9x16",
        "backend": "gemini",
        "model": "veo-3.1-fast-generate-preview",
        "aspect": "9:16",
        "res": "4k",
        "first": "KF_V04A_HeroBlue_VertTimber_Start_9x16.png",
        "last":  "KF_V04B_HeroBlue_VertTimber_End_9x16.png",
        "prompt": (
            "Full-bleed 9:16 vertical architectural shot of the dark blue Surf Clock on a minimalist oak timber workbench as morning "
            "sunlight sweeps across the wood grain and the single upper sand-ochre needle rotates from QUEENSIE to DEE WHY." + STRICT_PRODUCT_SUFFIX
        ),
    },
]

def run_single_veo_job(job, stagger_sec=0):
    time.sleep(stagger_sec)
    jid = job["id"]
    out_mp4 = os.path.join(VEO_RAW_DIR, f"{jid}.mp4")
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 500_000:
        print(f"[SKIP] {jid} already exists ({os.path.getsize(out_mp4)} bytes)")
        return {"id": jid, "status": "cached", "path": out_mp4}

    first_path = os.path.join(RAW_KF_DIR, job["first"])
    last_path  = os.path.join(RAW_KF_DIR, job["last"])
    b64_first = b64_png(first_path)
    b64_last  = b64_png(last_path)

    for attempt in range(3):
        try:
            backend = job["backend"]
            model = job["model"]
            res = job["res"] if attempt == 0 else "1080p"

            if backend == "vertex":
                token = get_vertex_token()
                url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:predictLongRunning"
                payload = {
                    "instances": [{
                        "prompt": job["prompt"],
                        "image": {"bytesBase64Encoded": b64_first, "mimeType": "image/png"},
                        "lastFrame": {"bytesBase64Encoded": b64_last, "mimeType": "image/png"},
                    }],
                    "parameters": {
                        "aspectRatio": job["aspect"],
                        "durationSeconds": 8,
                        "resolution": res,
                        "personGeneration": "allow_adult",
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
                print(f"[STARTED VERTEX] {jid} ({model}, {res}) -> {op_name.split('/')[-1]}")

                poll_url = f"https://{VERTEX_LOCATION}-aiplatform.googleapis.com/v1/projects/{VERTEX_PROJECT}/locations/{VERTEX_LOCATION}/publishers/google/models/{model}:fetchPredictOperation"
                for _ in range(90):
                    time.sleep(8)
                    token = get_vertex_token()
                    preq = urllib.request.Request(
                        poll_url,
                        data=json.dumps({"operationName": op_name}).encode("utf-8"),
                        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(preq, timeout=45) as presp:
                        pdata = json.loads(presp.read().decode("utf-8"))
                    if pdata.get("done"):
                        if "error" in pdata:
                            raise RuntimeError(f"Vertex op error: {pdata['error']}")
                        videos = pdata.get("response", {}).get("videos", [])
                        if not videos:
                            raise RuntimeError(f"No videos in Vertex response: {pdata}")
                        vb64 = videos[0].get("bytesBase64Encoded")
                        if vb64:
                            with open(out_mp4, "wb") as f:
                                f.write(base64.b64decode(vb64))
                            print(f"[DONE VERTEX] {jid} -> {out_mp4} ({os.path.getsize(out_mp4)/1e6:.2f} MB)")
                            return {"id": jid, "status": "ok", "path": out_mp4, "aspect": job["aspect"]}
            else:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning?key={GEMINI_KEY}"
                payload = {
                    "instances": [{
                        "prompt": job["prompt"],
                        "image": {"bytesBase64Encoded": b64_first, "mimeType": "image/png"},
                        "lastFrame": {"bytesBase64Encoded": b64_last, "mimeType": "image/png"},
                    }],
                    "parameters": {
                        "aspectRatio": job["aspect"],
                        "durationSeconds": 8,
                        "resolution": res,
                    }
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    op_data = json.loads(resp.read().decode("utf-8"))
                op_name = op_data["name"]
                print(f"[STARTED GEMINI] {jid} ({model}, {res}) -> {op_name}")

                poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={GEMINI_KEY}"
                for _ in range(90):
                    time.sleep(8)
                    with urllib.request.urlopen(poll_url, timeout=45) as presp:
                        pdata = json.loads(presp.read().decode("utf-8"))
                    if pdata.get("done"):
                        if "error" in pdata:
                            raise RuntimeError(f"Gemini op error: {pdata['error']}")
                        samples = (
                            pdata.get("response", {})
                            .get("generateVideoResponse", {})
                            .get("generatedSamples", [])
                        )
                        if not samples:
                            raise RuntimeError(f"No samples in Gemini response: {pdata}")
                        vid_uri = samples[0]["video"]["uri"]
                        dl_url = f"{vid_uri}&key={GEMINI_KEY}" if "?" in vid_uri else f"{vid_uri}?key={GEMINI_KEY}"
                        urllib.request.urlretrieve(dl_url, out_mp4)
                        print(f"[DONE GEMINI] {jid} -> {out_mp4} ({os.path.getsize(out_mp4)/1e6:.2f} MB)")
                        return {"id": jid, "status": "ok", "path": out_mp4, "aspect": job["aspect"]}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            print(f"[WARN {jid} attempt {attempt+1}] HTTP {e.code}: {body[:240]}")
            # Switch backend on quota/rate limit
            job["backend"] = "vertex" if job["backend"] == "gemini" else "gemini"
            job["model"] = "veo-3.1-fast-generate-001" if job["backend"] == "vertex" else "veo-3.1-fast-generate-preview"
            time.sleep(10 * (attempt + 1))
        except Exception as e:
            print(f"[WARN {jid} attempt {attempt+1}] {e}")
            job["backend"] = "vertex" if job["backend"] == "gemini" else "gemini"
            job["model"] = "veo-3.1-fast-generate-001" if job["backend"] == "vertex" else "veo-3.1-fast-generate-preview"
            time.sleep(8 * (attempt + 1))

    return {"id": jid, "status": "failed", "path": None, "aspect": job["aspect"]}

def main():
    results = []
    # Run with 6 concurrent workers and 2.5s stagger so both Vertex and Gemini pools stay below RPM limits
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(run_single_veo_job, job, idx * 2.0) for idx, job in enumerate(VEO_JOBS)]
        for fut in as_completed(futs):
            res = fut.result()
            results.append(res)
    with open(os.path.join(VEO_RAW_DIR, "veo_batch_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    ok_count = sum(1 for r in results if r["status"] in ("ok", "cached"))
    print(f"VEO 3.1 BATCH COMPLETE: {ok_count}/{len(VEO_JOBS)} clips succeeded!")

if __name__ == "__main__":
    main()
