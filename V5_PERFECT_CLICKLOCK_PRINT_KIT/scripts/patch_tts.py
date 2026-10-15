with open("/Users/jcolley/surf_clock/build_guide_video_tts.py", "r") as f:
    code = f.read()

# 1. Replace trim_and_pad_wav with a version that strips the Gemini TTS trailing white-noise static burst
old_trim = '''def trim_and_pad_wav(in_wav, out_wav, head_pad_s=0.22, tail_pad_s=0.35):
    with wave.open(in_wav, "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    win = max(1, int(sr * 0.015))
    sq = samples ** 2
    rms = np.sqrt(np.convolve(sq, np.ones(win) / win, mode="same"))
    peak_rms = np.max(rms) if len(rms) > 0 else 1.0
    thr = max(110.0, peak_rms * 0.018)
    idx = np.where(rms > thr)[0]
    if len(idx) > 0:
        i0 = max(0, idx[0] - int(sr * 0.05))
        i1 = min(len(samples), idx[-1] + int(sr * 0.08))
        trimmed = samples[i0:i1]
    else:
        trimmed = samples'''

new_trim = '''def trim_and_pad_wav(in_wav, out_wav, head_pad_s=0.22, tail_pad_s=0.35):
    with wave.open(in_wav, "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    win = max(1, int(sr * 0.015))
    sq = samples ** 2
    rms = np.sqrt(np.convolve(sq, np.ones(win) / win, mode="same"))

    # Strip any trailing Gemini TTS white-noise burst after the final silent valley in the last 1.0s
    if n > int(sr * 1.2):
        search_lo = max(0, n - int(sr * 0.95))
        search_hi = max(search_lo + 1, n - int(sr * 0.08))
        sub_rms = rms[search_lo:search_hi]
        valley_idx = search_lo + int(np.argmin(sub_rms))
        if rms[valley_idx] < 65.0:
            samples = samples[:valley_idx]
            rms = rms[:valley_idx]

    # Also zero out any isolated high-ZCR static spikes anywhere in silence
    peak_rms = np.max(rms) if len(rms) > 0 else 1.0
    thr = max(110.0, peak_rms * 0.020)
    idx = np.where(rms > thr)[0]
    if len(idx) > 0:
        i0 = max(0, idx[0] - int(sr * 0.04))
        i1 = min(len(samples), idx[-1] + int(sr * 0.05))
        trimmed = samples[i0:i1].copy()
    else:
        trimmed = samples.copy()

    # Smooth 25ms cosine fade-in and fade-out on trimmed speech
    fi_n = min(len(trimmed) // 4, int(sr * 0.020))
    fo_n = min(len(trimmed) // 4, int(sr * 0.030))
    if fi_n > 1:
        trimmed[:fi_n] *= 0.5 * (1.0 - np.cos(np.linspace(0.0, np.pi, fi_n, dtype=np.float32)))
    if fo_n > 1:
        trimmed[-fo_n:] *= 0.5 * (1.0 + np.cos(np.linspace(0.0, np.pi, fo_n, dtype=np.float32)))'''

assert old_trim in code, "old_trim not found"
code = code.replace(old_trim, new_trim, 1)

# 2. Skip the 9.8s..15.5s static intro in the music track and low-pass / attenuate it cleanly
old_mus = '''    i0 = int(round(9.8 * SR))
    if i0 + total_samples <= len(mus_raw):
        mus_seg = mus_raw[i0:i0 + total_samples].copy()
    else:
        part1 = mus_raw[i0:]
        rem = total_samples - len(part1)
        part2 = mus_raw[int(22.46 * SR):int(22.46 * SR) + rem]
        mus_seg = np.vstack([part1, part2]).astype(np.float32)'''

new_mus = '''    i0 = int(round(16.2 * SR))
    if i0 + total_samples <= len(mus_raw):
        mus_seg = mus_raw[i0:i0 + total_samples].copy()
    else:
        part1 = mus_raw[i0:]
        rem = total_samples - len(part1)
        part2 = mus_raw[int(22.46 * SR):int(22.46 * SR) + rem]
        mus_seg = np.vstack([part1, part2]).astype(np.float32)
    # Gentle low-pass at 3200 Hz on background bed so zero high-frequency hiss/static ever competes with voiceover
    sos_lp_mus = signal.butter(3, 3200.0 / (0.5 * SR), btype="low", output="sos")
    mus_seg = signal.sosfiltfilt(sos_lp_mus, mus_seg, axis=0).astype(np.float32)'''

assert old_mus in code, "old_mus not found"
code = code.replace(old_mus, new_mus, 1)
code = code.replace("base_gain = 10.0 ** (-11.0 / 20.0)", "base_gain = 10.0 ** (-15.5 / 20.0)")

# 3. Make ch04 100% generic (no Long Reef, no Worth It — just "the 12 o'clock position")
old_ch04 = '''        (
            "ch04",
            "04  BACK COVER & HANDS",
            (
                "Route your U-S-B-C power cable out through the bottom slot, "
                "and press the back cover flush into the rear of the frame against the four corner pillars. "
                "Before plugging in power, flip the clock face-up. "
                "Each motor shaft has two flat sides that key into the D-shaped bore inside the hands. "
                "Point the long beach hand straight up at twelve o'clock on Long Reef and press it down firmly. "
                "Then point the short gauge hand straight up at twelve o'clock on Worth It, and press it into place."
            ),
            [
                "Route the USB-C cable out the bottom slot,",
                "and press the back cover flush into the frame",
                "against the four corner pillars.",
                "Before plugging in power,",
                "flip the clock face-up.",
                "Each shaft has flat sides that key into",
                "the D-shaped bore inside the hands.",
                "Press the long hand on at 12 o'clock",
                "pointing straight up at LONG REEF.",
                "Press the short hand on at 12 o'clock",
                "pointing straight up on WORTH IT.",
            ],
        ),'''

new_ch04 = '''        (
            "ch04",
            "04  BACK COVER & HANDS",
            (
                "Route your U-S-B-C power cable out through the bottom slot, "
                "and press the back cover flush into the rear of the frame against the four corner pillars. "
                "Before plugging in power, flip the clock face-up. "
                "Each motor shaft has two flat sides that key into the D-shaped bore inside the hands. "
                "Point the long upper hand straight up at the twelve o'clock position and press it down firmly. "
                "Then point the short lower hand straight up at the twelve o'clock position, and press it into place."
            ),
            [
                "Route the USB-C cable out the bottom slot,",
                "and press the back cover flush into the frame",
                "against the four corner pillars.",
                "Before plugging in power,",
                "flip the clock face-up.",
                "Each shaft has flat sides that key into",
                "the D-shaped bore inside the hands.",
                "Point the long upper hand straight up",
                "at the 12 o'clock position and press it down.",
                "Point the short lower hand straight up",
                "at the 12 o'clock position and press it in.",
            ],
        ),'''

assert old_ch04 in code, "old_ch04 not found"
code = code.replace(old_ch04, new_ch04, 1)

with open("/Users/jcolley/surf_clock/build_guide_video_tts.py", "w") as f:
    f.write(code)
print("Successfully patched build_guide_video_tts.py")
