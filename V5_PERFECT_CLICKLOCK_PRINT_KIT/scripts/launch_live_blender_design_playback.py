import bpy
import bmesh
import os
import math
from mathutils import Vector, Euler, Matrix

MASTER_BLEND = "/Users/jcolley/surf_clock/SurfClock_V13_GoldenHour_Master.blend"
SAVE_BLEND = "/Users/jcolley/surf_clock/SurfClock_001_Live_Interactive_Design_Playback.blend"
STL_V7_PLATE = "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/NEWNEW3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl"
STL_4C_COVER = "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/4c_Back_Cover_FAST_1HR_CLEAR_WINDOW_PrusaMK4.stl"

bpy.context.preferences.view.show_splash = False
scn = bpy.context.scene

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)

WANTED = [
    "SurfClock_Master_60fps_Rig_bezel",
    "SurfClock_Master_60fps_Rig_dial_v2_flush",
    "Dial_Shadow_Moat_Backer",
    "CAD_Detail_01_Braun_Typography",
    "SurfClock_Master_60fps_Rig_beach_hand",
    "SurfClock_Master_60fps_Rig_cond_hand",
    "Front_Upper_Stepper_DShaft",
    "Front_Lower_Stepper_DShaft",
    "SurfClock_Master_60fps_Rig_Upper_Stepper_can",
    "SurfClock_Master_60fps_Rig_Upper_Stepper_ears",
    "SurfClock_Master_60fps_Rig_Upper_Stepper_boot",
    "SurfClock_Master_60fps_Rig_Upper_Stepper_m3_-17.5",
    "SurfClock_Master_60fps_Rig_Upper_Stepper_m3_17.5",
    "SurfClock_Master_60fps_Rig_Lower_Stepper_can",
    "SurfClock_Master_60fps_Rig_Lower_Stepper_ears",
    "SurfClock_Master_60fps_Rig_Lower_Stepper_boot",
    "SurfClock_Master_60fps_Rig_Lower_Stepper_m3_-17.5",
    "SurfClock_Master_60fps_Rig_Lower_Stepper_m3_17.5",
    "SurfClock_Master_60fps_Rig_ULN_Top",
    "SurfClock_Master_60fps_Rig_ULN_IC_22.0",
    "SurfClock_Master_60fps_Rig_ULN_XH_22.0",
    "SurfClock_Master_60fps_Rig_led_22.0_0",
    "SurfClock_Master_60fps_Rig_led_22.0_1",
    "SurfClock_Master_60fps_Rig_led_22.0_2",
    "SurfClock_Master_60fps_Rig_led_22.0_3",
    "SurfClock_Master_60fps_Rig_ULN_Bot",
    "SurfClock_Master_60fps_Rig_ULN_IC_-52.0",
    "SurfClock_Master_60fps_Rig_ULN_XH_-52.0",
    "SurfClock_Master_60fps_Rig_led_-52.0_0",
    "SurfClock_Master_60fps_Rig_led_-52.0_1",
    "SurfClock_Master_60fps_Rig_led_-52.0_2",
    "SurfClock_Master_60fps_Rig_led_-52.0_3",
    "SurfClock_Master_60fps_Rig_ESP32_S3",
    "SurfClock_Master_60fps_Rig_ESP32_Shield",
]

with bpy.data.libraries.load(MASTER_BLEND, link=False) as (data_from, data_to):
    data_to.objects = [name for name in WANTED if name in data_from.objects]

col_hud = bpy.data.collections.new("00_Viewport_Stage_HUD")
col_stage1 = bpy.data.collections.new("01_Stage1_Raw_Wireframe_Monolith")
col_stage2 = bpy.data.collections.new("02_Stage2_Outer_Frame_And_Dial_Plate")
col_stage3 = bpy.data.collections.new("03_Stage3_M600_Typography_And_Hands")
col_stage4 = bpy.data.collections.new("04_Stage4_V7_Motor_Mount_Plate_And_Steppers")
col_stage5 = bpy.data.collections.new("05_Stage5_ESP32_ULN2003_And_4c_Clear_Window_Back")
for c in (col_hud, col_stage1, col_stage2, col_stage3, col_stage4, col_stage5):
    scn.collection.children.link(c)

appended = {}
rest_transforms = {}
for obj in data_to.objects:
    if obj is None:
        continue
    obj.animation_data_clear()
    obj.parent = None
    obj.delta_location = Vector((0, 0, 0))
    obj.delta_rotation_euler = Euler((0, 0, 0), 'XYZ')
    obj.delta_scale = Vector((1, 1, 1))
    obj.hide_viewport = False
    obj.hide_set(False)
    appended[obj.name] = obj
    rest_transforms[obj.name] = (obj.location.copy(), Euler(obj.rotation_euler[:], 'XYZ'))

# Import actual V7 Click-Lock Motor Mount Plate STL
bpy.ops.wm.stl_import(filepath=STL_V7_PLATE)
carrier = bpy.context.active_object
carrier.name = "V7_Motor_Mount_Plate_ClickLock_PureRectLayer1"
for c in list(carrier.users_collection):
    c.objects.unlink(carrier)
M_plate = Matrix((
    (0, -1, 0, 0),
    (0,  0, 1, 14.0),
    (1,  0, 0, 0),
    (0,  0, 0, 1)
))
carrier.data.transform(M_plate)
carrier.data.update()
carrier.location = Vector((0, 0, 0))
mat_plate = bpy.data.materials.new("Mat_V7_Motor_Mount_Plate_Orange")
bsdf = mat_plate.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.95, 0.36, 0.08, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.32
carrier.data.materials.append(mat_plate)
appended[carrier.name] = carrier
rest_transforms[carrier.name] = (Vector((0, 0, 0)), Euler((0, 0, 0), 'XYZ'))

# Move ESP32_S3 and Shield into the V7 top-right cradle (STL X=+30, Y=-51 -> Scene X=+51, Z=+30)
for esp_name, y_off in [("SurfClock_Master_60fps_Rig_ESP32_S3", 23.5), ("SurfClock_Master_60fps_Rig_ESP32_Shield", 25.5)]:
    eo = appended.get(esp_name)
    if eo:
        eo.location = Vector((51.0, y_off, 28.0))
        rest_transforms[esp_name] = (eo.location.copy(), Euler(eo.rotation_euler[:], 'XYZ'))

# Import actual 4c Fast 1hr Clear Window Back Cover STL
bpy.ops.wm.stl_import(filepath=STL_4C_COVER)
rear_cover = bpy.context.active_object
rear_cover.name = "4c_Back_Cover_Fast_1Hr_Clear_Window"
for c in list(rear_cover.users_collection):
    c.objects.unlink(rear_cover)
M_cov = Matrix((
    (0, -1, 0, 0),
    (0,  0, -1, 46.5),
    (1,  0, 0, 0),
    (0,  0, 0, 1)
))
rear_cover.data.transform(M_cov)
rear_cover.data.update()
rear_cover.location = Vector((0, 0, 0))
mat_trans = bpy.data.materials.new("Mat_4c_Clear_Window_Cover")
bsdf = mat_trans.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.88, 0.92, 0.96, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.12
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = 0.30
rear_cover.data.materials.append(mat_trans)
rear_cover.color = (0.88, 0.92, 0.96, 0.30)
appended[rear_cover.name] = rear_cover
rest_transforms[rear_cover.name] = (Vector((0, 0, 0)), Euler((0, 0, 0), 'XYZ'))

bezel = appended.get("SurfClock_Master_60fps_Rig_bezel")
dial = appended.get("SurfClock_Master_60fps_Rig_dial_v2_flush")
moat = appended.get("Dial_Shadow_Moat_Backer")
typo = appended.get("CAD_Detail_01_Braun_Typography")
bh = appended.get("SurfClock_Master_60fps_Rig_beach_hand")
ch = appended.get("SurfClock_Master_60fps_Rig_cond_hand")
dshaft_u = appended.get("Front_Upper_Stepper_DShaft")
dshaft_l = appended.get("Front_Lower_Stepper_DShaft")

for o in (bezel, dial, moat):
    if o:
        col_stage2.objects.link(o)
if typo:
    for m in typo.modifiers:
        m.show_viewport = False
    col_stage3.objects.link(typo)
for o in (bh, ch, dshaft_u, dshaft_l):
    if o:
        col_stage3.objects.link(o)

stepper_objs = [carrier]
col_stage4.objects.link(carrier)
pcb_objs = []
for name, o in appended.items():
    if o in (bezel, dial, moat, typo, bh, ch, dshaft_u, dshaft_l, carrier, rear_cover):
        continue
    if "Stepper" in name:
        col_stage4.objects.link(o)
        stepper_objs.append(o)
    else:
        col_stage5.objects.link(o)
        pcb_objs.append(o)
col_stage5.objects.link(rear_cover)

# Create Stage 1 Raw Block
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=6, use_grid_fill=True)
me_blk = bpy.data.meshes.new("Mesh_Raw_Monolith_184x230x46mm")
bm.to_mesh(me_blk)
bm.free()
raw_block = bpy.data.objects.new("01_Raw_Monolith_184x230x46mm", me_blk)
raw_block.scale = Vector((184.0, 46.0, 230.0))
raw_block.location = Vector((0.0, 23.0, 0.0))
raw_block.show_wire = True
raw_block.show_all_edges = True
col_stage1.objects.link(raw_block)

# Create floating 3D HUD text above the clock
font_curve = bpy.data.curves.new(type="FONT", name="HUD_Stage_Text_Curve")
font_curve.body = "STAGE 1/6: RAW 184x230x52mm MONOLITH BLOCK"
font_curve.size = 9.0
font_curve.align_x = 'CENTER'
font_curve.extrude = 0.4
hud_obj = bpy.data.objects.new("HUD_Stage_Banner", font_curve)
hud_obj.location = Vector((0.0, 15.0, 132.0))
hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
mat_hud = bpy.data.materials.new("Mat_HUD_Orange")
bsdf_h = mat_hud.node_tree.nodes.get("Principled BSDF")
if bsdf_h:
    bsdf_h.inputs["Base Color"].default_value = (1.0, 0.35, 0.05, 1.0)
    if "Emission Color" in bsdf_h.inputs:
        bsdf_h.inputs["Emission Color"].default_value = (1.0, 0.35, 0.05, 1.0)
        bsdf_h.inputs["Emission Strength"].default_value = 1.5
hud_obj.data.materials.append(mat_hud)
col_hud.objects.link(hud_obj)

# Key sun lights
for idx_l, rot_deg in enumerate([(48, -22, 32), (65, 25, 145)]):
    ld = bpy.data.lights.new(f"Studio_Sun_{idx_l}", type='SUN')
    ld.energy = 3.8 if idx_l == 0 else 2.4
    lo = bpy.data.objects.new(f"Studio_Sun_{idx_l}", ld)
    lo.rotation_euler = Euler([math.radians(a) for a in rot_deg], 'XYZ')
    scn.collection.objects.link(lo)

TOTAL_FRAMES = 420
scn.frame_start = 1
scn.frame_end = TOTAL_FRAMES
scn.render.fps = 30

def smootherstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

def update_surfclock_build_frame(scene, depsgraph=None):
    f = scene.frame_current

    space3d = None
    r3d = None
    if bpy.context.window_manager:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for s in area.spaces:
                        if s.type == 'VIEW_3D':
                            space3d = s
                            r3d = s.region_3d
                            break

    raw_block.hide_viewport = True
    for o in (bezel, dial, moat, typo, bh, ch, dshaft_u, dshaft_l, rear_cover):
        if o:
            o.hide_viewport = True
    for o in stepper_objs + pcb_objs:
        o.hide_viewport = True

    # STAGE 1 (1..55): Raw Wireframe Block Extrusion
    if f <= 55:
        w = smootherstep((f - 1) / 48.0)
        raw_block.hide_viewport = False
        raw_block.scale = Vector((184.0, 46.0 * max(0.05, w), 230.0 * max(0.03, w)))
        raw_block.location = Vector((0.0, 23.0, -115.0 * (1.0 - w)))
        font_curve.body = "STAGE 1/6: EXTRUDING 184x230mm WIREFRAME MONOLITH"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
        if space3d:
            space3d.shading.type = 'WIREFRAME'
            space3d.shading.show_xray_wireframe = True
            space3d.overlay.show_wireframes = True

    # STAGE 2 (56..130): Carve Outer Frame & Drop In Flat Dial Faceplate
    elif f <= 130:
        w = smootherstep((f - 56) / 55.0)
        if bezel:
            bezel.hide_viewport = False
            bezel.location = Vector((0, 0, 0))
        if dial:
            dial.hide_viewport = False
            dial.location = Vector((0.0, -45.0 * (1.0 - w), 0.0))
        if moat and f >= 85:
            moat.hide_viewport = False
        font_curve.body = "STAGE 2/6: OUTER CLICK-LOCK FRAME & FLAT DIAL PLATE"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
        if space3d:
            space3d.shading.type = 'WIREFRAME' if f < 80 else 'SOLID'
            if f >= 80:
                space3d.shading.light = 'STUDIO'
                space3d.shading.color_type = 'OBJECT'
            space3d.overlay.show_wireframes = True
            space3d.overlay.wireframe_opacity = 0.55

    # STAGE 3 (131..210): Extrude +0.60mm M600 Typography & Drop In Capped Pointer Hands
    elif f <= 210:
        for o in (bezel, dial, moat, dshaft_u, dshaft_l):
            if o:
                o.hide_viewport = False
                o.location = rest_transforms[o.name][0].copy()
        if typo:
            typo.hide_viewport = False
            w_t = smootherstep((f - 131) / 35.0)
            typo.location = Vector((0.0, 0.8 * (1.0 - w_t), 0.0))
        if f >= 155:
            w_h = smootherstep((f - 155) / 45.0)
            if bh:
                bh.hide_viewport = False
                bh.location = Vector((0.0, 3.45 - 40.0 * (1.0 - w_h), 25.3))
                bh.rotation_euler = Euler((0, math.radians(-70.0 + 128.0 * w_h), 0), 'XYZ')
            if ch:
                ch.hide_viewport = False
                ch.location = Vector((0.0, 3.45 - 40.0 * (1.0 - w_h), -78.2))
                ch.rotation_euler = Euler((0, math.radians(-65.0 + 93.0 * w_h), 0), 'XYZ')
        font_curve.body = "STAGE 3/6: M600 RAISED TYPOGRAPHY & BRAUN POINTER HANDS"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
        if space3d:
            space3d.shading.type = 'SOLID'
            space3d.shading.light = 'STUDIO'
            space3d.shading.color_type = 'MATERIAL'
            space3d.overlay.show_wireframes = True
            space3d.overlay.wireframe_opacity = 0.35

    # STAGE 4 (211..290): Orbit to Rear — Assemble V7 Click-Lock Motor Mount Plate & Dual 28BYJ-48 Steppers
    elif f <= 290:
        for o in (bezel, dial, moat, typo, bh, ch, dshaft_u, dshaft_l):
            if o:
                o.hide_viewport = False
                o.location = rest_transforms[o.name][0].copy()
        w_s = smootherstep((f - 211) / 65.0)
        for idx_o, o in enumerate(stepper_objs):
            o.hide_viewport = False
            base_loc = rest_transforms[o.name][0]
            offset_y = (1.0 - w_s) * (55.0 + idx_o * 6.0)
            o.location = Vector((base_loc.x, base_loc.y + offset_y, base_loc.z))
        font_curve.body = "STAGE 4/6: V7 CLICK-LOCK MOTOR PLATE & 28BYJ-48 STEPPERS"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, math.pi), 'XYZ')
        if space3d:
            space3d.shading.type = 'MATERIAL'
            space3d.overlay.show_wireframes = True
            space3d.overlay.wireframe_opacity = 0.25

    # STAGE 5 (291..355): Drop In Dual ULN2003 Drivers, ESP32-S3 (Top-Right V7 Cradle) & 4c Clear Window Cover
    elif f <= 355:
        for o in (bezel, dial, moat, typo, bh, ch, dshaft_u, dshaft_l):
            if o:
                o.hide_viewport = False
                o.location = rest_transforms[o.name][0].copy()
        for o in stepper_objs:
            o.hide_viewport = False
            o.location = rest_transforms[o.name][0].copy()
        w_p = smootherstep((f - 291) / 40.0)
        for idx_o, o in enumerate(pcb_objs):
            o.hide_viewport = False
            base_loc = rest_transforms[o.name][0]
            offset_y = (1.0 - w_p) * (48.0 + idx_o * 4.0)
            o.location = Vector((base_loc.x, base_loc.y + offset_y, base_loc.z))
        if rear_cover and f >= 315:
            rear_cover.hide_viewport = False
            w_c = smootherstep((f - 315) / 35.0)
            base_loc = rest_transforms[rear_cover.name][0]
            rear_cover.location = Vector((base_loc.x, base_loc.y + (1.0 - w_c) * 65.0, base_loc.z))
        font_curve.body = "STAGE 5/6: ESP32-S3, ULN2003 DRIVERS & 4C CLEAR WINDOW BACK"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, math.pi), 'XYZ')
        if space3d:
            space3d.shading.type = 'MATERIAL'
            space3d.overlay.show_wireframes = False

    # STAGE 6 (356..420): Complete Hero Orbit & Live Pointer Hand Sweep
    else:
        for name, o in appended.items():
            o.hide_viewport = False
            o.location = rest_transforms[name][0].copy()
        w_f = smootherstep((f - 356) / 60.0)
        if bh:
            bh.rotation_euler = Euler((0, math.radians(58.0 - 95.0 * math.sin(math.pi * w_f)), 0), 'XYZ')
        if ch:
            ch.rotation_euler = Euler((0, math.radians(28.0 + 40.0 * math.sin(math.pi * w_f)), 0), 'XYZ')
        font_curve.body = "STAGE 6/6: SURF CLOCK 001 — COMPLETE V5/V7 CLICK-LOCK BUILD"
        hud_obj.rotation_euler = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
        if space3d:
            space3d.shading.type = 'MATERIAL'
            space3d.overlay.show_wireframes = False

    if r3d:
        r3d.view_perspective = 'PERSP'
        r3d.view_location = Vector((0.0, 12.0, 5.0))
        if f <= 200:
            u = (f - 1) / 199.0
            yaw = math.radians(-28.0 + 48.0 * u)
            pitch = math.radians(74.0 + 6.0 * math.sin(math.pi * u))
            dist = 395.0 - 35.0 * math.sin(math.pi * u)
        elif f <= 350:
            u = smootherstep((f - 200) / 45.0)
            u_rear = (f - 200) / 150.0
            yaw = math.radians(20.0 + 145.0 * u + 30.0 * u_rear)
            pitch = math.radians(74.0 + 5.0 * math.sin(math.pi * u_rear))
            dist = 380.0
        else:
            u = smootherstep((f - 350) / 65.0)
            yaw = math.radians(195.0 + 145.0 * u)
            pitch = math.radians(76.0)
            dist = 375.0
        r3d.view_rotation = Euler((pitch, 0.0, yaw), 'XYZ').to_quaternion()
        r3d.view_distance = dist

bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(update_surfclock_build_frame)
scn.frame_set(1)
update_surfclock_build_frame(scn)
bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)

def start_live_playback():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.show_gizmo = True
                        space.show_gizmo_navigate = True
                        space.overlay.show_overlays = True
                        space.overlay.show_floor = True
                        space.overlay.show_stats = True
    update_surfclock_build_frame(bpy.context.scene)
    if not bpy.context.screen.is_animation_playing:
        bpy.ops.screen.animation_play()
    return None

bpy.app.timers.register(start_live_playback, first_interval=0.5)
