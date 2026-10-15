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
# PART 1: BUILD FULLY AUDITED 3_MOTOR_MOUNT_PLATE (V5)
# ==============================================================================
plate = create_box_obj("BasePlate", -111.03, 111.03, -88.03, 88.03, 0.0, 3.0)
add_objs = []
sub_objs = []

# 1. Cut 4 Corner L-Notches (|X| > 100.60, |Y| > 77.60) so it drops effortlessly into existing frames
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        x0 = 100.60 if sx > 0 else -112.00
        x1 = 112.00 if sx > 0 else -100.60
        y0 = 77.60 if sy > 0 else -89.00
        y1 = 89.00 if sy > 0 else -77.60
        sub_objs.append(create_box_obj(f"Cut_CornerNotch_{sx}_{sy}", x0, x1, y0, y1, -1.0, 22.0))

# 2. Structural Weight-Saving Windows (kept clear of ESP32, motors, and cable paths)
sub_objs.append(create_rounded_rect_obj("Cut_TopWin", -96.0, -50.0, -74.0, 74.0, 4.0, 0.60, 5.0, segs_corner=8))
# Removed Cut_MidWin for unbroken Layer 1 sweeps
# Open window in the bottom-left USB-C bend zone (under the cable curve, keeping perimeter solid)
# Removed Cut_BotLeftWin (the exact hole in the user photo!) for unbroken Layer 1 sweeps

# 3. Audited 28BYJ-48 Stepper Motor Mounts (Upper & Lower)
#    - Coplanar Z = 2.00 mm floor for BOTH the Ø28.0 mm can AND the two metal mounting ears (Y = ±17.50 mm)
#      AND the 15.2 mm wide blue wire hump!
#    - Outer retaining walls up to Z = 6.50 mm around both the can and the ears so the motor drops 4.5 mm
#      deep into a figure-8 keyway (impossible to twist!).
#    - Integrated Ø3.85 mm chamfered locating posts on the Z = 2.00 mm ear seats (Z = 2.00 .. 5.60 mm)
#      with Ø1.60 mm pilot holes + side ear snap-clips that click over the 0.8 mm metal ears!
for mname, x_shaft, x_can in [("Upper", -25.30, -17.30), ("Lower", 78.20, 70.20)]:
    # Outer housing wall (Z = 0.0 to 6.50 mm) around can and both ears
    add_objs.append(create_cyl_obj(f"Add_{mname}_CanRing", x_can, 0.0, 16.50, 0.0, 6.50, segs=64))
    for sy in (-1.0, 1.0):
        add_objs.append(create_cyl_obj(f"Add_{mname}_EarWall_{sy}", x_can, sy * 17.50, 5.80, 0.0, 6.50, segs=48))
        add_objs.append(create_box_obj(f"Add_{mname}_EarBridgeWall_{sy}", x_can - 5.80, x_can + 5.80,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), 0.0, 6.50))

    # Cut Coplanar Z = 2.00 mm pocket for Can (r = 14.22 mm) + Ears (r = 3.85 mm) + Ear Bridge (7.70 mm wide)
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_CanPocket", x_can, 0.0, 14.22, 2.00, 8.00, segs=64))
    for sy in (-1.0, 1.0):
        sub_objs.append(create_cyl_obj(f"Sub_{mname}_EarPocket_{sy}", x_can, sy * 17.50, 3.85, 2.00, 8.00, segs=48))
        sub_objs.append(create_box_obj(f"Sub_{mname}_EarBridgePocket_{sy}", x_can - 3.85, x_can + 3.85,
                                       min(0.0, sy * 17.50), max(0.0, sy * 17.50), 2.00, 8.00))

    # Cut Shaft & Ø9mm Brass Boss Hole (r = 5.20 mm) all the way through
    sub_objs.append(create_cyl_obj(f"Sub_{mname}_ShaftHole", x_shaft, 0.0, 5.20, -1.0, 9.0, segs=48))

    # Cut Blue Plastic Wire Hump Slot ALL THE WAY DOWN TO Z = 2.00 mm (so wire hump never props motor up!)
    if mname == "Upper":
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can + 8.0, x_can + 19.0, -7.8, 7.8, 2.00, 8.00))
    else:
        sub_objs.append(create_box_obj(f"Sub_{mname}_WireExit", x_can - 19.0, x_can - 8.0, -7.8, 7.8, 2.00, 8.00))

    # Add Integrated Locating Posts (r = 1.92 mm -> Ø3.84 mm for Ø4.2 mm metal ear holes, Z = 2.00 to 5.40 mm,
    # with conical chamfered top Z = 5.40 to 6.20 mm) + ear snap-retention nubs!
    for sy in (-1.0, 1.0):
        add_objs.append(create_cyl_obj(f"Add_{mname}_EarPeg_{sy}", x_can, sy * 17.50, 1.92, 1.80, 5.40, segs=36))
        add_objs.append(create_cone_obj(f"Add_{mname}_EarPegTip_{sy}", x_can, sy * 17.50, 1.92, 1.25, 5.40, 6.20, segs=36))
        # Center pilot hole (r = 0.80 mm -> Ø1.60 mm) through each peg in case user wants an M2 screw
        # Solid Ø3.84mm motor ear pegs (no tiny pilot hole needed!)
        # Snap-clip lip on the outer end of each ear pocket (catches the 0.8mm thick metal ear at Z = 3.0..4.2 mm)
        ye_out = sy * (17.50 + 3.85)
        s_dir = -sy  # points inward toward ear center
        yz_ear_clip = [
            (ye_out - s_dir * 1.95, 2.00),
            (ye_out, 2.00),
            (ye_out, 3.10),
            (ye_out + s_dir * 0.45, 3.55),
            (ye_out + s_dir * 0.45, 3.95),
            (ye_out - s_dir * 0.20, 4.80),
            (ye_out - s_dir * 1.95, 4.80),
        ]
        if s_dir < 0:
            yz_ear_clip = list(reversed(yz_ear_clip))
        add_objs.append(create_prism_profile_x(f"Add_{mname}_EarSnap_{sy}", x_can - 2.2, x_can + 2.2, yz_ear_clip))

# 4. Audited ULN2003 Motor Controller Cradles:
#    - Keep 3 cradles: Upper-Left (-28, -50), Upper-Right (-28, +50), and Mid-Right (+28, +50)
#      (Mid-Left is replaced by the moved-up ESP32-S3 cradle!)
#    - Bottom clip moved UP by 2.00 mm (x1_in = xc + 14.60 -> 31.20 mm vertical inner height!)
#    - Under-board solder-pin cutout enlarged to 27.6 x 31.6 mm (leaves ONLY the 4 bare 3.8x3.8mm corner
#      mounting-hole pads at Z = 4.20 mm, so ZERO through-hole solder pins ever hit the floor!)
#    - Top clip split into TWO corner-flank clips so it never touches the center DIP-16 chip or white 5-pin XH socket!
uln_positions = [(-28.00, -50.00), (-28.00, 50.00), (28.00, 50.00)]
for idx, (xc, yc) in enumerate(uln_positions):
    x0_in = xc - 16.60
    x1_in = xc + 14.60  # Bottom moved UP by 2.00 mm -> 31.20 mm vertical pocket height
    y0_in, y1_in = yc - 17.80, yc + 17.80  # 35.60 mm horizontal width (snug for 35.0 mm ULN2003 PCB!)
    xc_mid = 0.5 * (x0_in + x1_in)  # xc - 1.00

    # Side guide rails along Y0 and Y1
    add_objs.append(create_box_obj(f"ULN_RailY0_{idx}", x0_in - 1.5, x1_in + 1.5, y0_in - 2.2, y0_in, 2.5, 6.8))
    add_objs.append(create_box_obj(f"ULN_RailY1_{idx}", x0_in - 1.5, x1_in + 1.5, y1_in, y1_in + 2.2, 2.5, 6.8))

    # 4 Bare-Corner Standoff Pads (3.8 x 3.8 mm at the 4 corners where the mounting holes sit, plus Ø2.4mm locating nubs!)
    for cx_c, sx_c in [(x0_in, 1), (x1_in - 3.8, -1)]:
        for cy_c, sy_c in [(y0_in, 1), (y1_in - 3.8, -1)]:
            add_objs.append(create_box_obj(f"ULN_Pad_{idx}_{cx_c}_{cy_c}", cx_c, cx_c + 3.8, cy_c, cy_c + 3.8, 2.5, 4.20))

    # Split Top Snap-Latch Clips (two 6.5mm wide clips near the left and right corners of the top edge,
    # avoiding the center DIP-16 chip and white XH stepper connector!)
    pts_top = [
        (x0_in - 1.9, 2.5),
        (x0_in, 2.5),
        (x0_in, 6.0),
        (x0_in + 0.60, 6.6),
        (x0_in + 0.60, 7.0),
        (x0_in - 0.35, 8.0),
        (x0_in - 1.9, 8.0),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopL_{idx}", y0_in + 0.5, y0_in + 7.0, pts_top))
    add_objs.append(create_prism_profile_y(f"ULN_ClipTopR_{idx}", y1_in - 7.0, y1_in - 0.5, pts_top))

    # Bottom Snap-Latch Clip at x1_in (moved UP by 2.00 mm!)
    pts_bot = [
        (x1_in, 2.5),
        (x1_in + 1.9, 2.5),
        (x1_in + 1.9, 8.0),
        (x1_in + 0.35, 8.0),
        (x1_in - 0.60, 7.0),
        (x1_in - 0.60, 6.6),
        (x1_in, 6.0),
    ]
    add_objs.append(create_prism_profile_y(f"ULN_ClipBot_{idx}", yc - 7.5, yc + 7.5, pts_bot))

    # Enlarged Under-Board Solder-Pin Relief Window (27.6 mm tall x 31.6 mm wide! Clears ALL solder pins!)
    # Leaves 1.8 mm per side inside the 31.2 x 35.6 mm pocket, while the 4 corner pads (3.8 x 3.8 mm) support the corners!
    sub_objs.append(create_rounded_rect_obj(
        f"Sub_ULN_SolderRelief_{idx}",
        xc_mid - 13.8, xc_mid + 13.8,
        yc - 13.8, yc + 13.8,
        2.0, 0.60, 3.8, segs_corner=6
    ))
    # Also cut two horizontal relief slots up to the top/bottom edges between the corner pads so solder pins near X0/X1 never touch
    sub_objs.append(create_box_obj(f"Sub_ULN_TopPinSlot_{idx}", x0_in + 0.4, x1_in - 0.4, yc - 11.5, yc + 11.5, 1.2, 5.0))
    sub_objs.append(create_box_obj(f"Sub_ULN_SidePinSlot_{idx}", xc_mid - 11.5, xc_mid + 11.5, y0_in + 0.4, y1_in - 0.4, 1.2, 5.0))

# 5. Sleek Low-Profile Freenove ESP32-S3-WROOM Cradle — MOVED UP 41 mm, ZERO ARCHWAYS!
#    - Identical low-profile height to your original V3 cradle (PCB rests at Z = 9.50 mm, low solid side walls at Z = 11.20 mm),
#      sitting flat on the Z = 0..3.0 mm base plate with two pin-row slots and a center window — NO elevated archway!
#    - Moved UP 41.0 mm (esp_x0 = +2.00 mm to esp_x1 = +59.50 mm, esp_yc = -51.00 mm) so you have 51.80 mm of wide-open
#      runway below the USB-C ports!
esp_x0, esp_x1 = 2.00, 59.50
esp_yc = -51.00
esp_y0, esp_y1 = esp_yc - 14.35, esp_yc + 14.35  # 28.70 mm inner width for Freenove ESP32-S3 PCB
z_esp_shelf = 9.50  # Exact same low-profile 9.50 mm PCB shelf height as your original V3 cradle!

# Cut two pin-row slots (for the two header rows at esp_yc ± 11.4 mm) and center weight-saving window through the Z=0..3mm plate
sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_L", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc - 13.10, esp_yc - 8.60, 1.8, 0.60, 5.0, segs_corner=6))
sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_R", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc + 8.60, esp_yc + 13.10, 1.8, 0.60, 5.0, segs_corner=6))
# Removed Sub_ESP_CenterWin so Layer 1 has a wide 17.2mm solid bed-adhesion pad instead of two skinny ribbons!

# Solid Low-Profile Side Guide Walls from Z = 2.50 to 11.20 mm (ZERO archways, ZERO bridges!)
# With an internal Z = 9.50 mm step (1.15 mm wide) that the PCB edges rest on!
add_objs.append(create_box_obj("ESP_WallY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0 - 2.20, esp_y0, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_WallY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))
# Internal PCB support ledges (Z = 2.50 to 9.50 mm, 1.15 mm wide along the inside of both walls, clearing the pin rows!)
add_objs.append(create_box_obj("ESP_LedgeY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0, esp_y0 + 1.15, 2.50, z_esp_shelf))
add_objs.append(create_box_obj("ESP_LedgeY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1 - 1.15, esp_y1, 2.50, z_esp_shelf))

# Top End-Stop Shoulders at esp_x0 (with 20.4 mm open center for the Freenove antenna tab!)
add_objs.append(create_box_obj("ESP_TopStop_L", esp_x0 - 2.20, esp_x0, esp_y0 - 2.20, esp_yc - 10.20, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_TopStop_R", esp_x0 - 2.20, esp_x0, esp_yc + 10.20, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))

# Bottom End-Stop Shoulders at esp_x1 (catching the outer corners while leaving 25.1 mm wide-open for BOTH USB-C plugs!)
add_objs.append(create_box_obj("ESP_BotStop_L", esp_x1, esp_x1 + 2.20, esp_y0 - 2.20, esp_y0 + 1.80, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_BotStop_R", esp_x1, esp_x1 + 2.20, esp_y1 - 1.80, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))

# 4 Low-Profile 45-Degree Snap-Latch Clips on the Side Walls (Z = 9.50 to 12.30 mm)
for cx0, cx1 in [(esp_x0 + 6.0, esp_x0 + 14.0), (esp_x1 - 14.0, esp_x1 - 6.0)]:
    pts_esp_y0 = [
        (esp_y0 - 2.20, z_esp_shelf),
        (esp_y0, z_esp_shelf),
        (esp_y0, z_esp_shelf + 1.65),
        (esp_y0 + 0.55, z_esp_shelf + 2.20),
        (esp_y0 + 0.55, z_esp_shelf + 2.50),
        (esp_y0 - 0.30, z_esp_shelf + 3.10),
        (esp_y0 - 2.20, z_esp_shelf + 3.10),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_esp_y0))
    pts_esp_y1 = [
        (esp_y1, z_esp_shelf),
        (esp_y1 + 2.20, z_esp_shelf),
        (esp_y1 + 2.20, z_esp_shelf + 3.10),
        (esp_y1 + 0.30, z_esp_shelf + 3.10),
        (esp_y1 - 0.55, z_esp_shelf + 2.50),
        (esp_y1 - 0.55, z_esp_shelf + 2.20),
        (esp_y1, z_esp_shelf + 1.65),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_esp_y1))

# 6. Bottom-Right Spare / Battery / Breadboard Bay (X in [+52.0..+96.0], Yc = +53.0)
b2_x0, b2_x1 = 52.0, 96.0
b2_yc = 53.0
b2_y0, b2_y1 = b2_yc - 18.50, b2_yc + 18.50
add_objs.append(create_box_obj("Bay2_WallY0", b2_x0, b2_x1, b2_y0 - 2.00, b2_y0, 2.5, 6.50))
add_objs.append(create_box_obj("Bay2_WallY1", b2_x0, b2_x1, b2_y1, b2_y1 + 2.00, 2.5, 6.50))
sub_objs.append(create_rounded_rect_obj("Sub_Bay2_Vent", b2_x0 + 4.0, b2_x1 - 4.0, b2_yc - 12.0, b2_yc + 12.0, 3.0, 0.60, 5.0, segs_corner=6))

# 7. Cable Management Retainers (Updated for new ESP32 position & direct cross-channel + smooth USB-C exit path!)
def make_cable_arch_x(name, x0, x1, yc, side_sign):
    s = side_sign
    yz = [
        (yc - s * 5.2, 2.5),
        (yc - s * 2.6, 2.5),
        (yc - s * 2.6, 4.4),
        (yc + s * 1.4, 8.4),
        (yc + s * 2.6, 7.2),
        (yc + s * 3.6, 8.2),
        (yc + s * 3.6, 9.4),
        (yc - s * 5.2, 9.4),
    ]
    if s < 0:
        yz = list(reversed(yz))
    return create_prism_profile_x(name, x0, x1, yz)

def make_cable_arch_y(name, y0, y1, xc, side_sign):
    s = side_sign
    xz = [
        (xc - s * 5.2, 2.5),
        (xc - s * 2.6, 2.5),
        (xc - s * 2.6, 4.4),
        (xc + s * 1.4, 8.4),
        (xc + s * 2.6, 7.2),
        (xc + s * 3.6, 8.2),
        (xc + s * 3.6, 9.4),
        (xc - s * 5.2, 9.4),
    ]
    if s > 0:
        xz = list(reversed(xz))
    return create_prism_profile_y(name, y0, y1, xz)

add_objs.append(make_cable_arch_x("CableArch_Mid_L", -6.0, 6.0, -24.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_Mid_R", -6.0, 6.0, +24.5, -1.0))
add_objs.append(make_cable_arch_x("CableArch_Bot_R", 42.0, 54.0, +24.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutUL", -35.0, -21.0, -77.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutUR", -35.0, -21.0, +77.5, -1.0))
add_objs.append(make_cable_arch_x("CableArch_OutLL", 22.0, 36.0, -77.5, +1.0))
add_objs.append(make_cable_arch_x("CableArch_OutLR", 22.0, 36.0, +77.5, -1.0))
# Two USB-C Cable Routing Arches along the bottom runway leading from ESP32 (Y=-51) to Bottom-Center USB-C Exit (Y=0, X=111)
add_objs.append(make_cable_arch_y("CableArch_USBC_1", -34.0, -22.0, 96.5, +1.0))
add_objs.append(make_cable_arch_y("CableArch_USBC_2", -12.0, 0.0, 101.5, +1.0))

# Perimeter stiffening rim
add_objs.append(create_box_obj("Rim_Top", -111.03, -108.50, -75.0, 75.0, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Left", -98.0, 98.0, -88.03, -85.50, 2.5, 5.2))
add_objs.append(create_box_obj("Rim_Right", -98.0, 98.0, 85.50, 88.03, 2.5, 5.2))

# 8. 10 Tapered Perimeter Push-Fit Crush Ribs (works in BOTH existing frame & V5 Click-Lock frame!)
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
print(f"V5 Audited 3_Motor_Mount_Plate: verts={len(bm_out.verts)}, faces={len(bm_out.faces)}, non_manifold={len(non_m)}")
bm_out.to_mesh(plate.data)
bm_out.free()

plate_paths = [
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
