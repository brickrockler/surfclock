#!/usr/bin/env python3
"""
Resumes and completes the final V6 16mm/35mm Photochemical Film & Sunlit Cream 4K60 Mastering Pass,
promotes all verified V6 stills & cinemagraphs, builds the V6 Contact Sheet, and compiles the V6 Master 4K60 Showreels.
"""
import os
import re
import sys
import glob
import json
import shutil
import subprocess
from PIL import Image, ImageDraw

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
SCRIPTS_DIR = os.path.join(BASE, "scripts")
V6_RAW = os.path.join(BASE, "raw_renders", "v6_film_explorations")
FFMPEG = "/Users/jcolley/.gemini/jetski/bin/ffmpeg"

def get_video_info(path):
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        return None
    try:
        p = subprocess.run([FFMPEG, "-i", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        err = p.stderr
        m_res = re.search(r"(\d{3,4})x(\d{3,4})", err)
        m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err)
        if not m_res:
            return None
        w, h = int(m_res.group(1)), int(m_res.group(2))
        dur = 8.0
        if m_dur:
            dur = int(m_dur.group(1))*3600 + int(m_dur.group(2))*60 + float(m_dur.group(3))
        return {"w": w, "h": h, "dur": dur}
    except Exception:
        return None

def master_raw_omni_to_4k60_film(raw_mp4, out_mp4, is_vertical=False, preset="poetry_camera_16mm_50D"):
    info = get_video_info(raw_mp4)
    if not info:
        return False
    dur = info["dur"] if info["dur"] > 0 else 8.0
    pts = 10.0 / dur if dur < 9.8 else 1.0
    tw, th = (2160, 3840) if is_vertical else (3840, 2160)
    if preset == "poetry_camera_16mm_50D":
        film_vf = (
            "rgbashift=rh=-2:bh=2:rv=1:bv=-1,"
            "colorbalance=rs=0.04:gs=0.01:bs=-0.03:rm=0.05:gm=0.02:bm=-0.04:rh=0.08:gh=0.04:bh=-0.05,"
            "eq=contrast=0.97:brightness=0.02:saturation=0.95,"
            "noise=c0s=5:c0f=t+u,"
            "vignette=PI/6"
        )
    else:
        film_vf = (
            "rgbashift=rh=-1:bh=1,"
            "colorbalance=rs=0.02:gs=0.01:bs=-0.02:rh=0.05:gh=0.02:bh=-0.03,"
            "noise=c0s=3:c0f=t+u"
        )
    vf = f"setpts={pts:.6f}*PTS,fps=60,scale={tw}:{th}:flags=lanczos,{film_vf}"
    cmd = [
        FFMPEG, "-y", "-i", raw_mp4,
        "-vf", vf, "-t", "10.0", "-an",
        "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-pix_fmt", "yuv420p",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 5_000_000

def build_contact_sheet(image_paths, out_path, cols=5, thumb_w=768, thumb_h=432, title=""):
    rows = (len(image_paths) + cols - 1) // cols
    header_h = 80 if title else 0
    sheet = Image.new("RGB", (cols * thumb_w, header_h + rows * thumb_h), (18, 22, 28))
    draw = ImageDraw.Draw(sheet)
    if title:
        draw.text((32, 26), title, fill=(240, 244, 248))
    for idx, p in enumerate(image_paths):
        r, c = idx // cols, idx % cols
        x0, y0 = c * thumb_w, header_h + r * thumb_h
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((thumb_w - 16, thumb_h - 40), Image.Resampling.LANCZOS)
            sheet.paste(im, (x0 + (thumb_w - im.width) // 2, y0 + 8))
            draw.text((x0 + 12, y0 + thumb_h - 28), f"{idx+1:02d}. {os.path.basename(p)[:50]}", fill=(215, 225, 235))
        except Exception:
            pass
    sheet.save(out_path, format="JPEG", quality=93)

def concat_videos(video_paths, out_mp4):
    if not video_paths:
        return
    list_txt = out_mp4 + ".txt"
    with open(list_txt, "w") as f:
        for vp in video_paths:
            f.write(f"file '{vp}'\n")
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_txt, "-c", "copy", out_mp4],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(list_txt):
        os.remove(list_txt)

def main():
    v6_stills_dir = os.path.join(BASE, "01_4K_STUDIO_KEYFRAMES_AND_STILLS", "V6_16MM_35MM_FILM_AND_SUNLIT_CREAM_4K")
    os.makedirs(v6_stills_dir, exist_ok=True)
    clips_16x9_dir = os.path.join(BASE, "02_INDIVIDUAL_4K_CLIPS_16x9")
    clips_9x16_dir = os.path.join(BASE, "03_INDIVIDUAL_4K_CLIPS_9x16")
    showreels_dir = os.path.join(BASE, "00_MASTER_SHOWREELS")

    promoted_stills = []
    promoted_16x9_vids = []
    promoted_9x16_vids = []

    for i in range(1, 21):
        ag = f"v6_agent_{i:02d}"
        ag_dir = os.path.join(V6_RAW, ag)
        if not os.path.exists(ag_dir):
            continue
        is_vert = (i in (19, 20))
        preset = "orchid_35mm_250D_warm" if i in (2, 3, 12, 14, 15, 18, 19) else "poetry_camera_16mm_50D"

        stills = sorted([
            os.path.join(ag_dir, f) for f in os.listdir(ag_dir)
            if f.endswith(".jpg") and "audit_grid" not in f.lower()
            and "raw" not in f.lower() and "ungraded" not in f.lower()
            and "master" not in f.lower() and "poetry_camera_16mm_50d" not in f.lower()
        ])
        for sp in stills:
            dst = os.path.join(v6_stills_dir, os.path.basename(sp))
            shutil.copy2(sp, dst)
            promoted_stills.append(dst)

        raw_omnis = sorted(glob.glob(os.path.join(ag_dir, "*_omni_raw.mp4")))
        final_vpath = os.path.join(ag_dir, f"V6_A{i:02d}_FINAL_FILM_MASTER_4K60.mp4")

        existing_valid = None
        for cand in sorted(glob.glob(os.path.join(ag_dir, "*.mp4"))):
            if "_omni_raw" in cand or "_pre" in cand.lower() or "ungraded" in cand.lower() or "_raw" in cand.lower():
                continue
            inf = get_video_info(cand)
            if inf and ((inf["w"] == 3840 and inf["h"] == 2160) or (inf["w"] == 2160 and inf["h"] == 3840)) and os.path.getsize(cand) > 8_000_000:
                existing_valid = cand
                break

        if existing_valid:
            print(f"[{ag}] Using completed 4K60 master: {os.path.basename(existing_valid)}", flush=True)
            target_v = existing_valid
        elif raw_omnis:
            print(f"[{ag}] Mastering {os.path.basename(raw_omnis[0])} -> 4K 60fps ({preset})...", flush=True)
            ok = master_raw_omni_to_4k60_film(raw_omnis[0], final_vpath, is_vertical=is_vert, preset=preset)
            target_v = final_vpath if ok else None
        else:
            target_v = None

        if target_v and os.path.exists(target_v):
            if is_vert:
                dst_v = os.path.join(clips_9x16_dir, f"V6_9x16_A{i:02d}_{os.path.basename(target_v)}")
                shutil.copy2(target_v, dst_v)
                promoted_9x16_vids.append(dst_v)
            else:
                dst_v = os.path.join(clips_16x9_dir, f"V6_16x9_A{i:02d}_{os.path.basename(target_v)}")
                shutil.copy2(target_v, dst_v)
                promoted_16x9_vids.append(dst_v)

    sheet_path = os.path.join(BASE, "04_CONTACT_SHEETS_AND_AUDIT", "V6_ALL_FILM_AND_SUNLIT_CREAM_STILLS_SHEET.jpg")
    build_contact_sheet(promoted_stills, sheet_path, cols=5, title="SURF CLOCK V6 — 16MM / 35MM PHOTOCHEMICAL FILM & SUNLIT CREAM 4K COLLECTION")

    v6_reel_16x9 = os.path.join(showreels_dir, "SURF_CLOCK_V6_16MM_35MM_FILM_AND_SUNLIT_CREAM_SHOWREEL_4K60_16x9.mp4")
    v6_reel_9x16 = os.path.join(showreels_dir, "SURF_CLOCK_V6_VERTICAL_FILM_CINEMAGRAPH_REEL_4K60_9x16.mp4")
    concat_videos(promoted_16x9_vids, v6_reel_16x9)
    concat_videos(promoted_9x16_vids, v6_reel_9x16)

    print(f"\n=== V6 FINALIZATION COMPLETE ===", flush=True)
    print(f"Promoted V6 4K Stills: {len(promoted_stills)} -> {v6_stills_dir}", flush=True)
    print(f"Promoted V6 16:9 4K60 Cinemagraphs: {len(promoted_16x9_vids)} -> {v6_reel_16x9}", flush=True)
    print(f"Promoted V6 9:16 4K60 Cinemagraphs: {len(promoted_9x16_vids)} -> {v6_reel_9x16}", flush=True)

if __name__ == "__main__":
    main()
