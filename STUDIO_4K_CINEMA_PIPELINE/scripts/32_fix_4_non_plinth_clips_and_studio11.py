#!/usr/bin/env python3
"""
Removes all calipers, wires/patch cables, and small pens/props that skewed scale.
Replaces them with art-directed compositions anchored at true large-hardcover-book scale (184 x 230 x 52 mm):
1. V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_16x9_4K.jpg (16:9)
2. V4_STUDIO_15_Sunlit_BirchPlywood_Table_And_LinenHardcoverBook_16x9_4K.jpg (16:9)
3. V4_STUDIO_24_Warm_Cork_Studio_Table_Minimalist_Sunlit_16x9_4K.jpg (16:9)
4. V4_9x16_15_ArtDirected_Green_DraftingGrid_Mat_Vertical_4K.jpg (9:16)
5. V4_9x16_19_Sunlit_BirchPlywood_Table_HardcoverScale_Vertical_4K.jpg (9:16)
And regenerates the 4 Veo 3.1 Pro clips (V4_28, V4_32, V4_33, V4_9x16_15), masters to 4K 60fps,
updates audit contact sheets, and rebuilds all 4 Master 4K 60fps Showreels.
"""
import os
import sys
import time
import json
import base64
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
import importlib.util

BASE = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")

spec30 = importlib.util.spec_from_file_location("v4_suite", str(BASE / "scripts" / "30_v4_veo31_locked_studio_and_aussie_cinema_suite.py"))
m = importlib.util.module_from_spec(spec30)
spec30.loader.exec_module(m)

spec31 = importlib.util.spec_from_file_location("v4_np", str(BASE / "scripts" / "31_v4_non_plinth_pure_studio_expansion.py"))
m31 = importlib.util.module_from_spec(spec31)
spec31.loader.exec_module(m31)


OLD_FILES_TO_REMOVE = [
    m.V4_16x9_STILLS / "V4_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_16x9_4K.jpg",
    m.V4_16x9_STILLS / "V4_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_16x9_4K.jpg",
    m.V4_16x9_STILLS / "V4_STUDIO_24_Warm_Cork_Pinboard_Desk_Editorial_StillLife_16x9_4K.jpg",
    m.V4_9x16_STILLS / "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_4K.jpg",
    m.V4_9x16_STILLS / "V4_9x16_19_Orchid_Synth_Desk_Birch_And_Cables_Vertical_4K.jpg",
    m.CLIPS_16x9_DIR / "V4_28_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_4K.mp4",
    m.CLIPS_16x9_DIR / "V4_32_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_4K.mp4",
    m.CLIPS_16x9_DIR / "V4_33_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_4K.mp4",
    m.CLIPS_9x16_DIR / "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_4K.mp4",
    m.RAW_V4_DIR / "V4_STUDIO_11_TeenageEng_DesignLab_CuttingMat_And_Calipers_1080p_locked.mp4",
    m.RAW_V4_DIR / "V4_STUDIO_15_Orchid_Synth_Studio_BirchPlywood_And_PatchCables_1080p_locked.mp4",
    m.RAW_V4_DIR / "V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_1080p_locked.mp4",
    m.RAW_V4_DIR / "V4_9x16_15_TeenageEng_DesignLab_CuttingMat_Vertical_1080p_locked.mp4",
]


def regenerate_upright_locked_still(out_name: str, aspect: str, prompt: str):
    out_dir = m.V4_16x9_STILLS if aspect == "16:9" else m.V4_9x16_STILLS
    out_path = out_dir / out_name
    if out_path.exists():
        out_path.unlink()

    b64_ref = m31.B64_MASTER_16x9 if aspect == "16:9" else m31.B64_MASTER_9x16
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={m31.GEMINI_KEY}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": b64_ref}},
                {"text": prompt},
            ],
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": "4K"},
        },
    }
    data = json.dumps(payload).encode("utf-8")
    ink_layers = m.render_ink_and_hands_4k(0.0, 0.0)

    for attempt in range(1, 6):
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
            if H is None:
                raise RuntimeError("Homography H was None (clock not upright/centered), retrying...")
            im = m.clean_frame_chimney_and_dial_v14(im, H, ink_layers, erase_chimney=False)
            cv2.imwrite(str(out_path), im, [cv2.IMWRITE_JPEG_QUALITY, 97])
            print(f"[LOCKED UPRIGHT 4K STILL] {out_name} (H verified!)", flush=True)
            return out_path
        except Exception as e:
            print(f"[RETRY {attempt}/5] {out_name}: {e}", flush=True)
            time.sleep(3 * attempt)
    raise RuntimeError(f"Failed to generate upright locked still {out_name}")


NEW_STILL_JOBS = [
    (
        "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_16x9_4K.jpg",
        "16:9",
        "Art-directed industrial design studio photograph shot on medium-format Hasselblad 80mm Planar lens (Kodak Portra 400). "
        "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument standing upright in the center of the frame. "
        "PHYSICAL SCALE: The instrument is the exact size of a large, heavy architectural hardcover monograph book (18.4 cm wide by 23.0 cm tall by 5.2 cm deep). "
        "It stands directly on a continuous, full-bleed matte sage-green architectural drafting & cutting mat surface with delicate, fine cream-white 1 cm graphic grid lines (so the base of the instrument spans ~18 fine grid squares wide). "
        "ZERO calipers, ZERO wires, ZERO cables, ZERO tools, ZERO clutter — only the pure, minimalist green graphic grid surface, deep warm studio chiaroscuro sunlight raking diagonally across the green grid, and a long architectural drop shadow. "
        + m31.ACCURATE_PRODUCT_LOCK
    ),
    (
        "V4_STUDIO_15_Sunlit_BirchPlywood_Table_And_LinenHardcoverBook_16x9_4K.jpg",
        "16:9",
        "Art-directed editorial design photograph shot on 35mm Kodak Vision3 250D film (Apartamento / Braun Kronberg / Telepathic Instruments aesthetic). "
        "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument standing upright in the center of a warm honey-toned Baltic birch plywood studio table with visible layered ply edge grain (NO plinth). "
        "PHYSICAL SCALE: The instrument is the exact size of a large hardcover art book (18.4 cm wide by 23.0 cm tall). Resting flat on the birch table to the left is a single closed, unbranded raw oatmeal-linen hardcover art monograph book of the exact same footprint, anchoring its substantial hardcover-book scale. "
        "ZERO wires, ZERO cables, ZERO knobs, ZERO electronics clutter. Warm late-afternoon window sunlight and soft dappled shadows across the birch table. "
        + m31.ACCURATE_PRODUCT_LOCK
    ),
    (
        "V4_STUDIO_24_Warm_Cork_Studio_Table_Minimalist_Sunlit_16x9_4K.jpg",
        "16:9",
        "Minimalist architectural studio photograph shot on medium-format Kodak Portra 400. "
        "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument (large hardcover book scale: 18.4 cm x 23.0 cm x 5.2 cm) standing directly on a continuous, thick, warm natural cork architect's worktable against a soft warm plaster studio wall (NO plinth). "
        "ZERO pens, ZERO notebooks, ZERO wires, ZERO props — pure tactile cork grain, matte slate-blue VDI-24 molded casing, and a crisp geometric diagonal window sunbeam casting a warm shadow. "
        + m31.ACCURATE_PRODUCT_LOCK
    ),
    (
        "V4_9x16_15_ArtDirected_Green_DraftingGrid_Mat_Vertical_4K.jpg",
        "9:16",
        "Native 9:16 vertical art-directed industrial design studio photograph shot on medium-format Hasselblad 80mm lens. "
        "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument (large hardcover book size: 18.4 cm wide by 23.0 cm tall) standing directly on a continuous matte sage-green architectural cutting/drafting mat with fine 1 cm cream-white grid lines (spanning ~18 grid squares wide). "
        "ZERO calipers, ZERO wires, ZERO cables, ZERO tools — completely clean, pure graphic green grid surface in the foreground and background, illuminated by warm raking afternoon studio sunlight casting a long dramatic shadow across the grid. "
        + m31.ACCURATE_PRODUCT_LOCK
    ),
    (
        "V4_9x16_19_Sunlit_BirchPlywood_Table_HardcoverScale_Vertical_4K.jpg",
        "9:16",
        "Native 9:16 vertical editorial studio photograph shot on 35mm Kodak Portra 400 film. "
        "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument (large hardcover book scale: 18.4 cm x 23.0 cm) standing directly on a sunlit Baltic birch plywood architect's table (NO plinth). "
        "ZERO wires, ZERO patch cables, ZERO props — pure warm birch wood grain and golden slanted afternoon window light with soft architectural shadows. "
        + m31.ACCURATE_PRODUCT_LOCK
    ),
]


def main():
    for p in OLD_FILES_TO_REMOVE:
        if p.exists():
            p.unlink()
            print(f"[REMOVED OLD] {p.name}", flush=True)

    print("=== STEP 1: GENERATING 5 CLEAN, HARDCOVER-SCALE, ZERO-WIRE/CALIPER 4K STILLS ===", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = [ex.submit(regenerate_upright_locked_still, name, aspect, prompt) for name, aspect, prompt in NEW_STILL_JOBS]
        for f in as_completed(futs):
            f.result()

    # Rebuild 24-still audit sheet from all current non-plinth stills
    np_16 = sorted(m.V4_16x9_STILLS.glob("V4_STUDIO_1[1-9]_*.jpg")) + sorted(m.V4_16x9_STILLS.glob("V4_STUDIO_2[0-6]_*.jpg"))
    np_9  = sorted(m.V4_9x16_STILLS.glob("V4_9x16_1[3-9]_*.jpg")) + sorted(m.V4_9x16_STILLS.glob("V4_9x16_20_*.jpg"))
    tiles = []
    for p in np_16 + np_9:
        im = cv2.imread(str(p))
        if im is not None:
            tile = cv2.resize(im, (480, 270))
            cv2.putText(tile, p.name[:34], (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 0, 0), 3)
            cv2.putText(tile, p.name[:34], (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 1)
            tiles.append(tile)
    while len(tiles) % 4 != 0:
        tiles.append(np.zeros((270, 480, 3), dtype=np.uint8))
    grid = np.vstack([np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)])
    cv2.imwrite(str(m.AUDIT_DIR / "AUDIT_V4_NON_PLINTH_PURE_STUDIO_24_STILLS.jpg"), grid, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print("[UPDATED AUDIT] AUDIT_V4_NON_PLINTH_PURE_STUDIO_24_STILLS.jpg", flush=True)

    print("=== STEP 2: GENERATING 4 CLEAN VEO 3.1 PRO CLIPS (ZERO CALIPERS/WIRES/HANDS) ===", flush=True)
    jobs_to_fix = [
        {
            "id": "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale",
            "out_mp4": "V4_28_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_4K.mp4",
            "aspect": "16:9",
            "kf": m.V4_16x9_STILLS / "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_16x9_4K.jpg",
            "sweep_beaches": True,
            "grain": "16mm",
            "prompt": (
                "Art-directed 35mm industrial design film shot on a clean matte sage-green architectural drafting grid mat (no plinth, no tools, no wires, no hands). "
                "Slow, smooth optical camera dolly push-in across the fine green graphic grid as warm afternoon studio sunlight and long architectural shadows glide gently across the surface."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
        {
            "id": "V4_STUDIO_15_Sunlit_BirchPlywood_Table_And_LinenHardcoverBook",
            "out_mp4": "V4_32_STUDIO_15_Sunlit_BirchPlywood_Table_HardcoverScale_4K.mp4",
            "aspect": "16:9",
            "kf": m.V4_16x9_STILLS / "V4_STUDIO_15_Sunlit_BirchPlywood_Table_And_LinenHardcoverBook_16x9_4K.jpg",
            "sweep_beaches": True,
            "grain": "16mm",
            "prompt": (
                "Artful editorial studio cinema shot on 35mm Kodak film. "
                "The matte slate-blue rectangular Braun instrument stands stationary on a warm Baltic birch plywood table beside a closed linen hardcover art book (strictly NO hands, NO wires, NO people). "
                "Slow, smooth optical camera slider push-in while warm golden window light shifts gently across the wood grain."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
        {
            "id": "V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_Clean",
            "out_mp4": "V4_33_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_4K.mp4",
            "aspect": "16:9",
            "kf": m.V4_16x9_STILLS / "V4_STUDIO_16_DonaldJudd_Limewash_Wall_Corner_ShadowGap_16x9_4K.jpg",
            "sweep_beaches": True,
            "grain": "studio",
            "prompt": (
                "Donald Judd Marfa architectural gallery film shot of the matte slate-blue rectangular Braun instrument mounted flush on a bright sunlit bone-white lime-washed wall. "
                "Bright, steady, constant warm daylight illuminates the entire matte slate-blue housing and dial face evenly throughout all 8 seconds (zero dark shadow covering the face). "
                "Slow, smooth optical camera dolly push-in."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
        {
            "id": "V4_9x16_15_ArtDirected_Green_DraftingGrid_Mat_Vertical",
            "out_mp4": "V4_9x16_15_ArtDirected_Green_DraftingGrid_Mat_Vertical_4K.mp4",
            "aspect": "9:16",
            "kf": m.V4_9x16_STILLS / "V4_9x16_15_ArtDirected_Green_DraftingGrid_Mat_Vertical_4K.jpg",
            "sweep_beaches": True,
            "grain": "16mm",
            "prompt": (
                "Native 9:16 vertical art-directed industrial design cinema shot on 35mm film. "
                "The matte slate-blue rectangular instrument stands stationary on a clean matte sage-green architectural drafting grid mat (zero tools, zero wires, zero hands). "
                "Slow, smooth optical camera push-in as warm studio sunlight shifts across the green graphic grid lines."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
    ]

    raw_map = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        fut_map = {ex.submit(m.generate_veo_1080p_first_last_locked, i, job): job for i, job in enumerate(jobs_to_fix)}
        for fut in as_completed(fut_map):
            job = fut_map[fut]
            raw_map[job["id"]] = fut.result()

    print("=== STEP 3: MASTERING 4 FIXED CLIPS TO 4K 60FPS ===", flush=True)
    for job in jobs_to_fix:
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

    print("=== STEP 4: UPDATING VIDEO AUDIT SHEETS & MASTER SHOWREELS ===", flush=True)
    vids_16x9_np = sorted(m.CLIPS_16x9_DIR.glob("V4_2[89]_*.mp4")) + sorted(m.CLIPS_16x9_DIR.glob("V4_3[0-9]_*.mp4"))
    vids_9x16_np = sorted(m.CLIPS_9x16_DIR.glob("V4_9x16_1[3-6]_*.mp4"))
    m.build_video_audit_sheet(vids_16x9_np, m.AUDIT_DIR / "AUDIT_V4_NON_PLINTH_12_16x9_VIDEOS_DIAL_ZOOM.jpg")
    m.build_video_audit_sheet(vids_9x16_np, m.AUDIT_DIR / "AUDIT_V4_NON_PLINTH_4_9x16_VIDEOS_DIAL_ZOOM.jpg")

    clips_16 = sorted(m.CLIPS_16x9_DIR.glob("V4_*.mp4"))
    clips_9  = sorted(m.CLIPS_9x16_DIR.glob("V4_*.mp4"))
    m.build_video_audit_sheet(clips_16, m.AUDIT_DIR / "AUDIT_V4_ALL_16x9_VIDEOS_DIAL_ZOOM.jpg")
    m.build_video_audit_sheet(clips_9,  m.AUDIT_DIR / "AUDIT_V4_ALL_9x16_VIDEOS_DIAL_ZOOM.jpg")

    studio_16 = [c for c in clips_16 if "_STUDIO_" in c.name or "_CREAM_" in c.name or "_MACRO_" in c.name]
    aussie_16 = [c for c in clips_16 if "_AUSSIE_" in c.name or "_CREAM_" in c.name]

    m.concat_videos(clips_16,  m.SHOWREELS_DIR / "01_SURF_CLOCK_MASTER_4K_60FPS_16x9_WIDESCREEN_SHOWREEL.mp4")
    m.concat_videos(clips_9,   m.SHOWREELS_DIR / "02_SURF_CLOCK_MASTER_4K_60FPS_9x16_VERTICAL_SOCIAL_REEL.mp4")
    m.concat_videos(studio_16, m.SHOWREELS_DIR / "03_SURF_CLOCK_CLEAN_STUDIO_PLINTHS_AND_DAPPLED_CREAM_4K_REEL.mp4")
    m.concat_videos(aussie_16, m.SHOWREELS_DIR / "04_SURF_CLOCK_AUSSIE_SURF_CULTURE_16MM_AND_CAMCORDER_4K_REEL.mp4")
    print("=== ALL CLEAN HARDCOVER-SCALE STILLS, CLIPS & SHOWREELS COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
