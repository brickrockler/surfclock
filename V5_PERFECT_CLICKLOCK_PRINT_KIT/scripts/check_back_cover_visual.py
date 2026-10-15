import struct, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

v, n = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
mask = n[:, 2] > 0.5
tris = v[mask]
fig, ax = plt.subplots(figsize=(6, 7), dpi=140)
ax.set_facecolor('#181B20')
polys = np.zeros((len(tris), 3, 2))
polys[:, :, 0] = tris[:, :, 1]
polys[:, :, 1] = -tris[:, :, 0]
ax.add_collection(PolyCollection(polys, facecolors='#66B2FF', edgecolors='none', alpha=0.85))
ax.set_xlim(-95, 95)
ax.set_ylim(-118, 118)
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig("/tmp/back_cover_check.png")
