import bpy
import bmesh

def add_box_obj(name, x0, x1, y0, y1, z0, z1):
    cx, cy, cz = 0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1)
    sx, sy, sz = (x1-x0), (y1-y0), (z1-z0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

# 2. ADD COMPLIANT PERIMETER CLICK-FLEX SLOTS & FINGER REMOVAL LOOPS TO 3_MOTOR_MOUNT_PLATE
#    (So the 10 perimeter click-tabs flex inward by 0.5mm effortlessly and CLICK into 1_Outer_Frame!)
# ==============================================================================
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl")
mplate = bpy.context.selected_objects[0]

flex_cuts = []
# Cut compliant flex slots (1.6mm wide x 18mm long) 2.2mm inset from the outer edge right behind each of the 10 click tabs!
# This turns each of the 10 perimeter tabs into a true compliant leaf-spring beam that deflects smoothly and CLICKS!
for sy in (-1.0, 1.0):
    for xc in (-62.0, 0.0, 62.0):
        y_slot_c = sy * 84.40
        flex_cuts.append(add_box_obj(f"FlexSlotY_{sy}_{xc}", xc - 8.5, xc + 8.5, y_slot_c - 0.9, y_slot_c + 0.9, 0.60, 10.0))

for sx in (-1.0, 1.0):
    for yc in (-45.0, 45.0):
        x_slot_c = sx * 107.40
        flex_cuts.append(add_box_obj(f"FlexSlotX_{sx}_{yc}", x_slot_c - 0.9, x_slot_c + 0.9, yc - 8.5, yc + 8.5, 0.60, 10.0))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = flex_cuts[0]
for o in flex_cuts:
    o.select_set(True)
bpy.ops.object.join()
all_fc = bpy.context.view_layer.objects.active
mod = mplate.modifiers.new(name="CutFlexSlots", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_fc
bpy.context.view_layer.objects.active = mplate
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_fc, do_unlink=True)

bm_m = bmesh.new()
bm_m.from_mesh(mplate.data)
bmesh.ops.remove_doubles(bm_m, verts=bm_m.verts, dist=1e-4)
bmesh.ops.triangulate(bm_m, faces=bm_m.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_m, faces=bm_m.faces)
non_mm = sum(1 for e in bm_m.edges if not e.is_manifold)
print(f"V5 Click-Flex 3_Motor_Mount_Plate: verts={len(bm_m.verts)}, faces={len(bm_m.faces)}, non_manifold={non_mm}")
bm_m.to_mesh(mplate.data)
bm_m.free()

bpy.ops.object.select_all(action='DESELECT')
mplate.select_set(True)
for mp in [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_ESP32_WiderClips_PilotHoles_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=mp, export_selected_objects=True, ascii_format=False)

# ==============================================================================
