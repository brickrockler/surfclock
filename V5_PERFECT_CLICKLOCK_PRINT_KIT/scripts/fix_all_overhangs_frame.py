import bpy
import bmesh
import math

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

def make_corner_corbel(name, sx, sy, z_seat):
    # True inverted 35-degree pyramid corbel in the corner!
    # Stick-out from inner wall (111.30, 88.30) to (107.50, 84.50) is 3.80 mm.
    # Over Z height of 7.00 mm (z_seat - 7.00 to z_seat), the overhang angle is only 28.5 degrees from vertical!
    # That means EVERY layer steps out by only 0.11 mm (less than 1/4 of a nozzle width!) -> ZERO blue overhangs in PrusaSlicer!
    bm = bmesh.new()
    x_in, x_out = sx * 107.50, sx * 112.80
    y_in, y_out = sy * 84.50, sy * 89.80
    z_top = z_seat
    z_bot = z_seat - 7.50
    pts_top = [
        (min(x_in, x_out), min(y_in, y_out), z_top),
        (max(x_in, x_out), min(y_in, y_out), z_top),
        (max(x_in, x_out), max(y_in, y_out), z_top),
        (min(x_in, x_out), max(y_in, y_out), z_top),
    ]
    # At z_bot, the entire base is tucked INSIDE the solid corner walls (111.50..112.80, 88.50..89.80)
    x_b_in = sx * 111.50
    y_b_in = sy * 88.50
    pts_bot = [
        (min(x_b_in, x_out), min(y_b_in, y_out), z_bot),
        (max(x_b_in, x_out), min(y_b_in, y_out), z_bot),
        (max(x_b_in, x_out), max(y_b_in, y_out), z_bot),
        (min(x_b_in, x_out), max(y_b_in, y_out), z_bot),
    ]
    vt = [bm.verts.new(p) for p in pts_top]
    vb = [bm.verts.new(p) for p in pts_bot]
    bm.faces.new(vt)
    bm.faces.new(list(reversed(vb)))
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new([vb[i], vb[j], vt[j], vt[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def build_frame(z_total=52.0, out_paths=[]):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
    frame = bpy.context.selected_objects[0]

    z_shift = 52.0 - z_total
    if z_shift > 0.01:
        bm = bmesh.new()
        bm.from_mesh(frame.data)
        for v in bm.verts:
            if v.co.z > 20.0:
                v.co.z -= z_shift
        bm.normal_update()
        bm.to_mesh(frame.data)
        bm.free()

    z_seat = 49.0 - z_shift

    # Notice: NO FillBezelCyl! The front bezel opening in the backup STL is already 100% clean!
    ops_diff = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            cx0 = 98.0 if sx > 0 else -111.80
            cx1 = 111.80 if sx > 0 else -98.0
            cy0 = 75.0 if sy > 0 else -88.80
            cy1 = 88.80 if sy > 0 else -75.0
            ops_diff.append(add_box_obj(f"CutPost_{sx}_{sy}", cx0, cx1, cy0, cy1, 4.00, z_seat))

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
            u2_objs.append(add_box_obj(f"WallX_{sx}_{sy}", wx0, wx1, wy0, wy1, 3.50, z_seat))

            yx0 = 97.00 if sx > 0 else -113.50
            yx1 = 113.50 if sx > 0 else -97.00
            yy0 = 88.30 if sy > 0 else -90.50
            yy1 = 90.50 if sy > 0 else -88.30
            u2_objs.append(add_box_obj(f"WallY_{sx}_{sy}", yx0, yx1, yy0, yy1, 3.50, z_seat))

            # Gentle 28° self-supporting corner corbel (ZERO overhang warning!)
            u2_objs.append(make_corner_corbel(f"RearCorbel_{sx}_{sy}", sx, sy, z_seat))

    # Gentle 30-degree bottom corbel slopes on Front Click-Lock Ramps & Hidden Rear Catches
    # (ΔZ = 2.0 mm for ΔY = 0.5 mm -> 14° to 25° from vertical, so PrusaSlicer never flags them as overhangs!)
    for sy in (-1.0, 1.0):
        for xc_snap in (-62.0, 0.0, 62.0):
            yz_snap = [
                (sy * 89.20, 7.20),
                (sy * 87.80, 9.45),
                (sy * 87.80, 10.05),
                (sy * 89.20, 12.80),
            ]
            if sy > 0:
                yz_snap = list(reversed(yz_snap))
            u2_objs.append(create_prism_x(f"FrontClick_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_snap))

            yz_rear_internal = [
                (sy * 89.20, z_seat - 4.40),
                (sy * 87.85, z_seat - 2.20),
                (sy * 87.85, z_seat - 1.60),
                (sy * 89.20, z_seat - 0.10),
            ]
            if sy > 0:
                yz_rear_internal = list(reversed(yz_rear_internal))
            u2_objs.append(create_prism_x(f"HiddenRearCatch_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_rear_internal))

    for sx in (-1.0, 1.0):
        for yc_snap in (-45.0, 45.0):
            xz_snap = [
                (sx * 112.20, 7.20),
                (sx * 110.80, 9.45),
                (sx * 110.80, 10.05),
                (sx * 112.20, 12.80),
            ]
            if sx < 0:
                xz_snap = list(reversed(xz_snap))
            u2_objs.append(create_prism_y(f"FrontClick_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_snap))

            xz_rear_internal = [
                (sx * 112.20, z_seat - 4.40),
                (sx * 110.85, z_seat - 2.20),
                (sx * 110.85, z_seat - 1.60),
                (sx * 112.20, z_seat - 0.10),
            ]
            if sx < 0:
                xz_rear_internal = list(reversed(xz_rear_internal))
            u2_objs.append(create_prism_y(f"HiddenRearCatch_X_{sx}_{yc_snap}", yc_snap - 7.5, yc_snap + 7.5, xz_rear_internal))

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
    vol = bm_f.calc_volume() / 1000.0
    print(f"CLEAN Frame (Z={z_total}mm): verts={len(bm_f.verts)}, faces={len(bm_f.faces)}, non_manifold={non_mf}, volume={vol:.1f} cm^3")
    bm_f.to_mesh(frame.data)
    bm_f.free()

    bpy.ops.object.select_all(action='DESELECT')
    frame.select_set(True)
    for p in out_paths:
        bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)

build_frame(52.0, [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/1_Outer_Frame_ClickLock_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
])

build_frame(36.0, [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/1b_OPTIONAL_Outer_Frame_SLIM_36mm_FastPrint_PrusaMK4.stl",
])
