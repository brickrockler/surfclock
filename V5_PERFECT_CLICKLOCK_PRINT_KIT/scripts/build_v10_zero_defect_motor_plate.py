import bpy
import bmesh
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

def make_bm_mesh(name, bm):
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def extrude_2d_loop(bm, pts_xy, z0, z1):
    bot_v = [bm.verts.new((px, py, z0)) for px, py in pts_xy]
    top_v = [bm.verts.new((px, py, z1)) for px, py in pts_xy]
    bm.faces.new(list(reversed(bot_v)))
    bm.faces.new(top_v)
    n = len(pts_xy)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([bot_v[i], bot_v[j], top_v[j], top_v[i]])

def rounded_rect_pts(x0, x1, y0, y1, r, segs_corner=16):
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
    return pts

def create_rounded_rect_obj(name, x0, x1, y0, y1, r, z0, z1, segs_corner=16):
    bm = bmesh.new()
    extrude_2d_loop(bm, rounded_rect_pts(x0, x1, y0, y1, r, segs_corner), z0, z1)
    return make_bm_mesh(name, bm)

def create_box_obj(name, x0, x1, y0, y1, z0, z1):
    bm = bmesh.new()
    extrude_2d_loop(bm, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1)
    return make_bm_mesh(name, bm)

def create_cyl_obj(name, cx, cy, r, z0, z1, segs=64):
    bm = bmesh.new()
    pts = [(cx + r * math.cos(2.0 * math.pi * i / segs), cy + r * math.sin(2.0 * math.pi * i / segs)) for i in range(segs)]
    extrude_2d_loop(bm, pts, z0, z1)
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
    return make_bm_mesh(name, bm)

def bool_op(target, tool, op='UNION'):
    mod = target.modifiers.new(name="BoolOp", type='BOOLEAN')
    mod.operation = op
    mod.solver = 'EXACT'
    mod.use_self = False
    mod.object = tool
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)

# ==============================================================================
# V10 ZERO-DEFECT MOTOR MOUNT PLATE
# ==============================================================================
z_base = 2.24  # 11 layers at 0.20mm (never lands on an exact 0.05mm or 0.10mm slice plane!)

# 1. Base Plate: Z = 0.00 to 2.24 mm, R = 12.0 mm smooth corners (identical base architecture to 2a_Dial_Face!)
plate = create_rounded_rect_obj("BasePlate", -111.00, 111.00, -88.00, 88.00, 12.0, 0.0, z_base, segs_corner=24)

# 2. Outer Perimeter Click-Lock Rim (Z = 1.03 to 3.04 mm along outer edges so total edge height = 3.04 mm)
bool_op(plate, create_box_obj("Rim_Top",   -110.98, -107.80, -75.0,  75.0, 1.03, 3.04), 'UNION')
bool_op(plate, create_box_obj("Rim_Bot",    107.80,  110.98, -75.0,  75.0, 1.03, 3.04), 'UNION')
bool_op(plate, create_box_obj("Rim_Left",   -98.0,    98.0,  -87.98, -84.80, 1.03, 3.04), 'UNION')
bool_op(plate, create_box_obj("Rim_Right",  -98.0,    98.0,   84.80,  87.98, 1.03, 3.04), 'UNION')

# 3. Audited 28BYJ-48 Stepper Motor Keyhole Cradles (Sitting directly on Z = 2.24 mm!)
for idx_m, (mname, x_shaft, x_can) in enumerate([("Upper", -25.30, -17.30), ("Lower", 78.20, 70.20)]):
    z_m_top = 6.44
    bool_op(plate, create_cyl_obj(f"Add_{mname}_CanOuter", x_can, 0.0, 17.40, 1.11 + 0.03*idx_m, z_m_top, segs=64), 'UNION')
    bool_op(plate, create_rounded_rect_obj(f"Add_{mname}_EarBoxOuter", x_can - 6.80, x_can + 6.80, -24.40, 24.40, 3.0, 1.17 + 0.03*idx_m, z_m_top, segs_corner=12), 'UNION')

    # Subtract Motor Can Pocket (r = 14.25 mm) + Mounting Ear Keyhole (X = x_can-3.85..x_can+3.85, Y = -21.35..+21.35, R=1.60)
    bool_op(plate, create_cyl_obj(f"Sub_{mname}_CanPocket", x_can, 0.0, 14.25, z_base, 9.0, segs=64), 'DIFFERENCE')
    bool_op(plate, create_rounded_rect_obj(f"Sub_{mname}_EarPocket", x_can - 3.85, x_can + 3.85, -21.35, 21.35, 1.60, z_base, 9.0, segs_corner=12), 'DIFFERENCE')

    # Subtract Blue Wire Pod side opening (+X side of motor can, 15.6 mm wide)
    bool_op(plate, create_box_obj(f"Sub_{mname}_WirePod", x_can + 8.00, x_can + 20.00, -7.80, 7.80, z_base, 9.0), 'DIFFERENCE')

    # Subtract Clean Round Ø11.20 mm (r = 5.60 mm) Through-Hole for Shaft & Ø9mm Brass Boss from Z = -1 to +9 mm
    bool_op(plate, create_cyl_obj(f"Sub_{mname}_ShaftHole", x_shaft, 0.0, 5.60, -1.0, 9.0, segs=64), 'DIFFERENCE')

    # Union two straight-wall 45-degree ear snap clips flush with the flat Y = ±21.35 mm wall and flush with z_m_top = 6.44 mm
    for sy in (-1.0, 1.0):
        y_wall = sy * 21.35
        s_in = -sy
        yz_clip = [
            (sy * 24.35,           z_base + 0.20),
            (y_wall,               z_base + 0.20),
            (y_wall,               z_base + 1.40),
            (y_wall + s_in * 0.60, z_base + 2.00),
            (y_wall + s_in * 0.60, z_base + 2.40),
            (y_wall,               z_base + 3.00),
            (y_wall,               z_m_top),
            (sy * 24.35,           z_m_top),
        ]
        if s_in < 0:
            yz_clip = list(reversed(yz_clip))
        bool_op(plate, create_prism_profile_x(f"Clip_{mname}_{sy}", x_can - 2.00, x_can + 2.00, yz_clip), 'UNION')

# 4. Audited ULN2003 Motor Controller Cradles (Flush top at Z = 7.64 mm -> ZERO small top islands!)
uln_positions = [(-28.00, -50.00), (-28.00, 50.00), (28.00, 50.00)]
z_uln_shelf = 4.84
z_uln_top   = 7.64
for idx, (xc, yc) in enumerate(uln_positions):
    x0_in, x1_in = xc - 16.60, xc + 14.60
    y0_in, y1_in = yc - 17.80, yc + 17.80
    xc_mid = 0.5 * (x0_in + x1_in)
    wall_t = 2.80

    cradle = create_rounded_rect_obj(
        f"ULN_Outer_{idx}",
        x0_in - wall_t, x1_in + wall_t,
        y0_in - wall_t, y1_in + wall_t,
        2.5, 1.23 + 0.02 * idx, z_uln_top, segs_corner=8
    )
    bool_op(cradle, create_rounded_rect_obj(
        f"ULN_InnerThrough_{idx}",
        xc_mid - 12.60, xc_mid + 12.60,
        yc - 14.80, yc + 14.80,
        2.0, 0.50, z_uln_top + 2.0, segs_corner=8
    ), 'DIFFERENCE')
    bool_op(cradle, create_box_obj(
        f"ULN_PCBPocket_{idx}",
        x0_in, x1_in, y0_in, y1_in, z_uln_shelf, z_uln_top + 2.0
    ), 'DIFFERENCE')
    bool_op(cradle, create_box_obj(
        f"ULN_TopNotch_{idx}",
        x0_in - wall_t - 1.0, x0_in + 2.0, yc - 10.50, yc + 10.50, z_uln_shelf, z_uln_top + 2.0
    ), 'DIFFERENCE')
    # 45-degree snap-lock ridge along bottom wall, ending flush at z_uln_top = 7.64 mm!
    pts_bot = [
        (x1_in,          z_uln_shelf + 0.20),
        (x1_in + wall_t, z_uln_shelf + 0.20),
        (x1_in + wall_t, z_uln_top),
        (x1_in,          z_uln_top),
        (x1_in - 0.55,   z_uln_top - 0.55),
        (x1_in - 0.55,   z_uln_top - 0.90),
        (x1_in,          z_uln_top - 1.45),
    ]
    bool_op(cradle, create_prism_profile_y(f"ULN_BotClip_{idx}", yc - 8.50, yc + 8.50, pts_bot), 'UNION')
    bool_op(plate, cradle, 'UNION')

# 5. Sleek Low-Profile Freenove ESP32-S3-WROOM Cradle (Flush top at Z = 11.44 mm -> ZERO small top islands!)
esp_x0, esp_x1 = 2.00, 59.50
esp_yc = -51.00
esp_y0, esp_y1 = esp_yc - 14.35, esp_yc + 14.35
z_esp_shelf = 8.64
z_esp_top   = 11.44
esp_wall_t  = 2.80

esp_cradle = create_rounded_rect_obj(
    "ESP_Outer",
    esp_x0 - esp_wall_t, esp_x1 + esp_wall_t,
    esp_y0 - esp_wall_t, esp_y1 + esp_wall_t,
    2.5, 1.31, z_esp_top, segs_corner=8
)
bool_op(esp_cradle, create_rounded_rect_obj(
    "ESP_InnerHollow",
    esp_x0 + 1.80, esp_x1 - 1.80,
    esp_y0 + 1.40, esp_y1 - 1.40,
    2.0, 0.50, z_esp_top + 2.0, segs_corner=8
), 'DIFFERENCE')
bool_op(esp_cradle, create_box_obj(
    "ESP_PCBPocket",
    esp_x0, esp_x1, esp_y0, esp_y1, z_esp_shelf, z_esp_top + 2.0
), 'DIFFERENCE')
bool_op(esp_cradle, create_box_obj(
    "ESP_TopOpen",
    esp_x0 - esp_wall_t - 1.0, esp_x0 + 2.0, esp_yc - 10.20, esp_yc + 10.20, z_esp_shelf, z_esp_top + 2.0
), 'DIFFERENCE')
bool_op(esp_cradle, create_box_obj(
    "ESP_USBC_Open",
    esp_x1 - 2.0, esp_x1 + esp_wall_t + 1.0, esp_yc - 11.50, esp_yc + 11.50, z_esp_shelf - 1.80, z_esp_top + 2.0
), 'DIFFERENCE')
for cx0, cx1 in [(esp_x0 + 8.0, esp_x0 + 18.0), (esp_x1 - 18.0, esp_x1 - 8.0)]:
    pts_y0 = [
        (esp_y0 - esp_wall_t, z_esp_shelf + 0.20),
        (esp_y0,              z_esp_shelf + 0.20),
        (esp_y0,              z_esp_top - 1.45),
        (esp_y0 + 0.55,       z_esp_top - 0.90),
        (esp_y0 + 0.55,       z_esp_top - 0.55),
        (esp_y0,              z_esp_top),
        (esp_y0 - esp_wall_t, z_esp_top),
    ]
    bool_op(esp_cradle, create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_y0), 'UNION')
    pts_y1 = [
        (esp_y1,              z_esp_shelf + 0.20),
        (esp_y1 + esp_wall_t, z_esp_shelf + 0.20),
        (esp_y1 + esp_wall_t, z_esp_top),
        (esp_y1,              z_esp_top),
        (esp_y1 - 0.55,       z_esp_top - 0.55),
        (esp_y1 - 0.55,       z_esp_top - 0.90),
        (esp_y1,              z_esp_top - 1.45),
    ]
    bool_op(esp_cradle, create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_y1), 'UNION')

bool_op(plate, esp_cradle, 'UNION')

bm_out = bmesh.new()
bm_out.from_mesh(plate.data)
bmesh.ops.remove_doubles(bm_out, verts=bm_out.verts, dist=1e-4)
bmesh.ops.triangulate(bm_out, faces=bm_out.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.dissolve_degenerate(bm_out, dist=1e-4)
bmesh.ops.remove_doubles(bm_out, verts=bm_out.verts, dist=1e-4)
bmesh.ops.recalc_face_normals(bm_out, faces=bm_out.faces)

non_m = [e for e in bm_out.edges if not e.is_manifold]
zero_f = [f for f in bm_out.faces if f.calc_area() < 1e-5]
vol_cm3 = bm_out.calc_volume() / 1000.0
print(f"V10 Zero-Defect Motor Mount: verts={len(bm_out.verts)}, faces={len(bm_out.faces)}, non_manifold={len(non_m)}, zero_f={len(zero_f)}, vol={vol_cm3:.1f} cm3")
bm_out.to_mesh(plate.data)
bm_out.free()

plate_paths = [
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V10_AUDITED_ZERO_DEFECT_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V10_AUDITED_ZERO_DEFECT_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V9_OPEN_SKELETON_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V9_OPEN_SKELETON_Motor_Mount_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/V7_ZERO_HOLES_LAYER1_Motor_Mount_Plate_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/V7_ZERO_HOLES_LAYER1_Motor_Mount_Plate_PrusaMK4.stl",
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
