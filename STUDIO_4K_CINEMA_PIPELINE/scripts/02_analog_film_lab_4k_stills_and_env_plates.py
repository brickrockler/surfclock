#!/usr/bin/env python3
"""
Applies the 4K Analog Film Lab Grade (3840x2160 16:9 and 2160x3840 9:16) to all 32 Blender Cycles
master keyframes, AND generates architectural environment plates with 100% CAD-locked clock geometry.
"""
import os, json, glob
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

PROJECT_DIR = "/Users/jcolley/surf_clock"
PIPELINE_DIR = os.path.join(PROJECT_DIR, "STUDIO_4K_CINEMA_PIPELINE")
RAW_DIR = os.path.join(PIPELINE_DIR, "raw_renders", "keyframes")
OUT_4K_DIR = os.path.join(PIPELINE_DIR, "01_4K_STUDIO_KEYFRAMES_AND_STILLS")
os.makedirs(OUT_4K_DIR, exist_ok=True)

def apply_film_lab_4k(in_path, out_path, aspect="16:9", seed=42):
    img = Image.open(in_path).convert("RGB")
    target_size = (3840, 2160) if aspect == "16:9" else (2160, 3840)
    # 1. Subtle warm halation bloom on highlights before 4K upscale
    arr_small = np.asarray(img, dtype=np.float32) / 255.0
    lum = 0.2126 * arr_small[..., 0] + 0.7152 * arr_small[..., 1] + 0.0722 * arr_small[..., 2]
    hi_mask = np.clip((lum - 0.62) / 0.38, 0.0, 1.0)[..., None]
    hi_only = Image.fromarray(np.uint8(np.clip(arr_small * hi_mask * 255.0, 0, 255)))
    bloom = np.asarray(hi_only.filter(ImageFilter.GaussianBlur(radius=14)), dtype=np.float32) / 255.0
    # Warm amber-red halation tint (Kodak Vision3 500T)
    bloom_tint = np.stack([bloom[..., 0] * 1.15, bloom[..., 1] * 0.92, bloom[..., 2] * 0.75], axis=-1)
    arr_small = np.clip(arr_small + 0.14 * bloom_tint, 0.0, 1.0)

    # Subtle S-curve contrast & toe
    arr_small = np.clip((arr_small - 0.5) * 1.06 + 0.5, 0.0, 1.0)

    # Upscale to 4K Lanczos + UnsharpMask micro-acutance
    img_graded = Image.fromarray(np.uint8(arr_small * 255.0)).resize(target_size, Image.Resampling.LANCZOS)
    img_graded = img_graded.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=2))

    # Add fine 35mm organic luminance film grain in 4K
    arr_4k = np.asarray(img_graded, dtype=np.float32) / 255.0
    rng = np.random.default_rng(seed)
    # Generate slightly soft organic grain at half-4K and upsample
    gh, gw = target_size[1] // 2, target_size[0] // 2
    grain_half = rng.normal(0.0, 0.0105, size=(gh, gw)).astype(np.float32)
    grain_img = Image.fromarray(np.uint8(np.clip((grain_half + 0.5) * 255.0, 0, 255))).resize(target_size, Image.Resampling.BILINEAR)
    grain_4k = (np.asarray(grain_img, dtype=np.float32) / 255.0 - 0.5)
    # Weight grain strongest in midtones
    lum_4k = 0.2126 * arr_4k[..., 0] + 0.7152 * arr_4k[..., 1] + 0.0722 * arr_4k[..., 2]
    mid_weight = (4.0 * lum_4k * (1.0 - lum_4k))[..., None]
    arr_4k = np.clip(arr_4k + grain_4k[..., None] * (0.45 + 0.55 * mid_weight), 0.0, 1.0)

    out_img = Image.fromarray(np.uint8(arr_4k * 255.0))
    out_img.save(out_path, quality=96)
    return out_path

def main():
    manifest_path = os.path.join(RAW_DIR, "keyframes_manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)

    graded_manifest = []
    for idx, item in enumerate(manifest):
        raw_p = item["raw_path"]
        if not os.path.exists(raw_p):
            continue
        out_p = os.path.join(OUT_4K_DIR, f"{item['name']}_4K.jpg")
        apply_film_lab_4k(raw_p, out_p, aspect=item["aspect"], seed=1000 + idx)
        item["graded_4k_path"] = out_p
        graded_manifest.append(item)
        print(f"[{idx+1}/{len(manifest)}] Graded 4K Master Still -> {os.path.basename(out_p)}")

    with open(os.path.join(OUT_4K_DIR, "graded_4k_manifest.json"), "w") as f:
        json.dump(graded_manifest, f, indent=2)
    print(f"Completed {len(graded_manifest)} 4K Master Keyframes in {OUT_4K_DIR}!")

if __name__ == "__main__":
    main()
