import bpy
import bmesh
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
orig_frame = "/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl"
bpy.ops.wm.stl_import(filepath=orig_frame)
frame = bpy.context.selected_objects[0]

# Wait: we can edit the bmesh of `frame` DIRECTLY or via clean boolean!
# Wait: `frame` only has 1,222 vertices! Let's inspect the vertices of the corner pillar in `frame`!
bm = bmesh.new()
bm.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)

# Let's see which vertices belong to the corner pillars!
# In the frame, the inner wall is at |X| = 111.30, |Y| = 88.30 (with R=0.60 fillet at |X|>=110.70, |Y|>=87.70).
# For Z in [6.30 .. 49.05], ANY vertex with |X| < 110.65 and |Y| < 87.65 (and |X| > 95, |Y| > 72) is EXCLUSIVELY part of the 4 corner pillars!
pillar_verts = [
    v for v in bm.verts
    if 6.30 <= v.co.z <= 49.05
    and abs(v.co.x) > 95.0 and abs(v.co.y) > 72.0
    and not (abs(v.co.x) >= 110.65 and abs(v.co.y) >= 87.65)
    and abs(v.co.x) < 111.25 and abs(v.co.y) < 88.25
]
print("Pillar interior vertices count:", len(pillar_verts))
for v in pillar_verts[:20]:
    if v.co.x > 0 and v.co.y > 0:
        print(f"  ({v.co.x:.2f}, {v.co.y:.2f}, {v.co.z:.2f})")
