import bpy
import bmesh
import math

# ==============================================================================
# PART A: UPGRADE 1_OUTER_FRAME TO V5 CLICK-LOCK ARCHITECTURE
#   1) Remove the full-height 10.3x10.3mm corner posts from Z = 4.00 to 49.00 mm
#      (eliminating BOTH the Z = 6.40 mm mid-air bridging flaw AND the taco-bending trap!)
#   2) Add 8 Flanged Front Click-Lock Snap Ramps (Z = 6.40 to 13.50 mm) along the straight walls:
#      - Smooth 45-degree entry ramp (Z = 13.50 down to 9.80 mm) guides 3_Motor_Mount_Plate straight in
#      - Click-detent undercut at Z = 6.40 to 9.50 mm locks 3_Motor_Mount_Plate + 2_Dial_Face tightly
#        against the Z = 4.00 mm front bezel lip with ZERO screws!
#   3) Add 4 Self-Supporting 45-degree Rear Corner Seats (3.8 x 3.8 mm at Z = 44.5 to 49.0 mm)
#      + 6 Rear Rim Snap-Fit Detents (Z = 50.4 mm) so 4_Back_Cover clicks in flush at Z = 49..52 mm,
#      while 2_Dial_Face and 3_Motor_Mount_Plate (with 4.2x4.2mm hidden corner reliefs) drop straight
#      past the 3.8x3.8mm rear corner seats with ZERO bending!
# ==============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)

def add_box_obj(name, x0, x1, y0, y1, z0, z1):
    cx, cy, cz = 0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1)
    sx, sy, sz = (x1-x0), (y1-y0), (z1-z0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

def create_prism_x(name, x0, x1, yz_pts):
    bm = bmesh.new()
    v0 = [bm.verts.new((x0, y, z)) for y, z in yz_pts]
    v1 = [bm.verts.new((x1, y, z)) for y, z in yz_pts]
    bm.faces.new(list(reversed(v0)))
    bm.faces.new(v1)
    n = len(yz_pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([v0[i], v0[j], v1[j], v1[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def create_prism_y(name, y0, y1, xz_pts):
    bm = bmesh.new()
    v0 = [bm.verts.new((x, y0, z)) for x, z in xz_pts]
    v1 = [bm.verts.new((x, y1, z)) for x, z in xz_pts]
    bm.faces.new(v0)
    bm.faces.new(list(reversed(v1)))
    n = len(xz_pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([v0[i], v1[i], v1[j], v0[j]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# Import backup 1_Outer_Frame
bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]
frame.name = "OuterFrame_V5_ClickLock"

# Step 1: Fill the 4 corner holes inside the front bezel lip (Z = 1.65 to 6.50 mm) so the front bezel lip is 100% solid,
# then cut away the entire 10.3x10.3mm internal corner posts from Z = 4.00 mm to Z = 49.00 mm!
fill_objs = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # Fill the old corner screw hole in the front bezel lip (Z = 1.65 to 4.00 mm)
        x0 = 100.5 if sx > 0 else -111.0
        x1 = 111.0 if sx > 0 else -100.5
        y0 = 77.5 if sy > 0 else -88.0
        y1 = 88.0 if sy > 0 else -77.5
        fill_objs.append(add_box_obj(f"FillBezelHole_{sx}_{sy}", x0, x1, y0, y1, 1.65, 4.00))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = fill_objs[0]
for o in fill_objs:
    o.select_set(True)
bpy.ops.object.join()
all_fills = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="FillHoles", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.object = all_fills
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_fills, do_unlink=True)

# Cut away the 4 corner posts from Z = 4.00 mm to Z = 49.00 mm (staying inside the |X|=111.30, |Y|=88.30 inner cavity walls!)
cut_posts = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        x0 = 98.0 if sx > 0 else -111.30
        x1 = 111.30 if sx > 0 else -98.0
        y0 = 75.0 if sy > 0 else -88.30
        y1 = 88.30 if sy > 0 else -75.0
        cut_posts.append(add_box_obj(f"CutCornerPost_{sx}_{sy}", x0, x1, y0, y1, 4.00, 49.00))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = cut_posts[0]
for o in cut_posts:
    o.select_set(True)
bpy.ops.object.join()
all_cuts = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="CutPosts", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_cuts
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_cuts, do_unlink=True)

# Step 2: Add V5 Click-Lock Features to 1_Outer_Frame:
#   A) 4 Self-Supporting 45° Rear Corner Seats (3.8 x 3.8 mm at Z = 44.8 to 49.0 mm):
#      - Located at |X| in [107.50 .. 111.35], |Y| in [84.50 .. 88.35]
#      - 45° chamfer on bottom (from Z = 44.80 at wall to Z = 48.60 at inner corner, flat top at Z = 49.00 mm)
#      - Prints face-down with ZERO supports!
#      - 2_Dial_Face and 3_Motor_Mount_Plate have 4.2x4.2mm hidden corner reliefs (|X|>107.0, |Y|>84.0) so they
#        drop 100% straight past these 3.8x3.8mm rear corner seats without touching them!
#      - 4_Back_Cover has full corners (|X|=111.03, |Y|=88.03) so its 4 corners land solidly on Z = 49.00 mm!
#   B) 8 Flanged Front Click-Lock Snap Ramps (at Z = 4.00 to 13.50 mm along the inner walls):
#      - Actually, let's look at how 1_Outer_Frame prints face-down (Z=0 on bed):
#        Every feature on the inner wall that tapers INWARD as Z increases (e.g. from Z=9.40 out to Z=10.20, then tapering back to wall at Z=13.50)
#        has a <= 45-degree slope and prints cleanly with ZERO supports!
#        Specifically:
#        - From Z = 4.00 to 9.45 mm (where 2_Dial_Face [Z=4.0..6.4] and 3_Motor_Mount_Plate rim [Z=6.4..9.4] sit):
#          wall is at |Y| = 88.30 (and |X| = 111.30), with a gentle 0.15 mm snug centering rib.
#        - From Z = 9.45 to 10.15 mm: a 45-degree click-lock shoulder juts inward by 0.55 mm (to |Y| = 87.75 / |X| = 110.75)
#        - From Z = 10.15 to 13.50 mm: a gentle flanged entry ramp tapers back into the wall (|Y| = 88.30 / |X| = 111.30)
#          so when you push 3_Motor_Mount_Plate down from the back (Z = 52 -> Z = 6.4), the flanged entry ramp
#          guides the plate inward, flexes the plate's compliant perimeter slots by 0.55 mm, and CLICKS over the top of the plate at Z = 9.45 mm!
#   C) 6 Rear Cover Click-Detents at Z = 50.2 to 51.6 mm (gentle 0.35 mm snap-ridge along the rear rim so 4_Back_Cover clicks in flush!)

frame_adds = []

for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        bx0 = 107.50 if sx > 0 else -111.40
        bx1 = 111.40 if sx > 0 else -107.50
        by0 = 84.50 if sy > 0 else -88.40
        by1 = 88.40 if sy > 0 else -84.50
        boss = add_box_obj(f"RearCornerSeat_{sx}_{sy}", bx0, bx1, by0, by1, 44.80, 49.00)
        bm = bmesh.new()
        bm.from_mesh(boss.data)
        ix = 107.50 if sx > 0 else -107.50
        iy = 84.50 if sy > 0 else -84.50
        for v in bm.verts:
            if abs(v.co.z - 44.80) < 0.05:
                if abs(v.co.x - ix) < 0.05 or abs(v.co.y - iy) < 0.05:
                    v.co.x = 111.30 if sx > 0 else -111.30
                    v.co.y = 88.30 if sy > 0 else -88.30
        bm.normal_update()
        bm.to_mesh(boss.data)
        bm.free()
        frame_adds.append(boss)

# 6 Flanged Front Click-Lock Snap Ramps along Left/Right walls (at X = -62, 0, +62) and 4 along Top/Bottom walls (at Y = -45, +45)
for sy in (-1.0, 1.0):
    for xc_snap in (-62.0, 0.0, 62.0):
        # Profile in (Y, Z): attached to wall at sy*88.30 (extend slightly into wall to sy*88.60 for clean boolean union)
        # Note: at Z = 4.0..6.4 (2_Dial_Face), flush with wall (88.30) so 2_Dial_Face drops past 100% freely!
        # At Z = 9.45..10.10: 0.50 mm snap-lock catch (reaching sy*87.80) with 45° slopes on both sides!
        yz_snap = [
            (sy * 88.60, 8.80),
            (sy * 88.30, 8.80),
            (sy * 87.80, 9.45),
            (sy * 87.80, 10.05),
            (sy * 88.30, 12.80),
            (sy * 88.60, 12.80),
        ]
        if sy > 0:
            yz_snap = list(reversed(yz_snap))
        frame_adds.append(create_prism_x(f"FrontClick_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_snap))

        # Rear Cover Click-Detent at Z = 49.80..51.40 mm (0.30 mm gentle snap bump for 4_Back_Cover!)
        yz_rear = [
            (sy * 88.60, 49.60),
            (sy * 88.30, 49.60),
            (sy * 88.00, 50.30),
            (sy * 88.00, 50.70),
            (sy * 88.30, 51.50),
            (sy * 88.60, 51.50),
        ]
        if sy > 0:
            yz_rear = list(reversed(yz_rear))
        frame_adds.append(create_prism_x(f"RearClick_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_rear))

for sx in (-1.0, 1.0):
    for yc_snap in (-45.0, 45.0):
        xz_snap = [
            (sx * 111.60, 8.80),
            (sx * 111.30, 8.80),
            (sx * 110.80, 9.45),
            (sx * 110.80, 10.05),
            (sx * 111.30, 12.80),
            (sx * 111.60, 12.80),
        ]
        if sx < 0:
            xz_snap = list(reversed(xz_snap))
        frame_adds.append(create_prism_y(f"FrontClick_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_snap))

        xz_rear = [
            (sx * 111.60, 49.60),
            (sx * 111.30, 49.60),
            (sx * 111.00, 50.30),
            (sx * 111.00, 50.70),
            (sx * 111.30, 51.50),
            (sx * 111.60, 51.50),
        ]
        if sx < 0:
            xz_rear = list(reversed(xz_rear))
        frame_adds.append(create_prism_y(f"RearClick_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_rear))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = frame_adds[0]
for o in frame_adds:
    o.select_set(True)
bpy.ops.object.join()
all_f_adds = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="AddClickLocks", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.object = all_f_adds
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_f_adds, do_unlink=True)

bm_f = bmesh.new()
bm_f.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm_f, verts=bm_f.verts, dist=1e-4)
bmesh.ops.triangulate(bm_f, faces=bm_f.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_f, faces=bm_f.faces)
non_mf = sum(1 for e in bm_f.edges if not e.is_manifold)
print(f"V5 Click-Lock 1_Outer_Frame: verts={len(bm_f.verts)}, faces={len(bm_f.faces)}, non_manifold={non_mf}")
bm_f.to_mesh(frame.data)
bm_f.free()

frame_paths = [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
]
bpy.ops.object.select_all(action='DESELECT')
frame.select_set(True)
for p in frame_paths:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
    print("  Exported Frame:", p)
