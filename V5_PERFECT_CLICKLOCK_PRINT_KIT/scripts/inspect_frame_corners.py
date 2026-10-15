import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

for name, p in [
    ("1_Outer_Frame_MATTE_WHITE", "/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl"),
    ("1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes", "/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl"),
]:
    v, n = load_stl(p)
    print(f"=== {name} ===")
    for z_val in [4.0, 6.4, 6.65, 9.65, 10.0, 11.2, 47.9, 49.0]:
        sub = v[np.abs(v[:, :, 2].mean(axis=1) - z_val) < 0.25]
        if len(sub):
            pts = sub.reshape(-1, 3)
            # look at positive quadrant (X>0, Y>0)
            q1 = pts[(pts[:,0] > 0) & (pts[:,1] > 0)]
            print(f"  Z ~ {z_val:5.2f} (tris={len(sub):4d}): Q1 X in [{q1[:,0].min():6.2f}, {q1[:,0].max():6.2f}], Y in [{q1[:,1].min():6.2f}, {q1[:,1].max():6.2f}]")

    # Also slice a cross-section of Q1 corner at Z = 5.0, Z = 8.0, Z = 25.0, Z = 48.5
    pts = v.reshape(-1, 3)
    for z0, z1 in [(4.0, 6.4), (6.4, 10.0), (10.0, 12.5), (12.5, 47.0), (47.0, 49.0)]:
        mid = v[(v[:,:,2].mean(axis=1) > z0) & (v[:,:,2].mean(axis=1) < z1)]
        q1 = mid.reshape(-1, 3)
        q1 = q1[(q1[:,0] > 50) & (q1[:,1] > 50)]
        if len(q1):
            print(f"  Slice Z in ({z0:4.1f}, {z1:4.1f}): Q1 inner X_min={q1[:,0].min():6.2f}, Y_min={q1[:,1].min():6.2f}")
