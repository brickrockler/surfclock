#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

PIPE_DIR = Path("/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE")
USER_REF = Path("/Users/jcolley/.gemini/jetski/brain/47620447-b5c2-401d-af72-8cea98f34b48/.user_uploaded/media_1791970931092.jpg")
OUT_DIR = PIPE_DIR / "01_4K_STUDIO_KEYFRAMES_AND_STILLS" / "V3_ORCHID_POETRY_ARCHDIGEST_4K"
OUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR = PIPE_DIR / "04_CONTACT_SHEETS_AND_AUDIT"

font_path = "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf"
if not Path(font_path).exists():
    font_path = "/System/Library/Fonts/HelveticaNeue.ttc"

LABELS_4K = [
    (1835,  668, 2005,  722, "LONG REEF", 1920,  694, 30),
    (1595,  808, 1745,  858, "QUEENSIE",  1669,  832, 27),
    (2110,  802, 2255,  854, "DEE WHY",   2182,  826, 27),
    (1598, 1046, 1735, 1094, "FRESHIE",   1666, 1069, 26),
    (2100, 1046, 2265, 1096, "CURL CURL", 2184, 1071, 26),
    (1700, 1414, 1782, 1460, "NAH",       1741, 1437, 22),
    (2068, 1424, 2156, 1470, "YEAH",      2112, 1447, 22),
    (1845, 1480, 1990, 1528, "WORTH IT?", 1918, 1504, 22),
]

def remove_electric_cyan_highlights(img: np.ndarray) -> np.ndarray:
    """Eliminates any weird electric cyan-blue highlight along white gauge arcs or bevels (media_1792014355089.png)."""
    out = img.astype(np.float32)
    b, g, r = out[:, :, 0], out[:, :, 1], out[:, :, 2]
    # Electric cyan has high B and G, much lower R, and high brightness
    cyan_excess = np.maximum(0.0, np.minimum(b, g) - r - 38.0)
    mask = np.clip((cyan_excess - 10.0) / 35.0, 0.0, 1.0)
    # Desaturate electric cyan toward neutral matte off-white / slate navy
    neutral = (0.25 * b + 0.40 * g + 0.35 * r)
    out[:, :, 0] = b * (1.0 - 0.75 * mask) + neutral * (0.75 * mask)
    out[:, :, 1] = g * (1.0 - 0.80 * mask) + neutral * (0.80 * mask)
    out[:, :, 2] = r * (1.0 - 0.65 * mask) + neutral * (0.65 * mask)
    return np.clip(out, 0, 255).astype(np.uint8)

def clean_box_with_local_navy(img: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> None:
    pad = 8
    roi_ext = img[y1-pad:y2+pad, x1-pad:x2+pad].astype(np.float32)
    mask = np.zeros(roi_ext.shape[:2], dtype=np.uint8)
    mask[pad:-pad, pad:-pad] = 255
    b, g, r = cv2.split(roi_ext)
    bright = ((r > 70) | (g > 70) | (b > 95)).astype(np.uint8) * 255
    mask = cv2.bitwise_or(mask, bright)
    inpainted = cv2.inpaint(roi_ext.astype(np.uint8), mask, 9, cv2.INPAINT_NS)
    inpainted_blur = cv2.GaussianBlur(inpainted, (11, 11), 3.0)
    img[y1:y2, x1:x2] = inpainted_blur[pad:-pad, pad:-pad]

def upgrade_clock_dial_and_molded_texture(img_4k: np.ndarray) -> np.ndarray:
    out = remove_electric_cyan_highlights(img_4k)
    for x1, y1, x2, y2, txt, cx, cy, fsz in LABELS_4K:
        clean_box_with_local_navy(out, x1, y1, x2, y2)

    h, w = out.shape[:2]
    txt_layer = Image.new("L", (w * 2, h * 2), 0)
    for x1, y1, x2, y2, txt, cx, cy, fsz in LABELS_4K:
        font = ImageFont.truetype(font_path, int(fsz * 2))
        tmp = Image.new("L", (640, 160), 0)
        tdraw = ImageDraw.Draw(tmp)
        bbox = tdraw.textbbox((0, 0), txt, font=font, stroke_width=1)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tdraw.text((320 - tw // 2 - bbox[0], 80 - th // 2 - bbox[1]), txt, fill=255, font=font, stroke_width=1)
        new_w = int(640 * 0.88)
        tmp_cond = tmp.resize((new_w, 160), resample=Image.Resampling.BICUBIC)
        txt_layer.paste(tmp_cond, (int(cx * 2 - new_w // 2), int(cy * 2 - 80)))

    txt_mask = cv2.resize(np.array(txt_layer, dtype=np.float32) / 255.0, (w, h), interpolation=cv2.INTER_AREA)
    txt_shadow = np.roll(np.roll(txt_mask, 1, axis=0), 1, axis=1)
    txt_mask_blur = cv2.GaussianBlur(txt_mask, (3, 3), 0.50)[..., None]
    txt_shad_blur = cv2.GaussianBlur(txt_shadow, (3, 3), 0.8)[..., None]

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    shade = np.clip(1.0 - 0.13 * ((xx - 1600.0) / 700.0), 0.84, 1.04)[..., None]
    ink_bgr = np.array([232.0, 229.0, 224.0], dtype=np.float32)[None, None, :] * shade

    out_f = out.astype(np.float32)
    out_f = out_f * (1.0 - 0.38 * txt_shad_blur)
    out_f = out_f * (1.0 - 0.94 * txt_mask_blur) + ink_bgr * (0.94 * txt_mask_blur)

    # Authentic VDI-24 Braun / Orchid / Teenage Engineering micro-bead molded polymer grain
    rng = np.random.default_rng(42)
    noise_fine = rng.standard_normal((h, w)).astype(np.float32)
    noise_med  = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (3, 3), 0.9)
    emboss = cv2.Sobel(noise_med, cv2.CV_32F, 1, 1, ksize=3) * 0.60 + noise_fine * 0.70
    emboss = np.clip(emboss, -2.6, 2.6) * 2.85

    clock_mask = np.zeros((h, w), dtype=np.float32)
    clock_mask[456:1648, 1460:2380] = 1.0
    clock_mask = cv2.GaussianBlur(clock_mask, (7, 7), 1.5)
    out_f = out_f + (emboss * clock_mask)[..., None]

    return np.clip(out_f, 0, 255).astype(np.uint8)

raw = cv2.imread(str(USER_REF))
img_4k_raw = cv2.resize(raw, (3840, 2160), interpolation=cv2.INTER_LANCZOS4)
img_4k_crisp = upgrade_clock_dial_and_molded_texture(img_4k_raw)

master_16x9_path = OUT_DIR / "MASTER_REF_4K_16x9_CrispBraunMolded.jpg"
cv2.imwrite(str(master_16x9_path), img_4k_crisp, [cv2.IMWRITE_JPEG_QUALITY, 98])

crop_9x16 = img_4k_crisp[:, 1312:2527]
master_9x16 = cv2.resize(crop_9x16, (2160, 3840), interpolation=cv2.INTER_LANCZOS4)
master_9x16_path = OUT_DIR / "MASTER_REF_4K_9x16_CrispBraunMolded.jpg"
cv2.imwrite(str(master_9x16_path), master_9x16, [cv2.IMWRITE_JPEG_QUALITY, 98])

before_crop = img_4k_raw[440:1660, 1440:2400].copy()
after_crop  = img_4k_crisp[440:1660, 1440:2400].copy()
cv2.putText(before_crop, "BEFORE (1024x571 Blurry Text)", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 180, 255), 2)
cv2.putText(after_crop,  "AFTER (4K Crisp Pad-Print + VDI-24 Molded)", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 255, 180), 2)
comp_path = AUDIT_DIR / "V3_BEFORE_AFTER_4K_CRISP_BRAUN_MOLDED_DIAL.jpg"
cv2.imwrite(str(comp_path), np.hstack([before_crop, after_crop]), [cv2.IMWRITE_JPEG_QUALITY, 96])
print("Updated", comp_path)
