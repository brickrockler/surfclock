import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

v, n = load_stl("/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4NEW.stl")
pts = v.reshape(-1, 3)
print("NEW plate bbox:", pts.min(axis=0), "to", pts.max(axis=0))
print("Unique Z in NEW plate:", np.unique(np.round(pts[:, 2], 2)))
