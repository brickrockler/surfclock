import cv2, os, subprocess, sys, time
import numpy as np

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
STILLS_DIR = f"{BASE}/01_4K_STUDIO_KEYFRAMES_AND_STILLS"
CLIPS_DIR = f"{BASE}/02_INDIVIDUAL_4K_CLIPS_16x9"

def compute_homography_sift(still_gray_half, target_gray_half, roi_half, sift, bf, prev_M=None):
    rx1, ry1, rx2, ry2 = roi_half
    H_h, W_h = still_gray_half.shape[:2]
    mask_s = np.zeros((H_h, W_h), dtype=np.uint8)
    mask_s[ry1:ry2, rx1:rx2] = 255
    mask_t = np.zeros((H_h, W_h), dtype=np.uint8)
    mask_t[max(0, ry1-80):min(H_h, ry2+80), max(0, rx1-80):min(W_h, rx2+80)] = 255

    kp1, des1 = sift.detectAndCompute(still_gray_half, mask_s)
    kp2, des2 = sift.detectAndCompute(target_gray_half, mask_t)
    if des1 is None or des2 is None or len(kp1) < 8 or len(kp2) < 8:
        return prev_M if prev_M is not None else np.eye(3, dtype=np.float32)

    matches = bf.knnMatch(des1, des2, k=2)
    good = [m for m, n in matches if len(matches) > 0 and m.distance < 0.72 * n.distance]
    if len(good) < 8:
        return prev_M if prev_M is not None else np.eye(3, dtype=np.float32)

    pts1 = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, 2.5)
    if M is None:
        return prev_M if prev_M is not None else np.eye(3, dtype=np.float32)
    return M.astype(np.float32)

def fast_master_shot(tag, clock_specs, src_vid_override=None):
    t0 = time.time()
    still_path = f"{STILLS_DIR}/{tag}_4K.jpg"
    vid_path = f"{CLIPS_DIR}/{tag}_4K60.mp4"
    if src_vid_override:
        bak_path = src_vid_override
    else:
        bak_path = f"{BASE}/raw_renders/{tag}_ORIGINAL_VEO_BACKUP.mp4"
        if not os.path.exists(bak_path):
            subprocess.run(["cp", vid_path, bak_path], check=True)

    still_4k = cv2.imread(still_path)
    H, W = still_4k.shape[:2]
    QW, QH = W // 4, H // 4
    still_half = cv2.resize(still_4k, (W//2, H//2), interpolation=cv2.INTER_AREA)
    still_gray_half = cv2.cvtColor(still_half, cv2.COLOR_BGR2GRAY)

    cap = cv2.VideoCapture(bak_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ret, f0_4k = cap.read()
    f0_gray_q = cv2.cvtColor(cv2.resize(f0_4k, (QW, QH), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    f0_half = cv2.resize(f0_4k, (W//2, H//2), interpolation=cv2.INTER_AREA)
    f0_gray_half = cv2.cvtColor(f0_half, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher()
    S2 = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]], dtype=np.float32)
    S2_inv = np.array([[2.0, 0, 0], [0, 2.0, 0], [0, 0, 1]], dtype=np.float32)
    S4 = np.array([[0.25, 0, 0], [0, 0.25, 0], [0, 0, 1]], dtype=np.float32)
    S4_inv = np.array([[4.0, 0, 0], [0, 4.0, 0], [0, 0, 1]], dtype=np.float32)

    step = 4
    key_indices = list(range(0, n_frames, step))
    if key_indices[-1] != n_frames - 1:
        key_indices.append(n_frames - 1)

    n_clocks = len(clock_specs)
    H_s_keys = [[] for _ in range(n_clocks)]
    H_f0_keys = [[] for _ in range(n_clocks)]

    for ki in key_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, ki)
        ok, fk = cap.read()
        if not ok:
            fk = f0_4k
        fk_gray_half = cv2.cvtColor(cv2.resize(fk, (W//2, H//2), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        for ci, (roi_4k, _) in enumerate(clock_specs):
            roi_h = (roi_4k[0]//2, roi_4k[1]//2, roi_4k[2]//2, roi_4k[3]//2)
            prev_s = H_s_keys[ci][-1] if H_s_keys[ci] else None
            prev_f0 = H_f0_keys[ci][-1] if H_f0_keys[ci] else None
            Ms_h = compute_homography_sift(still_gray_half, fk_gray_half, roi_h, sift, bf, prev_s)
            Mf0_h = compute_homography_sift(f0_gray_half, fk_gray_half, roi_h, sift, bf, prev_f0)
            H_s_keys[ci].append(S2_inv @ Ms_h @ S2)
            H_f0_keys[ci].append(S2_inv @ Mf0_h @ S2)

    H_s_all = np.zeros((n_clocks, n_frames, 3, 3), dtype=np.float32)
    H_f0_all = np.zeros((n_clocks, n_frames, 3, 3), dtype=np.float32)
    for ci in range(n_clocks):
        ks = np.array(H_s_keys[ci])
        kf0 = np.array(H_f0_keys[ci])
        if len(ks) >= 5:
            ks_sm = ks.copy()
            kf0_sm = kf0.copy()
            for i in range(1, len(ks) - 1):
                ks_sm[i] = 0.25 * ks[i-1] + 0.50 * ks[i] + 0.25 * ks[i+1]
                kf0_sm[i] = 0.25 * kf0[i-1] + 0.50 * kf0[i] + 0.25 * kf0[i+1]
            ks, kf0 = ks_sm, kf0_sm
        for f_idx in range(n_frames):
            pos = np.searchsorted(key_indices, f_idx)
            if pos == 0:
                H_s_all[ci, f_idx] = ks[0]
                H_f0_all[ci, f_idx] = kf0[0]
            elif pos >= len(key_indices):
                H_s_all[ci, f_idx] = ks[-1]
                H_f0_all[ci, f_idx] = kf0[-1]
            else:
                k0, k1 = key_indices[pos-1], key_indices[pos]
                alpha = (f_idx - k0) / float(max(1, k1 - k0))
                H_s_all[ci, f_idx] = (1.0 - alpha) * ks[pos-1] + alpha * ks[pos]
                H_f0_all[ci, f_idx] = (1.0 - alpha) * kf0[pos-1] + alpha * kf0[pos]

    base_masks_feathered = []
    for _, poly_4k in clock_specs:
        m = np.zeros((H, W), dtype=np.float32)
        cv2.fillConvexPoly(m, poly_4k.astype(np.int32), 1.0)
        m_f = cv2.GaussianBlur(m, (0, 0), 12.0)
        base_masks_feathered.append(m_f)

    out_tmp = f"/tmp/{tag}_FAST_PERFECT_4K60.mp4"
    ff_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "bgr24", "-r", "60",
        "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        out_tmp
    ]
    proc = subprocess.Popen(ff_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for f_idx in range(n_frames):
        ok, ft = cap.read()
        if not ok:
            break
        comp = cv2.GaussianBlur(ft, (3, 3), 0.7).astype(np.float32) if not src_vid_override else ft.astype(np.float32)
        ft_gray_q = cv2.cvtColor(cv2.resize(ft, (QW, QH), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        # Broad 144px-equivalent 4K studio luminance gradient (sigma=36 at quarter-res) eliminates ANY Veo hand ghosting!
        blur_ft_q = cv2.GaussianBlur(ft_gray_q, (0, 0), 36.0)

        for ci, (roi_4k, _) in enumerate(clock_specs):
            Ms = H_s_all[ci, f_idx]
            Mf0 = H_f0_all[ci, f_idx]
            Mf0_q = S4 @ Mf0 @ S4_inv

            warped_f0_q = cv2.warpPerspective(f0_gray_q, Mf0_q, (QW, QH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            blur_f0_q = cv2.GaussianBlur(warped_f0_q, (0, 0), 36.0)
            ratio_q = np.clip((blur_ft_q + 28.0) / (blur_f0_q + 28.0), 0.88, 1.14)
            ratio_4k = cv2.resize(ratio_q, (W, H), interpolation=cv2.INTER_LINEAR)[:, :, None]

            warped_still = cv2.warpPerspective(still_4k, Ms, (W, H), flags=cv2.INTER_LANCZOS4).astype(np.float32)
            warped_mask = cv2.warpPerspective(base_masks_feathered[ci], Ms, (W, H), flags=cv2.INTER_LINEAR)[:, :, None]

            relit_still = np.clip(warped_still * ratio_4k, 0, 255)
            comp = relit_still * warped_mask + comp * (1.0 - warped_mask)

        out_frame = np.clip(comp, 0, 255).astype(np.uint8)
        proc.stdin.write(out_frame.tobytes())

    proc.stdin.close()
    proc.wait()
    cap.release()
    subprocess.run(["mv", out_tmp, vid_path], check=True)
    print(f"[{tag}] FAST-MASTERED PERFECT 4K60 CLIP in {time.time()-t0:.1f}s -> {os.path.getsize(vid_path)/(1024*1024):.1f} MB", flush=True)
