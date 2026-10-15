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

def create_rounded_rect_obj(name, x0, x1, y0, y1, r, z0, z1, segs_corner=16):
    bm = bmesh.new()
    r = min(r, 0.46 * (x1 - x0), 0.46 * (y1 - y0))
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
# V9 OPEN SKELETON TRUSS MOTOR MOUNT PLATE — ZERO GRID INFILL, ZERO BRIDGING
# ==============================================================================
z_web = 1.80  # 9 layers at 0.20mm -> 100% solid layers (4 bot + 5 top), ZERO Grid infill, ZERO Internal Bridge!

plate = create_rounded_rect_obj("BaseWeb", -111.00, 111.00, -88.00, 88.00, 12.0, 0.0, z_web, segs_corner=24)
add_objs = []
sub_objs = []
post_sub_add_objs = []

# Outer Click-Lock Perimeter Rim (Z = 0.00 to 3.00 mm, width = 2.80 mm = 100% perimeters!)
outer_rim_add = create_rounded_rect_obj("OuterClickRim_Add", -111.00, 111.00, -88.00, 88.00, 12.0, 1.40, 3.00, segs_corner=24)
outer_rim_sub = create_rounded_rect_obj("OuterClickRim_Sub", -108.20, 108.20, -85.20, 85.20, 9.2, 1.20, 3.50, segs_corner=24)
mod_rim = outer_rim_add.modifiers.new(name="RimHollow", type='BOOLEAN')
mod_rim.operation = 'DIFFERENCE'
mod_rim.solver = 'EXACT'
mod_rim.object = outer_rim_sub
bpy.context.view_layer.objects.active = outer_rim_add
bpy.ops.object.modifier_apply(modifier=mod_rim.name)
bpy.data.objects.remove(outer_rim_sub, do_unlink=True)
add_objs.append(outer_rim_add)

# Structural I-Beam Stiffening Ribs (2.50 mm wide = 6 perimeters = 100% perimeter loops, Z = 1.40 to 4.40 mm)
# Two main vertical spine ribs at Y = ±22.5 mm + three horizontal cross-ribs
add_objs.append(create_box_obj("Rib_Vert_L",    -108.5, 108.5, -23.75, -21.25, 1.40, 4.40))
add_objs.append(create_box_obj("Rib_Vert_R",    -108.5, 108.5,  21.25,  23.75, 1.40, 4.40))
add_objs.append(create_box_obj("Rib_Cross_Top",  -49.0, -46.5, -85.5,   85.5,  1.40, 4.40))
add_objs.append(create_box_obj("Rib_Cross_Mid",  -11.5,  -9.0, -85.5,   85.5,  1.40, 4.40))
add_objs.append(create_box_obj("Rib_Cross_Bot",   62.0,  64.5, -85.5,   85.5,  1.40, 4.40))

# 1. Audited 28BYJ-48 Stepper Motor Mounts Sitting Directly on Z = 1.80 mm Web (NO recessed pocket!)
for mname, x_shaft, x_can in [("Upper", -25.30, -17.30), ("Lower", 78.20, 70.20)]:
    add_objs.append(create_cyl_obj(f"Add_{mname}_CanRing", x_can, 0.0, 16.80, 1.40, 6.30, segs=64))
    for sy in (-1.0, 1.0):
        add_objs.append(create_cyl_obj(f"Add_{mname}_EarWall_{sy}", x_can, sy * 17.50, 6.40, 1.40, 6.30, segs=48))
        add_objs.append(create_box_obj(f"Add_{mname}_EarBridgeWall_{sy}", x_can - 6.40, x_can + 6.40,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), 1.40, 6.30))

    # Motor sits at Z = 1.80 mm (coplanar with the Z = 1.80 mm web — ZERO pocket step in the web!)
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_CanPocket", x_can, 0.0, 14.22, z_web, 8.00, segs=64))
    for sy in (-1.0, 1.0):
        sub_objs.append(create_cyl_obj(f"Sub_{mname}_EarPocket_{sy}", x_can, sy * 17.50, 3.85, z_web, 8.00, segs=48))
        sub_objs.append(create_box_obj(f"Sub_{mname}_EarBridgePocket_{sy}", x_can - 3.85, x_can + 3.85,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), z_web, 8.00))

    # Single clean round Ø11.2 mm (r = 5.60 mm) through-hole at (x_shaft, 0) for Shaft & Ø9mm Brass Boss!
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_ShaftBoss", x_shaft, 0.0, 5.60, -1.00, 8.00, segs=64))

    # Blue wire pod side opening at Bottom (+X) of motor can
    sub_objs.append(create_box_obj(f"Sub_{mname}_WirePod", x_can + 8.00, x_can + 19.50, -8.00, 8.00, z_web, 8.00))

    # Post-boolean additions: Locating pegs + 45-degree ear snap clips
    for sy in (-1.0, 1.0):
        post_sub_add_objs.append(create_cyl_obj(f"PostAdd_{mname}_EarPeg_{sy}", x_can, sy * 17.50, 1.85, 1.20, 5.40, segs=32))
        post_sub_add_objs.append(create_cone_obj(f"PostAdd_{mname}_EarPegTip_{sy}", x_can, sy * 17.50, 1.85, 1.25, 5.40, 6.00, segs=32))
        y_outer = sy * (17.50 + 3.85)
        s_dir = -sy
        yz_ear_clip = [
            (y_outer - s_dir * 2.55, z_web),
            (y_outer, z_web),
            (y_outer, 3.00),
            (y_outer + s_dir * 0.55, 3.55),
            (y_outer + s_dir * 0.55, 3.90),
            (y_outer - s_dir * 0.30, 4.60),
            (y_outer - s_dir * 2.55, 4.60),
        ]
        if s_dir < 0:
            yz_ear_clip = list(reversed(yz_ear_clip))
        post_sub_add_objs.append(create_prism_profile_x(f"PostAdd_{mname}_EarSnap_{sy}", x_can - 1.8, x_can + 1.8, yz_ear_clip))

# 2. Audited ULN2003 Motor Controller Cradles with Full Through-Windows (2.5 mm perimeter walls)
uln_positions = [(-28.00, -50.00), (-28.00, 50.00), (28.00, 50.00)]
z_uln_shelf = 3.60
for idx, (xc, yc) in enumerate(uln_positions):
    x0_in = xc - 16.60
    x1_in = xc + 14.60
    y0_in, y1_in = yc - 17.80, yc + 17.80
    xc_mid = 0.5 * (x0_in + x1_in)

    add_objs.append(create_box_obj(f"ULN_RailY0_{idx}", x0_in - 2.4, x1_in + 2.4, y0_in - 2.5, y0_in, 1.4, z_uln_shelf + 2.40))
    add_objs.append(create_box_obj(f"ULN_RailY1_{idx}", x0_in - 2.4, x1_in + 2.4, y1_in, y1_in + 2.5, 1.4, z_uln_shelf + 2.40))
    add_objs.append(create_box_obj(f"ULN_WallTopL_{idx}", x0_in - 2.4, x0_in, y0_in - 2.5, y0_in + 7.0, 1.4, z_uln_shelf + 1.80))
    add_objs.append(create_box_obj(f"ULN_WallTopR_{idx}", x0_in - 2.4, x0_in, y1_in - 7.0, y1_in + 2.5, 1.4, z_uln_shelf + 1.80))
    add_objs.append(create_box_obj(f"ULN_WallBot_{idx}", x1_in, x1_in + 2.4, y0_in - 2.5, y1_in + 2.5, 1.4, z_uln_shelf + 1.80))

    add_objs.append(create_box_obj(f"ULN_LedgeY0_{idx}", x0_in - 2.4, x1_in + 2.4, y0_in, yc - 14.0, 1.4, z_uln_shelf))
    add_objs.append(create_box_obj(f"ULN_LedgeY1_{idx}", x0_in - 2.4, x1_in + 2.4, yc + 14.0, y1_in, 1.4, z_uln_shelf))
    add_objs.append(create_box_obj(f"ULN_LedgeX0_{idx}", x0_in - 2.4, xc_mid - 12.4, yc - 14.5, yc + 14.5, 1.4, z_uln_shelf))
    add_objs.append(create_box_obj(f"ULN_LedgeX1_{idx}", xc_mid + 12.4, x1_in + 2.4, yc - 14.5, yc + 14.5, 1.4, z_uln_shelf))

    pts_top = [
        (x0_in - 2.4, 1.4),
        (x0_in, 1.4),
        (x0_in, z_uln_shelf + 1.80),
        (x0_in + 0.55, z_uln_shelf + 2.35),
        (x0_in + 0.55, z_uln_shelf + 2.75),
        (x0_in - 0.30, z_uln_shelf + 3.50),
        (x0_in - 2.4, z_uln_shelf + 3.50),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopL_{idx}", y0_in - 2.5, y0_in + 7.0, pts_top))
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopR_{idx}", y1_in - 7.0, y1_in + 2.5, pts_top))

    pts_bot = [
        (x1_in, 1.4),
        (x1_in + 2.4, 1.4),
        (x1_in + 2.4, z_uln_shelf + 3.50),
        (x1_in + 0.30, z_uln_shelf + 3.50),
        (x1_in - 0.55, z_uln_shelf + 2.75),
        (x1_in - 0.55, z_uln_shelf + 2.35),
        (x1_in, z_uln_shelf + 1.80),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipBot_{idx}", yc - 8.5, yc + 8.5, pts_bot))

    sub_objs.append(create_rounded_rect_obj(
        f"Sub_ULN_Window_{idx}",
        xc_mid - 12.4, xc_mid + 12.4,
        yc - 14.0, yc + 14.0,
        4.5, -1.0, 6.0, segs_corner=12
    ))

# 3. Sleek Low-Profile Freenove ESP32-S3-WROOM Cradle (X = +2.00 to +59.50 mm, Y = -51.00 mm)
esp_x0, esp_x1 = 2.00, 59.50
esp_yc = -51.00
esp_y0, esp_y1 = esp_yc - 14.35, esp_yc + 14.35
z_esp_shelf = 8.40

sub_objs.append(create_rounded_rect_obj(
    "Sub_ESP_SingleWindow",
    esp_x0 + 2.5, esp_x1 - 2.5,
    esp_yc - 12.50, esp_yc + 12.50,
    4.5, -1.0, 6.0, segs_corner=12
))

add_objs.append(create_box_obj("ESP_WallY0", esp_x0 - 2.4, esp_x1 + 2.4, esp_y0 - 2.50, esp_y0, 1.40, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_WallY1", esp_x0 - 2.4, esp_x1 + 2.4, esp_y1, esp_y1 + 2.50, 1.40, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_LedgeY0", esp_x0 - 2.4, esp_x1 + 2.4, esp_y0, esp_y0 + 1.25, 1.40, z_esp_shelf))
add_objs.append(create_box_obj("ESP_LedgeY1", esp_x0 - 2.4, esp_x1 + 2.4, esp_y1 - 1.25, esp_y1, 1.40, z_esp_shelf))

add_objs.append(create_box_obj("ESP_TopStop_L", esp_x0 - 2.40, esp_x0, esp_y0 - 2.50, esp_yc - 10.20, 1.40, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_TopStop_R", esp_x0 - 2.40, esp_x0, esp_yc + 10.20, esp_y1 + 2.50, 1.40, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_BotStop_L", esp_x1, esp_x1 + 2.40, esp_y0 - 2.50, esp_y0 + 1.80, 1.40, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_BotStop_R", esp_x1, esp_x1 + 2.40, esp_y1 - 1.80, esp_y1 + 2.50, 1.40, z_esp_shelf + 1.70))

for cx0, cx1 in [(esp_x0 + 6.0, esp_x0 + 14.0), (esp_x1 - 14.0, esp_x1 - 6.0)]:
    pts_esp_y0 = [
        (esp_y0 - 2.50, z_esp_shelf),
        (esp_y0, z_esp_shelf),
        (esp_y0, z_esp_shelf + 1.65),
        (esp_y0 + 0.55, z_esp_shelf + 2.20),
        (esp_y0 + 0.55, z_esp_shelf + 2.50),
        (esp_y0 - 0.30, z_esp_shelf + 3.00),
        (esp_y0 - 2.50, z_esp_shelf + 3.00),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_esp_y0))
    pts_esp_y1 = [
        (esp_y1, z_esp_shelf),
        (esp_y1 + 2.50, z_esp_shelf),
        (esp_y1 + 2.50, z_esp_shelf + 3.00),
        (esp_y1 + 0.30, z_esp_shelf + 3.00),
        (esp_y1 - 0.55, z_esp_shelf + 2.50),
        (esp_y1 - 0.55, z_esp_shelf + 2.20),
        (esp_y1, z_esp_shelf + 1.65),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_esp_y1))

# 4. CLEAN WIDE OPEN SKELETON TRUSS WINDOWS — Zero skinny strips, all wide R=5.5mm windows!
truss_windows = [
    # Top-Left quadrant (X = -102.5 to -52, Y = -79.5 to -26.5)
    ("Bay_TL_Outer", -102.5, -52.0, -79.5, -55.5, 5.5),
    ("Bay_TL_Inner", -102.5, -52.0, -47.0, -26.5, 5.5),
    # Top-Center spine above Upper Motor (X = -102.5 to -52 and -43.5 to -37.5, Y = -18.5 to +18.5)
    ("Bay_TC_Upper", -102.5, -52.0, -18.5,  18.5, 5.5),
    # Top-Right quadrant (X = -102.5 to -52, Y = +26.5 to +79.5)
    ("Bay_TR_Inner", -102.5, -52.0,  26.5,  47.0, 5.5),
    ("Bay_TR_Outer", -102.5, -52.0,  55.5,  79.5, 5.5),
    # Mid-Center spine between Upper Motor and Lower Motor (X = +4.0 to +50.0, Y = -18.5 to +18.5)
    ("Bay_MC_Center",   4.0,  50.0, -18.5,  18.5, 5.5),
    # Outer Left flank beside ULN_0 and ESP32 (Y = -79.5 to -71.0)
    ("Bay_Flank_L1",  -43.5, -14.0, -79.5, -71.0, 3.8),
    ("Bay_Flank_L2",    2.0,  59.0, -79.5, -71.0, 3.8),
    # Outer Right flank beside ULN_1 and ULN_2 (Y = +71.0 to +79.5)
    ("Bay_Flank_R1",  -43.5, -14.0,  71.0,  79.5, 3.8),
    ("Bay_Flank_R2",   11.0,  43.0,  71.0,  79.5, 3.8),
    # Single clean wide window between ULN_1 and ULN_2 on Right side (X = -6.0 to +8.0, Y = +29.5 to +68.5)
    ("Bay_Mid_R",      -6.0,   8.0,  29.5,  68.5, 4.5),
    # Bottom-Left below ESP32 (X = +67.0 to +102.5, Y = -79.5 to -26.5)
    ("Bay_BL_Outer",   67.0, 102.5, -79.5, -55.5, 5.5),
    ("Bay_BL_Inner",   67.0, 102.5, -47.0, -26.5, 5.5),
    # Bottom-Right below ULN_2 (X = +48.0 to +59.0 and +67.0 to +102.5, Y = +26.5 to +79.5)
    ("Bay_BR_Mid",     48.0,  59.0,  29.5,  78.0, 4.5),
    ("Bay_BR_Inner",   67.0, 102.5,  26.5,  47.0, 5.5),
    ("Bay_BR_Outer",   67.0, 102.5,  55.5,  79.5, 5.5),
    # Bottom-Center below Lower Motor (X = +90.5 to +102.5, Y = -18.5 to +18.5)
    ("Bay_BC_Bot",     90.5, 102.5, -18.5,  18.5, 4.5),
]
for bname, x0, x1, y0, y1, r in truss_windows:
    sub_objs.append(create_rounded_rect_obj(bname, x0, x1, y0, y1, r, -1.0, 6.0, segs_corner=12))

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

# Step C: Boolean UNION post_sub_add_objs
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
vol_cm3 = bm_out.calc_volume() / 1000.0
print(f"V9 Open Skeleton Motor Mount: verts={len(bm_out.verts)}, faces={len(bm_out.faces)}, non_manifold={len(non_m)}, vol={vol_cm3:.1f} cm3")
bm_out.to_mesh(plate.data)
bm_out.free()

plate_paths = [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V9_OPEN_SKELETON_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V9_OPEN_SKELETON_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V7_ZERO_HOLES_LAYER1_Motor_Mount_Plate_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V7_ZERO_HOLES_LAYER1_Motor_Mount_Plate_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V8_FAST_50MIN_Motor_Mount_Plate_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V8_FAST_50MIN_Motor_Mount_Plate_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/NEW3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
]
bpy.ops.object.select_all(action='DESELECT')
plate.select_set(True)
for p in plate_paths:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
    print("  Exported:", p)
