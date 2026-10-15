import bpy
import math
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.engine = "BLENDER_EEVEE"
scn.eevee.taa_render_samples = 16
scn.render.resolution_x = 920
scn.render.resolution_y = 880

world = bpy.data.worlds.new("StudioWorld")
scn.world = world
bg_node = world.node_tree.nodes.get("Background")
bg_node.inputs[0].default_value = (0.055, 0.060, 0.070, 1.0)
bg_node.inputs[1].default_value = 0.55

def make_mat(name, rgba, rough=0.45, metal=0.0):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

mat_frame_white = make_mat("FrameMatteWhite", (0.90, 0.89, 0.86, 1.0), rough=0.55)
mat_dial_white  = make_mat("DialMatteWhite",  (0.96, 0.95, 0.92, 1.0), rough=0.50)
mat_dial_black  = make_mat("DialMatteBlack",  (0.04, 0.04, 0.05, 1.0), rough=0.45)
mat_mp_orange   = make_mat("MotorPlateOrange",(0.92, 0.35, 0.08, 1.0), rough=0.45)
mat_hand_orange = make_mat("HandBraunOrange", (0.96, 0.28, 0.04, 1.0), rough=0.38)
mat_cover_white = make_mat("CoverTransWhite", (0.86, 0.89, 0.92, 1.0), rough=0.35)
mat_steel       = make_mat("MotorSteel",      (0.78, 0.80, 0.84, 1.0), rough=0.25, metal=0.85)
mat_brass       = make_mat("MotorBrass",      (0.88, 0.70, 0.24, 1.0), rough=0.28, metal=0.80)
mat_blue_plast  = make_mat("MotorBluePlast",  (0.14, 0.42, 0.88, 1.0), rough=0.40)
mat_pcb_green   = make_mat("PCBGreen",        (0.06, 0.42, 0.24, 1.0), rough=0.38)
mat_pcb_dark    = make_mat("PCBDark",         (0.10, 0.12, 0.16, 1.0), rough=0.35)
mat_ic_black    = make_mat("ICBlack",         (0.05, 0.05, 0.06, 1.0), rough=0.50)
mat_jst_white   = make_mat("JSTWhite",        (0.94, 0.94, 0.92, 1.0), rough=0.40)

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
root = bpy.context.active_object
root.name = "Clock_Root"

def import_stl_part(path, name, mat, parent=root, loc=(0,0,0), rot=(0,0,0)):
    bpy.ops.wm.stl_import(filepath=path)
    obj = bpy.context.selected_objects[0]
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    obj.parent = parent
    obj.location = loc
    obj.rotation_euler = rot
    return obj

f_obj = import_stl_part(
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "1_Outer_Frame",
    mat_frame_white,
    loc=(0, 0, 0),
)

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 6.40), rotation=(math.pi, 0, 0))
dial_grp = bpy.context.active_object
dial_grp.name = "2_Dial_Group"
dial_grp.parent = root
import_stl_part("/tmp/dial_base_white.stl", "2a_Dial_White", mat_dial_white, parent=dial_grp)
import_stl_part("/tmp/dial_text_black.stl", "2b_Dial_Black", mat_dial_black, parent=dial_grp)

mp_obj = import_stl_part(
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
    "3_Motor_Mount_Plate",
    mat_mp_orange,
    loc=(0, 0, 6.50),
)

bc_obj = import_stl_part(
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl",
    "4_Back_Cover",
    mat_cover_white,
    loc=(0, 0, 49.00),
)

# Hands (Part 0 & Part 2 have closed sculpted crown cap at +Z_hand; so we keep +Z_hand pointing toward -Z_frame!)
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(-25.30, 0.0, 3.85), rotation=(0, 0, 0))
up_piv = bpy.context.active_object
up_piv.parent = root
import_stl_part("/tmp/hand_upper_centered.stl", "5a_Upper_Hand", mat_hand_orange, parent=up_piv, loc=(0,0,0), rot=(math.pi, 0, -0.5*math.pi))

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(78.20, 0.0, 3.85), rotation=(0, 0, 0))
lo_piv = bpy.context.active_object
lo_piv.parent = root
import_stl_part("/tmp/hand_lower_centered.stl", "5b_Lower_Hand", mat_hand_orange, parent=lo_piv, loc=(0,0,0), rot=(math.pi, 0, -0.5*math.pi))

up_piv.rotation_euler = (0, 0, math.radians(60.0))
lo_piv.rotation_euler = (0, 0, math.radians(45.0))

def build_stepper_28byj48(name, x_can, x_shaft, z_seat=11.50):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(x_can, 0, z_seat))
    grp = bpy.context.active_object
    grp.name = name
    grp.parent = root
    dx_s = x_shaft - x_can
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=14.0, depth=19.0, location=(0, 0, 9.5))
    can = bpy.context.active_object
    can.data.materials.append(mat_steel)
    can.parent = grp
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.4))
    ears = bpy.context.active_object
    ears.scale = (7.0, 42.0, 0.8)
    ears.data.materials.append(mat_steel)
    ears.parent = grp
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=4.5, depth=3.0, location=(dx_s, 0, -1.5))
    boss = bpy.context.active_object
    boss.data.materials.append(mat_brass)
    boss.parent = grp
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=2.5, depth=10.5, location=(dx_s, 0, -5.25))
    sh = bpy.context.active_object
    sh.data.materials.append(mat_steel)
    sh.parent = grp
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-dx_s * 1.45, 0, 8.0))
    chute = bpy.context.active_object
    chute.scale = (8.0, 14.6, 15.0)
    chute.data.materials.append(mat_blue_plast)
    chute.parent = grp
    return grp

m_up = build_stepper_28byj48("Motor_Upper", -17.30, -25.30, 11.50)
m_lo = build_stepper_28byj48("Motor_Lower",  70.20,  78.20, 11.50)

# Build ULN2003 Driver Boards in the two cradles: (-28.0, -50.0) and (28.0, -50.0) or (-28.0, +50.0)
def build_uln2003(name, xc, yc, z_seat=10.70):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(xc, yc, z_seat))
    grp = bpy.context.active_object
    grp.name = name
    grp.parent = root
    # Green PCB (31 x 35 x 1.6 mm)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.8))
    pcb = bpy.context.active_object
    pcb.scale = (31.0, 35.0, 1.6)
    pcb.data.materials.append(mat_pcb_green)
    pcb.parent = grp
    # Black ULN2003A DIP-16 IC chip in center
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2.8))
    ic = bpy.context.active_object
    ic.scale = (19.0, 7.0, 2.5)
    ic.data.materials.append(mat_ic_black)
    ic.parent = grp
    # White 5-pin JST motor socket
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -11.5, 4.5))
    jst = bpy.context.active_object
    jst.scale = (14.5, 5.5, 6.0)
    jst.data.materials.append(mat_jst_white)
    jst.parent = grp
    # 4-pin IN1-IN4 header pins (brass)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-4.0, 12.5, 4.5))
    hdr = bpy.context.active_object
    hdr.scale = (11.0, 2.5, 6.0)
    hdr.data.materials.append(mat_brass)
    hdr.parent = grp
    return grp

uln_up = build_uln2003("ULN2003_Upper", -28.0, -50.0, 10.70)
uln_lo = build_uln2003("ULN2003_Lower",  28.0,  50.0, 10.70)

# Build ESP32-S3 Board in bottom-left cradle (Xc = 74.0, Yc = -53.0, Z = 16.0)
def build_esp32(name, xc=74.0, yc=-53.0, z_seat=16.0):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(xc, yc, z_seat))
    grp = bpy.context.active_object
    grp.name = name
    grp.parent = root
    # Dark PCB (52 x 28 x 1.6 mm)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.8))
    pcb = bpy.context.active_object
    pcb.scale = (52.0, 28.0, 1.6)
    pcb.data.materials.append(mat_pcb_dark)
    pcb.parent = grp
    # Silver RF Shield module near top (-X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-10.0, 0, 2.8))
    rf = bpy.context.active_object
    rf.scale = (18.0, 18.0, 2.6)
    rf.data.materials.append(mat_steel)
    rf.parent = grp
    # USB-C port at bottom (+X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(24.0, 0, 2.6))
    usbc = bpy.context.active_object
    usbc.scale = (7.5, 9.0, 3.2)
    usbc.data.materials.append(mat_steel)
    usbc.parent = grp
    # Two rows of gold header pins
    for sy in (-12.0, 12.0):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, sy, 0.0))
        pins = bpy.context.active_object
        pins.scale = (46.0, 2.2, 6.0)
        pins.data.materials.append(mat_brass)
        pins.parent = grp
    return grp

esp_obj = build_esp32("ESP32_S3")

mat_upright = mathutils.Matrix((
    ( 0.0, -1.0,  0.0, 0.0),
    ( 0.0,  0.0,  1.0, 0.0),
    (-1.0,  0.0,  0.0, 0.0),
    ( 0.0,  0.0,  0.0, 1.0),
))
root.matrix_world = mat_upright

def add_sun(name, dir_vec, energy, angle_deg=12.0, color=(1.0, 0.98, 0.95)):
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 0))
    lt = bpy.context.active_object
    lt.name = name
    lt.data.energy = energy
    lt.data.angle = math.radians(angle_deg)
    lt.data.color = color
    lt.rotation_euler = mathutils.Vector(dir_vec).to_track_quat("-Z", "Y").to_euler()
    return lt

add_sun("SunKeyFront", ( 0.45,  0.85, -0.55), 3.4, angle_deg=10.0)
add_sun("SunFillFront",(-0.55,  0.80, -0.25), 1.4, angle_deg=25.0, color=(0.90, 0.95, 1.0))
add_sun("SunKeyRear",  ( 0.45, -0.85, -0.55), 3.2, angle_deg=10.0)
add_sun("SunFillRear", (-0.55, -0.80, -0.25), 1.5, angle_deg=25.0, color=(0.90, 0.95, 1.0))

bpy.ops.object.camera_add(location=(20, -430, 10))
cam = bpy.context.active_object
scn.camera = cam
cam.data.lens = 58.0
direction = mathutils.Vector((0, 0, 0)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

scn.render.filepath = "/tmp/test_front.png"
bpy.ops.render.render(write_still=True)

bc_obj.hide_render = True
cam.location = (-110, 410, 90)
direction = mathutils.Vector((0, 15, 0)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scn.render.filepath = "/tmp/test_rear.png"
bpy.ops.render.render(write_still=True)
print("Done")
