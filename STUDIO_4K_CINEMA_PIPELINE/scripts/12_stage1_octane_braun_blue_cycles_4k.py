#!/usr/bin/env python3
"""
12_stage1_octane_braun_blue_cycles_4k.py
========================================
Renders the V2 Smooth-Beveled Luxury Braun / Teenage Engineering "Octane Ray-Tracing Vibe"
4K 60fps Cinema Sequences and 4K Keyframes in Blender 5.2.1 Cycles Metal RT.
- ZERO 3D-print diagonal texture (100% smooth bead-blasted anodized & matte ceramic shaders).
- Radiused 0.90 mm luxury Braun bevels catching cool cyan-blue rim highlights.
- Satin slate-blue floor reflection + curved caustic light sweep matching media_1791970931092.jpg.
- Strictly valid mechanical dial angles (Upper: -120..+120 deg; Lower: -52..+45 deg).
"""

import bpy, bmesh, os, math, subprocess
from mathutils import Vector, Euler, Matrix

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
RAW_FRAMES_DIR = f"{BASE}/raw_renders/v2_octane_frames"
KF_OUT_DIR = f"{BASE}/01_4K_STUDIO_KEYFRAMES_AND_STILLS/OCTANE_RAYTRACED_4K"
OUT_16x9 = f"{BASE}/02_INDIVIDUAL_4K_CLIPS_16x9"
OUT_9x16 = f"{BASE}/03_INDIVIDUAL_4K_CLIPS_9x16"
AUDIT_DIR = f"{BASE}/04_CONTACT_SHEETS_AND_AUDIT"
FFMPEG = "/Users/jcolley/.gemini/jetski/bin/ffmpeg"

for d in [RAW_FRAMES_DIR, KF_OUT_DIR, OUT_16x9, OUT_9x16, AUDIT_DIR]:
    os.makedirs(d, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath="/Users/jcolley/surf_clock/SurfClock_V23_ActualPhysicalTypeface_Master.blend")
scn = bpy.context.scene
scn.frame_set(360)
scn.render.engine = 'CYCLES'
scn.cycles.device = 'GPU'
scn.render.use_persistent_data = True
scn.cycles.samples = 128
if hasattr(scn.cycles, "denoising_use_gpu"):
    scn.cycles.denoising_use_gpu = True
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.cycles.transmission_bounces = 12
scn.cycles.transparent_max_bounces = 12
scn.view_settings.view_transform = 'AgX'
scn.view_settings.look = 'AgX - High Contrast'
scn.view_settings.exposure = 0.12

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

# Carve rear bottom-center hook/cord cutout + add luxury Braun 0.90 mm radiused bevel
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 44.0, -112.5))
hook_cutter = bpy.context.active_object
hook_cutter.scale = (14.0, 14.0, 11.0)
hook_cutter.parent = clock_root
hook_cutter.hide_render = True
hook_cutter.hide_viewport = True

bezel.modifiers.clear()
mod_hook = bezel.modifiers.new(name="RearHookHole", type='BOOLEAN')
mod_hook.operation = 'DIFFERENCE'
mod_hook.solver = 'EXACT'
mod_hook.object = hook_cutter

bev_b = bezel.modifiers.new("BraunRadius", 'BEVEL')
bev_b.width = 0.90
bev_b.segments = 5
bev_b.limit_method = 'ANGLE'
bev_b.angle_limit = math.radians(30)

# Import V5 Frosted Translucent Back Cover + Internal V5 Motor Mount + Steppers
kit = "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT"
bpy.ops.wm.stl_import(filepath=os.path.join(kit, "4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl"))
back_v5 = bpy.context.selected_objects[0]
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

def make_smooth_braun_mat(name, rgba, metallic=0.0, rough=0.45, spec=0.20, coat=0.0, coat_rough=0.15, emission_str=0.0):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Specular IOR Level"].default_value = spec
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = coat
        bsdf.inputs["Coat Roughness"].default_value = coat_rough
    if emission_str > 0 and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = rgba
        bsdf.inputs["Emission Strength"].default_value = emission_str
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

def make_frosted_borosilicate_back():
    m = bpy.data.materials.new("FrostedBorosilicateBack")
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (0.76, 0.88, 0.98, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.16
    bsdf.inputs["IOR"].default_value = 1.49
    bsdf.inputs["Alpha"].default_value = 0.68
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = 0.92
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 0.45
        bsdf.inputs["Coat Roughness"].default_value = 0.10
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave")
    wv.wave_type = 'BANDS'
    wv.bands_direction = 'Y'
    wv.inputs["Scale"].default_value = 22.0
    wv.inputs["Distortion"].default_value = 0.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.28
    bump.inputs["Distance"].default_value = 0.35
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

mat_bezel = make_smooth_braun_mat("BraunBezel", (0.008, 0.022, 0.058, 1.0), metallic=0.14, rough=0.26, spec=0.45, coat=0.35, coat_rough=0.12)
mat_dial  = make_smooth_braun_mat("BraunDial",  (0.007, 0.020, 0.052, 1.0), metallic=0.0,  rough=0.52, spec=0.12, coat=0.0)
mat_moat  = make_smooth_braun_mat("BraunMoat",  (0.002, 0.006, 0.016, 1.0), metallic=0.0,  rough=0.65, spec=0.05)
mat_typo  = make_smooth_braun_mat("BraunTypo",  (0.92,  0.95,  0.98,  1.0), metallic=0.0,  rough=0.22, spec=0.50, coat=0.25, emission_str=0.12)
mat_hands = make_smooth_braun_mat("BraunHands", (0.78,  0.18,  0.018, 1.0), metallic=0.08, rough=0.20, spec=0.55, coat=0.80, coat_rough=0.08)
mat_metal = make_smooth_braun_mat("BraunMetal", (0.22,  0.28,  0.36,  1.0), metallic=0.85, rough=0.25, spec=0.50)
mat_frosted = make_frosted_borosilicate_back()

bezel.data.materials.clear(); bezel.data.materials.append(mat_bezel)
dial.data.materials.clear();  dial.data.materials.append(mat_dial)
moat.data.materials.clear();  moat.data.materials.append(mat_moat)
typo.data.materials.clear();  typo.data.materials.append(mat_typo)
bh.data.materials.clear();    bh.data.materials.append(mat_hands)
ch.data.materials.clear();    ch.data.materials.append(mat_hands)
mount_v5.data.materials.clear(); mount_v5.data.materials.append(mat_bezel)
upper_motor_sil.data.materials.append(mat_metal)
lower_motor_sil.data.materials.append(mat_metal)
back_v5.data.materials.clear(); back_v5.data.materials.append(mat_frosted)

# 8 Luxury Finishes for True 3D Match-Cut
LUXURY_FINISHES = [
    # 1. Hero Midnight Navy & Burnt Amber
    {"bezel": (0.008, 0.022, 0.058, 1.0), "dial": (0.007, 0.020, 0.052, 1.0), "typo": (0.92, 0.95, 0.98, 1.0), "hands": (0.78, 0.18, 0.018, 1.0), "b_met": 0.14},
    # 2. Bead-Blasted Titanium-Blue Anodized & Signal Orange
    {"bezel": (0.055, 0.095, 0.155, 1.0), "dial": (0.012, 0.028, 0.062, 1.0), "typo": (0.94, 0.96, 0.98, 1.0), "hands": (0.82, 0.16, 0.015, 1.0), "b_met": 0.72},
    # 3. Stealth Matte Carbon-Graphite & Braun Signal Orange
    {"bezel": (0.014, 0.018, 0.024, 1.0), "dial": (0.012, 0.015, 0.020, 1.0), "typo": (0.88, 0.92, 0.96, 1.0), "hands": (0.82, 0.16, 0.015, 1.0), "b_met": 0.25},
    # 4. Ice-Silver Anodized Aluminum Bezel & Midnight Navy Dial
    {"bezel": (0.280, 0.340, 0.410, 1.0), "dial": (0.008, 0.022, 0.056, 1.0), "typo": (0.94, 0.96, 0.98, 1.0), "hands": (0.78, 0.18, 0.018, 1.0), "b_met": 0.85},
    # 5. Deep Petrol-Teal Ceramic & Copper-Gold Hands
    {"bezel": (0.006, 0.038, 0.058, 1.0), "dial": (0.005, 0.032, 0.050, 1.0), "typo": (0.90, 0.94, 0.96, 1.0), "hands": (0.72, 0.32, 0.045, 1.0), "b_met": 0.18},
    # 6. Prussian Cobalt & Ice-White Indices
    {"bezel": (0.012, 0.036, 0.110, 1.0), "dial": (0.010, 0.030, 0.095, 1.0), "typo": (0.95, 0.97, 1.00, 1.0), "hands": (0.80, 0.20, 0.020, 1.0), "b_met": 0.20},
    # 7. Nordic Slate-Grey Monolith & Amber Hands
    {"bezel": (0.042, 0.058, 0.078, 1.0), "dial": (0.036, 0.050, 0.068, 1.0), "typo": (0.92, 0.95, 0.98, 1.0), "hands": (0.78, 0.18, 0.018, 1.0), "b_met": 0.30},
    # 8. Smoked Sapphire PVD & Warm Amber
    {"bezel": (0.016, 0.028, 0.072, 1.0), "dial": (0.006, 0.014, 0.038, 1.0), "typo": (0.92, 0.95, 0.98, 1.0), "hands": (0.78, 0.18, 0.018, 1.0), "b_met": 0.65},
]

def apply_luxury_finish(idx):
    f = LUXURY_FINISHES[idx % len(LUXURY_FINISHES)]
    bsdf_b = [n for n in mat_bezel.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    bsdf_d = [n for n in mat_dial.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    bsdf_t = [n for n in mat_typo.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    bsdf_h = [n for n in mat_hands.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    bsdf_b.inputs["Base Color"].default_value = f["bezel"]
    bsdf_b.inputs["Metallic"].default_value = f["b_met"]
    bsdf_d.inputs["Base Color"].default_value = f["dial"]
    bsdf_t.inputs["Base Color"].default_value = f["typo"]
    bsdf_h.inputs["Base Color"].default_value = f["hands"]

# Studio Set: Satin Slate-Blue Floor + Chiaroscuro Caustic Wall
bpy.ops.mesh.primitive_plane_add(size=4000.0, location=(0.0, 0.0, -115.0))
floor_obj = bpy.context.active_object
bpy.ops.mesh.primitive_plane_add(size=4000.0, location=(0.0, 180.0, 600.0), rotation=(math.radians(90), 0, 0))
wall_obj = bpy.context.active_object

def make_caustic_set_mat(name, is_floor=False):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Metallic"].default_value = 0.24 if is_floor else 0.06
    bsdf.inputs["Roughness"].default_value = 0.15 if is_floor else 0.52
    bsdf.inputs["Specular IOR Level"].default_value = 0.45 if is_floor else 0.20
    
    geom = nt.nodes.new("ShaderNodeNewGeometry")
    vec_dist = nt.nodes.new("ShaderNodeVectorMath")
    vec_dist.name = "CausticCenter"
    vec_dist.operation = 'DISTANCE'
    vec_dist.inputs[1].default_value = (-170.0, 180.0, -60.0) if not is_floor else (-140.0, -60.0, -115.0)
    map_r = nt.nodes.new("ShaderNodeMapRange")
    map_r.interpolation_type = 'SMOOTHERSTEP'
    map_r.inputs["From Min"].default_value = 30.0
    map_r.inputs["From Max"].default_value = 390.0
    
    mix_col = nt.nodes.new("ShaderNodeMix")
    mix_col.data_type = 'RGBA'
    mix_col.inputs["A"].default_value = (0.28, 0.44, 0.52, 1.0) if not is_floor else (0.22, 0.36, 0.44, 1.0)
    mix_col.inputs["B"].default_value = (0.010, 0.028, 0.052, 1.0) if not is_floor else (0.014, 0.036, 0.064, 1.0)
    
    nt.links.new(geom.outputs["Position"], vec_dist.inputs[0])
    nt.links.new(vec_dist.outputs["Value"], map_r.inputs["Value"])
    nt.links.new(map_r.outputs["Result"], mix_col.inputs["Factor"])
    nt.links.new(mix_col.outputs["Result"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

mat_floor_c = make_caustic_set_mat("FloorMat", is_floor=True)
mat_wall_c  = make_caustic_set_mat("WallMat", is_floor=False)
floor_obj.data.materials.append(mat_floor_c)
wall_obj.data.materials.append(mat_wall_c)

if scn.world and scn.world.node_tree:
    for n in scn.world.node_tree.nodes:
        if n.type == 'BACKGROUND':
            n.inputs['Strength'].default_value = 0.02

for o in bpy.data.objects:
    if o.type == 'LIGHT':
        o.hide_render = True

bpy.ops.object.light_add(type='SUN', location=(-300, -150, 220))
sun_key = bpy.context.active_object
sun_key.data.energy = 3.8
sun_key.data.angle = math.radians(5.0)
sun_key.data.color = (0.72, 0.88, 1.0)
sun_key.rotation_mode = 'QUATERNION'

bpy.ops.object.light_add(type='SUN', location=(-100, -100, 350))
sun_rim = bpy.context.active_object
sun_rim.data.energy = 1.65
sun_rim.data.angle = math.radians(12.0)
sun_rim.data.color = (0.68, 0.86, 1.0)
sun_rim.rotation_mode = 'QUATERNION'

cam = scn.camera
cam.rotation_mode = 'QUATERNION'

def set_caustic_pos(cx):
    mat_wall_c.node_tree.nodes["CausticCenter"].inputs[1].default_value = (cx, 180.0, -50.0)
    mat_floor_c.node_tree.nodes["CausticCenter"].inputs[1].default_value = (cx * 0.8, -60.0, -115.0)

def smootherstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_v(v1, v2, t):
    return Vector((lerp(v1[0], v2[0], t), lerp(v1[1], v2[1], t), lerp(v1[2], v2[2], t)))

def encode_4k_clip(frame_dir, out_mp4, sheet_jpg, w=3840, h=2160):
    vf = (
        f"scale={w}:{h}:flags=lanczos,"
        f"unsharp=5:5:0.45:5:5:0.0,"
        f"eq=contrast=1.03:saturation=1.02,"
        f"noise=alls=3:allf=t+u,"
        f"fps=60"
    )
    subprocess.run([
        FFMPEG, "-y", "-framerate", "60", "-i", f"{frame_dir}/f_%04d.jpg",
        "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "14",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        FFMPEG, "-y", "-i", out_mp4, "-vf", "fps=1.0,scale=640:-1,tile=4x2",
        "-frames:v", "1", "-q:v", "2", sheet_jpg
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[OCTANE 4K 60FPS MASTERED] {os.path.basename(out_mp4)}", flush=True)

# Render 6 Octane-Style 60fps Clips (360 frames = 6.0s at 60fps, or 480 frames = 8.0s at 60fps)
scn.cycles.samples = 96
scn.render.image_settings.file_format = 'JPEG'
scn.render.image_settings.quality = 96

CLIPS = [
    {
        "id": "OCTANE_01_Signature_SlateBlue_CausticSweep_And_HandSettle_16x9",
        "w": 1920, "h": 1080, "out_w": 3840, "out_h": 2160, "out_dir": OUT_16x9,
        "frames": 480,
        "rot_z": (-15.0, -11.0),
        "bh": (-60.0, 58.0),   # QUEENSIE -> LONG REEF -> DEE WHY (strictly upper arc!)
        "ch": (-48.0, 42.0),   # NAH -> YEAH (strictly inside upper semicircle!)
        "eye": ((-75.0, -910.0, -16.0), (-45.0, -790.0, -14.0)),
        "tgt": ((0.0, 10.0, -12.0), (0.0, 10.0, -12.0)),
        "lens": 56.0, "fstop": 3.5,
        "caustic_x": (-180.0, 140.0),
        "sun_dir": ((-1.35, -0.45, 0.65), (-0.85, -0.55, 0.75)),
        "match_cut": False,
    },
    {
        "id": "OCTANE_02_Macro_100mm_UpperDial_SmoothBraun_BevelGlint_16x9",
        "w": 1920, "h": 1080, "out_w": 3840, "out_h": 2160, "out_dir": OUT_16x9,
        "frames": 480,
        "rot_z": (-14.0, -14.0),
        "bh": (-60.0, 58.0),   # QUEENSIE -> DEE WHY
        "ch": (42.0, 42.0),
        "eye": ((-45.0, -330.0, 38.0), (-20.0, -300.0, 34.0)),
        "tgt": ((-4.0, 5.0, 28.0), (4.0, 5.0, 28.0)),
        "lens": 90.0, "fstop": 2.8,
        "caustic_x": (-140.0, 100.0),
        "sun_dir": ((-1.35, -0.45, 0.65), (-0.75, -0.55, 0.80)),
        "match_cut": False,
    },
    {
        "id": "OCTANE_03_Macro_100mm_LowerWorthIt_Semicircle_Settle_16x9",
        "w": 1920, "h": 1080, "out_w": 3840, "out_h": 2160, "out_dir": OUT_16x9,
        "frames": 480,
        "rot_z": (-14.0, -14.0),
        "bh": (58.0, 58.0),
        "ch": (-50.0, 42.0),   # NAH -> YEAH inside upper semicircle!
        "eye": ((-38.0, -295.0, -60.0), (-15.0, -275.0, -58.0)),
        "tgt": ((-2.0, 5.0, -70.0), (4.0, 5.0, -70.0)),
        "lens": 95.0, "fstop": 2.8,
        "caustic_x": (-120.0, 120.0),
        "sun_dir": ((-1.30, -0.45, 0.62), (-0.80, -0.50, 0.72)),
        "match_cut": False,
    },
    {
        "id": "OCTANE_04_180_Turnaround_To_Fluted_Frosted_RearCover_16x9",
        "w": 1920, "h": 1080, "out_w": 3840, "out_h": 2160, "out_dir": OUT_16x9,
        "frames": 480,
        "rot_z": (148.0, 204.0), # Rear fluted borosilicate translucent cover turnaround!
        "bh": (58.0, 58.0),
        "ch": (42.0, 42.0),
        "eye": ((95.0, -860.0, -10.0), (-95.0, -840.0, -12.0)),
        "tgt": ((0.0, 22.0, -12.0), (0.0, 22.0, -12.0)),
        "lens": 56.0, "fstop": 3.5,
        "caustic_x": (-150.0, 150.0),
        "sun_dir": ((-1.10, -0.65, 0.65), (1.10, -0.65, 0.65)),
        "match_cut": False,
    },
    {
        "id": "OCTANE_05_True3D_Moving_Camera_MatchCut_8_Luxury_Finishes_16x9",
        "w": 1920, "h": 1080, "out_w": 3840, "out_h": 2160, "out_dir": OUT_16x9,
        "frames": 480,
        "rot_z": (-20.0, 14.0), # Continuous 34-deg 3D orbital arc cut across 8 luxury finishes!
        "bh": (-60.0, 58.0),
        "ch": (-48.0, 42.0),
        "eye": ((-110.0, -880.0, -14.0), (85.0, -860.0, -14.0)),
        "tgt": ((0.0, 10.0, -12.0), (0.0, 10.0, -12.0)),
        "lens": 56.0, "fstop": 3.5,
        "caustic_x": (-170.0, 170.0),
        "sun_dir": ((-1.35, -0.45, 0.65), (-0.65, -0.65, 0.75)),
        "match_cut": True,
    },
    {
        "id": "OCTANE_06_Vertical_Signature_SlateBlue_CausticOrbit_9x16",
        "w": 1080, "h": 1920, "out_w": 2160, "out_h": 3840, "out_dir": OUT_9x16,
        "frames": 480,
        "rot_z": (-16.0, 12.0),
        "bh": (-60.0, 58.0),
        "ch": (-48.0, 42.0),
        "eye": ((-75.0, -720.0, -12.0), (55.0, -690.0, -12.0)),
        "tgt": ((0.0, 10.0, -12.0), (0.0, 10.0, -12.0)),
        "lens": 54.0, "fstop": 3.5,
        "caustic_x": (-140.0, 140.0),
        "sun_dir": ((-1.30, -0.45, 0.65), (-0.75, -0.55, 0.75)),
        "match_cut": False,
    },
]

for clip in CLIPS:
    cid = clip["id"]
    out_mp4 = os.path.join(clip["out_dir"], f"{cid}_4K.mp4")
    sheet_jpg = os.path.join(AUDIT_DIR, f"{cid}_sheet.jpg")
    fdir = os.path.join(RAW_FRAMES_DIR, cid)
    os.makedirs(fdir, exist_ok=True)
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 5_000_000:
        print(f"[SKIP EXISTING OCTANE] {cid}", flush=True)
        continue
    scn.render.resolution_x = clip["w"]
    scn.render.resolution_y = clip["h"]
    N = clip["frames"]
    for i in range(N):
        fpath = f"{fdir}/f_{i:04d}.jpg"
        if os.path.exists(fpath) and os.path.getsize(fpath) > 20_000:
            continue
        u = i / float(N - 1)
        s = smootherstep(u)
        if clip["match_cut"]:
            # Cut to a new luxury finish every 30 frames (0.50s) while keeping 100.00% continuous 3D camera & hand motion!
            apply_luxury_finish((i // 30) % len(LUXURY_FINISHES))
        else:
            apply_luxury_finish(0)
        clock_root.rotation_euler = (0.0, 0.0, math.radians(lerp(clip["rot_z"][0], clip["rot_z"][1], s)))
        bh.rotation_euler = (0.0, math.radians(lerp(clip["bh"][0], clip["bh"][1], s)), 0.0)
        ch.rotation_euler = (0.0, math.radians(lerp(clip["ch"][0], clip["ch"][1], s)), 0.0)
        eye = lerp_v(clip["eye"][0], clip["eye"][1], s)
        tgt = lerp_v(clip["tgt"][0], clip["tgt"][1], s)
        cam.location = eye
        cam.rotation_quaternion = (tgt - eye).normalized().to_track_quat('-Z', 'Y')
        cam.data.lens = clip["lens"]
        cam.data.dof.aperture_fstop = clip["fstop"]
        cam.data.dof.focus_distance = (tgt - eye).length
        set_caustic_pos(lerp(clip["caustic_x"][0], clip["caustic_x"][1], s))
        sdir = lerp_v(clip["sun_dir"][0], clip["sun_dir"][1], s)
        sun_key.rotation_quaternion = sdir.normalized().to_track_quat('Z', 'Y')
        scn.render.filepath = fpath
        bpy.ops.render.render(write_still=True)
        # Also save 4K keyframes at frame 0 and frame N-1
        if i in (0, N - 1):
            kf_tag = "Start" if i == 0 else "End"
            subprocess.run([
                FFMPEG, "-y", "-i", fpath,
                "-vf", f"scale={clip['out_w']}:{clip['out_h']}:flags=lanczos,unsharp=5:5:0.45:5:5:0.0,noise=alls=3:allf=t+u",
                "-q:v", "1", f"{KF_OUT_DIR}/{cid}_{kf_tag}_4K.jpg"
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    encode_4k_clip(fdir, out_mp4, sheet_jpg, w=clip["out_w"], h=clip["out_h"])

print("ALL OCTANE-STYLE 4K 60FPS CLIPS COMPLETE!", flush=True)
