import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

# 1. Check Z-Stackup of 1_Outer_Frame, 2_Dial_Face, 3_Motor_Mount_Plate, 28BYJ-48 Shaft, and 5_Hands
v_f, n_f = load_stl("/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl")
v_d, n_d = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl")
v_m, n_m = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl")
v_b, n_b = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
v_h, n_h = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/5_Skinny_Elegant_Extended_Hands_PrusaMINI.stl")
v_p, n_p = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/6_Snap_Lock_Pins_No_Screws_Needed.stl")

print("=== SYSTEM 5: Z-STACKUP & 28BYJ-48 SHAFT REACH AUDIT ===")
# In 1_Outer_Frame:
# Front face is Z = 0.0 mm
# Inner bezel lip seat where 2_Dial_Face rests:
# Let's check triangles with normal +Z near the perimeter of 1_Outer_Frame
up_f = v_f[n_f[:, 2] > 0.9]
for z_val in np.unique(np.round(up_f[:, :, 2].mean(axis=1), 2)):
    sub = up_f[np.abs(up_f[:, :, 2].mean(axis=1) - z_val) < 0.05]
    pts = sub.reshape(-1, 3)
    print(f"  Frame +Z ledge at Z = {z_val:6.2f} mm: X in [{pts[:,0].min():7.2f}, {pts[:,0].max():7.2f}], Y in [{pts[:,1].min():7.2f}, {pts[:,1].max():7.2f}] (tris={len(sub)})")

down_f = v_f[n_f[:, 2] < -0.9]
for z_val in np.unique(np.round(down_f[:, :, 2].mean(axis=1), 2)):
    sub = down_f[np.abs(down_f[:, :, 2].mean(axis=1) - z_val) < 0.05]
    pts = sub.reshape(-1, 3)
    print(f"  Frame -Z face  at Z = {z_val:6.2f} mm: X in [{pts[:,0].min():7.2f}, {pts[:,0].max():7.2f}], Y in [{pts[:,1].min():7.2f}, {pts[:,1].max():7.2f}] (tris={len(sub)})")

print("\n=== 2_DIAL_FACE Z LEVELS ===")
pts_d = v_d.reshape(-1, 3)
print("  Dial X:", pts_d[:,0].min(), "to", pts_d[:,0].max(), "Y:", pts_d[:,1].min(), "to", pts_d[:,1].max())
print("  Dial base thickness Z = 2.40 mm, raised text Z = 3.16 mm (+0.76 mm text height)")

print("\n=== 5_HANDS DIMENSIONS ===")
pts_h = v_h.reshape(-1, 3)
print("  Hands bbox:", pts_h.min(axis=0), "to", pts_h.max(axis=0))
print("  Unique Z in hands:", np.unique(np.round(pts_h[:, 2], 2)))

print("\n=== 6_SNAP_LOCK_PINS DIMENSIONS ===")
pts_p = v_p.reshape(-1, 3)
print("  Pins bbox:", pts_p.min(axis=0), "to", pts_p.max(axis=0))
print("  Unique Z in pins:", np.unique(np.round(pts_p[:, 2], 2)))
