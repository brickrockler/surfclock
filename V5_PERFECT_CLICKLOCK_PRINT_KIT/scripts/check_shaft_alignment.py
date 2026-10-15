import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

for name, path in [
    ("2_Dial_Face_WHITE_then_BLACK", "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl"),
    ("2_Dial_Face_QUEENSIE", "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl"),
    ("3_Motor_Mount_Plate (Backup)", "/tmp/stl_backups/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl"),
    ("3_Motor_Mount_Plate (NEW)", "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4NEW.stl"),
]:
    v, n = load_stl(path)
    # Find cylindrical holes near Y=0 (|Y| < 12, |n_z| < 0.1)
    side_tris = v[(np.abs(n[:, 2]) < 0.1) & (np.abs(v[:, :, 1].mean(axis=1)) < 10.0) & (v[:, :, 2].mean(axis=1) < 2.2)]
    xs = side_tris[:, :, 0].flatten()
    upper_x = xs[xs < 0]
    lower_x = xs[xs > 40]
    print(f"{name:35s}:")
    if len(upper_x):
        print(f"  Upper hole X range: [{upper_x.min():.2f}, {upper_x.max():.2f}] -> center X = {0.5*(upper_x.min()+upper_x.max()):.2f}")
    if len(lower_x):
        print(f"  Lower hole X range: [{lower_x.min():.2f}, {lower_x.max():.2f}] -> center X = {0.5*(lower_x.min()+lower_x.max()):.2f}")
