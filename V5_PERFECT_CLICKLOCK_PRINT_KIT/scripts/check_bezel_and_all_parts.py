import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

v_f, n_f = load_stl("/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl")
# Check inner bezel opening at Z < 4.0
bezel = v_f[v_f[:, :, 2].max(axis=1) <= 4.01].reshape(-1, 3)
inner_bezel = bezel[(np.abs(bezel[:, 0]) < 110.0) & (np.abs(bezel[:, 1]) < 87.0)]
print("Front bezel inner opening max |X|, |Y|:", np.abs(inner_bezel[:, 0]).max(), np.abs(inner_bezel[:, 1]).max())
q1_b = inner_bezel[(inner_bezel[:, 0] > 95.0) & (inner_bezel[:, 1] > 72.0)]
print("Front bezel Q1 corner points (X>95, Y>72):")
for pt in np.unique(np.round(q1_b, 2), axis=0):
    print(" ", pt)
