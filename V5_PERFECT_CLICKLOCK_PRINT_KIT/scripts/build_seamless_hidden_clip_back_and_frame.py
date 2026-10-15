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

# ==============================================================================
# 1. UPDATE 1_OUTER_FRAME SO THE REAR RIM (Z=49..52mm) IS 100% SMOOTH & SEAMLESS,
#    WITH HIDDEN INTERNAL SNAP-CATCHES BELOW Z=49.0mm!
# ==============================================================================
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]

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

        # 4 Self-Supporting 45° Rear Corner Seats at Z = 44.20 to 49.00 mm
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

# Add Front Click-Lock Ramps (Z=8.6..13.0mm) AND Hidden Internal Rear Cover Snap-Catches (Z=45.5..48.2mm, completely BELOW Z=49.0mm!)
# Because the rear snap-catches are at Z=45.5..48.2mm (inside the box, behind the 3mm back cover!),
# the outer rear rim at Z=49.0..52.0mm is 100% UNTOUCHED AND RAZOR-CLEAN!
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

        # Hidden internal snap ridge at Z = 45.80..48.20 mm (juts inward to 87.85 mm, which is STILL outside the 87.55 mm
        # bypass notches on 2_Dial_Face so 2_Dial_Face drops right past it too!)
        yz_rear_internal = [
            (sy * 89.20, 45.60),
            (sy * 87.85, 46.80),
            (sy * 87.85, 47.40),
            (sy * 89.20, 48.60),
        ]
        if sy > 0:
            yz_rear_internal = list(reversed(yz_rear_internal))
        u2_objs.append(create_prism_x(f"HiddenRearCatch_Y_{sy}_{xc_snap}", xc_snap - 7.5, xc_snap + 7.5, yz_rear_internal))

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

        xz_rear_internal = [
            (sx * 112.20, 45.60),
            (sx * 110.85, 46.80),
            (sx * 110.85, 47.40),
            (sx * 112.20, 48.60),
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
print(f"Seamless-Rim V5 1_Outer_Frame: verts={len(bm_f.verts)}, faces={len(bm_f.faces)}, non_manifold={non_mf}")
bm_f.to_mesh(frame.data)
bm_f.free()

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

# ==============================================================================
# 2. BUILD SEAMLESS HIDDEN-CLIP 4_BACK_COVER (BOTH LOUVERED & FLAT TRANSLUCENT!)
#    - ZERO through-slots on the outer face!
#    - ZERO corner screw holes on the outer face!
#    - 10 Hidden Internal Cantilever Snap-Clips rising from the INSIDE surface (Z = 2.5 to 5.8 mm)
#      that reach inside the frame to Z_frame = 46.2..49.0 mm and click over the internal catches!
# ==============================================================================
def add_internal_snap_clips_to_back_cover():
    clips = []
    # Along Y = ±88.03 edges (at X = -62, 0, +62):
    # Base of clip sits on inside of back cover (Z = 2.4 to 3.0 mm) at |Y| in [84.8..87.4 mm],
    # rising up to Z = 5.6 mm (which projects 2.6 mm into the clock interior, Z_frame = 49.0 - 2.6 = 46.4 mm!)
    # with an outward snap barb at Z = 4.6..5.2 mm reaching |Y| = 88.22 mm to click under the 87.85 mm frame catch!
    for sy in (-1.0, 1.0):
        for xc in (-62.0, 0.0, 62.0):
            yz_clip = [
                (sy * 85.20, 2.20),
                (sy * 87.55, 2.20),
                (sy * 87.55, 4.30),
                (sy * 88.22, 4.80),
                (sy * 88.22, 5.15),
                (sy * 87.20, 5.80),
                (sy * 85.80, 5.80),
                (sy * 85.80, 3.00),
                (sy * 85.20, 3.00),
            ]
            if sy < 0:
                yz_clip = list(reversed(yz_clip))
            clips.append(create_prism_x(f"BackHiddenClipY_{sy}_{xc}", xc - 7.0, xc + 7.0, yz_clip))

    for sx in (-1.0, 1.0):
        for yc in (-45.0, 45.0):
            xz_clip = [
                (sx * 108.20, 2.20),
                (sx * 110.55, 2.20),
                (sx * 110.55, 4.30),
                (sx * 111.22, 4.80),
                (sx * 111.22, 5.15),
                (sx * 110.20, 5.80),
                (sx * 108.80, 5.80),
                (sx * 108.80, 3.00),
                (sx * 108.20, 3.00),
            ]
            if sx > 0:
                xz_clip = list(reversed(xz_clip))
            clips.append(create_prism_y(f"BackHiddenClipX_{sx}_{yc}", yc - 7.0, yc + 7.0, xz_clip))
    return clips

# Build Version A: Seamless Louvered/Exhibition Back Cover (4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl)
# Start from original backup or clean import, fill the 4 corner screw holes so the back is 100% screwless,
# and add the 10 hidden internal snap-clips on the inside face!
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/SURF_CLOCK_GDRIVE_HANDOFF_PACKAGE/01_FINAL_3D_PRINT_STLS_AND_MANUALS/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl")
bcover = bpy.context.selected_objects[0]

b_adds = add_internal_snap_clips_to_back_cover()
# Fill the 4 old corner screw holes at (±104.5, ±81.5) so the outer rear surface has ZERO screw holes!
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        b_adds.append(add_cyl_obj(f"FillBackCornerHole_{sx}_{sy}", sx * 104.50, sy * 81.50, 2.50, 0.00, 3.00, segs=36))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = b_adds[0]
for o in b_adds:
    o.select_set(True)
bpy.ops.object.join()
all_ba = bpy.context.view_layer.objects.active
mod = bcover.modifiers.new(name="AddHiddenClips", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.use_self = True
mod.object = all_ba
bpy.context.view_layer.objects.active = bcover
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_ba, do_unlink=True)

bm_b = bmesh.new()
bm_b.from_mesh(bcover.data)
bmesh.ops.remove_doubles(bm_b, verts=bm_b.verts, dist=1e-4)
bmesh.ops.triangulate(bm_b, faces=bm_b.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_b, faces=bm_b.faces)
non_mb = sum(1 for e in bm_b.edges if not e.is_manifold)
print(f"Seamless Hidden-Clip 4_Back_Cover: verts={len(bm_b.verts)}, faces={len(bm_b.faces)}, non_manifold={non_mb}")
bm_b.to_mesh(bcover.data)
bm_b.free()

bpy.ops.object.select_all(action='DESELECT')
bcover.select_set(True)
for bp in [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=bp, export_selected_objects=True, ascii_format=False)

# Build Version B: Pure Flat Frosted Translucent Exhibition Back Cover (zero louvers, uniform 2.0mm window + 3.0mm rim + hidden clips!)
bpy.ops.wm.read_factory_settings(use_empty=True)
flat_back = add_box_obj("FlatBackBase", -111.03, 111.03, -88.03, 88.03, 0.0, 3.0)
fb_adds = add_internal_snap_clips_to_back_cover()
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = fb_adds[0]
for o in fb_adds:
    o.select_set(True)
bpy.ops.object.join()
all_fba = bpy.context.view_layer.objects.active
mod = flat_back.modifiers.new(name="AddClipsFlat", type='BOOLEAN')
mod.operation = 'UNION'
mod.solver = 'EXACT'
mod.use_self = True
mod.object = all_fba
bpy.context.view_layer.objects.active = flat_back
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_fba, do_unlink=True)

# Cut bottom USB-C notch (X in [102.53..112.0], Y in [-6.5..+6.5]) and recessed 2.0mm uniform optical window on inside (Z = 2.0..3.1, |X|<98, |Y|<75)
fb_cuts = [
    add_box_obj("CutUSBNotch", 102.53, 112.0, -6.50, 6.50, -1.0, 5.0),
    add_box_obj("OpticalRecess", -98.0, 98.0, -76.0, 76.0, 2.00, 3.50),
]
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = fb_cuts[0]
for o in fb_cuts:
    o.select_set(True)
bpy.ops.object.join()
all_fbc = bpy.context.view_layer.objects.active
mod = flat_back.modifiers.new(name="CutFlatBack", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_fbc
bpy.context.view_layer.objects.active = flat_back
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_fbc, do_unlink=True)

bm_fb = bmesh.new()
bm_fb.from_mesh(flat_back.data)
bmesh.ops.remove_doubles(bm_fb, verts=bm_fb.verts, dist=1e-4)
bmesh.ops.triangulate(bm_fb, faces=bm_fb.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_fb, faces=bm_fb.faces)
non_mfb = sum(1 for e in bm_fb.edges if not e.is_manifold)
print(f"Pure Flat Frosted Exhibition 4_Back_Cover: verts={len(bm_fb.verts)}, faces={len(bm_fb.faces)}, non_manifold={non_mfb}")
bm_fb.to_mesh(flat_back.data)
bm_fb.free()

bpy.ops.object.select_all(action='DESELECT')
flat_back.select_set(True)
for fbp in [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_OPTIONAL_Back_Cover_PURE_FLAT_TRANSLUCENT_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/4_OPTIONAL_Back_Cover_PURE_FLAT_TRANSLUCENT_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=fbp, export_selected_objects=True, ascii_format=False)
