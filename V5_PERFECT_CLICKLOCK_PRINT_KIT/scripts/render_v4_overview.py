import struct
import numpy as np
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

fig, axes = plt.subplots(1, 2, figsize=(18, 9), dpi=160)
fig.patch.set_facecolor('#141619')

# Panel 1: Updated 3_Motor_Mount_Plate (rotated into Portrait Clock orientation so TOP=12 o'clock is UP)
ax = axes[0]
ax.set_facecolor('#1C1F24')
verts, norms = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl")
# Map MK4 bed (X_bed, Y_bed) -> Portrait Clock (X_clock = Y_bed, Y_clock = -X_bed) so Top is UP!
tris_top = verts[norms[:, 2] > 0.15]
n_top = norms[norms[:, 2] > 0.15]
light = np.array([-0.3, 0.4, 0.86])
light /= np.linalg.norm(light)
shade = np.clip(np.dot(n_top, light), 0.25, 1.0)

polys = np.zeros((len(tris_top), 3, 2))
polys[:, :, 0] = tris_top[:, :, 1]   # Horizontal = Y_bed
polys[:, :, 1] = -tris_top[:, :, 0]  # Vertical = -X_bed (so -X_bed is UP)

colors = np.zeros((len(tris_top), 4))
# Highlight the raised features (Z > 2.25) in TE Orange and base plate in warm grey-orange
z_mean = tris_top[:, :, 2].mean(axis=1)
for i in range(len(tris_top)):
    if z_mean[i] > 2.25:
        colors[i] = [1.0 * shade[i], 0.38 * shade[i], 0.08 * shade[i], 1.0]
    else:
        colors[i] = [0.85 * shade[i], 0.48 * shade[i], 0.22 * shade[i], 1.0]

pc = PolyCollection(polys, facecolors=colors, edgecolors='none')
ax.add_collection(pc)

# Annotate the -2.0mm bottom clips moved UP by 2mm
for y_clock in [22.0, -68.0]:
    # Bottom clip sits at X_bed = xc + 14.60 -> Y_clock = -xc - 14.60 = y_clock - 14.60
    y_bot = y_clock - 14.60
    ax.plot([28.5, 62.5], [y_bot, y_bot], color='#00FF9D', lw=2.2, ls='--')
    ax.annotate("Bottom clip moved UP +2.0mm\n(31.2mm snug ULN2003 fit)",
                xy=(45.5, y_bot), xytext=(45.5, y_bot - 18.0),
                ha='center', va='top', color='#00FF9D', fontsize=8.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', fc='#0E1114', ec='#00FF9D', lw=1.2),
                arrowprops=dict(arrowstyle='->', color='#00FF9D', lw=1.5))

# Annotate the 4 corner notches
for sx in [-1, 1]:
    for sy in [-1, 1]:
        rect = plt.Rectangle((sx*77.60 if sx>0 else -88.5, sy*100.60 if sy>0 else -111.5),
                             10.9, 10.9, fill=False, ec='#52B4FF', lw=1.8, ls=':')
        ax.add_patch(rect)
ax.annotate("4x Corner Notches (10.4 x 10.4mm)\nBypasses outer frame corner posts",
            xy=(-82.5, 105.5), xytext=(-38.0, 104.0),
            ha='left', va='center', color='#52B4FF', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', fc='#0E1114', ec='#52B4FF', lw=1.2),
            arrowprops=dict(arrowstyle='->', color='#52B4FF', lw=1.5))

ax.annotate("10x Tapered Push-Fit Friction Ribs\n(Snug press-in along straight walls)",
            xy=(-88.1, 45.0), xytext=(-48.0, 56.0),
            ha='left', va='center', color='#FFD166', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', fc='#0E1114', ec='#FFD166', lw=1.2),
            arrowprops=dict(arrowstyle='->', color='#FFD166', lw=1.5))

ax.set_xlim(-102, 102)
ax.set_ylim(-124, 124)
ax.set_aspect('equal')
ax.set_title("1. Updated 3_Motor_Mount_Plate (Fits Your Existing Outer Frame)\n• ULN2003 Bottom Clips Moved UP 2mm  • 4 Corner Notches  • Snug Push-Fit Ribs",
             color='white', fontsize=11.5, fontweight='bold', pad=12)
ax.tick_params(colors='#88929E')

# Panel 2: Cross-section / Corner Architecture Comparison (Full-Height Pillar vs V4 Split-Zone Frame)
ax2 = axes[1]
ax2.set_facecolor('#1C1F24')

# Draw side-by-side Z-depth architectural cross-sections (Z = 0 Front Bezel to Z = 49mm Rear Cover)
def draw_section(ax, x_off, title, split_zone=False):
    # Outer Wall (Z=0 to 49)
    ax.add_patch(plt.Rectangle((x_off, 0), 6.2, 49.0, fc='#D8DCE0', ec='#FFFFFF', lw=1.2))
    # Front Bezel Lip (Z=0 to 4.0)
    ax.add_patch(plt.Rectangle((x_off+6.2, 0), 14.0, 4.0, fc='#D8DCE0', ec='#FFFFFF', lw=1.2))
    # Dial Faceplate (Z=4.0 to 6.4)
    ax.add_patch(plt.Rectangle((x_off+6.4, 4.0), 34.0, 2.4, fc='#F4F5F7', ec='#52B4FF', lw=1.5))
    ax.text(x_off+23.0, 5.2, "2_Dial_Face (2.4mm)", ha='center', va='center', color='#141619', fontsize=7.5, fontweight='bold')
    # Motor Mount Plate (Z=6.5 to 8.5 base + 14.6 motor ring)
    ax.add_patch(plt.Rectangle((x_off+6.3, 6.5), 34.0, 2.0, fc='#FF5B14', ec='#FFD166', lw=1.5))
    ax.text(x_off+23.0, 7.5, "3_Motor_Plate (Push-Fit)", ha='center', va='center', color='white', fontsize=7.5, fontweight='bold')

    if not split_zone:
        # Old full-height corner post (Z=6.65 to 49.0)
        ax.add_patch(plt.Rectangle((x_off+6.2, 8.6), 10.3, 40.4, fc='#7A3E3E', ec='#FF6B6B', lw=1.4, ls='--'))
        ax.text(x_off+11.35, 27.5, "OLD 40mm\nCorner Post\n(Blocks plate\nwithout notches)", ha='center', va='center', color='#FFD6D6', fontsize=7.5, fontweight='bold')
    else:
        # New V4 Split-Zone: Open Cavity from Z=10.2 to 37.0, plus 45-deg self-supporting rear boss
        ax.add_patch(plt.Rectangle((x_off+6.2, 8.6), 4.5, 1.6, fc='#00FF9D', ec='white', lw=1.0))
        ax.text(x_off+18.5, 9.5, "← Snap / Friction Retention Zone", ha='left', va='center', color='#00FF9D', fontsize=7.5, fontweight='bold')
        ax.text(x_off+21.0, 24.0, "100% OPEN INTERIOR CAVITY\n(Zero Corner Posts in Middle!\nClean look through Translucent Back)",
                ha='center', va='center', color='#A9E5FF', fontsize=8.0, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', fc='#112233', ec='#52B4FF', lw=1.0))
        # 45-degree chamfered rear corner tab (Z=37 to 49)
        poly_boss = np.array([
            [x_off+6.2, 37.0],
            [x_off+12.2, 43.0],
            [x_off+12.2, 46.0],
            [x_off+6.2, 46.0]
        ])
        ax2.add_patch(plt.Polygon(poly_boss, fc='#D8DCE0', ec='#00FF9D', lw=1.4))
        ax.text(x_off+13.2, 42.5, "45° Print-in-Place\nRear Tab (for Back Cover)", ha='left', va='center', color='#00FF9D', fontsize=7.5, fontweight='bold')

    # Rear Cover (Z=46.0 to 49.0)
    ax.add_patch(plt.Rectangle((x_off+6.4, 46.0), 34.0, 3.0, fc='#88C9FF', alpha=0.55, ec='#52B4FF', lw=1.5))
    ax.text(x_off+23.0, 47.5, "5_Translucent_Back (3.0mm)", ha='center', va='center', color='white', fontsize=7.5, fontweight='bold')
    ax.text(x_off+20.0, -3.2, title, ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')

draw_section(ax2, 6.0, "A. Existing Outer Frame\n(Works Today w/ Notched Plate)", split_zone=False)
draw_section(ax2, 54.0, "B. New V4 Split-Zone Frame\n(For Your Next Cool Grey Print)", split_zone=True)

ax2.set_xlim(0, 100)
ax2.set_ylim(54, -8)  # Z=0 at top, Z=49 at bottom
ax2.set_ylabel("Depth from Front Face Z (mm)", color='white', fontsize=10)
ax2.set_xticks([])
ax2.tick_params(colors='#88929E')
ax2.set_title("2. Frame & Assembly Architecture: Why Split-Zone Beats Full Corner Posts\n(And Why Separate Dial + Orange Motor Plate Beats 1-Piece Fused Print)",
              color='white', fontsize=11.5, fontweight='bold', pad=12)

plt.tight_layout()
out_img = "/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/motor_plate_v4_and_frame_architecture.png"
plt.savefig(out_img, dpi=160)
print("Saved diagram:", out_img)
