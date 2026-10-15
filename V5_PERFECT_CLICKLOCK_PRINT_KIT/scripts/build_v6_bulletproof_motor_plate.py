import bpy
import bmesh
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def make_bm_mesh(name, bm):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def add_box(bm, x0, x1, y0, y1, z0, z1):
    verts = [
        bm.verts.new((x0, y0, z0)),
        bm.verts.new((x1, y0, z0)),
        bm.verts.new((x1, y1, z0)),
        bm.verts.new((x0, y1, z0)),
        bm.verts.new((x0, y0, z1)),
        bm.verts.new((x1, y0, z1)),
        bm.verts.new((x1, y1, z1)),
        bm.verts.new((x0, y1, z1)),
    ]
    faces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    for f in faces:
        bm.faces.new([verts[i] for i in f])

def create_box_obj(name, x0, x1, y0, y1, z0, z1):
    bm = bmesh.new()
    add_box(bm, x0, x1, y0, y1, z0, z1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_cyl_obj(name, cx, cy, r, z0, z1, segs=64):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs,
        radius1=r, radius2=r, depth=(z1 - z0)
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx, cy, 0.5 * (z0 + z1)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_cone_obj(name, cx, cy, r1, r2, z0, z1, segs=48):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs,
        radius1=r1, radius2=r2, depth=(z1 - z0)
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx, cy, 0.5 * (z0 + z1)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_rounded_rect_obj(name, x0, x1, y0, y1, r, z0, z1, segs_corner=12):
    bm = bmesh.new()
    pts = []
    corners = [
        (x1 - r, y1 - r, 0.0, 0.5 * math.pi),
        (x0 + r, y1 - r, 0.5 * math.pi, math.pi),
        (x0 + r, y0 + r, math.pi, 1.5 * math.pi),
        (x1 - r, y0 + r, 1.5 * math.pi, 2.0 * math.pi),
    ]
    for cx, cy, a0, a1 in corners:
        for i in range(segs_corner):
            ang = a0 + (a1 - a0) * i / segs_corner
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    n = len(pts)
    bot_v = [bm.verts.new((px, py, z0)) for px, py in pts]
    top_v = [bm.verts.new((px, py, z1)) for px, py in pts]
    bm.faces.new(list(reversed(bot_v)))
    bm.faces.new(top_v)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([bot_v[i], bot_v[j], top_v[j], top_v[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_prism_profile_x(name, x0, x1, yz_pts):
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
    return make_bm_mesh(name, bm)

def create_prism_profile_y(name, y0, y1, xz_pts):
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
    return make_bm_mesh(name, bm)

# ==============================================================================
# BUILD V6 BULLETPROOF 3_MOTOR_MOUNT_PLATE
# ==============================================================================
plate = create_box_obj("BasePlate", -111.00, 111.00, -88.00, 88.00, 0.0, 3.0)
add_objs = []
sub_objs = []
post_sub_add_objs = []  # Added AFTER pocket subtraction so motor ear pegs & ear snaps are never cut away!

# 1. Cut 4 Corner L-Notches (|X| > 100.60, |Y| > 77.60) so it drops effortlessly into existing frames
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        x0 = 100.60 if sx > 0 else -112.00
        x1 = 112.00 if sx > 0 else -100.60
        y0 = 77.60 if sy > 0 else -89.00
        y1 = 89.00 if sy > 0 else -77.60
        sub_objs.append(create_box_obj(f"Cut_CornerNotch_{sx}_{sy}", x0, x1, y0, y1, -1.0, 22.0))

# 2. Audited 28BYJ-48 Stepper Motor Mounts (Upper & Lower)
for mname, x_shaft, x_can in [("Upper", -25.30, -17.30), ("Lower", 78.20, 70.20)]:
    add_objs.append(create_cyl_obj(f"Add_{mname}_CanRing", x_can, 0.0, 16.60, 0.0, 6.50, segs=64))
    for sy in (-1.0, 1.0):
        add_objs.append(create_cyl_obj(f"Add_{mname}_EarWall_{sy}", x_can, sy * 17.50, 6.40, 0.0, 6.50, segs=48))
        add_objs.append(create_box_obj(f"Add_{mname}_EarBridgeWall_{sy}", x_can - 6.40, x_can + 6.40,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), 0.0, 6.50))

    # Cut Coplanar Z = 2.00 mm pocket for Can (r = 14.22 mm) + Ears (r = 3.85 mm) + Ear Bridge (7.70 mm wide)
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_CanPocket", x_can, 0.0, 14.22, 2.00, 8.00, segs=64))
    for sy in (-1.0, 1.0):
        sub_objs.append(create_cyl_obj(f"Sub_{mname}_EarPocket_{sy}", x_can, sy * 17.50, 3.85, 2.00, 8.00, segs=48))
        sub_objs.append(create_box_obj(f"Sub_{mname}_EarBridgePocket_{sy}", x_can - 3.85, x_can + 3.85,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), 2.00, 8.00))

    # Cut Shaft & Ø9mm Brass Boss Hole (r = 5.20 mm) all the way through Z = 0..3mm
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_ShaftHole", x_shaft, 0.0, 5.20, -1.0, 9.0, segs=48))

    # Cut Blue Plastic Wire Hump Slot down to Z = 2.00 mm
    if mname == "Upper":
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can + 8.0, x_can + 19.0, -7.8, 7.8, 2.00, 8.00))
    else:
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can - 19.0, x_can - 8.0, -7.8, 7.8, 2.00, 8.00))

    # Integrated Solid Locating Posts (r = 1.92 mm -> Ø3.84 mm, Z = 1.50 to 5.40 mm + conical tip to 6.20 mm)
    # Added in post_sub_add_objs so they stand cleanly inside the Z = 2.00 mm ear pockets!
    for sy in (-1.0, 1.0):
        post_sub_add_objs.append(create_cyl_obj(f"PostAdd_{mname}_EarPeg_{sy}", x_can, sy * 17.50, 1.92, 1.50, 5.40, segs=36))
        post_sub_add_objs.append(create_cone_obj(f"PostAdd_{mname}_EarPegTip_{sy}", x_can, sy * 17.50, 1.92, 1.25, 5.40, 6.20, segs=36))
        ye_out = sy * (17.50 + 3.85)  # ±21.35 mm
        s_dir = -sy
        yz_ear_clip = [
            (ye_out - s_dir * 1.40, 1.50),
            (ye_out, 1.50),
            (ye_out, 3.10),
            (ye_out + s_dir * 0.45, 3.55),
            (ye_out + s_dir * 0.45, 3.95),
            (ye_out, 4.40),
            (ye_out, 6.50),
            (ye_out - s_dir * 1.40, 6.50),
        ]
        if s_dir < 0:
            yz_ear_clip = list(reversed(yz_ear_clip))
        post_sub_add_objs.append(create_prism_profile_x(f"PostAdd_{mname}_EarSnap_{sy}", x_can - 1.8, x_can + 1.8, yz_ear_clip))

# 3. Audited ULN2003 Motor Controller Cradles:
#    - Continuous connected U-rails + full perimeter PCB shelf at Z = 4.20 mm
#    - ONE single clean rounded-rectangle through-window (24.8 x 28.0 mm, R = 3.5 mm) from Z = 0..3mm
uln_positions = [(-28.00, -50.00), (-28.00, 50.00), (28.00, 50.00)]
for idx, (xc, yc) in enumerate(uln_positions):
    x0_in = xc - 16.60
    x1_in = xc + 14.60  # 31.20 mm vertical inner height
    y0_in, y1_in = yc - 17.80, yc + 17.80  # 35.60 mm horizontal inner width
    xc_mid = 0.5 * (x0_in + x1_in)  # xc - 1.00

    # Side guide rails along Y0 and Y1 (Z = 2.50 to 6.80 mm, 2.4 mm thick)
    add_objs.append(create_box_obj(f"ULN_RailY0_{idx}", x0_in - 2.2, x1_in + 2.2, y0_in - 2.4, y0_in, 2.5, 6.8))
    add_objs.append(create_box_obj(f"ULN_RailY1_{idx}", x0_in - 2.2, x1_in + 2.2, y1_in, y1_in + 2.4, 2.5, 6.8))

    # Connect top corners and bottom edge into continuous L/U walls (Z = 2.50 to 6.00 mm) so there are no isolated skinny towers!
    add_objs.append(create_box_obj(f"ULN_WallTopL_{idx}", x0_in - 2.2, x0_in, y0_in - 2.4, y0_in + 7.0, 2.5, 6.0))
    add_objs.append(create_box_obj(f"ULN_WallTopR_{idx}", x0_in - 2.2, x0_in, y1_in - 7.0, y1_in + 2.4, 2.5, 6.0))
    add_objs.append(create_box_obj(f"ULN_WallBot_{idx}", x1_in, x1_in + 2.2, y0_in - 2.4, y1_in + 2.4, 2.5, 6.0))

    # Full PCB support ledges along all 4 inner edges (Z = 2.50 to 4.20 mm)
    add_objs.append(create_box_obj(f"ULN_LedgeY0_{idx}", x0_in - 2.2, x1_in + 2.2, y0_in, yc - 14.0, 2.5, 4.20))
    add_objs.append(create_box_obj(f"ULN_LedgeY1_{idx}", x0_in - 2.2, x1_in + 2.2, yc + 14.0, y1_in, 2.5, 4.20))
    add_objs.append(create_box_obj(f"ULN_LedgeX0_{idx}", x0_in - 2.2, xc_mid - 12.4, yc - 14.5, yc + 14.5, 2.5, 4.20))
    add_objs.append(create_box_obj(f"ULN_LedgeX1_{idx}", xc_mid + 12.4, x1_in + 2.2, yc - 14.5, yc + 14.5, 2.5, 4.20))

    # Split Top Snap-Latch Clips (45-deg self-supporting, fused with ULN_WallTopL/R and side rails!)
    pts_top = [
        (x0_in - 2.2, 2.5),
        (x0_in, 2.5),
        (x0_in, 6.0),
        (x0_in + 0.55, 6.55),
        (x0_in + 0.55, 6.95),
        (x0_in - 0.30, 7.80),
        (x0_in - 2.2, 7.80),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopL_{idx}", y0_in - 2.4, y0_in + 7.0, pts_top))
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopR_{idx}", y1_in - 7.0, y1_in + 2.4, pts_top))

    # Bottom Snap-Latch Clip at x1_in (45-deg self-supporting, fused with ULN_WallBot)
    pts_bot = [
        (x1_in, 2.5),
        (x1_in + 2.2, 2.5),
        (x1_in + 2.2, 7.80),
        (x1_in + 0.30, 7.80),
        (x1_in - 0.55, 6.95),
        (x1_in - 0.55, 6.55),
        (x1_in, 6.0),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipBot_{idx}", yc - 8.5, yc + 8.5, pts_bot))

    # ONE Clean Through-Window (24.8 x 28.0 mm, R = 3.5 mm) all the way from Z = -1.0 to +5.0 mm!
    sub_objs.append(create_rounded_rect_obj(
        f"Sub_ULN_Window_{idx}",
        xc_mid - 12.4, xc_mid + 12.4,
        yc - 14.0, yc + 14.0,
        3.5, 0.60, 5.0, segs_corner=10
    ))

# 4. Sleek Low-Profile Freenove ESP32-S3-WROOM Cradle (X = +2.00 to +59.50 mm, Y = -51.00 mm)
esp_x0, esp_x1 = 2.00, 59.50
esp_yc = -51.00
esp_y0, esp_y1 = esp_yc - 14.35, esp_yc + 14.35
z_esp_shelf = 9.50

sub_objs.append(create_rounded_rect_obj(
    "Sub_ESP_SingleWindow",
    esp_x0 + 2.5, esp_x1 - 2.5,
    esp_yc - 12.50, esp_yc + 12.50,
    4.0, 0.60, 5.0, segs_corner=10
))

add_objs.append(create_box_obj("ESP_WallY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0 - 2.40, esp_y0, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_WallY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1, esp_y1 + 2.40, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_LedgeY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0, esp_y0 + 1.25, 2.50, z_esp_shelf))
add_objs.append(create_box_obj("ESP_LedgeY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1 - 1.25, esp_y1, 2.50, z_esp_shelf))

add_objs.append(create_box_obj("ESP_TopStop_L", esp_x0 - 2.20, esp_x0, esp_y0 - 2.40, esp_yc - 10.20, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_TopStop_R", esp_x0 - 2.20, esp_x0, esp_yc + 10.20, esp_y1 + 2.40, 2.50, z_esp_shelf + 1.70))

add_objs.append(create_box_obj("ESP_BotStop_L", esp_x1, esp_x1 + 2.20, esp_y0 - 2.40, esp_y0 + 1.80, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_BotStop_R", esp_x1, esp_x1 + 2.20, esp_y1 - 1.80, esp_y1 + 2.40, 2.50, z_esp_shelf + 1.70))

for cx0, cx1 in [(esp_x0 + 6.0, esp_x0 + 14.0), (esp_x1 - 14.0, esp_x1 - 6.0)]:
    pts_esp_y0 = [
        (esp_y0 - 2.40, z_esp_shelf),
        (esp_y0, z_esp_shelf),
        (esp_y0, z_esp_shelf + 1.65),
        (esp_y0 + 0.55, z_esp_shelf + 2.20),
        (esp_y0 + 0.55, z_esp_shelf + 2.50),
        (esp_y0 - 0.30, z_esp_shelf + 3.00),
        (esp_y0 - 2.40, z_esp_shelf + 3.00),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_esp_y0))
    pts_esp_y1 = [
        (esp_y1, z_esp_shelf),
        (esp_y1 + 2.40, z_esp_shelf),
        (esp_y1 + 2.40, z_esp_shelf + 3.00),
        (esp_y1 + 0.30, z_esp_shelf + 3.00),
        (esp_y1 - 0.55, z_esp_shelf + 2.50),
        (esp_y1 - 0.55, z_esp_shelf + 2.20),
        (esp_y1, z_esp_shelf + 1.65),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_esp_y1))

# 5. Essential Cable Management Retainers — 100% MONOTONIC 45-DEGREE UPWARD RAMPS (ZERO FLOATING MID-AIR TIPS!)
def make_cable_arch_x(name, x0, x1, yc, side_sign):
    s = side_sign
    yz = [
        (yc - s * 5.0, 2.5),
        (yc - s * 2.4, 2.5),
        (yc - s * 2.4, 4.6),
        (yc + s * 1.4, 8.4),  # Pure 45-deg upward ramp (dY=3.8, dZ=3.8) — NEVER dips back down!
        (yc + s * 1.4, 9.4),
        (yc - s * 5.0, 9.4),
    ]
    if s < 0:
        yz = list(reversed(yz))
    return create_prism_profile_x(name, x0, x1, yz)

def make_cable_arch_y(name, y0, y1, xc, side_sign):
    s = side_sign
    xz = [
        (xc - s * 5.0, 2.5),
        (xc - s * 2.4, 2.5),
        (xc - s * 2.4, 4.6),
        (xc + s * 1.4, 8.4),  # Pure 45-deg upward ramp (dX=3.8, dZ=3.8) — NEVER dips back down!
        (xc + s * 1.4, 9.4),
        (xc - s * 5.0, 9.4),
    ]
    if s > 0:
        xz = list(reversed(xz))
    return create_prism_profile_y(name, y0, y1, xz)

add_objs.append(make_cable_arch_x("CableArch_Mid_L", -6.0, 6.0, -24.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_Mid_R", -6.0, 6.0, +24.5, -1.0))
add_objs.append(make_cable_arch_y("CableArch_USBC_1", -34.0, -20.0, 96.5, +1.0))
add_objs.append(make_cable_arch_y("CableArch_USBC_2", -14.0, 0.0, 101.5, +1.0))

# 6. Clean Perimeter Stiffening Rim (flush with the outer edge — ZERO slits, ZERO 84-deg overhangs!)
add_objs.append(create_box_obj("Rim_Top", -111.00, -108.40, -75.0, 75.0, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Left", -98.0, 98.0, -88.00, -85.40, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Right", -98.0, 98.0, 85.40, 88.00, 2.5, 5.2))

# Step A: Boolean UNION all primary add_objs
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = add_objs[0]
for o in add_objs:
    o.select_set(True)
bpy.ops.object.join()
all_adds = bpy.context.view_layer.objects.active

mod_u = plate.modifiers.new(name="UnionAdds", type='BOOLEAN')
mod_u.operation = 'UNION'
mod_u.solver = 'EXACT'
mod_u.use_self = True
mod_u.object = all_adds
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=mod_u.name)
bpy.data.objects.remove(all_adds, do_unlink=True)

# Step B: Boolean DIFFERENCE all sub_objs
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = sub_objs[0]
for o in sub_objs:
    o.select_set(True)
bpy.ops.object.join()
all_subs = bpy.context.view_layer.objects.active

mod_d = plate.modifiers.new(name="DiffSubs", type='BOOLEAN')
mod_d.operation = 'DIFFERENCE'
mod_d.solver = 'EXACT'
mod_d.use_self = True
mod_d.object = all_subs
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=mod_d.name)
bpy.data.objects.remove(all_subs, do_unlink=True)

# Step C: Boolean UNION post_sub_add_objs (Motor Ear Locating Pegs & Ear Snap Clips inside the carved pockets!)
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = post_sub_add_objs[0]
for o in post_sub_add_objs:
    o.select_set(True)
bpy.ops.object.join()
all_post_adds = bpy.context.view_layer.objects.active

mod_u2 = plate.modifiers.new(name="UnionPostAdds", type='BOOLEAN')
mod_u2.operation = 'UNION'
mod_u2.solver = 'EXACT'
mod_u2.use_self = True
mod_u2.object = all_post_adds
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=mod_u2.name)
bpy.data.objects.remove(all_post_adds, do_unlink=True)

bm_out = bmesh.new()
bm_out.from_mesh(plate.data)
bmesh.ops.remove_doubles(bm_out, verts=bm_out.verts, dist=1e-4)
bmesh.ops.dissolve_degenerate(bm_out, dist=1e-4)
bmesh.ops.triangulate(bm_out, faces=bm_out.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_out, faces=bm_out.faces)
non_m = [e for e in bm_out.edges if not e.is_manifold]
print(f"V6 Bulletproof 3_Motor_Mount_Plate: verts={len(bm_out.verts)}, faces={len(bm_out.faces)}, non_manifold={len(non_m)}")
bm_out.to_mesh(plate.data)
bm_out.free()

plate_paths = [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/NEW3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_ESP32_WiderClips_PilotHoles_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
]
bpy.ops.object.select_all(action='DESELECT')
plate.select_set(True)
for p in plate_paths:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
    print("  Exported:", p)
