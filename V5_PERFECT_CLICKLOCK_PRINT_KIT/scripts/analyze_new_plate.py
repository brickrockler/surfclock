import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

v, n = load_stl("/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4NEW.stl")

# Find all features above Z = 3.0 mm
high_tris = v[v[:, :, 2].max(axis=1) > 3.05]
print("Total triangles > Z=3.05:", len(high_tris))

# Let's inspect what script generated 3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4NEW.stl or 03_internal_engineering_deck.stl!
