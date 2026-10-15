import bpy
import os
import math
from mathutils import Vector, Euler

PROJECT_DIR = "/Users/jcolley/surf_clock"
BLEND_IN = os.path.join(PROJECT_DIR, "SurfClock_V23_ActualPhysicalTypeface_Master.blend")

bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

scn = bpy.context.scene
scn.frame_set(360)
scn.render.engine = 'CYCLES'
scn.cycles.device = 'GPU'
scn.render.use_persistent_data = False
scn.cycles.samples = 48
if hasattr(scn.cycles, "denoising_use_gpu"):
    scn.cycles.denoising_use_gpu = True
scn.cycles.use_denoising = True
scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scn.cycles.max_bounces = 6
scn.cycles.diffuse_bounces = 3
scn.cycles.glossy_bounces = 4
scn.cycles.transmission_bounces = 6
scn.render.resolution_x = 2560
scn.render.resolution_y = 1440
scn.render.image_settings.file_format = 'JPEG'
scn.render.image_settings.quality = 96

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

for o in bpy.data.objects:
    o.animation_data_clear()
    o.delta_location = Vector((0, 0, 0))
    o.delta_rotation_euler = Euler((0, 0, 0), 'XYZ')
    o.delta_scale = Vector((1, 1, 1))
    if (
        o.name in (
            "Chassis_Glass_Back",
            "CAD_Laser_Scan_Plane",
            "Stepper_Crash_Cage",
            "Front_Upper_Stepper_DShaft",
            "Front_Lower_Stepper_DShaft",
            "Rear_Lower_Shaft_Axis_Marker",
            "V13_Plaque_TopLine",
            "Duo_Rear_Exploded_Axis_Guides",
            "Coiled_Tabletop_USBC_Cord",
            "Duo_Rear_Internal_USBC_Lead",
            "Duo_Rear_USBC_Strain_Boot",
            "USBC_Braided_Power_Cable",
        )
        or o.name.startswith("Dim_")
    ):
        o.hide_render = True

for o in bpy.data.objects:
    if o.name.startswith("Duo_Rear") and o.name not in (
        "Duo_Rear_Exploded_Axis_Guides",
        "Duo_Rear_Internal_USBC_Lead",
        "Duo_Rear_USBC_Strain_Boot",
    ):
        o.hide_render = False
    if o.name.startswith("Duo_Rear_LED_Halo"):
        o.hide_render = False

typo = bpy.data.objects.get("CAD_Detail_01_Braun_Typography")
if typo:
    typo.hide_render = False
    typo.location = Vector((0.0, 0.0, 0.0))
    typo.delta_location = Vector((0.0, -0.080, 0.0))

bh = bpy.data.objects.get("SurfClock_Master_60fps_Rig_beach_hand")
ch = bpy.data.objects.get("SurfClock_Master_60fps_Rig_cond_hand")
if bh: bh.rotation_euler = (0.0, math.radians(52.0), 0.0)
if ch: ch.rotation_euler = (0.0, math.radians(24.0), 0.0)

# Set up True TE Cool Light Grey Matte PLA (RAL 7035 / Polymaker Ash Grey) on the Outer Frame (#1)
mat_bezel = bpy.data.materials.get("Live_Anodized_Alu")
if mat_bezel and mat_bezel.node_tree:
    nt_b = mat_bezel.node_tree
    for n in nt_b.nodes:
        if n.name == "Mix.001" and n.type == "MIX":
            # Distinct Cool Light-Slate Grey (linear RGB ~0.23-0.31 -> sRGB cool steel/slate grey)
            n.inputs[6].default_value = (0.21, 0.24, 0.28, 1.0)
            n.inputs[7].default_value = (0.27, 0.30, 0.35, 1.0)
        elif n.type == "TEX_NOISE":
            n.inputs["Scale"].default_value = 320.0
        elif n.type == "TEX_VORONOI":
            n.inputs["Scale"].default_value = 650.0
        elif n.type == "BUMP":
            # 0.1mm Fuzzy Skin micro-pebble texture on outer bezel
            n.inputs["Strength"].default_value = 0.36
            n.inputs["Distance"].default_value = 0.06
        elif n.type == "BSDF_PRINCIPLED":
            n.inputs["Metallic"].default_value = 0.0
            n.inputs["Roughness"].default_value = 0.56
            n.inputs["Diffuse Roughness"].default_value = 0.75
            n.inputs["Specular IOR Level"].default_value = 0.28
            n.inputs["Coat Weight"].default_value = 0.0

mat_dial = bpy.data.materials.get("Live_Plaster")
moat = bpy.data.objects.get("Front_Dial_Shadow_Moat")
if moat and mat_bezel:
    moat.data.materials.clear()
    moat.data.materials.append(mat_bezel)

# Frosted Translucent Clear/Smoke PLA Back Cover (#4) with Aligned-Rectilinear micro-lines
rc = bpy.data.objects.get("Duo_Rear_SurfClock_Master_60fps_Rig_RearCover")
if rc:
    rc.hide_render = False
    rc.location = Vector((0.0, 46.0, 0.0))
    mat_rc = bpy.data.materials.new("Mat_TE_Frosted_Translucent_Back_PLA_V2")
    mat_rc.use_nodes = True
    nt_rc = mat_rc.node_tree
    nt_rc.nodes.clear()

    out_rc = nt_rc.nodes.new("ShaderNodeOutputMaterial")
    bsdf_rc = nt_rc.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf_rc.inputs["Base Color"].default_value = (0.86, 0.90, 0.95, 1.0)
    bsdf_rc.inputs["Metallic"].default_value = 0.0
    bsdf_rc.inputs["Roughness"].default_value = 0.18
    bsdf_rc.inputs["IOR"].default_value = 1.46
    bsdf_rc.inputs["Transmission Weight"].default_value = 0.85
    bsdf_rc.inputs["Alpha"].default_value = 0.42
    bsdf_rc.inputs["Specular IOR Level"].default_value = 0.65
    bsdf_rc.inputs["Coat Weight"].default_value = 0.40
    bsdf_rc.inputs["Coat Roughness"].default_value = 0.08

    tex_coord = nt_rc.nodes.new("ShaderNodeTexCoord")
    mapping = nt_rc.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value = (0.0, 0.0, math.radians(45.0))
    wave = nt_rc.nodes.new("ShaderNodeTexWave")
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'X'
    wave.inputs["Scale"].default_value = 1.6
    wave.inputs["Distortion"].default_value = 0.0

    bump_rc = nt_rc.nodes.new("ShaderNodeBump")
    bump_rc.inputs["Strength"].default_value = 0.16
    bump_rc.inputs["Distance"].default_value = 0.06

    nt_rc.links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])
    nt_rc.links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    nt_rc.links.new(wave.outputs["Fac"], bump_rc.inputs["Height"])
    nt_rc.links.new(bump_rc.outputs["Normal"], bsdf_rc.inputs["Normal"])
    nt_rc.links.new(bsdf_rc.outputs["BSDF"], out_rc.inputs["Surface"])

    rc.data.materials.clear()
    rc.data.materials.append(mat_rc)

# Warm architectural studio backdrop so the Cool Light Grey bezel pops against the background
for wname, col in (
    ("Mat_V13_Sunlit_Plaster_Wall", (0.78, 0.76, 0.72, 1.0)),
    ("Mat_V13_Left_Shadow_Wall", (0.65, 0.63, 0.60, 1.0)),
    ("Mat_V13_Travertine_Desk", (0.72, 0.69, 0.64, 1.0)),
):
    mw = bpy.data.materials.get(wname)
    if mw and mw.node_tree:
        for n in mw.node_tree.nodes:
            if n.type == "MIX" and n.data_type == 'RGBA':
                n.inputs[6].default_value = (col[0]*0.88, col[1]*0.88, col[2]*0.88, 1.0)
                n.inputs[7].default_value = col

cam = scn.camera
cam.rotation_mode = 'QUATERNION'
cam.data.dof.use_dof = False
eye_duo = Vector((104.0, -560.0, 8.0))
tgt_duo = Vector((104.0, 0.0, -4.0))
cam.data.lens = 35.0
cam.location = eye_duo
cam.rotation_quaternion = (tgt_duo - eye_duo).normalized().to_track_quat('-Z', 'Y')

gobo = bpy.data.objects.get("V13_Venetian_Blinds_Gobo")
sun = bpy.data.objects.get("KeyLight_Grazing")
spec_strip = bpy.data.objects.get("Chamfer_Specular_Strip")

if gobo: gobo.hide_render = False
if spec_strip:
    spec_strip.hide_render = False
    spec_strip.data.energy = 2600.0
if sun:
    sun_dir_gh = Vector((-1.05, -1.20, 0.62)).normalized()
    sun.rotation_mode = 'QUATERNION'
    sun.rotation_quaternion = sun_dir_gh.to_track_quat('Z', 'Y')
    sun.data.energy = 7.5
    sun.data.angle = math.radians(2.2)
    sun.data.color = (1.0, 0.96, 0.90)

# OPTION 1: Cool Light Grey Bezel (#1) + Crisp Chalk White Dial (#2) + Frosted Translucent Back (#4)
if mat_dial and mat_dial.node_tree:
    for n in mat_dial.node_tree.nodes:
        if n.name == "Mix.001" and n.type == "MIX":
            n.inputs[6].default_value = (0.74, 0.75, 0.77, 1.0)
            n.inputs[7].default_value = (0.82, 0.83, 0.85, 1.0)
        elif n.type == "BSDF_PRINCIPLED":
            n.inputs["Roughness"].default_value = 0.45
            n.inputs["Specular IOR Level"].default_value = 0.32
            n.inputs["Coat Weight"].default_value = 0.0

out_opt1 = os.path.join(PROJECT_DIR, "render_te_cool_light_grey_bezel_white_dial_translucent_back.jpg")
scn.render.filepath = out_opt1
bpy.ops.render.render(write_still=True)

# OPTION 2: Full TE RAL 7035 Cool Light Grey Monolith (Both Bezel #1 AND Dial #2 in Cool Light Grey) + Frosted Translucent Back (#4)
if mat_dial and mat_dial.node_tree:
    for n in mat_dial.node_tree.nodes:
        if n.name == "Mix.001" and n.type == "MIX":
            n.inputs[6].default_value = (0.33, 0.36, 0.40, 1.0)
            n.inputs[7].default_value = (0.39, 0.43, 0.47, 1.0)
        elif n.type == "BSDF_PRINCIPLED":
            n.inputs["Roughness"].default_value = 0.48
            n.inputs["Specular IOR Level"].default_value = 0.30
            n.inputs["Coat Weight"].default_value = 0.0

out_opt2 = os.path.join(PROJECT_DIR, "render_te_all_cool_light_grey_monolith_translucent_back.jpg")
scn.render.filepath = out_opt2
bpy.ops.render.render(write_still=True)
print("Finished both Option 1 & Option 2 renders!")
