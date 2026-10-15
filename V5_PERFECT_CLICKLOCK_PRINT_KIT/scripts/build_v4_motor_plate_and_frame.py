import bpy
import bmesh
import math
import os

# ==============================================================================
# PART 1: Rebuild 3_Motor_Mount_Plate with:
#   1) Bottom side of ULN2003 motor controller clips moved UP by 2.0 mm
#      (x1_in moved from xc + 16.60 to xc + 14.60 -> vertical pocket height = 31.20 mm instead of 33.20 mm!)
#   2) All 4 corners cleanly notched (|X| > 100.60, |Y| > 77.60) so it drops straight past
#      both old & new outer frame corner posts!
#   3) Tapered perimeter snug-fit friction tabs along the 4 straight edges so it pushes down
#      smoothly and locks in snugly at the bottom without needing corner screws!
# ==============================================================================

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
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segs,
        radius1=r,
        radius2=r,
        depth=(z1 - z0),
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx, cy, 0.5 * (z0 + z1)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_cone_obj(name, cx, cy, r1, r2, z0, z1, segs=48):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segs,
        radius1=r1,
        radius2=r2,
        depth=(z1 - z0),
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx, cy, 0.5 * (z0 + z1)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return make_bm_mesh(name, bm)

def create_rounded_rect_obj(name, x0, x1, y0, y1, r, z0, z1, segs_corner=16):
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

# 1. Base Plate with Notched Corners:
# Outer span: 222.06 x 176.06 mm (|X| <= 111.03, |Y| <= 88.03), Z = 0.0 .. 3.0 mm
# Corner notches at |X| > 100.60, |Y| > 77.60 so all 4 corners bypass the outer frame corner pillars!
plate = create_box_obj("BasePlate", -111.03, 111.03, -88.03, 88.03, 0.0, 3.0)

add_objs = []
sub_objs = []

# Cut the 4 corner L-notches (|X| > 100.60 and |Y| > 77.60) through the full Z range
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        x0 = 100.60 if sx > 0 else -112.00
        x1 = 112.00 if sx > 0 else -100.60
        y0 = 77.60 if sy > 0 else -89.00
        y1 = 89.00 if sy > 0 else -77.60
        sub_objs.append(create_box_obj(f"Cut_CornerNotch_{sx}_{sy}", x0, x1, y0, y1, -1.0, 15.0))

# 2. Structural Window Cutouts
sub_objs.append(create_rounded_rect_obj("Cut_TopWin", -96.0, -48.0, -74.0, 74.0, 4.0, -1.0, 5.0, segs_corner=8))
sub_objs.append(create_rounded_rect_obj("Cut_MidWin", 16.0, 40.0, -20.0, 20.0, 3.0, -1.0, 5.0, segs_corner=8))

# 3. Upper & Lower 28BYJ-48 Stepper Motor Mounts
for mname, x_shaft, x_can in [("Upper", -25.30, -17.30), ("Lower", 78.20, 70.20)]:
    add_objs.append(create_cyl_obj(f"Add_{mname}_CanRing", x_can, 0.0, 16.40, 0.0, 6.00, segs=64))
    for sy in (-1.0, 1.0):
        add_objs.append(create_cyl_obj(f"Add_{mname}_Ear_{sy}", x_can, sy * 17.50, 4.90, 0.0, 5.00, segs=48))
        add_objs.append(create_box_obj(f"Add_{mname}_EarBridge_{sy}", x_can - 4.90, x_can + 4.90, min(0.0, sy * 17.50), max(0.0, sy * 17.50), 0.0, 5.00))
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_CanPocket", x_can, 0.0, 14.25, 2.00, 7.00, segs=64))
    for sy in (-1.0, 1.0):
        sub_objs.append(create_box_obj(f"Sub_{mname}_EarFlat_{sy}", x_can - 6.0, x_can + 6.0, sy * 17.50 - 6.0 if sy < 0 else 13.8, -13.8 if sy < 0 else sy * 17.50 + 6.0, 5.00, 7.00))
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_ShaftHole", x_shaft, 0.0, 5.20, -1.0, 8.0, segs=48))
    if mname == "Upper":
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can + 8.0, x_can + 18.0, -8.5, 8.5, 3.00, 7.00))
    else:
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can - 18.0, x_can - 8.0, -8.5, 8.5, 3.00, 7.00))
    for sy in (-1.0, 1.0):
        sub_objs.append(create_cyl_obj(f"Sub_{mname}_Pilot_{sy}", x_can, sy * 17.50, 0.775, -1.0, 6.0, segs=32))
        sub_objs.append(create_cone_obj(f"Sub_{mname}_CSink_{sy}", x_can, sy * 17.50, 0.775, 1.40, 4.30, 5.05, segs=32))

# 4. ULN2003 Motor Controller Cradles — Bottom clip moved UP by 2.0 mm!
# In Portrait Clock Space (yp = -X_bed):
#   - Top clip is at x0_in = xc - 16.60
#   - Bottom clip was at x1_in = xc + 16.60 (making pocket 33.20 mm tall, 2.0 mm too big!)
#   - Moving the bottom clip UP (toward -X_bed) by 2.0 mm sets x1_in = xc + 14.60 (pocket height = 31.20 mm!)
for ix, xc in enumerate([-28.00, 28.00]):
    for iy, yc in enumerate([-50.00, 50.00]):
        x0_in = xc - 16.60
        x1_in = xc + 14.60  # Moved UP by 2.00 mm! (31.20 mm inner height instead of 33.20 mm)
        y0_in, y1_in = yc - 18.60, yc + 18.60
        xc_mid = 0.5 * (x0_in + x1_in)  # xc - 1.00

        # Side guide rails along Y0 and Y1
        add_objs.append(create_box_obj(f"ULN_RailY0_{ix}_{iy}", x0_in - 1.0, x1_in + 1.0, y0_in - 2.2, y0_in, 2.5, 6.8))
        add_objs.append(create_box_obj(f"ULN_RailY1_{ix}_{iy}", x0_in - 1.0, x1_in + 1.0, y1_in, y1_in + 2.2, 2.5, 6.8))
        # 4 Corner PCB Standoff Ledges (Z = 2.5..4.20 mm, 4.5 x 4.5 mm)
        for cx_c in [x0_in, x1_in - 4.5]:
            for cy_c in [y0_in, y1_in - 4.5]:
                add_objs.append(create_box_obj(f"ULN_Pad_{ix}_{iy}_{cx_c}_{cy_c}", cx_c, cx_c + 4.5, cy_c, cy_c + 4.5, 2.5, 4.20))

        # Top Snap-Latch Clip at x0_in
        pts_top = [
            (x0_in - 1.9, 2.5),
            (x0_in, 2.5),
            (x0_in, 6.8),
            (x0_in + 0.65, 7.6),
            (x0_in + 0.65, 8.0),
            (x0_in - 0.35, 9.0),
            (x0_in - 1.9, 9.0),
        ]
        add_objs.append(create_prism_profile_y(f"ULN_ClipTop_{ix}_{iy}", yc - 6.0, yc + 6.0, pts_top))

        # Bottom Snap-Latch Clip at x1_in (moved UP by 2.00 mm!)
        pts_bot = [
            (x1_in, 2.5),
            (x1_in + 1.9, 2.5),
            (x1_in + 1.9, 9.0),
            (x1_in + 0.35, 9.0),
            (x1_in - 0.65, 8.0),
            (x1_in - 0.65, 7.6),
            (x1_in, 6.8),
        ]
        add_objs.append(create_prism_profile_y(f"ULN_ClipBot_{ix}_{iy}", yc - 6.0, yc + 6.0, pts_bot))

        # Ventilation / solder-pin relief window centered in the 31.20 mm pocket
        sub_objs.append(create_rounded_rect_obj(f"Sub_ULN_Vent_{ix}_{iy}", xc_mid - 9.5, xc_mid + 9.5, yc - 12.0, yc + 12.0, 2.5, -1.0, 5.0, segs_corner=6))

# 5. Bottom ESP32 Cradle & Retaining Clips (Bottom-Left Bay: X in [+45.0..+100.0], Yc = -53.0)
esp_x0, esp_x1 = 45.0, 100.0
esp_yc = -53.0
esp_y0, esp_y1 = esp_yc - 15.10, esp_yc + 15.10  # [-68.10 .. -37.90]
add_objs.append(create_box_obj("ESP_Wall_Y0", esp_x0 - 2.0, esp_x1, esp_y0 - 2.20, esp_y0, 2.5, 11.20))
add_objs.append(create_box_obj("ESP_Shelf_Y0", esp_x0, esp_x1, esp_y0, esp_y0 + 2.30, 2.5, 9.50))
add_objs.append(create_box_obj("ESP_Wall_Y1", esp_x0 - 2.0, esp_x1, esp_y1, esp_y1 + 2.20, 2.5, 11.20))
add_objs.append(create_box_obj("ESP_Shelf_Y1", esp_x0, esp_x1, esp_y1 - 2.30, esp_y1, 2.5, 9.50))
add_objs.append(create_box_obj("ESP_TopStop_L", esp_x0 - 2.20, esp_x0, esp_y0 - 2.20, esp_yc - 6.0, 2.5, 11.50))
add_objs.append(create_box_obj("ESP_TopStop_R", esp_x0 - 2.20, esp_x0, esp_yc + 6.0, esp_y1 + 2.20, 2.5, 11.50))
add_objs.append(create_box_obj("ESP_BotStop_L", esp_x1, esp_x1 + 2.20, esp_y0 - 2.20, esp_yc - 8.0, 2.5, 11.50))
add_objs.append(create_box_obj("ESP_BotStop_R", esp_x1, esp_x1 + 2.20, esp_yc + 8.0, esp_y1 + 2.20, 2.5, 11.50))

for cx0, cx1 in [(52.0, 64.0), (80.0, 92.0)]:
    pts_esp_y0 = [
        (esp_y0 - 2.20, 9.0),
        (esp_y0, 9.0),
        (esp_y0, 11.1),
        (esp_y0 + 0.70, 11.7),
        (esp_y0 + 0.70, 12.1),
        (esp_y0 - 0.30, 13.1),
        (esp_y0 - 2.20, 13.1),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_esp_y0))
    pts_esp_y1 = [
        (esp_y1, 9.0),
        (esp_y1 + 2.20, 9.0),
        (esp_y1 + 2.20, 13.1),
        (esp_y1 + 0.30, 13.1),
        (esp_y1 - 0.70, 12.1),
        (esp_y1 - 0.70, 11.7),
        (esp_y1, 11.1),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_esp_y1))

for sy in (-1.0, 1.0):
    py_pin = esp_yc + sy * 12.0
    sub_objs.append(create_rounded_rect_obj(f"Sub_ESP_PinSlot_{sy}", esp_x0 + 2.0, esp_x1 - 2.0, py_pin - 2.8, py_pin + 2.8, 1.5, -1.0, 9.6, segs_corner=6))
sub_objs.append(create_rounded_rect_obj("Sub_ESP_CenterVent", esp_x0 + 5.0, esp_x1 - 5.0, esp_yc - 6.0, esp_yc + 6.0, 2.5, -1.0, 5.0, segs_corner=6))

# 6. Second Bottom Bay (Bottom-Right: X in [+46.0..+98.0], Yc = +53.0)
b2_x0, b2_x1 = 46.0, 98.0
b2_yc = 53.0
b2_y0, b2_y1 = b2_yc - 19.10, b2_yc + 19.10
add_objs.append(create_box_obj("Bay2_WallY0", b2_x0 - 2.0, b2_x1 + 2.0, b2_y0 - 2.20, b2_y0, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_WallY1", b2_x0 - 2.0, b2_x1 + 2.0, b2_y1, b2_y1 + 2.20, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_TopStopL", b2_x0 - 2.20, b2_x0, b2_y0 - 2.20, b2_yc - 8.0, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_TopStopR", b2_x0 - 2.20, b2_x0, b2_yc + 8.0, b2_y1 + 2.20, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_BotStopL", b2_x1, b2_x1 + 2.20, b2_y0 - 2.20, b2_yc - 8.0, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_BotStopR", b2_x1, b2_x1 + 2.20, b2_yc + 8.0, b2_y1 + 2.20, 2.5, 8.50))
add_objs.append(create_box_obj("Bay2_StepL", b2_x0 + 2.0, b2_x1 - 2.0, b2_y0, b2_y0 + 4.0, 2.5, 4.20))
add_objs.append(create_box_obj("Bay2_StepR", b2_x0 + 2.0, b2_x1 - 2.0, b2_y1 - 4.0, b2_y1, 2.5, 4.20))
for cx0, cx1 in [(54.0, 66.0), (78.0, 90.0)]:
    pts_b2_y0 = [
        (b2_y0 - 2.20, 7.5),
        (b2_y0, 7.5),
        (b2_y0, 9.2),
        (b2_y0 + 0.75, 9.9),
        (b2_y0 + 0.75, 10.3),
        (b2_y0 - 0.30, 11.3),
        (b2_y0 - 2.20, 11.3),
    ]
    add_objs.append(create_prism_profile_x(f"Bay2_ClipY0_{cx0}", cx0, cx1, pts_b2_y0))
    pts_b2_y1 = [
        (b2_y1, 7.5),
        (b2_y1 + 2.20, 7.5),
        (b2_y1 + 2.20, 11.3),
        (b2_y1 + 0.30, 11.3),
        (b2_y1 - 0.75, 10.3),
        (b2_y1 - 0.75, 9.9),
        (b2_y1, 9.2),
    ]
    add_objs.append(create_prism_profile_x(f"Bay2_ClipY1_{cx0}", cx0, cx1, pts_b2_y1))
sub_objs.append(create_rounded_rect_obj("Sub_Bay2_Vent", b2_x0 + 7.0, b2_x1 - 7.0, b2_yc - 11.0, b2_yc + 11.0, 3.0, -1.0, 5.0, segs_corner=6))

# 7. Cable Management Retainers
def make_cable_arch_x(name, x0, x1, yc, side_sign):
    s = side_sign
    yz = [
        (yc - s * 5.2, 2.5),
        (yc - s * 2.6, 2.5),
        (yc - s * 2.6, 5.5),
        (yc - s * 0.6, 7.5),
        (yc + s * 3.0, 7.5),
        (yc + s * 3.8, 6.5),
        (yc + s * 4.8, 6.5),
        (yc + s * 4.8, 8.5),
        (yc + s * 3.8, 9.3),
        (yc - s * 5.2, 9.3),
    ]
    if s < 0:
        yz = list(reversed(yz))
    return create_prism_profile_x(name, x0, x1, yz)

def make_cable_arch_y(name, y0, y1, xc, side_sign):
    s = side_sign
    xz = [
        (xc - s * 5.2, 2.5),
        (xc - s * 2.6, 2.5),
        (xc - s * 2.6, 5.5),
        (xc - s * 0.6, 7.5),
        (xc + s * 3.0, 7.5),
        (xc + s * 3.8, 6.5),
        (xc + s * 4.8, 6.5),
        (xc + s * 4.8, 8.5),
        (xc + s * 3.8, 9.3),
        (xc - s * 5.2, 9.3),
    ]
    if s > 0:
        xz = list(reversed(xz))
    return create_prism_profile_y(name, y0, y1, xz)

add_objs.append(make_cable_arch_x("CableArch_Mid_L", -8.0, 6.0, -23.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_Mid_R", -8.0, 6.0, +23.5, -1.0))
add_objs.append(make_cable_arch_x("CableArch_Bot_L", 44.0, 58.0, -25.0, -1.0))
add_objs.append(make_cable_arch_x("CableArch_Bot_R", 44.0, 58.0, +25.0, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutUL", -35.0, -21.0, -77.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutUR", -35.0, -21.0, +77.5, -1.0))
add_objs.append(make_cable_arch_x("CableArch_OutLL", 20.0, 34.0, -77.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutLR", 20.0, 34.0, +77.5, -1.0))
add_objs.append(make_cable_arch_y("CableArch_USBC", -16.0, -2.0, 96.5, +1.0))

# Perimeter stiffening rim (staying inside the notched corners: X in [-98..+98], Y in [-75..+75])
add_objs.append(create_box_obj("Rim_Top", -111.03, -108.50, -75.0, 75.0, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Left", -98.0, 98.0, -88.03, -85.50, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Right", -98.0, 98.0, 85.50, 88.03, 2.5, 5.2))

# 8. Snug Push-Fit Tapered Friction Tabs along the 4 outer edges:
# The Outer Frame inner cavity is |X| = 111.30 mm, |Y| = 88.30 mm.
# Our base plate is |X| = 111.03 mm, |Y| = 88.03 mm (0.27 mm clearance per side so it enters easily).
# We add 8 gentle tapered friction tabs (16 mm wide each) along the straight edges that flare from
# +0.00 mm at Z = 0.0..1.0 mm (easy lead-in!) to +0.17 mm at Z = 2.4..5.2 mm (reaching |X| = 111.20 mm, |Y| = 88.20 mm,
# a 0.10 mm per-side snug friction engagement against the frame wall!).
for sy in (-1.0, 1.0):
    for xc_tab in (-62.0, 0.0, 62.0):
        yz_tab = [
            (sy * 87.00, 0.0),
            (sy * 88.03, 0.0),
            (sy * 88.03, 0.8),
            (sy * 88.20, 2.4),
            (sy * 88.20, 5.2),
            (sy * 87.00, 5.2),
        ]
        if sy < 0:
            yz_tab = list(reversed(yz_tab))
        add_objs.append(create_prism_profile_x(f"SnugTab_Y_{sy}_{xc_tab}", xc_tab - 8.0, xc_tab + 8.0, yz_tab))

for sx in (-1.0, 1.0):
    for yc_tab in (-45.0, 45.0):
        xz_tab = [
            (sx * 110.00, 0.0),
            (sx * 111.03, 0.0),
            (sx * 111.03, 0.8),
            (sx * 111.20, 2.4),
            (sx * 111.20, 5.2),
            (sx * 110.00, 5.2),
        ]
        if sx > 0:
            xz_tab = list(reversed(xz_tab))
        add_objs.append(create_prism_profile_y(f"SnugTab_X_{sx}_{yc_tab}", yc_tab - 8.0, yc_tab + 8.0, xz_tab))

# Boolean UNION all add_objs
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

# Boolean DIFFERENCE all sub_objs
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

bm_out = bmesh.new()
bm_out.from_mesh(plate.data)
bmesh.ops.remove_doubles(bm_out, verts=bm_out.verts, dist=1e-4)
bmesh.ops.triangulate(bm_out, faces=bm_out.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_out, faces=bm_out.faces)
non_m = [e for e in bm_out.edges if not e.is_manifold]
print(f"Upgraded 3_Motor_Mount_Plate (Pilot Holes): verts={len(bm_out.verts)}, faces={len(bm_out.faces)}, non_manifold={len(non_m)}")
bm_out.to_mesh(plate.data)
bm_out.free()

pilot_paths = [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_ESP32_WiderClips_PilotHoles_PrusaMK4.stl",
]
bpy.ops.object.select_all(action='DESELECT')
plate.select_set(True)
for p in pilot_paths:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
    print("  Exported:", p)

# Also create the Screwless Push-Stud version (Ø2.85mm motor ear holes) with the exact same notched corners + 2mm tighter ULN clips!
for idx, (hx, hy) in enumerate([(-17.30, -17.50), (-17.30, 17.50), (70.20, -17.50), (70.20, 17.50)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.425, depth=20.0, location=(hx, hy, 5.0))
    cutter = bpy.context.active_object
    mod = plate.modifiers.new(name=f"PushHole_{idx}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

bm_s = bmesh.new()
bm_s.from_mesh(plate.data)
bmesh.ops.remove_doubles(bm_s, verts=bm_s.verts, dist=1e-4)
bmesh.ops.triangulate(bm_s, faces=bm_s.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm_s, faces=bm_s.faces)
non_ms = [e for e in bm_s.edges if not e.is_manifold]
print(f"Upgraded 3_Motor_Mount_Plate (Screwless): verts={len(bm_s.verts)}, faces={len(bm_s.faces)}, non_manifold={len(non_ms)}")
bm_s.to_mesh(plate.data)
bm_s.free()

bpy.ops.object.select_all(action='DESELECT')
plate.select_set(True)
for p in [
    "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
]:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True, ascii_format=False)
    print("  Exported:", p)
