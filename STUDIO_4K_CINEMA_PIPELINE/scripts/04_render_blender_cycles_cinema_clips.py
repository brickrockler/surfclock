import bpy, bmesh, os, math, subprocess, shutil
from mathutils import Vector, Euler, Matrix

PROJECT_DIR = "/Users/jcolley/surf_clock"
PIPELINE_DIR = os.path.join(PROJECT_DIR, "STUDIO_4K_CINEMA_PIPELINE")
CYCLES_RAW_DIR = os.path.join(PIPELINE_DIR, "raw_renders", "cycles_sequences")
OUT_16x9_DIR = os.path.join(PIPELINE_DIR, "02_INDIVIDUAL_4K_CLIPS_16x9")
OUT_9x16_DIR = os.path.join(PIPELINE_DIR, "03_INDIVIDUAL_4K_CLIPS_9x16")
FFMPEG = "/Users/jcolley/.gemini/jetski/bin/ffmpeg"

os.makedirs(CYCLES_RAW_DIR, exist_ok=True)
os.makedirs(OUT_16x9_DIR, exist_ok=True)
os.makedirs(OUT_9x16_DIR, exist_ok=True)

BLEND_IN = os.path.join(PROJECT_DIR, "SurfClock_V23_ActualPhysicalTypeface_Master.blend")
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

scn = bpy.context.scene
scn.frame_set(360)
scn.render.engine = 'CYCLES'
scn.cycles.device = 'GPU'
scn.render.use_persistent_data = True
scn.cycles.samples = 48
if hasattr(scn.cycles, "denoising_use_gpu"):
    scn.cycles.denoising_use_gpu = True
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.cycles.transmission_bounces = 10
scn.cycles.transparent_max_bounces = 10
scn.render.image_settings.file_format = 'JPEG'
scn.render.image_settings.quality = 96
scn.view_settings.view_transform = 'AgX'
scn.view_settings.look = 'AgX - Medium High Contrast'
scn.view_settings.exposure = 0.15

try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'
    if hasattr(prefs, 'metalrt'):
        prefs.metalrt = 'ON'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = (d.type == 'METAL')
except Exception:
    pass

KEEP_HERO = {
    "SurfClock_Master_60fps_Rig_bezel",
    "SurfClock_Master_60fps_Rig_dial_v2_flush",
    "Dial_Shadow_Moat_Backer",
    "CAD_Detail_01_Braun_Typography",
    "SurfClock_Master_60fps_Rig_beach_hand",
    "SurfClock_Master_60fps_Rig_cond_hand",
}
for o in bpy.data.objects:
    o.animation_data_clear()
    o.delta_location = Vector((0, 0, 0))
    o.delta_rotation_euler = Euler((0, 0, 0), 'XYZ')
    o.delta_scale = Vector((1, 1, 1))
    if o.type in ('MESH', 'CURVE', 'SURFACE', 'FONT'):
        hide = (o.name not in KEEP_HERO)
        o.hide_render = hide
        o.hide_viewport = hide

clock_root = bpy.data.objects.get("Left_Clock_Root")
clock_root.location = Vector((0.0, 0.0, 0.0))
clock_root.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')
clock_root.scale = Vector((1.0, 1.0, 1.0))

typo = bpy.data.objects.get("CAD_Detail_01_Braun_Typography")
typo.location = Vector((0.0, 0.0, 0.0))
typo.delta_location = Vector((0.0, -0.080, 0.0))

dial = bpy.data.objects.get("SurfClock_Master_60fps_Rig_dial_v2_flush")
moat = bpy.data.objects.get("Dial_Shadow_Moat_Backer")
bh = bpy.data.objects.get("SurfClock_Master_60fps_Rig_beach_hand")
ch = bpy.data.objects.get("SurfClock_Master_60fps_Rig_cond_hand")
bezel = bpy.data.objects.get("SurfClock_Master_60fps_Rig_bezel")

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 44.0, -112.5))
hook_cutter = bpy.context.active_object
hook_cutter.name = "Rear_Hook_Hole_Cutter"
hook_cutter.scale = (14.0, 14.0, 11.0)
hook_cutter.parent = clock_root
hook_cutter.hide_render = True
hook_cutter.hide_viewport = True
bezel.modifiers.clear()
mod = bezel.modifiers.new(name="RearHookHole", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = hook_cutter

kit = "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT"
bpy.ops.wm.stl_import(filepath=os.path.join(kit, "4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl"))
back_v5 = bpy.context.selected_objects[0]
back_v5.name = "V5_Translucent_Back_With_Hook_Hole"
back_v5.parent = clock_root
back_v5.matrix_parent_inverse = Matrix.Identity(4)
back_v5.matrix_basis = Matrix((
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0, -1.0, 46.0),
    (-1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))

bpy.ops.wm.stl_import(filepath=os.path.join(kit, "NEW3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl"))
mount_v5 = bpy.context.selected_objects[0]
mount_v5.name = "V5_Internal_Motor_Mount_Plate"
mount_v5.parent = clock_root
mount_v5.matrix_parent_inverse = Matrix.Identity(4)
mount_v5.matrix_basis = Matrix((
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0, -1.0, 42.5),
    (-1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))

bpy.ops.mesh.primitive_cylinder_add(radius=14.0, depth=18.0, location=(0.0, 35.0, 25.3))
upper_motor_sil = bpy.context.active_object
upper_motor_sil.rotation_euler = (math.radians(90), 0, 0)
upper_motor_sil.parent = clock_root

bpy.ops.mesh.primitive_cylinder_add(radius=14.0, depth=18.0, location=(0.0, 35.0, -78.2))
lower_motor_sil = bpy.context.active_object
lower_motor_sil.rotation_euler = (math.radians(90), 0, 0)
lower_motor_sil.parent = clock_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 39.5, 41.0))
jst_up = bpy.context.active_object
jst_up.scale = (14.0, 6.0, 8.0)
jst_up.parent = clock_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 39.5, -62.5))
jst_lo = bpy.context.active_object
jst_lo.scale = (14.0, 6.0, 8.0)
jst_lo.parent = clock_root

if scn.world and scn.world.node_tree:
    for n in scn.world.node_tree.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Strength'].default_value = 0.02
            n.inputs['Color'].default_value = (0.010, 0.018, 0.035, 1.0)

def make_tactile_mat(name, base_rgba, rough=0.38, coat=0.18, coat_rough=0.25, sss=0.12, bump_str=0.04, bump_scale=65.0, diag_lines=False):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = base_rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Specular IOR Level"].default_value = 0.45
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = coat
        bsdf.inputs["Coat Roughness"].default_value = coat_rough
    if sss > 0 and "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = sss
        bsdf.inputs["Subsurface Scale"].default_value = 1.2

    tc = nt.nodes.new("ShaderNodeTexCoord")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = bump_scale
    noise.inputs["Detail"].default_value = 10.0
    noise.inputs["Roughness"].default_value = 0.75
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_str
    bump.inputs["Distance"].default_value = 0.12

    if diag_lines:
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Rotation"].default_value = (0.0, math.radians(45.0), 0.0)
        wv = nt.nodes.new("ShaderNodeTexWave")
        wv.wave_type = 'BANDS'
        wv.bands_direction = 'X'
        wv.inputs["Scale"].default_value = 1.8
        wv.inputs["Distortion"].default_value = 0.25
        ma = nt.nodes.new("ShaderNodeMath")
        ma.operation = 'MULTIPLY_ADD'
        ma.inputs[1].default_value = 0.35
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"])
        nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
        nt.links.new(wv.outputs["Fac"], ma.inputs[0])
        nt.links.new(noise.outputs["Fac"], ma.inputs[2])
        nt.links.new(ma.outputs["Value"], bump.inputs["Height"])
    else:
        nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
        nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

def make_frosted_back_mat():
    m = bpy.data.materials.new("Mat_V5_Frosted_Fluted_Back")
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (0.86, 0.90, 0.96, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.15
    bsdf.inputs["IOR"].default_value = 1.49
    bsdf.inputs["Alpha"].default_value = 0.62
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = 0.92
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 0.40
        bsdf.inputs["Coat Roughness"].default_value = 0.12

    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave")
    wv.wave_type = 'BANDS'
    wv.bands_direction = 'Y'
    wv.inputs["Scale"].default_value = 18.0
    wv.inputs["Distortion"].default_value = 0.15

    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 90.0
    noise.inputs["Detail"].default_value = 8.0

    ma = nt.nodes.new("ShaderNodeMath")
    ma.operation = 'MULTIPLY_ADD'
    ma.inputs[1].default_value = 0.75

    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.32
    bump.inputs["Distance"].default_value = 0.40

    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], ma.inputs[0])
    nt.links.new(noise.outputs["Fac"], ma.inputs[2])
    nt.links.new(ma.outputs["Value"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

PALETTES = {
    "HERO_DARK_BLUE": {
        "bezel": (0.016, 0.032, 0.078, 1.0),
        "dial":  (0.018, 0.036, 0.086, 1.0),
        "moat":  (0.005, 0.010, 0.025, 1.0),
        "typo":  (0.88,  0.87,  0.84,  1.0),
        "hands": (0.68,  0.28,  0.032, 1.0),
    },
    "CHALK_WHITE": {
        "bezel": (0.84,  0.82,  0.78,  1.0),
        "dial":  (0.86,  0.84,  0.80,  1.0),
        "moat":  (0.18,  0.17,  0.16,  1.0),
        "typo":  (0.025, 0.025, 0.028, 1.0),
        "hands": (0.72,  0.22,  0.025, 1.0),
    },
    "OCHRE_WHITE_DUOTONE": {
        "bezel": (0.58,  0.22,  0.028, 1.0),
        "dial":  (0.85,  0.83,  0.79,  1.0),
        "moat":  (0.15,  0.06,  0.01,  1.0),
        "typo":  (0.025, 0.025, 0.028, 1.0),
        "hands": (0.62,  0.22,  0.028, 1.0),
    },
    "ALL_OCHRE_MONO": {
        "bezel": (0.56,  0.21,  0.026, 1.0),
        "dial":  (0.60,  0.24,  0.030, 1.0),
        "moat":  (0.16,  0.05,  0.008, 1.0),
        "typo":  (0.90,  0.88,  0.84,  1.0),
        "hands": (0.016, 0.032, 0.078, 1.0),
    },
}

mat_bezel = make_tactile_mat("DynBezel", PALETTES["HERO_DARK_BLUE"]["bezel"], rough=0.38, coat=0.22, bump_str=0.055, bump_scale=75.0)
mat_dial  = make_tactile_mat("DynDial",  PALETTES["HERO_DARK_BLUE"]["dial"],  rough=0.42, coat=0.16, bump_str=0.045, bump_scale=65.0, diag_lines=True)
mat_moat  = make_tactile_mat("DynMoat",  PALETTES["HERO_DARK_BLUE"]["moat"],  rough=0.55, coat=0.0,  bump_str=0.02)
mat_typo  = make_tactile_mat("DynTypo",  PALETTES["HERO_DARK_BLUE"]["typo"],  rough=0.28, coat=0.25, sss=0.18, bump_str=0.025)
mat_hands = make_tactile_mat("DynHands", PALETTES["HERO_DARK_BLUE"]["hands"], rough=0.26, coat=0.38, sss=0.15, bump_str=0.025)
mat_metal = make_tactile_mat("DynMetal", (0.32, 0.34, 0.38, 1.0), rough=0.35, coat=0.20, bump_str=0.01)
mat_white_jst = make_tactile_mat("DynJST", (0.88, 0.87, 0.84, 1.0), rough=0.30, coat=0.15, bump_str=0.01)
mat_frosted_back = make_frosted_back_mat()

bezel.data.materials.clear(); bezel.data.materials.append(mat_bezel)
dial.data.materials.clear();  dial.data.materials.append(mat_dial)
moat.data.materials.clear();  moat.data.materials.append(mat_moat)
typo.data.materials.clear();  typo.data.materials.append(mat_typo)
bh.data.materials.clear();    bh.data.materials.append(mat_hands)
ch.data.materials.clear();    ch.data.materials.append(mat_hands)
mount_v5.data.materials.clear(); mount_v5.data.materials.append(mat_bezel)
upper_motor_sil.data.materials.append(mat_metal)
lower_motor_sil.data.materials.append(mat_metal)
jst_up.data.materials.append(mat_white_jst)
jst_lo.data.materials.append(mat_white_jst)
back_v5.data.materials.clear(); back_v5.data.materials.append(mat_frosted_back)

def apply_palette(pal_name):
    p = PALETTES[pal_name]
    for mat, key in [(mat_bezel, "bezel"), (mat_dial, "dial"), (mat_moat, "moat"), (mat_typo, "typo"), (mat_hands, "hands")]:
        bsdf = [n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
        bsdf.inputs["Base Color"].default_value = p[key]

cyc_mesh = bpy.data.meshes.new("Hero_Blue_Cyclorama")
cyc_obj = bpy.data.objects.new("Hero_Blue_Cyclorama", cyc_mesh)
bpy.context.collection.objects.link(cyc_obj)

bm = bmesh.new()
R_cove = 210.0
cy_cove = 420.0 - R_cove
cz_cove = -115.0 + R_cove
profile_pts = []
for i in range(40):
    y = -1500.0 + (cy_cove - (-1500.0)) * (i / 39.0)
    profile_pts.append((y, -115.0))
for i in range(1, 33):
    ang = -math.pi / 2.0 + (math.pi / 2.0) * (i / 32.0)
    profile_pts.append((cy_cove + R_cove * math.cos(ang), cz_cove + R_cove * math.sin(ang)))
for i in range(1, 30):
    z = cz_cove + (1200.0 - cz_cove) * (i / 29.0)
    profile_pts.append((cy_cove + R_cove, z))

x_vals = [-1800.0 + 3600.0 * (i / 64.0) for i in range(65)]
grid_verts = [[bm.verts.new((x, y, z)) for x in x_vals] for (y, z) in profile_pts]
for r in range(len(grid_verts) - 1):
    for c in range(len(x_vals) - 1):
        bm.faces.new((grid_verts[r][c], grid_verts[r][c+1], grid_verts[r+1][c+1], grid_verts[r+1][c]))
bm.to_mesh(cyc_mesh)
bm.free()
for p in cyc_mesh.polygons:
    p.use_smooth = True

mat_cyc = bpy.data.materials.new("Mat_Hero_Blue_Cyclorama")
nt = mat_cyc.node_tree
nt.nodes.clear()
out_c = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf_c = nt.nodes.new("ShaderNodeBsdfPrincipled")
bsdf_c.inputs["Roughness"].default_value = 0.24
bsdf_c.inputs["Specular IOR Level"].default_value = 0.38
if "Coat Weight" in bsdf_c.inputs:
    bsdf_c.inputs["Coat Weight"].default_value = 0.22
    bsdf_c.inputs["Coat Roughness"].default_value = 0.18

tc_c = nt.nodes.new("ShaderNodeTexCoord")
noise_c = nt.nodes.new("ShaderNodeTexNoise")
noise_c.inputs["Scale"].default_value = 95.0
noise_c.inputs["Detail"].default_value = 10.0
bump_c = nt.nodes.new("ShaderNodeBump")
bump_c.inputs["Strength"].default_value = 0.06
bump_c.inputs["Distance"].default_value = 0.08

vec_dist = nt.nodes.new("ShaderNodeVectorMath")
vec_dist.operation = 'DISTANCE'
vec_dist.inputs[1].default_value = (-60.0, -40.0, -115.0)
map_r = nt.nodes.new("ShaderNodeMapRange")
map_r.interpolation_type = 'SMOOTHERSTEP'
map_r.inputs["From Min"].default_value = 40.0
map_r.inputs["From Max"].default_value = 560.0

mix_col = nt.nodes.new("ShaderNodeMix")
mix_col.data_type = 'RGBA'
mix_col.inputs["A"].default_value = (0.14, 0.24, 0.34, 1.0)
mix_col.inputs["B"].default_value = (0.015, 0.032, 0.058, 1.0)

nt.links.new(tc_c.outputs["Object"], noise_c.inputs["Vector"])
nt.links.new(noise_c.outputs["Fac"], bump_c.inputs["Height"])
nt.links.new(bump_c.outputs["Normal"], bsdf_c.inputs["Normal"])
nt.links.new(tc_c.outputs["Object"], vec_dist.inputs[0])
nt.links.new(vec_dist.outputs["Value"], map_r.inputs["Value"])
nt.links.new(map_r.outputs["Result"], mix_col.inputs["Factor"])
nt.links.new(mix_col.outputs["Result"], bsdf_c.inputs["Base Color"])
nt.links.new(bsdf_c.outputs["BSDF"], out_c.inputs["Surface"])
cyc_mesh.materials.append(mat_cyc)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, -155.0))
arch_bench = bpy.context.active_object
arch_bench.scale = (2400.0, 900.0, 80.0)
arch_bench.hide_render = True

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 260.0, 350.0))
arch_wall = bpy.context.active_object
arch_wall.scale = (2600.0, 40.0, 1400.0)
arch_wall.hide_render = True

mat_timber = make_tactile_mat("Mat_Timber_Workbench", (0.34, 0.20, 0.09, 1.0), rough=0.36, coat=0.15, bump_str=0.08, bump_scale=45.0, diag_lines=True)
mat_terracotta = make_tactile_mat("Mat_Honed_Terracotta", (0.48, 0.21, 0.11, 1.0), rough=0.52, coat=0.05, bump_str=0.12, bump_scale=110.0)
mat_walnut = make_tactile_mat("Mat_Walnut_Shelf", (0.14, 0.07, 0.035, 1.0), rough=0.28, coat=0.25, bump_str=0.06, bump_scale=55.0, diag_lines=True)
mat_plaster = make_tactile_mat("Mat_Warm_Plaster_Wall", (0.62, 0.58, 0.52, 1.0), rough=0.65, coat=0.0, bump_str=0.10, bump_scale=85.0)
mat_dark_plaster = make_tactile_mat("Mat_Slate_Wall", (0.04, 0.06, 0.09, 1.0), rough=0.60, coat=0.0, bump_str=0.09, bump_scale=85.0)

def set_environment(env_mode):
    if env_mode == "BLUE_CYCLORAMA":
        cyc_obj.hide_render = False; arch_bench.hide_render = True; arch_wall.hide_render = True
        mix_col.inputs["A"].default_value = (0.14, 0.24, 0.34, 1.0)
        mix_col.inputs["B"].default_value = (0.015, 0.032, 0.058, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.24
    elif env_mode == "MIDNIGHT_CYCLORAMA":
        cyc_obj.hide_render = False; arch_bench.hide_render = True; arch_wall.hide_render = True
        mix_col.inputs["A"].default_value = (0.06, 0.11, 0.18, 1.0)
        mix_col.inputs["B"].default_value = (0.005, 0.010, 0.022, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.18
    elif env_mode == "TIMBER_WORKBENCH":
        cyc_obj.hide_render = True; arch_bench.hide_render = False; arch_wall.hide_render = False
        arch_bench.data.materials.clear(); arch_bench.data.materials.append(mat_timber)
        arch_wall.data.materials.clear(); arch_wall.data.materials.append(mat_dark_plaster)
    elif env_mode == "TERRACOTTA_PLINTH":
        cyc_obj.hide_render = True; arch_bench.hide_render = False; arch_wall.hide_render = False
        arch_bench.data.materials.clear(); arch_bench.data.materials.append(mat_terracotta)
        arch_wall.data.materials.clear(); arch_wall.data.materials.append(mat_plaster)
    elif env_mode == "WALNUT_BOOKSHELF":
        cyc_obj.hide_render = True; arch_bench.hide_render = False; arch_wall.hide_render = False
        arch_bench.data.materials.clear(); arch_bench.data.materials.append(mat_walnut)
        arch_wall.data.materials.clear(); arch_wall.data.materials.append(mat_plaster)

for o in bpy.data.objects:
    if o.type == 'LIGHT':
        o.hide_render = True

bpy.ops.object.light_add(type='SUN', location=(-300, -350, 260))
sun_key = bpy.context.active_object
sun_key.data.energy = 5.2
sun_key.data.angle = math.radians(5.5)
sun_key.data.color = (1.0, 0.96, 0.90)
sun_key.rotation_mode = 'QUATERNION'

bpy.ops.object.light_add(type='SUN', location=(280, -320, 220))
sun_fill = bpy.context.active_object
sun_fill.data.energy = 1.15
sun_fill.data.angle = math.radians(28.0)
sun_fill.data.color = (0.76, 0.88, 1.0)
sun_fill.rotation_mode = 'QUATERNION'
sun_fill.rotation_quaternion = Vector((0.75, -1.0, 0.55)).normalized().to_track_quat('Z', 'Y')

cam = scn.camera
cam.rotation_mode = 'QUATERNION'

def smootherstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_vec(va, vb, t):
    return tuple(lerp(a, b, t) for a, b in zip(va, vb))

def encode_4k_cinema_clip(seq_dir, out_mp4, aspect="16:9", n_frames=36):
    w, h = (3840, 2160) if aspect == "16:9" else (2160, 3840)
    # Render 36 frames -> interpolate to 60fps 6.0-second ultra-smooth slow-motion 4K cinema clip with Kodak Vision3 grain & halation!
    vf = (
        f"minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir,"
        f"scale={w}:{h}:flags=lanczos,"
        f"unsharp=5:5:0.85:3:3:0.0,"
        f"eq=contrast=1.04:saturation=1.05:gamma=0.98,"
        f"noise=c0s=5:c0f=t+u"
    )
    cmd = [
        FFMPEG, "-y",
        "-framerate", "6",
        "-i", os.path.join(seq_dir, "frame_%04d.jpg"),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "16",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[4K CYCLES CLIP READY] {out_mp4} ({os.path.getsize(out_mp4)/1e6:.2f} MB)")

def render_sequence(clip_name, aspect, n_frames, state_fn):
    out_dir = OUT_16x9_DIR if aspect == "16:9" else OUT_9x16_DIR
    out_mp4 = os.path.join(out_dir, f"{clip_name}.mp4")
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 500_000:
        print(f"[SKIP] {clip_name} already exists")
        return
    seq_dir = os.path.join(CYCLES_RAW_DIR, clip_name)
    os.makedirs(seq_dir, exist_ok=True)
    scn.render.resolution_x = 1920 if aspect == "16:9" else 1080
    scn.render.resolution_y = 1080 if aspect == "16:9" else 1920

    for i in range(n_frames):
        u = i / float(max(1, n_frames - 1))
        s = smootherstep(u)
        st = state_fn(u, s, i)
        apply_palette(st["pal"])
        set_environment(st["env"])
        clock_root.rotation_euler = (0.0, 0.0, math.radians(st["rot_z"]))
        bh.rotation_euler = (0.0, math.radians(st["bh_ang"]), 0.0)
        ch.rotation_euler = (0.0, math.radians(st["ch_ang"]), 0.0)
        sun_key.rotation_quaternion = Vector(st["sun_dir"]).normalized().to_track_quat('Z', 'Y')
        vec_dist.inputs[1].default_value = st["pool"]
        eye = Vector(st["eye"])
        tgt = Vector(st["tgt"])
        cam.location = eye
        cam.rotation_quaternion = (tgt - eye).normalized().to_track_quat('-Z', 'Y')
        cam.data.lens = st["lens"]
        cam.data.dof.use_dof = True
        cam.data.dof.aperture_fstop = st["fstop"]
        cam.data.dof.focus_distance = (tgt - eye).length

        frame_path = os.path.join(seq_dir, f"frame_{i:04d}.jpg")
        if not os.path.exists(frame_path):
            scn.render.filepath = frame_path
            bpy.ops.render.render(write_still=True)

    encode_4k_cinema_clip(seq_dir, out_mp4, aspect=aspect, n_frames=n_frames)

# 1. CLIP_01: Hero Dark Blue Slow Studio Turntable + Hand Sweep (16:9 4K)
render_sequence("CYCLES_01_HeroBlue_Slow_Turntable_And_HandSweep_16x9_4K", "16:9", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-26.0, 22.0, s),
    "bh_ang": lerp(-60.0, 58.0, s),
    "ch_ang": lerp(-48.0, 42.0, s),
    "eye": lerp_vec((-130, -910, 18), (110, -890, 14), s),
    "tgt": (0, 18, -12), "lens": 54.0, "fstop": 5.6,
    "sun_dir": lerp_vec((-0.85, -1.0, 0.72), (0.65, -1.0, 0.68), s),
    "pool": lerp_vec((-90, -50, -115), (70, -40, -115), s),
})

# 2. CLIP_02: Hero Dark Blue 180-Degree Turnaround from Front to Frosted Translucent Back with Hook Hole (16:9 4K)
render_sequence("CYCLES_02_HeroBlue_180_Turnaround_To_Frosted_Back_16x9_4K", "16:9", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-18.0, 168.0, s),
    "bh_ang": 58.0, "ch_ang": 42.0,
    "eye": lerp_vec((-95, -900, 16), (85, -880, 15), s),
    "tgt": (0, 20, -12), "lens": 54.0, "fstop": 5.2,
    "sun_dir": lerp_vec((-0.82, -1.0, 0.72), (-0.65, -1.0, 0.70), s),
    "pool": (-60, -40, -115),
})

# 3. CLIP_03: Extreme Macro Upper Dial Hand Sweep QUEENSIE -> LONG REEF -> DEE WHY (16:9 4K)
render_sequence("CYCLES_03_HeroBlue_Macro_UpperDial_Queensie_To_DeeWhy_16x9_4K", "16:9", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-18.0, -10.0, s),
    "bh_ang": lerp(-60.0, 58.0, s),
    "ch_ang": 42.0,
    "eye": lerp_vec((-60, -315, 42), (-30, -310, 40), s),
    "tgt": lerp_vec((-6, 5, 28), (4, 5, 28), s), "lens": 85.0, "fstop": 3.5,
    "sun_dir": lerp_vec((-0.85, -1.0, 0.70), (-0.45, -1.0, 0.78), s),
    "pool": (-50, -40, -115),
})

# 4. CLIP_04: Extreme Macro Lower WORTH IT? Hand Sweep NAH -> YEAH (16:9 4K)
render_sequence("CYCLES_04_HeroBlue_Macro_LowerWorthIt_Nah_To_Yeah_16x9_4K", "16:9", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-15.0, -8.0, s),
    "bh_ang": 58.0,
    "ch_ang": lerp(-52.0, 42.0, s),
    "eye": lerp_vec((-48, -285, -62), (-20, -280, -60), s),
    "tgt": lerp_vec((-2, 5, -72), (4, 5, -72), s), "lens": 90.0, "fstop": 3.5,
    "sun_dir": lerp_vec((-0.82, -1.0, 0.68), (-0.45, -1.0, 0.75), s),
    "pool": (-40, -40, -115),
})

# 5. CLIP_05: NOPIA MK1 Rhythmic Match-Cut Orbit Across Colorways & Environments (16:9 4K)
PAL_CYCLE = ["HERO_DARK_BLUE", "CHALK_WHITE", "OCHRE_WHITE_DUOTONE", "ALL_OCHRE_MONO", "HERO_DARK_BLUE", "HERO_DARK_BLUE"]
ENV_CYCLE = ["BLUE_CYCLORAMA", "BLUE_CYCLORAMA", "TIMBER_WORKBENCH", "TERRACOTTA_PLINTH", "WALNUT_BOOKSHELF", "BLUE_CYCLORAMA"]
render_sequence("CYCLES_05_NopiaStyle_Colorway_And_Environment_MatchCut_16x9_4K", "16:9", 36, lambda u, s, i: {
    "pal": PAL_CYCLE[min(5, i // 6)],
    "env": ENV_CYCLE[min(5, i // 6)],
    "rot_z": lerp(-24.0, 20.0, s),
    "bh_ang": lerp(-120.0, 120.0, s),
    "ch_ang": lerp(-52.0, 42.0, s),
    "eye": lerp_vec((-120, -890, 22), (95, -870, 16), s),
    "tgt": (0, 18, -12), "lens": 55.0, "fstop": 5.2,
    "sun_dir": lerp_vec((-0.85, -0.95, 0.68), (0.65, -0.95, 0.72), s),
    "pool": lerp_vec((-80, -45, -115), (65, -40, -115), s),
})

# 6. CLIP_06: Vertical 9:16 Hero Dark Blue Slow Orbit & Hand Sweep (9:16 4K)
render_sequence("CYCLES_06_HeroBlue_Vertical_Slow_Orbit_9x16_4K", "9:16", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-22.0, 18.0, s),
    "bh_ang": lerp(-60.0, 58.0, s),
    "ch_ang": lerp(-50.0, 42.0, s),
    "eye": lerp_vec((-95, -720, 16), (85, -710, 12), s),
    "tgt": (0, 18, -10), "lens": 52.0, "fstop": 5.6,
    "sun_dir": lerp_vec((-0.82, -1.05, 0.72), (0.68, -1.05, 0.72), s),
    "pool": lerp_vec((-60, -40, -115), (60, -40, -115), s),
})

# 7. CLIP_07: Vertical 9:16 180-Degree Turnaround to Frosted Translucent Back Cover (9:16 4K)
render_sequence("CYCLES_07_HeroBlue_Vertical_180_Turnaround_To_Frosted_Back_9x16_4K", "9:16", 36, lambda u, s, i: {
    "pal": "HERO_DARK_BLUE", "env": "BLUE_CYCLORAMA",
    "rot_z": lerp(-16.0, 166.0, s),
    "bh_ang": 58.0, "ch_ang": 42.0,
    "eye": lerp_vec((-85, -720, 15), (80, -710, 14), s),
    "tgt": (0, 20, -10), "lens": 52.0, "fstop": 5.2,
    "sun_dir": lerp_vec((-0.80, -1.0, 0.70), (-0.60, -1.0, 0.70), s),
    "pool": (-60, -40, -115),
})

# 8. CLIP_08: Vertical 9:16 Rhythmic Match-Cut Orbit Across Colorways & Environments (9:16 4K)
render_sequence("CYCLES_08_Vertical_Colorway_And_Environment_MatchCut_9x16_4K", "9:16", 36, lambda u, s, i: {
    "pal": PAL_CYCLE[min(5, i // 6)],
    "env": ENV_CYCLE[min(5, i // 6)],
    "rot_z": lerp(-22.0, 18.0, s),
    "bh_ang": lerp(-120.0, 120.0, s),
    "ch_ang": lerp(-52.0, 42.0, s),
    "eye": lerp_vec((-95, -710, 20), (80, -700, 14), s),
    "tgt": (0, 18, -10), "lens": 52.0, "fstop": 5.2,
    "sun_dir": lerp_vec((-0.85, -0.95, 0.68), (0.65, -0.95, 0.72), s),
    "pool": lerp_vec((-60, -40, -115), (60, -40, -115), s),
})

print("ALL 8 BLENDER CYCLES 4K 60FPS CINEMA CLIPS COMPLETED!")
