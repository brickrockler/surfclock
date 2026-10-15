#!/usr/bin/env python3
"""
Refines V4_STUDIO_11 (and V4_28 video) + adds V4_STUDIO_27 (and V4_40 video) so the green cutting mat
is a flat horizontal A1 graphic drafting mat on a sunlit designer's table (NOT a vertical tile wall),
with ZERO calipers and ZERO wires, and true large hardcover-book scale (18.4 x 23.0 cm = ~18 x 23 grid squares).
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

spec32 = importlib.util.spec_from_file_location("v4_fix", str(BASE / "scripts" / "32_fix_4_non_plinth_clips_and_studio11.py"))
m32 = importlib.util.module_from_spec(spec32)
spec32.loader.exec_module(m32)


def main():
    print("=== Regenerating V4_STUDIO_11 (Horizontal Green Cutting Mat on Sunlit Studio Table) & Adding V4_STUDIO_27 ===", flush=True)
    raw_old = m.RAW_V4_DIR / "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_1080p_locked.mp4"
    if raw_old.exists():
        raw_old.unlink()

    stills = [
        (
            "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_16x9_4K.jpg",
            "16:9",
            "Art-directed 35mm Kodak Vision3 250D industrial design film photograph in a sunlit Stockholm / Kronberg design studio. "
            "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument standing upright in the center of the frame. "
            "It stands on a FLAT HORIZONTAL dark sage-green self-healing A1 graphic cutting mat resting on a warm oak architect's workbench table, with a softly blurred sunlit studio window and plaster wall in the background (the green grid mat is flat on the horizontal table surface, NOT on the wall). "
            "SCALE: The instrument is the exact size of a large hardcover coffee-table monograph book (18.4 cm wide by 23.0 cm tall by 5.2 cm deep), spanning ~18 fine 1cm grid squares across its base on the horizontal green cutting mat. "
            "STRICTLY ZERO calipers, ZERO wires, ZERO cables, ZERO tools, ZERO clutter — only the clean horizontal green grid mat on the timber table, warm raking afternoon window light, and a long diagonal shadow across the mat. "
            + m31.ACCURATE_PRODUCT_LOCK
        ),
        (
            "V4_STUDIO_27_Green_CuttingMat_With_Hardcover_Monograph_Book_16x9_4K.jpg",
            "16:9",
            "Art-directed medium-format Kodak Portra 400 editorial design photograph. "
            "Keep the exact upright front-facing matte slate-blue rectangular Braun Surf Instrument standing upright in the center of the frame on a FLAT HORIZONTAL matte forest-green graphic cutting mat with fine 1cm white grid lines on a studio table. "
            "Beside it on the left lies a closed, unbranded cream-linen large hardcover art monograph book flat on the green grid mat, immediately showing that the Surf Instrument is the exact size and substantial scale of a large hardcover book (18.4 cm x 23.0 cm x 5.2 cm). "
            "STRICTLY ZERO calipers, ZERO wires, ZERO cables, ZERO pens. Warm dappled studio sunlight and long architectural shadows across the green grid mat. "
            + m31.ACCURATE_PRODUCT_LOCK
        ),
    ]

    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(m32.regenerate_upright_locked_still, name, aspect, prompt) for name, aspect, prompt in stills]
        for f in as_completed(futs):
            f.result()

    # Rebuild non-plinth stills audit sheet
    np_16 = sorted(m.V4_16x9_STILLS.glob("V4_STUDIO_1[1-9]_*.jpg")) + sorted(m.V4_16x9_STILLS.glob("V4_STUDIO_2[0-7]_*.jpg"))
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

    veo_jobs = [
        {
            "id": "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_Tabletop_V2",
            "out_mp4": "V4_28_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_4K.mp4",
            "aspect": "16:9",
            "kf": m.V4_16x9_STILLS / "V4_STUDIO_11_ArtDirected_Green_DraftingGrid_Mat_HardcoverScale_16x9_4K.jpg",
            "sweep_beaches": True,
            "grain": "16mm",
            "prompt": (
                "Art-directed 35mm industrial design film shot in a sunlit design studio. "
                "The matte slate-blue rectangular Braun instrument (large hardcover book scale) stands stationary on a flat horizontal green graphic cutting mat on a wooden studio workbench (strictly NO calipers, NO wires, NO hands). "
                "Slow, smooth optical camera dolly push-in as warm afternoon window light glides across the green grid mat."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
        {
            "id": "V4_STUDIO_27_Green_CuttingMat_With_Hardcover_Monograph_Book",
            "out_mp4": "V4_40_STUDIO_27_Green_CuttingMat_With_Hardcover_Book_4K.mp4",
            "aspect": "16:9",
            "kf": m.V4_16x9_STILLS / "V4_STUDIO_27_Green_CuttingMat_With_Hardcover_Monograph_Book_16x9_4K.jpg",
            "sweep_beaches": True,
            "grain": "16mm",
            "prompt": (
                "Art-directed medium-format studio film shot on Kodak Portra 35mm film. "
                "The matte slate-blue rectangular Braun instrument stands stationary on a flat horizontal forest-green graphic grid mat beside a closed linen hardcover art monograph book (strictly NO wires, NO tools, NO hands). "
                "Slow, smooth optical camera slider push-in while warm dappled studio sunlight shifts gently across the green grid."
                + m.NO_CLOCK_WORD_RULE
            ),
        },
    ]

    raw_map = {}
    with ThreadPoolExecutor(max_workers=2) as ex:
        fut_map = {ex.submit(m.generate_veo_1080p_first_last_locked, i, job): job for i, job in enumerate(veo_jobs)}
        for fut in as_completed(fut_map):
            job = fut_map[fut]
            raw_map[job["id"]] = fut.result()

    for job in veo_jobs:
        raw_mp4 = raw_map[job["id"]]
        m.master_clip_v4_perfect(
            raw_mp4=raw_mp4,
            out_mp4=m.CLIPS_16x9_DIR / job["out_mp4"],
            aspect="16:9",
            kf_4k_path=job["kf"],
            sweep_beaches=job["sweep_beaches"],
            grain_mode=job["grain"],
            erase_chimney=False,
        )

    vids_16x9_np = sorted(m.CLIPS_16x9_DIR.glob("V4_2[89]_*.mp4")) + sorted(m.CLIPS_16x9_DIR.glob("V4_3[0-9]_*.mp4")) + sorted(m.CLIPS_16x9_DIR.glob("V4_40_*.mp4"))
    m.build_video_audit_sheet(vids_16x9_np, m.AUDIT_DIR / "AUDIT_V4_NON_PLINTH_12_16x9_VIDEOS_DIAL_ZOOM.jpg")

    clips_16 = sorted(m.CLIPS_16x9_DIR.glob("V4_*.mp4"))
    m.build_video_audit_sheet(clips_16, m.AUDIT_DIR / "AUDIT_V4_ALL_16x9_VIDEOS_DIAL_ZOOM.jpg")

    studio_16 = [c for c in clips_16 if "_STUDIO_" in c.name or "_CREAM_" in c.name or "_MACRO_" in c.name]
    m.concat_videos(clips_16,  m.SHOWREELS_DIR / "01_SURF_CLOCK_MASTER_4K_60FPS_16x9_WIDESCREEN_SHOWREEL.mp4")
    m.concat_videos(studio_16, m.SHOWREELS_DIR / "03_SURF_CLOCK_CLEAN_STUDIO_PLINTHS_AND_DAPPLED_CREAM_4K_REEL.mp4")
    print("=== PERFECT HORIZONTAL GREEN GRID & HARDCOVER SCALE COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
