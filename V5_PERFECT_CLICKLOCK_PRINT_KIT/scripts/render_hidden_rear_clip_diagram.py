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

fig, axes = plt.subplots(1, 3, figsize=(20, 7.5), dpi=160)
fig.patch.set_facecolor('#111317')

# Panel 1: OUTSIDE REAR VIEW of 4_Back_Cover (Z = 0 face — what you see on the back of the clock!)
ax1 = axes[0]
ax1.set_facecolor('#181B20')
v1, n1 = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
mask_out = n1[:, 2] < -0.5  # Z = 0 outer rear face!
tris_out = v1[mask_out]
polys_out = np.zeros((len(tris_out), 3, 2))
polys_out[:, :, 0] = tris_out[:, :, 1]
polys_out[:, :, 1] = -tris_out[:, :, 0]
ax1.add_collection(PolyCollection(polys_out, facecolors='#D8DFE8', edgecolors='none'))
ax1.annotate("ZERO Corner Screw Holes!\n(Filled solid & flush)",
             xy=(81.5, 104.5), xytext=(10.0, 95.0),
             color='#00FF9D', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#00FF9D', lw=1.3),
             arrowprops=dict(arrowstyle='->', color='#00FF9D', lw=1.6))
ax1.annotate("ZERO Perimeter Through-Slots!\n(100% unbroken outer border)",
             xy=(-86.0, 0.0), xytext=(-55.0, 0.0),
             color='#66E0FF', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#66E0FF', lw=1.3),
             arrowprops=dict(arrowstyle='->', color='#66E0FF', lw=1.6))
ax1.set_xlim(-98, 98)
ax1.set_ylim(-120, 120)
ax1.set_aspect('equal')
ax1.set_title("1. Outside Rear Face (What You See)\n100% Seamless — Zero Slots, Zero Screw Holes", color='white', fontsize=11, fontweight='bold', pad=10)
ax1.tick_params(colors='#78828E')

# Panel 2: INSIDE VIEW of Pure Flat Frosted Translucent Back Cover (Showing the 10 Hidden Internal Snap-Clips!)
ax2 = axes[1]
ax2.set_facecolor('#181B20')
v2, n2 = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_OPTIONAL_Back_Cover_PURE_FLAT_TRANSLUCENT_PrusaMK4.stl")
mask_in = n2[:, 2] > 0.1
tris_in = v2[mask_in]
z_in = tris_in[:, :, 2].mean(axis=1)
polys_in = np.zeros((len(tris_in), 3, 2))
polys_in[:, :, 0] = tris_in[:, :, 1]
polys_in[:, :, 1] = -tris_in[:, :, 0]
cols_in = np.zeros((len(tris_in), 4))
for i in range(len(tris_in)):
    if z_in[i] > 3.2:
        cols_in[i] = [0.00, 1.00, 0.62, 1.0]  # Hidden internal snap clips (Z = 3.0..5.8mm)
    elif z_in[i] > 2.5:
        cols_in[i] = [0.40, 0.78, 1.00, 0.90] # 3.0mm outer rim
    else:
        cols_in[i] = [0.28, 0.55, 0.78, 0.55] # 2.0mm flat optical window
ax2.add_collection(PolyCollection(polys_in, facecolors=cols_in, edgecolors='none'))
ax2.annotate("10x Hidden Internal Cantilever Snap-Clips\n(Stand up on the INSIDE face Z=3.0..5.8mm,\ncompletely invisible from the outside!)",
             xy=(-86.5, 62.0), xytext=(-68.0, 25.0),
             color='#00FF9D', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#00FF9D', lw=1.3),
             arrowprops=dict(arrowstyle='->', color='#00FF9D', lw=1.6))
ax2.annotate("Uniform 2.0mm Flat Optical Window\n(For Translucent Frosted PLA/PETG!)",
             xy=(0.0, -20.0), xytext=(-62.0, -55.0),
             color='#66E0FF', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#66E0FF', lw=1.3),
             arrowprops=dict(arrowstyle='->', color='#66E0FF', lw=1.6))
ax2.set_xlim(-98, 98)
ax2.set_ylim(-120, 120)
ax2.set_aspect('equal')
ax2.set_title("2. Inside Face of Back Cover\n(10 Hidden Internal Snap-Clips + Flat Exhibition Option)", color='white', fontsize=11, fontweight='bold', pad=10)
ax2.tick_params(colors='#78828E')

# Panel 3: Cross-Section of How the Hidden Internal Snap-Clip Works Inside 1_Outer_Frame
ax3 = axes[2]
ax3.set_facecolor('#181B20')

# Draw Outer Frame Wall near rear (Z = 42 to 52 mm)
ax3.add_patch(plt.Rectangle((10, 42.0), 10.0, 10.0, fc='#D0D6DC', ec='white', lw=1.5))
ax3.text(15.0, 44.0, "1_Outer_Frame\nWall", ha='center', va='center', color='#111317', fontsize=8.5, fontweight='bold')

# Draw Hidden Internal Catch on Frame Wall (Z = 45.6 to 48.6 mm, BELOW the Z = 49..52mm back cover!)
catch_poly = np.array([[20.0, 45.6], [23.5, 46.8], [23.5, 47.4], [20.0, 48.6]])
ax3.add_patch(plt.Polygon(catch_poly, fc='#66E0FF', ec='white', lw=1.3))
ax3.annotate("Hidden Internal Frame Catch\n(Z = 45.6..48.6mm, INSIDE the clock\nso outer seam at Z=52mm is 100% smooth!)",
             xy=(23.5, 47.1), xytext=(36.0, 44.0),
             color='#66E0FF', fontsize=8.2, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#66E0FF', lw=1.2),
             arrowprops=dict(arrowstyle='->', color='#66E0FF', lw=1.5))

# Draw 4_Back_Cover Base Plate sitting flush at Z = 49.0 to 52.0 mm
ax3.add_patch(plt.Rectangle((20.4, 49.0), 65.0, 3.0, fc='#4BA3FF', alpha=0.85, ec='white', lw=1.5))
ax3.text(55.0, 50.5, "4_Back_Cover (Flush at Z = 49.0..52.0mm)", ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')

# Draw Hidden Cantilever Snap-Clip rising from the INSIDE of 4_Back_Cover (from Z=49.0 up to Z=46.2mm inside the cavity)
clip_poly = np.array([
    [22.5, 49.0],
    [22.5, 47.7],
    [20.2, 47.0],
    [20.2, 46.6],
    [23.0, 46.0],
    [26.5, 46.0],
    [26.5, 49.0],
])
ax3.add_patch(plt.Polygon(clip_poly, fc='#00FF9D', ec='white', lw=1.3))
ax3.annotate("Hidden Internal Cantilever Clip\n(Rises from INSIDE of Back Cover,\nflexes inward & CLICKS behind frame catch!)",
             xy=(23.0, 46.4), xytext=(36.0, 47.5),
             color='#00FF9D', fontsize=8.2, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#0D1014', ec='#00FF9D', lw=1.2),
             arrowprops=dict(arrowstyle='->', color='#00FF9D', lw=1.5))

# Highlight the 100% unbroken outside rear surface at Z = 52.0 mm
ax3.plot([10, 85], [52.0, 52.0], color='#FFD166', lw=3.0, ls='--')
ax3.text(48.0, 53.3, "↑ OUTSIDE BACK SURFACE (Z = 52.0mm): 100% Flush, Unbroken & Slot-Free! ↑",
         ha='center', va='center', color='#FFD166', fontsize=8.5, fontweight='bold')

ax3.set_xlim(5, 90)
ax3.set_ylim(54.5, 41.0)
ax3.set_ylabel("Depth Z (mm)", color='white', fontsize=9.5)
ax3.set_xticks([])
ax3.tick_params(colors='#78828E')
ax3.set_title("3. Cross-Section: How Hidden Internal Snap Works\n(Clicks Inside at Z=47mm — Zero Visible Marks on Outside!)", color='white', fontsize=11, fontweight='bold', pad=10)

plt.tight_layout()
out_p = "/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/hidden_rear_snap_clip_mechanism.png"
plt.savefig(out_p, dpi=160)
print("Saved:", out_p)
