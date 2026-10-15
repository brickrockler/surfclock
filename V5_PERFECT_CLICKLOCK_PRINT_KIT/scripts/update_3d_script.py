with open("/Users/jcolley/surf_clock/render_real_3d_stl_chapters.py", "r") as f:
    code = f.read()

# 1. Enable GTAO and tune studio lighting + world exposure so white frame never blows out
old_world = '''# World background: Warm Architectural Alabaster / Stone (#E6E2D8 -> linear ~0.78, 0.75, 0.68)
world = bpy.data.worlds.new("StudioWorld")
scn.world = world
bg_node = world.node_tree.nodes.get("Background")
bg_node.inputs[0].default_value = (0.78, 0.75, 0.68, 1.0)
bg_node.inputs[1].default_value = 0.92'''

new_world = '''scn.eevee.use_gtao = True
scn.eevee.gtao_distance = 22.0
scn.eevee.gtao_factor = 0.95

# World background: Warm Architectural Stone (#D8D3C6)
world = bpy.data.worlds.new("StudioWorld")
scn.world = world
bg_node = world.node_tree.nodes.get("Background")
bg_node.inputs[0].default_value = (0.64, 0.61, 0.55, 1.0)
bg_node.inputs[1].default_value = 0.58'''

assert old_world in code, "old_world not found"
code = code.replace(old_world, new_world, 1)

# Tune materials so white frame & dial have distinct sculptural shading and never clip to 255
old_mats = '''mat_frame_white = make_mat("FrameMatteWhite", (0.95, 0.94, 0.91, 1.0), rough=0.58)
mat_dial_white  = make_mat("DialMatteWhite",  (0.97, 0.96, 0.93, 1.0), rough=0.52)
mat_dial_black  = make_mat("DialMatteBlack",  (0.03, 0.03, 0.035, 1.0), rough=0.45)
mat_mp_orange   = make_mat("MotorPlateOrange",(0.95, 0.24, 0.02, 1.0), rough=0.48)
mat_hand_orange = make_mat("HandBraunOrange", (0.98, 0.22, 0.01, 1.0), rough=0.38)
mat_cover_white = make_mat("CoverTransWhite", (0.89, 0.91, 0.93, 1.0), rough=0.40)
mat_steel       = make_mat("MotorSteel",      (0.76, 0.79, 0.83, 1.0), rough=0.28, metal=0.82)
mat_brass       = make_mat("MotorBrass",      (0.88, 0.68, 0.20, 1.0), rough=0.30, metal=0.78)
mat_blue_plast  = make_mat("MotorBluePlast",  (0.10, 0.38, 0.85, 1.0), rough=0.42)
mat_pcb_green   = make_mat("PCBGreen",        (0.05, 0.36, 0.20, 1.0), rough=0.40)
mat_pcb_dark    = make_mat("PCBDark",         (0.08, 0.09, 0.12, 1.0), rough=0.38)
mat_ic_black    = make_mat("ICBlack",         (0.04, 0.04, 0.05, 1.0), rough=0.50)
mat_jst_white   = make_mat("JSTWhite",        (0.95, 0.95, 0.93, 1.0), rough=0.42)
mat_table       = make_mat("StudioTable",     (0.76, 0.73, 0.66, 1.0), rough=0.82)'''

new_mats = '''mat_frame_white = make_mat("FrameMatteWhite", (0.83, 0.82, 0.79, 1.0), rough=0.62)
mat_dial_white  = make_mat("DialMatteWhite",  (0.87, 0.86, 0.83, 1.0), rough=0.56)
mat_dial_black  = make_mat("DialMatteBlack",  (0.025, 0.025, 0.03, 1.0), rough=0.45)
mat_mp_orange   = make_mat("MotorPlateOrange",(0.86, 0.22, 0.02, 1.0), rough=0.52)
mat_hand_orange = make_mat("HandBraunOrange", (0.94, 0.20, 0.01, 1.0), rough=0.38)
mat_cover_white = make_mat("CoverTransWhite", (0.78, 0.81, 0.84, 1.0), rough=0.42)
mat_steel       = make_mat("MotorSteel",      (0.70, 0.73, 0.77, 1.0), rough=0.32, metal=0.75)
mat_brass       = make_mat("MotorBrass",      (0.84, 0.64, 0.18, 1.0), rough=0.32, metal=0.75)
mat_blue_plast  = make_mat("MotorBluePlast",  (0.08, 0.34, 0.78, 1.0), rough=0.42)
mat_pcb_green   = make_mat("PCBGreen",        (0.04, 0.32, 0.18, 1.0), rough=0.42)
mat_pcb_dark    = make_mat("PCBDark",         (0.07, 0.08, 0.11, 1.0), rough=0.40)
mat_ic_black    = make_mat("ICBlack",         (0.03, 0.03, 0.04, 1.0), rough=0.50)
mat_jst_white   = make_mat("JSTWhite",        (0.88, 0.88, 0.86, 1.0), rough=0.45)
mat_table       = make_mat("StudioTable",     (0.56, 0.53, 0.47, 1.0), rough=0.85)'''

assert old_mats in code, "old_mats not found"
code = code.replace(old_mats, new_mats, 1)

# 2. Replace Dial Base with a pure, ghost-free bmesh plate with 2 circular shaft holes at (-25.3, 0) and (78.2, 0)
old_dial = '''import_stl_part("/tmp/dial_base_white.stl", "2a_Dial_White", mat_dial_white, parent=dial_grp)
import_stl_part("/tmp/dial_ticks_pure.stl", "2b_Dial_Black", mat_dial_black, parent=dial_grp)

for sx0, sx1 in [(-110.8, -32.0), (-18.0, 71.0), (85.0, 110.8)]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.5*(sx0+sx1), 0.0, 1.18))
    sl = bpy.context.active_object
    sl.scale = (sx1 - sx0, 175.6, 2.36)
    sl.data.materials.append(mat_dial_white)
    sl.parent = dial_grp'''

new_dial = '''import_stl_part("/tmp/dial_ticks_pure.stl", "2b_Dial_Black", mat_dial_black, parent=dial_grp)

# Build a 100% smooth, ghost-free matte white Dial Plate (221.6 x 175.6 x 2.40 mm) with two shaft clearances
for sx0, sx1, sy0, sy1 in [
    (-110.8, -30.5, -87.8, 87.8),
    (-20.1,   73.0, -87.8, 87.8),
    ( 83.4,  110.8, -87.8, 87.8),
    (-30.5,  -20.1, -87.8, -5.2),
    (-30.5,  -20.1,   5.2, 87.8),
    ( 73.0,   83.4, -87.8, -5.2),
    ( 73.0,   83.4,   5.2, 87.8),
]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.5*(sx0+sx1), 0.5*(sy0+sy1), 1.20))
    sl = bpy.context.active_object
    sl.scale = (sx1 - sx0, sy1 - sy0, 2.40)
    sl.data.materials.append(mat_dial_white)
    sl.parent = dial_grp'''

assert old_dial in code, "old_dial not found"
code = code.replace(old_dial, new_dial, 1)

# 3. Route Lower ULN2003 wires cleanly down the right spine (Y=+25.5) and across the bottom solid bridge (X=96.5) through the bottom C-clip so zero wires ever touch the lower motor or cross the middle window!
old_wires = '''# 3) Lower IN1-IN4 -> GPIO 15, 16, 17, 18 (parallel orthogonal ribbon along Y=+23.5 spine -> X=48 cross-rib -> ESP32!)
w_lo_sig1 = make_ortho_wire("W_Lo_Sig1", [
    (39.5, 45.0, 14.5),
    (48.0, 45.0, 11.5),
    (48.0, 23.5, 11.5),
    (48.0, -26.6, 11.5),
    (74.0, -26.6, 11.5),
    (74.0, -41.0, 16.8),
], mat_w_amber, radius=0.82)

w_lo_sig2 = make_ortho_wire("W_Lo_Sig2", [
    (39.5, 47.5, 14.5),
    (50.2, 47.5, 11.5),
    (50.2, 25.0, 11.5),
    (50.2, -28.4, 11.5),
    (78.0, -28.4, 11.5),
    (78.0, -41.0, 16.8),
], mat_w_orange, radius=0.82)

# 4) 5V VBUS (Red) & GND (Dark Slate) orthogonal power bus along the spine
w_pwr_5v = make_ortho_wire("W_Pwr_5V", [
    (-16.5, -51.0, 14.5),
    (2.2, -51.0, 11.2),
    (2.2, -21.2, 11.2),
    (86.0, -21.2, 11.2),
    (86.0, -41.0, 16.8),
    (86.0, -21.2, 11.2),
    (52.4, -21.2, 11.2),
    (52.4, 51.0, 11.2),
    (39.5, 51.0, 14.5),
], mat_w_red, radius=0.85)

w_pwr_gnd = make_ortho_wire("W_Pwr_GND", [
    (-16.5, -53.2, 14.5),
    (4.0, -53.2, 11.0),
    (4.0, -19.5, 11.0),
    (90.0, -19.5, 11.0),
    (90.0, -41.0, 16.8),
    (90.0, -19.5, 11.0),
    (54.2, -19.5, 11.0),
    (54.2, 53.2, 11.0),
    (39.5, 53.2, 14.5),
], mat_w_gnd, radius=0.85)'''

new_wires = '''# 3) Lower IN1-IN4 -> GPIO 15, 16, 17, 18 (routed along right spine Y=+25.5 through C-clip -> bottom solid bridge X=95.5 -> ESP32!)
w_lo_sig1 = make_ortho_wire("W_Lo_Sig1", [
    (39.5, 45.0, 14.5),
    (48.5, 45.0, 11.5),
    (48.5, 24.5, 11.5),
    (94.5, 24.5, 11.5),
    (94.5, -26.5, 11.5),
    (74.0, -26.5, 11.5),
    (74.0, -41.0, 16.8),
], mat_w_amber, radius=0.82)

w_lo_sig2 = make_ortho_wire("W_Lo_Sig2", [
    (39.5, 47.5, 14.5),
    (50.5, 47.5, 11.5),
    (50.5, 26.2, 11.5),
    (96.2, 26.2, 11.5),
    (96.2, -28.2, 11.5),
    (78.0, -28.2, 11.5),
    (78.0, -41.0, 16.8),
], mat_w_orange, radius=0.82)

# 4) 5V VBUS (Red) & GND (Dark Slate) orthogonal power bus along left spine -> ESP32 -> bottom bridge -> right spine!
w_pwr_5v = make_ortho_wire("W_Pwr_5V", [
    (-16.5, -51.0, 14.5),
    (2.2, -51.0, 11.2),
    (2.2, -21.2, 11.2),
    (86.0, -21.2, 11.2),
    (86.0, -41.0, 16.8),
    (86.0, -21.2, 11.2),
    (97.8, -21.2, 11.2),
    (97.8, 28.0, 11.2),
    (52.5, 28.0, 11.2),
    (52.5, 51.0, 11.2),
    (39.5, 51.0, 14.5),
], mat_w_red, radius=0.85)

w_pwr_gnd = make_ortho_wire("W_Pwr_GND", [
    (-16.5, -53.2, 14.5),
    (4.0, -53.2, 11.0),
    (4.0, -19.5, 11.0),
    (90.0, -19.5, 11.0),
    (90.0, -41.0, 16.8),
    (90.0, -19.5, 11.0),
    (99.5, -19.5, 11.0),
    (99.5, 29.8, 11.0),
    (54.5, 29.8, 11.0),
    (54.5, 53.2, 11.0),
    (39.5, 53.2, 14.5),
], mat_w_gnd, radius=0.85)'''

assert old_wires in code, "old_wires not found"
code = code.replace(old_wires, new_wires, 1)

# 4. Tune Sun light energies so whites are creamy architectural off-white (#ECEAE2) with crisp bevel contrast
old_lights = '''add_sun("SunKey1",   ( 0.38,  0.55, -0.82), 2.1, angle_deg=1.5, cast_shadow=True)
add_sun("SunFill1",  (-0.55,  0.45, -0.65), 1.15, color=(0.96, 0.98, 1.0), cast_shadow=False)
add_sun("SunRim1",   ( 0.15, -0.75, -0.65), 0.95, color=(1.0, 0.98, 0.95), cast_shadow=False)
add_sun("SunBounce", ( 0.0,   0.20,  0.90), 0.45, color=(0.95, 0.94, 0.90), cast_shadow=False)'''

new_lights = '''add_sun("SunKey1",   ( 0.42,  0.58, -0.78), 1.35, angle_deg=1.5, cast_shadow=True)
add_sun("SunFill1",  (-0.60,  0.45, -0.60), 0.65, color=(0.94, 0.97, 1.0), cast_shadow=False)
add_sun("SunRim1",   ( 0.20, -0.78, -0.58), 0.55, color=(1.0, 0.97, 0.92), cast_shadow=False)
add_sun("SunBounce", ( 0.0,   0.20,  0.90), 0.25, color=(0.92, 0.90, 0.86), cast_shadow=False)'''

assert old_lights in code, "old_lights not found"
code = code.replace(old_lights, new_lights, 1)

with open("/Users/jcolley/surf_clock/render_real_3d_stl_chapters.py", "w") as f:
    f.write(code)
print("Updated render_real_3d_stl_chapters.py")
