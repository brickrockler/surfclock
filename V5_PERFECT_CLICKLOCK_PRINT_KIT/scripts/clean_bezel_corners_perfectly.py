import bpy
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]

# Remove the tiny r=2.55mm cylinder protrusion at (105.5375, 82.5375) between Z = 2.55 and 4.00 mm
# while keeping Z = 0.00..2.55 mm solid!
cuts = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=2.65, depth=2.0, location=(sx*105.5375, sy*82.5375, 3.55))
        cuts.append(bpy.context.active_object)

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = cuts[0]
for o in cuts:
    o.select_set(True)
bpy.ops.object.join()
all_c = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="CleanCorner", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_c
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_c, do_unlink=True)

bm = bmesh.new()
bm.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
bmesh.ops.triangulate(bm, faces=bm.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
non_mf = sum(1 for e in bm.edges if not e.is_manifold)
print(f"Ultra-Clean V5 Click-Lock 1_Outer_Frame: verts={len(bm.verts)}, faces={len(bm.faces)}, non_manifold={non_mf}")
bm.to_mesh(frame.data)
bm.free()

bpy.ops.object.select_all(action='DESELECT')
frame.select_set(True)
for p in [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
