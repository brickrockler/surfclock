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

def add_cyl_obj(name, cx, cy, r, z0, z1, segs=48):
    cz = 0.5*(z0+z1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=segs, radius=r, depth=(z1-z0), location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
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

bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]
frame.name = "OuterFrame_V5_ClickLock"

# Notice in 1_Outer_Frame_MATTE_WHITE:
# The front bezel lip is Z = 0.00 to 4.00 mm, and at Z = 4.00 to 6.40 mm there is ALREADY NO corner post
# (the corner post only starts at Z = 6.40 mm, except for the cylinder wall around the corner hole at (105.54, 82.54) from Z=1.65..6.40)!
# Wait: at Z = 1.65 to 4.00 mm, that cylinder hole at (105.54, 82.54, r=2.47mm) is inside the solid corner of the bezel lip (which has R=3.8mm corner rounding)!
# So if we fill ONLY the cylinder (105.5375, 82.5375, r=2.55mm) from Z = 1.00 to 4.00 mm, and cut everything inside the cavity from Z = 4.00 to 49.00 mm:
ops_union = []
ops_diff = []

for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        ops_union.append(add_cyl_obj(f"FillBezelCyl_{sx}_{sy}", sx * 105.5375, sy * 82.5375, 2.55, 1.00, 2.55, segs=48))
        cx0 = 98.0 if sx > 0 else -111.80
        cx1 = 111.80 if sx > 0 else -98.0
        cy0 = 75.0 if sy > 0 else -88.80
        cy1 = 88.80 if sy > 0 else -75.0
        ops_diff.append(add_box_obj(f"CutPost_{sx}_{sy}", cx0, cx1, cy0, cy1, 4.00, 49.00))

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

u2_objs = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        wx0 = 111.30 if sx > 0 else -113.50
        wx1 = 113.50 if sx > 0 else -111.30
        wy0 = 74.00 if sy > 0 else -90.50
        wy1 = 90.50 if sy > 0 else -74.00
        u2_objs.append(add_box_obj(f"WallX_{sx}_{sy}", wx0, wx1, wy0, wy1, 3.50, 49.00))

        yx0 = 97.00 if sx > 0 else -113.50
        yx1 = 113.50 if sx > 0 else -97.00
        yy0 = 88.30 if sy > 0 else -90.50
        yy1 = 90.50 if sy > 0 else -88.30
        u2_objs.append(add_box_obj(f"WallY_{sx}_{sy}", yx0, yx1, yy0, yy1, 3.50, 49.00))

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
print(f"Perfect V5 Click-Lock 1_Outer_Frame: verts={len(bm_f.verts)}, faces={len(bm_f.faces)}, non_manifold={non_mf}")
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
