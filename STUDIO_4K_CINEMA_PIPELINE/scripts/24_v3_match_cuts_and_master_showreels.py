#!/usr/bin/env python3
"""
V3 STAGE 4: PRECISION CENTER-LOCKED MATCH-CUT ENGINE & 4K 60FPS MASTER SHOWREEL ASSEMBLER
- Aligns the Surf Clock across Orchid 16mm Wildflower Meadow, Weightless Floating, Wall-Mounted,
  Tabletop, and Clean VDI-24 Studio finishes to the exact center pixel grid before cutting.
- Assembles the 4 flagship 4K 60fps Master Showreels in 00_MASTER_SHOWREELS/.
- Extracts mid-clip video audit contact sheets to verify zero black glow, zero cyan highlights,
  zero garbled text, and zero double hands.
"""

import os
import glob
import json
import subprocess
import cv2
import numpy as np

BASE_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
V3_16x9_IMG_DIR = os.path.join(BASE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS/V3_ORCHID_POETRY_ARCHDIGEST_4K")
V3_9x16_IMG_DIR = os.path.join(BASE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS/V3_9x16_VERTICAL_STUDIO_AND_ORCHID_4K")
CLIPS_16x9_DIR = os.path.join(BASE_DIR, "02_INDIVIDUAL_4K_CLIPS_16x9")
CLIPS_9x16_DIR = os.path.join(BASE_DIR, "03_INDIVIDUAL_4K_CLIPS_9x16")
SHOWREELS_DIR = os.path.join(BASE_DIR, "00_MASTER_SHOWREELS")
AUDIT_DIR = os.path.join(BASE_DIR, "04_CONTACT_SHEETS_AND_AUDIT")
os.makedirs(SHOWREELS_DIR, exist_ok=True)

def detect_clock_center_and_height(img_bgr):
    """
    Finds the burnt-orange upper and lower pointer hands in the image to lock the exact
    dial center and scale across different environments!
    """
    h, w = img_bgr.shape[:2]
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # Burnt orange hue in OpenCV (0..180): roughly 5..18, high saturation & value
    mask = cv2.inRange(hsv, np.array([4, 130, 120]), np.array([19, 255, 255]))
    # Restrict to central 65% of image to avoid background orange poppies/wood
    yy, xx = np.mgrid[0:h, 0:w]
    central = (xx > w * 0.25) & (xx < w * 0.75) & (yy > h * 0.15) & (yy < h * 0.85)
    mask = mask & (central.astype(np.uint8) * 255)

    ys, xs = np.where(mask > 0)
    if len(xs) < 80:
        return (w * 0.5, h * 0.5, h * 0.42)

    # Split into upper hand (y < median) and lower hand (y > median)
    med_y = np.median(ys)
    upper_pts = ys < med_y
    lower_pts = ys >= med_y
    if np.sum(upper_pts) < 20 or np.sum(lower_pts) < 20:
        return (float(np.mean(xs)), float(np.mean(ys)), h * 0.42)

    ux, uy = float(np.median(xs[upper_pts])), float(np.median(ys[upper_pts]))
    lx, ly = float(np.median(xs[lower_pts])), float(np.median(ys[lower_pts]))
    span_y = abs(ly - uy)
    if span_y < h * 0.08 or span_y > h * 0.45:
        return (w * 0.5, h * 0.5, h * 0.42)

    cx = 0.5 * (ux + lx)
    cy = uy + 0.42 * (ly - uy)
    return (cx, cy, span_y)

def align_plate_to_reference(img_bgr, target_cx, target_cy, target_span, out_wh):
    out_w, out_h = out_wh
    img_resized = cv2.resize(img_bgr, (out_w, out_h), interpolation=cv2.INTER_LANCZOS4)
    cx, cy, span = detect_clock_center_and_height(img_resized)
    scale = np.clip(target_span / max(1.0, span), 0.82, 1.22)
    M = np.array([
        [scale, 0.0, target_cx - scale * cx],
        [0.0, scale, target_cy - scale * cy]
    ], dtype=np.float32)
    aligned = cv2.warpAffine(img_resized, M, (out_w, out_h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT_101)
    return aligned

def render_center_locked_match_cut_clip(plate_paths, out_mp4, aspect_ratio="16:9", frames_per_cut=30, loops=2, fps=60):
    out_w, out_h = (3840, 2160) if aspect_ratio == "16:9" else (2160, 3840)
    valid_imgs = []
    for p in plate_paths:
        if os.path.exists(p):
            im = cv2.imread(p)
            if im is not None:
                valid_imgs.append(im)
    if not valid_imgs:
        return None

    # Use first image (Studio Master Ref) as geometric anchor
    ref_im = cv2.resize(valid_imgs[0], (out_w, out_h), interpolation=cv2.INTER_LANCZOS4)
    t_cx, t_cy, t_span = detect_clock_center_and_height(ref_im)

    aligned_plates = [ref_im]
    for im in valid_imgs[1:]:
        aligned_plates.append(align_plate_to_reference(im, t_cx, t_cy, t_span, (out_w, out_h)))

    seq = aligned_plates * loops
    total_frames = len(seq) * frames_per_cut

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{out_w}x{out_h}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        plate_idx = min(len(seq) - 1, f_idx // frames_per_cut)
        base = seq[plate_idx]
        # Continuous slow push-in dolly across the entire match-cut sequence (1.0 -> 1.07x)
        u = f_idx / max(1, total_frames - 1)
        zoom = 1.0 + 0.065 * (0.5 - 0.5 * np.cos(np.pi * u))
        M = np.array([
            [zoom, 0.0, t_cx * (1.0 - zoom)],
            [0.0, zoom, t_cy * (1.0 - zoom)]
        ], dtype=np.float32)
        frame = cv2.warpAffine(base, M, (out_w, out_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"[MATCH-CUT RENDERED] {os.path.basename(out_mp4)} ({os.path.getsize(out_mp4)/1e6:.2f} MB)")
    return out_mp4

def concat_mp4_list(clip_paths, out_mp4):
    valid = [p for p in clip_paths if os.path.exists(p) and os.path.getsize(p) > 500_000]
    if not valid:
        return None
    list_txt = out_mp4 + ".txt"
    with open(list_txt, "w") as f:
        for p in valid:
            f.write(f"file '{p}'\n")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_txt,
        "-c", "copy",
        "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(list_txt)
    dur_out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", out_mp4
    ]).decode().strip()
    print(f"[SHOWREEL BUILT] {os.path.basename(out_mp4)} | Duration: {float(dur_out):.1f}s ({float(dur_out)/60.0:.2f} min) | Size: {os.path.getsize(out_mp4)/1e6:.1f} MB")
    return out_mp4

def build_video_audit_sheet(clip_dir, out_jpg, aspect_ratio="16:9", max_clips=24):
    clips = sorted(glob.glob(os.path.join(clip_dir, "V3_*.mp4")))[:max_clips]
    if not clips:
        return
    tw, th = (480, 270) if aspect_ratio == "16:9" else (270, 480)
    cols = 4
    rows = len(clips)
    sheet = np.zeros((rows * th, cols * tw, 3), dtype=np.uint8)
    for r, cp in enumerate(clips):
        cap = cv2.VideoCapture(cp)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_idxs = [int(n_frames * q) for q in (0.12, 0.38, 0.64, 0.88)]
        for c, f_idx in enumerate(sample_idxs):
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, f_idx))
            ok, frm = cap.read()
            if ok and frm is not None:
                tile = cv2.resize(frm, (tw, th), interpolation=cv2.INTER_AREA)
                if c == 0:
                    cv2.putText(tile, os.path.basename(cp)[:32], (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 180), 1, cv2.LINE_AA)
                sheet[r*th:(r+1)*th, c*tw:(c+1)*tw] = tile
        cap.release()
    cv2.imwrite(out_jpg, sheet, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    print(f"[VIDEO AUDIT SHEET SAVED] {out_jpg}")

if __name__ == "__main__":
    print("=== V3 STAGE 4: BUILDING CENTER-LOCKED MATCH CUTS & 4K 60FPS MASTER SHOWREELS ===")

    # 1. Select upright 16:9 plates for Center-Locked Match Cuts
    mc_16x9_names = [
        "V3_29_Studio_Signature_Clean_SlateBlue_Chiaroscuro_4K.jpg",
        "V3_01_Orchid_Wildflower_Meadow_16mm_GoldenHour_4K.jpg",
        "V3_03_PoetryCam_Sunlit_Linen_Picnic_Wildflowers_16mm_4K.jpg",
        "V3_15_Wall_Mounted_Warm_Venetian_Plaster_Dappled_Sunlight_4K.jpg",
        "V3_21_Table_Roman_Travertine_CoffeeTable_Espresso_ArtBooks_4K.jpg",
        "V3_30_Studio_Warm_Ulm_1965_DieterRams_IceGrey_Edition_4K.jpg",
        "V3_05_PoetryCam_Botanical_Conservatory_Dappled_Ferns_35mm_4K.jpg",
        "V3_16_Wall_Mounted_MidCentury_Walnut_And_Concrete_Loft_4K.jpg",
        "V3_22_Table_MidCentury_Teak_Credenza_Vinyl_Turntable_Orchid_4K.jpg",
        "V3_31_Studio_BeadBlasted_Titanium_Silver_Warm_Gallery_4K.jpg",
        "V3_07_Orchid_Mossy_Kyoto_Stone_Garden_MorningMist_35mm_4K.jpg",
        "V3_18_Wall_Mounted_DieterRams_IceGrey_On_Terracotta_Plaster_4K.jpg",
        "V3_23_Table_Brutalist_Concrete_Window_Ledge_Overlooking_Surf_4K.jpg",
        "V3_32_Studio_Forest_Sage_Green_Molded_On_Raw_Travertine_4K.jpg",
        "V3_08_PoetryCam_SunBleached_Driftwood_Bench_GoldenHour_16mm_4K.jpg",
        "V3_26_Table_Calacatta_Viola_Marble_Plinth_Warm_Morning_4K.jpg"
    ]
    mc_16x9_paths = [os.path.join(V3_16x9_IMG_DIR, n) for n in mc_16x9_names]

    mc1_out = os.path.join(CLIPS_16x9_DIR, "V3_37_MatchCut_Orchid_Nature_Wall_Table_Studio_120BPM_4K_60fps.mp4")
    mc2_out = os.path.join(CLIPS_16x9_DIR, "V3_38_MatchCut_HyperRapid_Finish_And_Locations_240BPM_4K_60fps.mp4")
    render_center_locked_match_cut_clip(mc_16x9_paths, mc1_out, "16:9", frames_per_cut=30, loops=2, fps=60)
    render_center_locked_match_cut_clip(mc_16x9_paths, mc2_out, "16:9", frames_per_cut=15, loops=3, fps=60)

    # 2. 9:16 Vertical Center-Locked Match Cut across Clean Studio & Orchid Vertical Plates
    mc_9x16_names = [
        "V3_9x16_01_Studio_SlateBlue_Chiaroscuro_BraunMolded_4K.jpg",
        "V3_9x16_02_Studio_Braun_1965_IceGrey_RAL7035_Molded_4K.jpg",
        "V3_9x16_03_Studio_Orchid_ForestSage_And_WarmPutty_Molded_4K.jpg",
        "V3_9x16_04_Studio_BeadBlasted_Titanium_And_Navy_4K.jpg",
        "V3_9x16_07_Studio_GoldenHour_VenetianBlinds_SlateMonolith_4K.jpg",
        "V3_9x16_09_Orchid_Wildflower_Meadow_16mm_Vertical_4K.jpg",
        "V3_9x16_10_PoetryCam_Sunlit_Linen_Picnic_Vertical_4K.jpg",
        "V3_9x16_13_Wall_Venetian_Plaster_DappledLeaves_Vertical_4K.jpg",
        "V3_9x16_14_Wall_Whitewashed_BeachShack_Timber_Vertical_4K.jpg",
        "V3_9x16_15_Tabletop_Travertine_CoffeeTable_Vertical_4K.jpg",
        "V3_9x16_16_Tabletop_Danish_Teak_HiFi_Credenza_Vertical_4K.jpg"
    ]
    mc_9x16_paths = [os.path.join(V3_9x16_IMG_DIR, n) for n in mc_9x16_names]
    mc3_out = os.path.join(CLIPS_9x16_DIR, "V3_9x16_17_MatchCut_Vertical_Studio_And_Orchid_120BPM_4K_60fps.mp4")
    render_center_locked_match_cut_clip(mc_9x16_paths, mc3_out, "9:16", frames_per_cut=28, loops=2, fps=60)

    # 3. Assemble Master Showreels in 00_MASTER_SHOWREELS/
    veo_16x9 = sorted(glob.glob(os.path.join(CLIPS_16x9_DIR, "V3_*_Veo31Pro_LiveMotion_4K_60fps.mp4")))
    pan_16x9 = sorted([
        p for p in glob.glob(os.path.join(CLIPS_16x9_DIR, "V3_*_4K_60fps.mp4"))
        if "_Veo31Pro_" not in p and "_MatchCut_" not in p
    ])
    mc_16x9 = [mc1_out, mc2_out]

    # Interleave Veo 3.1 Pro live-motion shots, Match-Cuts, and 4K 60fps Cinema Camera Pans for > 5.5 minutes!
    master_16x9_seq = veo_16x9 + [mc1_out] + pan_16x9 + [mc2_out]
    concat_mp4_list(master_16x9_seq, os.path.join(SHOWREELS_DIR, "SURF_CLOCK_4K_60FPS_MASTER_COMMERCIAL_16x9.mp4"))
    concat_mp4_list(veo_16x9 + pan_16x9[:28], os.path.join(SHOWREELS_DIR, "SURF_CLOCK_4K_60FPS_ORCHID_AND_POETRY_16MM_SHOWCASE_16x9.mp4"))
    concat_mp4_list([mc1_out, mc2_out, mc1_out], os.path.join(SHOWREELS_DIR, "SURF_CLOCK_4K_60FPS_MATCH_CUT_SHOWCASE_16x9.mp4"))

    # 9:16 Vertical Master Reel: Clean Studio 9:16 first (V3_9x16_01..08), then Match-Cut, then Orchid / Floating / Wall / Tabletop 9:16 + Veo 3.1 Pro 9:16!
    pan_9x16 = sorted([
        p for p in glob.glob(os.path.join(CLIPS_9x16_DIR, "V3_9x16_*_4K_60fps.mp4"))
        if "_Veo31Pro_" not in p and "_MatchCut_" not in p
    ])
    veo_9x16 = sorted(glob.glob(os.path.join(CLIPS_9x16_DIR, "V3_9x16_*_Veo31Pro_LiveMotion_4K_60fps.mp4")))
    vertical_seq = pan_9x16[:8] + [mc3_out] + veo_9x16 + pan_9x16[8:]
    concat_mp4_list(vertical_seq, os.path.join(SHOWREELS_DIR, "SURF_CLOCK_4K_60FPS_VERTICAL_REEL_9x16.mp4"))

    # 4. Build mid-clip video audit sheets
    build_video_audit_sheet(CLIPS_16x9_DIR, os.path.join(AUDIT_DIR, "V3_VIDEO_CLIPS_16x9_MIDFRAME_AUDIT.jpg"), "16:9", max_clips=24)
    build_video_audit_sheet(CLIPS_9x16_DIR, os.path.join(AUDIT_DIR, "V3_VIDEO_CLIPS_9x16_MIDFRAME_AUDIT.jpg"), "9:16", max_clips=20)
    print("=== V3 STAGE 4 COMPLETE ===")
