import bpy
import bmesh
import glob

def add_box_obj(name, x0, x1, y0, y1, z0, z1):
    cx, cy, cz = 0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1)
    sx, sy, sz = (x1-x0), (y1-y0), (z1-z0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

def create_rounded_slot_obj(name, x0, x1, y0, y1, z0, z1):
    return add_box_obj(name, x0, x1, y0, y1, z0, z1)

# ==============================================================================
# 1. UPGRADE ALL 2_DIAL_FACE STLs WITH HIDDEN DROP-IN RELIEFS
#    (100% hidden behind the |X|<=107.0, |Y|<=84.0 front bezel window opening,
#     allowing 2_Dial_Face to drop straight down to Z=4.00mm under gravity alone!)
# ==============================================================================
dial_files = [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
]

# Group identical dial files so we only process each unique dial once
unique_dials = [
    (
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl",
        ]
    ),
    (
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
        ]
    ),
    (
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
        ]
    ),
]

for src_path, dst_paths in unique_dials:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath=src_path)
    dial = bpy.context.selected_objects[0]
    cuts = []
    # 4 Corner reliefs (|X| > 107.15, |Y| > 84.15 -> clears the 107.50 / 84.50 rear corner seats by 0.35mm per side!)
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            x0 = 107.15 if sx > 0 else -112.0
            x1 = 112.0 if sx > 0 else -107.15
            y0 = 84.15 if sy > 0 else -89.0
            y1 = 89.0 if sy > 0 else -84.15
            cuts.append(add_box_obj(f"DialCorner_{sx}_{sy}", x0, x1, y0, y1, -1.0, 5.0))
    # 10 Perimeter Click-Ramp Bypass Notches (|Y| > 87.55 at X=-62,0,62 and |X| > 110.55 at Y=-45,45)
    # Completely hidden behind the |X|=107.0, |Y|=84.0 front bezel lip, lets Dial drop past the Z=9.45mm snaps freely!
    for sy in (-1.0, 1.0):
        for xc in (-62.0, 0.0, 62.0):
            y0 = 87.55 if sy > 0 else -89.0
            y1 = 89.0 if sy > 0 else -87.55
            cuts.append(add_box_obj(f"DialBypassY_{sy}_{xc}", xc - 8.2, xc + 8.2, y0, y1, -1.0, 5.0))
    for sx in (-1.0, 1.0):
        for yc in (-45.0, 45.0):
            x0 = 110.55 if sx > 0 else -112.0
            x1 = 112.0 if sx > 0 else -110.55
            cuts.append(add_box_obj(f"DialBypassX_{sx}_{yc}", x0, x1, yc - 8.2, yc + 8.2, -1.0, 5.0))

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = cuts[0]
    for o in cuts:
        o.select_set(True)
    bpy.ops.object.join()
    all_c = bpy.context.view_layer.objects.active
    mod = dial.modifiers.new(name="CutDialReliefs", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = all_c
    bpy.context.view_layer.objects.active = dial
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(all_c, do_unlink=True)

    bpy.ops.object.select_all(action='DESELECT')
    dial.select_set(True)
    for dp in dst_paths:
        bpy.ops.wm.stl_export(filepath=dp, export_selected_objects=True, ascii_format=False)
    print("Upgraded Dial:", src_path.split("/")[-1])

# ==============================================================================
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
        flex_cuts.append(add_box_obj(f"FlexSlotY_{sy}_{xc}", xc - 8.5, xc + 8.5, y_slot_c - 0.9, y_slot_c + 0.9, -1.0, 10.0))

for sx in (-1.0, 1.0):
    for yc in (-45.0, 45.0):
        x_slot_c = sx * 107.40
        flex_cuts.append(add_box_obj(f"FlexSlotX_{sx}_{yc}", x_slot_c - 0.9, x_slot_c + 0.9, yc - 8.5, yc + 8.5, -1.0, 10.0))

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
# 3. UPGRADE 4_BACK_COVER WITH COMPLIANT PERIMETER CLICK-FLEX SLOTS
#    (So 4_Back_Cover clicks into the 10 rear snap-detents on 1_Outer_Frame with zero screws!)
# ==============================================================================
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
bcover = bpy.context.selected_objects[0]

b_cuts = []
for sy in (-1.0, 1.0):
    for xc in (-62.0, 0.0, 62.0):
        y_slot_c = sy * 85.20
        b_cuts.append(add_box_obj(f"BackFlexY_{sy}_{xc}", xc - 8.5, xc + 8.5, y_slot_c - 0.8, y_slot_c + 0.8, -1.0, 5.0))

for sx in (-1.0, 1.0):
    for yc in (-45.0, 45.0):
        x_slot_c = sx * 108.20
        b_cuts.append(add_box_obj(f"BackFlexX_{sx}_{yc}", x_slot_c - 0.8, x_slot_c + 0.8, yc - 8.5, yc + 8.5, -1.0, 5.0))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = b_cuts[0]
for o in b_cuts:
    o.select_set(True)
bpy.ops.object.join()
all_bc = bpy.context.view_layer.objects.active
mod = bcover.modifiers.new(name="CutBackFlex", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_bc
bpy.context.view_layer.objects.active = bcover
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_bc, do_unlink=True)

bm_b = bmesh.new()
bm_b.from_mesh(bcover.data)
bmesh.ops.remove_doubles(bm_b, verts=bm_b.verts, dist=1e-4)
bmesh.ops.triangulate(bm_b, faces=bm_b.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_b, faces=bm_b.faces)
non_mb = sum(1 for e in bm_b.edges if not e.is_manifold)
print(f"V5 Click-Flex 4_Back_Cover: verts={len(bm_b.verts)}, faces={len(bm_b.faces)}, non_manifold={non_mb}")
bm_b.to_mesh(bcover.data)
bm_b.free()

bpy.ops.object.select_all(action='DESELECT')
bcover.select_set(True)
for bp in [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=bp, export_selected_objects=True, ascii_format=False)
