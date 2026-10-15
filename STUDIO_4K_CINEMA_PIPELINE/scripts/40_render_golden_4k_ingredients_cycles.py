import bpy, bmesh, os, math
from mathutils import Vector, Euler, Matrix

PROJECT_DIR = "/Users/jcolley/surf_clock"
PIPELINE_DIR = os.path.join(PROJECT_DIR, "STUDIO_4K_CINEMA_PIPELINE")
OUT_DIR = os.path.join(PIPELINE_DIR, "00_GOLDEN_INGREDIENTS_4K")
os.makedirs(OUT_DIR, exist_ok=True)

BLEND_IN = os.path.join(PROJECT_DIR, "SurfClock_V23_ActualPhysicalTypeface_Master.blend")
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

scn = bpy.context.scene
scn.frame_set(360)
scn.render.engine = 'CYCLES'
scn.cycles.device = 'GPU'
scn.render.use_persistent_data = True
scn.cycles.samples = 96
if hasattr(scn.cycles, "denoising_use_gpu"):
    scn.cycles.denoising_use_gpu = True
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.render.image_settings.file_format = 'JPEG'
scn.render.image_settings.quality = 98
scn.view_settings.view_transform = 'AgX'
scn.view_settings.look = 'AgX - Medium High Contrast'
scn.view_settings.exposure = 0.20

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
bm_t = bmesh.new()
bm_t.from_mesh(typo.data)
bmesh.ops.remove_doubles(bm_t, verts=bm_t.verts, dist=0.005)
bmesh.ops.recalc_face_normals(bm_t, faces=bm_t.faces)
bm_t.to_mesh(typo.data)
bm_t.free()
for poly in typo.data.polygons:
    poly.use_smooth = False

dial = bpy.data.objects.get("SurfClock_Master_60fps_Rig_dial_v2_flush")
moat = bpy.data.objects.get("Dial_Shadow_Moat_Backer")
bh = bpy.data.objects.get("SurfClock_Master_60fps_Rig_beach_hand")
ch = bpy.data.objects.get("SurfClock_Master_60fps_Rig_cond_hand")
bezel = bpy.data.objects.get("SurfClock_Master_60fps_Rig_bezel")

if scn.world and scn.world.node_tree:
    for n in scn.world.node_tree.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Strength'].default_value = 0.03
            n.inputs['Color'].default_value = (0.010, 0.018, 0.035, 1.0)

def make_tactile_mat(name, base_rgba, rough=0.38, coat=0.18, coat_rough=0.25, sss=0.12, bump_str=0.075, bump_scale=85.0, diag_lines=False):
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
    noise.inputs["Detail"].default_value = 12.0
    noise.inputs["Roughness"].default_value = 0.78
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_str
    bump.inputs["Distance"].default_value = 0.14

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
        ma.inputs[1].default_value = 0.25
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

mat_bezel = make_tactile_mat("DynBezel", (0.016, 0.032, 0.078, 1.0), rough=0.38, coat=0.22, bump_str=0.075, bump_scale=85.0)
mat_dial  = make_tactile_mat("DynDial",  (0.018, 0.036, 0.086, 1.0), rough=0.42, coat=0.16, bump_str=0.065, bump_scale=75.0, diag_lines=True)
mat_moat  = make_tactile_mat("DynMoat",  (0.005, 0.010, 0.025, 1.0), rough=0.55, coat=0.0,  bump_str=0.02)
mat_typo  = make_tactile_mat("DynTypo",  (0.90,  0.89,  0.86,  1.0), rough=0.28, coat=0.25, sss=0.18, bump_str=0.035)
mat_hands = make_tactile_mat("DynHands", (0.68,  0.28,  0.032, 1.0), rough=0.26, coat=0.38, sss=0.15, bump_str=0.035)

bezel.data.materials.clear(); bezel.data.materials.append(mat_bezel)
dial.data.materials.clear();  dial.data.materials.append(mat_dial)
moat.data.materials.clear();  moat.data.materials.append(mat_moat)
typo.data.materials.clear();  typo.data.materials.append(mat_typo)
bh.data.materials.clear();    bh.data.materials.append(mat_hands)
ch.data.materials.clear();    ch.data.materials.append(mat_hands)

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

for o in bpy.data.objects:
    if o.type == 'LIGHT':
        o.hide_render = True

bpy.ops.object.light_add(type='SUN', location=(-300, -350, 260))
sun_key = bpy.context.active_object
sun_key.name = "Hero_Sun_Key"
sun_key.data.energy = 5.4
sun_key.data.angle = math.radians(5.5)
sun_key.data.color = (1.0, 0.96, 0.90)
sun_key.rotation_mode = 'QUATERNION'

bpy.ops.object.light_add(type='SUN', location=(280, -320, 220))
sun_fill = bpy.context.active_object
sun_fill.name = "Hero_Cool_Fill"
sun_fill.data.energy = 1.35
sun_fill.data.angle = math.radians(28.0)
sun_fill.data.color = (0.76, 0.88, 1.0)
sun_fill.rotation_mode = 'QUATERNION'
sun_fill.rotation_quaternion = Vector((0.75, -1.0, 0.55)).normalized().to_track_quat('Z', 'Y')

def set_sun(dir_vec, energy=5.4, angle_deg=5.5, color=(1.0, 0.96, 0.90), pool_center=(-60.0, -40.0, -115.0)):
    sun_key.rotation_quaternion = Vector(dir_vec).normalized().to_track_quat('Z', 'Y')
    sun_key.data.energy = energy
    sun_key.data.angle = math.radians(angle_deg)
    sun_key.data.color = color
    vec_dist.inputs[1].default_value = pool_center

def set_cyc_palette(mode):
    if mode == "BLUE":
        mix_col.inputs["A"].default_value = (0.14, 0.24, 0.34, 1.0)
        mix_col.inputs["B"].default_value = (0.015, 0.032, 0.058, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.24
    elif mode == "WHITE":
        mix_col.inputs["A"].default_value = (0.92, 0.91, 0.89, 1.0)
        mix_col.inputs["B"].default_value = (0.72, 0.71, 0.69, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.35
    elif mode == "CREAM":
        mix_col.inputs["A"].default_value = (0.86, 0.79, 0.68, 1.0)
        mix_col.inputs["B"].default_value = (0.58, 0.50, 0.41, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.42

cam = scn.camera
cam.rotation_mode = 'QUATERNION'
def set_cam(eye, tgt, lens=54.0, fstop=5.6):
    cam.location = Vector(eye)
    cam.rotation_quaternion = (Vector(tgt) - Vector(eye)).normalized().to_track_quat('-Z', 'Y')
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = fstop
    cam.data.dof.focus_distance = (Vector(tgt) - Vector(eye)).length

SHOTS = [
    ("INGREDIENT_01_FRONT_ORTHO_9TICK_4K.jpg", 3840, 2160, "BLUE",   0.0, -58.0, 42.0, (0, -880, 5), (0, 10, -8), 54.0, 8.0, (-0.75, -1.0, 0.68), (-60, -40, -115)),
    ("INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg", 3840, 2160, "BLUE", -20.0, -58.0, 42.0, (-125, -890, 18), (0, 18, -10), 54.0, 5.6, (-0.85, -1.0, 0.72), (-90, -50, -115)),
    ("INGREDIENT_03_THREE_QUARTER_RIGHT_9TICK_4K.jpg", 3840, 2160, "BLUE",  18.0,  58.0, 42.0, ( 110, -890, 14), (0, 18, -10), 54.0, 5.6, ( 0.65, -1.0, 0.68), ( 70, -40, -115)),
    ("INGREDIENT_04_MACRO_UPPER_DIAL_9TICK_4K.jpg", 3840, 2160, "BLUE", -14.0, -58.0, 42.0, (-45, -340, 38), (-2, 5, 26), 82.0, 4.0, (-0.82, -1.05, 0.72), (-60, -40, -115)),
    ("INGREDIENT_05_MACRO_LOWER_WORTHIT_4K.jpg", 3840, 2160, "BLUE", -12.0, 58.0, 42.0, (-30, -300, -58), (2, 5, -70), 88.0, 4.0, (-0.65, -1.0, 0.72), (-20, -40, -115)),
    ("INGREDIENT_06_WHITE_CYCLORAMA_9TICK_4K.jpg", 3840, 2160, "WHITE", -16.0, 0.0, 42.0, (-95, -890, 16), (0, 18, -10), 54.0, 5.6, (-0.80, -1.0, 0.70), (-60, -40, -115)),
    ("INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg", 3840, 2160, "CREAM", -14.0, 58.0, 42.0, (-85, -880, 18), (0, 18, -10), 54.0, 5.6, (-0.85, -0.95, 0.62), (-70, -40, -115)),
    ("INGREDIENT_08_VERTICAL_9x16_HERO_9TICK_4K.jpg", 2160, 3840, "BLUE", -18.0, -58.0, 42.0, (-90, -720, 15), (0, 18, -10), 52.0, 5.6, (-0.82, -1.05, 0.72), (-60, -40, -115)),
]

for fname, rx, ry, cyc_mode, rot_z, bh_ang, ch_ang, eye, tgt, lens, fstop, sun_dir, pool in SHOTS:
    scn.render.resolution_x = rx
    scn.render.resolution_y = ry
    set_cyc_palette(cyc_mode)
    clock_root.rotation_euler = (0.0, 0.0, math.radians(rot_z))
    bh.rotation_euler = (0.0, math.radians(bh_ang), 0.0)
    ch.rotation_euler = (0.0, math.radians(ch_ang), 0.0)
    set_sun(sun_dir, pool_center=pool)
    set_cam(eye, tgt, lens=lens, fstop=fstop)
    out_path = os.path.join(OUT_DIR, fname)
    scn.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print("Rendered:", out_path)

print("ALL 8 GOLDEN 4K INGREDIENTS RENDERED SUCCESSFULLY!")
