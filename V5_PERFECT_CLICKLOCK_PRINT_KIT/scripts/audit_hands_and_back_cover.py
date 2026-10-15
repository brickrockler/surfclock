import struct, numpy as np

def load_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        dt = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        data = np.frombuffer(f.read(n * 50), dtype=dt)
    return data['v'], data['n']

# Check all hands STLs in FINAL_PRINT_FILES
import glob
for p in sorted(glob.glob("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/5*.stl")):
    v, n = load_stl(p)
    pts = v.reshape(-1, 3)
    rel = p.split("/")[-1]
    print(f"{rel:62s} | Z in [{pts[:,2].min():5.2f}, {pts[:,2].max():5.2f}] | X in [{pts[:,0].min():6.2f}, {pts[:,0].max():6.2f}] | Y in [{pts[:,1].min():6.2f}, {pts[:,1].max():6.2f}]")

# Check 4_Back_Cover fit against 1_Outer_Frame rear recess (Z = 49.00 to 52.00 mm)
v_b, n_b = load_stl("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
pts_b = v_b.reshape(-1, 3)
print("\n4_Back_Cover span:", pts_b.min(axis=0), "to", pts_b.max(axis=0))
# Check where corner holes are in 4_Back_Cover
corner_tris = v_b[(np.abs(n_b[:, 2]) < 0.1) & (np.abs(v_b[:, :, 0].mean(axis=1)) > 95.0) & (np.abs(v_b[:, :, 1].mean(axis=1)) > 72.0)]
c_pts = corner_tris.reshape(-1, 3)
q1_c = c_pts[(c_pts[:, 0] > 0) & (c_pts[:, 1] > 0)]
if len(q1_c):
    print("4_Back_Cover Q1 corner hole X range:", q1_c[:,0].min(), "to", q1_c[:,0].max(), "center=", 0.5*(q1_c[:,0].min()+q1_c[:,0].max()))
    print("4_Back_Cover Q1 corner hole Y range:", q1_c[:,1].min(), "to", q1_c[:,1].max(), "center=", 0.5*(q1_c[:,1].min()+q1_c[:,1].max()))
    print("4_Back_Cover Q1 corner hole diameter:", q1_c[:,0].max() - q1_c[:,0].min())

# Compare with 1_Outer_Frame corner hole center at Z = 47.90..49.00 mm!
v_f, n_f = load_stl("/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl")
f_corner = v_f[(np.abs(n_f[:, 2]) < 0.1) & (v_f[:, :, 0].mean(axis=1) > 100.0) & (v_f[:, :, 1].mean(axis=1) > 77.0) & (v_f[:, :, 2].mean(axis=1) > 45.0)]
fc_pts = f_corner.reshape(-1, 3)
# filter to the cylindrical pilot hole inside (102..107, 79..84)
hole_pts = fc_pts[(fc_pts[:,0] > 102.0) & (fc_pts[:,0] < 107.0) & (fc_pts[:,1] > 79.0) & (fc_pts[:,1] < 84.0)]
if len(hole_pts):
    print("1_Outer_Frame Q1 corner hole X range:", hole_pts[:,0].min(), "to", hole_pts[:,0].max(), "center=", 0.5*(hole_pts[:,0].min()+hole_pts[:,0].max()))
    print("1_Outer_Frame Q1 corner hole Y range:", hole_pts[:,1].min(), "to", hole_pts[:,1].max(), "center=", 0.5*(hole_pts[:,1].min()+hole_pts[:,1].max()))
    print("1_Outer_Frame Q1 corner hole diameter:", hole_pts[:,0].max() - hole_pts[:,0].min())
