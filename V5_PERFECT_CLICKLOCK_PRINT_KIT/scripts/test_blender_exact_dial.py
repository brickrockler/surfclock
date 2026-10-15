import bpy
import bmesh

for p in [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2a_Dial_Face_NORTHERN_BEACHES_Queensie_M600_at_Z2.6mm_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2b_Dial_Face_SYDNEY_ICONS_Bondi_Bronte_M600_at_Z2.6mm_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2c_Dial_Face_EASTERN_SUBURBS_Bondi_Coogee_M600_at_Z2.6mm_PrusaMK4.stl",
]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath=p)
    obj = bpy.context.selected_objects[0]

    # Run EXACT self-union Boolean to fuse all overlapping letter strokes and the base plate into ONE single 100% manifold solid!
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.0, 0.0, 1.0))
    dummy = bpy.context.active_object
    mod = obj.modifiers.new(name="SelfUnion", type='BOOLEAN')
    mod.operation = 'UNION'
    mod.solver = 'EXACT'
    mod.use_self = True
    mod.object = dummy
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(dummy, do_unlink=True)

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    non_mf = sum(1 for e in bm.edges if not e.is_manifold)
    print(p.split("/")[-1], "-> verts:", len(bm.verts), "faces:", len(bm.faces), "non_manifold:", non_mf)
    bm.to_mesh(obj.data)
    bm.free()

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
