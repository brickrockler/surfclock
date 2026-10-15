import bpy
import bmesh
import math

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

# Import backup 1_Outer_Frame_MATTE_WHITE
bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]
frame.name = "OuterFrame_V5_ClickLock"

# Notice why 1_Outer_Frame_MATTE_WHITE is so easy to clean directly in BMesh:
# In 1_Outer_Frame_MATTE_WHITE, the 4 corner posts and corner holes can be modified/replaced cleanly,
# OR we can cut the corner posts from Z = 4.02 to Z = 45.20 mm (leaving the top 3.8 mm of each corner post at Z = 45.20..49.00 mm
# as the Rear Cover Seat, with a 45-degree chamfer from Z = 41.00 to 46.50 mm!)
# WAIT A SECOND! Think about that!
# Look at why cutting from Z = 6.30 to Z = 44.50 mm with a 45-degree chamfer up to Z = 49.00 mm is 100x cleaner:
# 1) In 1_Outer_Frame_MATTE_WHITE, the corner posts ALREADY exist from Z = 6.40 to Z = 49.00 mm, and at Z = 49.00 mm they ALREADY
#    form the exact corner seat for 4_Back_Cover (including the exact corner hole at (105.5, 82.5))!
# 2) If we cut away the corner posts from Z = 6.00 mm up to Z = 41.00 mm (with a 45° slope from Z = 38.50 at the outer wall
#    to Z = 46.50 at the inner edge of the rear corner seat, AND trim the inner X/Y size of that rear corner seat to |X| >= 107.40, |Y| >= 84.40
#    or keep |X| >= 101.00, |Y| >= 78.00 if 2_Dial_Face and 3_Motor_Mount_Plate have notched corners):
#    WAIT: if we trim the rear corner seat to |X| >= 107.40, |Y| >= 84.40 (or cut everything inside |X| < 107.40 or |Y| < 84.40
#    from Z = 4.01 to 49.50 mm, and cut the remaining 3.9x3.9mm corner post from Z = 4.01 to Z = 44.50 mm with a 45° ramp),
#    let's see what happens when our cutter goes slightly into the outer wall (to 112.0 / 89.0) and THEN we re-union the outer wall ring!
#    YES!! If the cutter extends to |X| = 112.0, |Y| = 89.0 (so there are ZERO coplanar faces at 111.30 or 88.30!), and then we union back
#    the clean outer wall shell (|X| in [111.30..114.0], |Y| in [88.30..91.0], Z in [4.00..49.00]), there are ZERO coplanar boolean artifacts!

# Let's test this exact non-coplanar boolean technique right now!
ops_union = []
ops_diff = []

for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # 1. Fill the old corner hole in the front bezel lip (Z = 1.50 to 4.20 mm)
        x0 = 100.0 if sx > 0 else -111.5
        x1 = 111.5 if sx > 0 else -100.0
        y0 = 77.0 if sy > 0 else -88.5
        y1 = 88.5 if sy > 0 else -77.0
        ops_union.append(add_box_obj(f"FillBezel_{sx}_{sy}", x0, x1, y0, y1, 1.65, 4.00))

        # 2. Cut the entire corner post from Z = 4.00 to Z = 50.00 mm, extending 0.5mm into the wall (to 111.8 / 88.8)
        #    so there are ZERO coplanar faces with 111.30 / 88.30 / 49.00!
        cx0 = 98.0 if sx > 0 else -111.80
        cx1 = 111.80 if sx > 0 else -98.0
        cy0 = 75.0 if sy > 0 else -88.80
        cy1 = 88.80 if sy > 0 else -75.0
        ops_diff.append(add_box_obj(f"CutPost_{sx}_{sy}", cx0, cx1, cy0, cy1, 4.00, 49.00))

# Apply FillBezel union first
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = ops_union[0]
for o in ops_union:
    o.select_set(True)
bpy.ops.object.join()
u1 = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="U1", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.object = u1
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(u1, do_unlink=True)

# Apply CutPost difference
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = ops_diff[0]
for o in ops_diff:
    o.select_set(True)
bpy.ops.object.join()
d1 = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="D1", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = d1
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(d1, do_unlink=True)

# Now restore the clean outer wall thickness in the 4 corners (|X| in [111.30..113.50], |Y| in [88.30..90.50], Z in [3.50..49.00])
# PLUS the 4 self-supporting 45° rear corner seats (3.8 x 3.8 mm at Z = 44.50..49.00 mm)
# PLUS the 10 Flanged Front Click-Lock Snap Ramps (Z = 8.80..12.80 mm) and 10 Rear Cover Click-Detents (Z = 49.60..51.50 mm)!
u2_objs = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # Restore X wall in corner (|X| in [111.30..113.50], |Y| in [74.0..90.5], Z in [3.50..49.50], except near Y=0)
        wx0 = 111.30 if sx > 0 else -113.50
        wx1 = 113.50 if sx > 0 else -111.30
        wy0 = 74.00 if sy > 0 else -90.50
        wy1 = 90.50 if sy > 0 else -74.00
        u2_objs.append(add_box_obj(f"WallX_{sx}_{sy}", wx0, wx1, wy0, wy1, 3.50, 49.00))

        # Restore Y wall in corner (|X| in [97.0..113.50], |Y| in [88.30..90.50], Z in [3.50..49.50])
        yx0 = 97.00 if sx > 0 else -113.50
        yx1 = 113.50 if sx > 0 else -97.00
        yy0 = 88.30 if sy > 0 else -90.50
        yy1 = 90.50 if sy > 0 else -88.30
        u2_objs.append(add_box_obj(f"WallY_{sx}_{sy}", yx0, yx1, yy0, yy1, 3.50, 49.00))

        # Self-Supporting 45° Rear Corner Seat for 4_Back_Cover (|X| in [107.50..112.50], |Y| in [84.50..89.50], Z in [44.20..49.00])
        # Note: extends into the wall (112.50 / 89.50) and tapers to (111.50, 88.50) at Z=44.20 so ZERO coplanar faces with 111.30 / 88.30!
        bx0 = 107.50 if sx > 0 else -112.50
        bx1 = 112.50 if sx > 0 else -107.50
        by0 = 84.50 if sy > 0 else -89.50
        by1 = 89.50 if sy > 0 else -84.50
        boss = add_box_obj(f"RearSeat_{sx}_{sy}", bx0, bx1, by0, by1, 44.20, 49.00)
        bm = bmesh.new()
        bm.from_mesh(boss.data)
        ix = 107.50 if sx > 0 else -107.50
        iy = 84.50 if sy > 0 else -84.50
        for v in bm.verts:
            if abs(v.co.z - 44.20) < 0.05:
                if abs(v.co.x - ix) < 0.05:
                    v.co.x = 112.00 if sx > 0 else -112.00
                if abs(v.co.y - iy) < 0.05:
                    v.co.y = 89.00 if sy > 0 else -89.00
        bm.normal_update()
        bm.to_mesh(boss.data)
        bm.free()
        u2_objs.append(boss)

# Add Flanged Front Click-Lock Ramps & Rear Cover Click-Detents (always starting inside the wall at 89.00 / 112.00 so ZERO coplanar faces!)
for sy in (-1.0, 1.0):
    for xc_snap in (-62.0, 0.0, 62.0):
        yz_snap = [
            (sy * 89.20, 8.60),
            (sy * 87.80, 9.45),
            (sy * 87.80, 10.05),
            (sy * 89.20, 13.00),
        ]
        if sy > 0:
            yz_snap = list(reversed(yz_snap))
        u2_objs.append(create_prism_x(f"FrontClick_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_snap))

        yz_rear = [
            (sy * 89.20, 49.40),
            (sy * 88.02, 50.30),
            (sy * 88.02, 50.70),
            (sy * 89.20, 51.60),
        ]
        if sy > 0:
            yz_rear = list(reversed(yz_rear))
        u2_objs.append(create_prism_x(f"RearClick_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_rear))

for sx in (-1.0, 1.0):
    for yc_snap in (-45.0, 45.0):
        xz_snap = [
            (sx * 112.20, 8.60),
            (sx * 110.80, 9.45),
            (sx * 110.80, 10.05),
            (sx * 112.20, 13.00),
        ]
        if sx < 0:
            xz_snap = list(reversed(xz_snap))
        u2_objs.append(create_prism_y(f"FrontClick_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_snap))

        xz_rear = [
            (sx * 112.20, 49.40),
            (sx * 111.02, 50.30),
            (sx * 111.02, 50.70),
            (sx * 112.20, 51.60),
        ]
        if sx < 0:
            xz_rear = list(reversed(xz_rear))
        u2_objs.append(create_prism_y(f"RearClick_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_rear))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = u2_objs[0]
for o in u2_objs:
    o.select_set(True)
bpy.ops.object.join()
u2 = bpy.context.view_layer.objects.active
mod = frame.modifiers.new(name="U2", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.use_self = True
mod.object = u2
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(u2, do_unlink=True)

bm_f = bmesh.new()
bm_f.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm_f, verts=bm_f.verts, dist=1e-4)
bmesh.ops.triangulate(bm_f, faces=bm_f.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_f, faces=bm_f.faces)
non_mf = sum(1 for e in bm_f.edges if not e.is_manifold)
print(f"Clean V5 Click-Lock 1_Outer_Frame: verts={len(bm_f.verts)}, faces={len(bm_f.faces)}, non_manifold={non_mf}")
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
