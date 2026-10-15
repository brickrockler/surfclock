import struct
import numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

# 1. Inspect 1_Outer_Frame
v_frame, n_frame = load_stl("/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl")
pts_f = v_frame.reshape(-1, 3)
print("=== 1_OUTER_FRAME ===")
print("Bounding box:", pts_f.min(axis=0), "to", pts_f.max(axis=0))
# Check where the USB-C cutout or bottom wall openings are
bot_wall = pts_f[(pts_f[:, 0] > 108.0)]
print("Unique Z levels in frame:", np.unique(np.round(pts_f[:, 2], 2)))
# Check if there is ANY USB-C hole in 1_Outer_Frame!
# In X > 110, check Y and Z distribution of faces with normal in Y or Z
for axis, name in [(0, 'X'), (1, 'Y'), (2, 'Z')]:
    pass

# Check if 1_Outer_Frame has a USB hole at X = +111.3..+115.0!
x_max_tris = v_frame[(v_frame[:, :, 0].mean(axis=1) > 105.0)]
print("Triangles near X > 105 count:", len(x_max_tris))
# Let's check normal directions near X > 105 and |Y| < 50
mid_bot = v_frame[(v_frame[:, :, 0].mean(axis=1) > 105.0) & (np.abs(v_frame[:, :, 1].mean(axis=1)) < 60.0)]
print("Triangles near bottom wall center (X>105, |Y|<60):", len(mid_bot))
for t in mid_bot:
    print("  tri X:", np.round(t[:,0],2), "Y:", np.round(t[:,1],2), "Z:", np.round(t[:,2],2))

# 2. Inspect 4_Back_Cover
v_back, n_back = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
pts_b = v_back.reshape(-1, 3)
print("\n=== 4_BACK_COVER ===")
print("Bounding box:", pts_b.min(axis=0), "to", pts_b.max(axis=0))
print("Unique Z levels in back cover:", np.unique(np.round(pts_b[:, 2], 2)))
# Find cutouts in 4_Back_Cover (triangles with |n_z| < 0.5 and inside outer perimeter)
inner_b = v_back[(np.abs(n_back[:, 2]) < 0.5) & (np.abs(v_back[:, :, 0].mean(axis=1)) < 110.5) & (np.abs(v_back[:, :, 1].mean(axis=1)) < 87.5)]
print("Inner cutout triangles in 4_Back_Cover:", len(inner_b))
# Group by approximate center
centers_b = inner_b.mean(axis=1)
print("Back cover inner feature X range:", centers_b[:,0].min(), "to", centers_b[:,0].max())
print("Back cover inner feature Y range:", centers_b[:,1].min(), "to", centers_b[:,1].max())
# Find USB hole in 4_Back_Cover or edge notches
edge_b = v_back[(np.abs(n_back[:, 2]) < 0.5) & (v_back[:, :, 0].mean(axis=1) > 95.0) & (np.abs(v_back[:, :, 1].mean(axis=1)) < 70.0)]
print("Back cover bottom edge features (X>95, |Y|<70):", len(edge_b))
for t in edge_b[:20]:
    print("  back tri X:", np.round(t[:,0],2), "Y:", np.round(t[:,1],2), "Z:", np.round(t[:,2],2))

# 3. Inspect 2_Dial_Face
v_dial, n_dial = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl")
pts_d = v_dial.reshape(-1, 3)
print("\n=== 2_DIAL_FACE ===")
print("Bounding box:", pts_d.min(axis=0), "to", pts_d.max(axis=0))
print("Unique Z levels in dial:", np.unique(np.round(pts_d[:, 2], 2)))
