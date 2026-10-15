import bpy
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]
bm = bmesh.new()
bm.from_mesh(frame.data)
for e in bm.edges:
    if not e.is_manifold:
        print("Non-manifold edge:", [tuple(round(c, 2) for c in v.co) for v in e.verts])
