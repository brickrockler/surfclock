import bpy
import bmesh
import math
from mathutils import Vector, Euler, Matrix

bpy.context.preferences.view.show_splash = False
scn = bpy.context.scene

# Clear scene completely
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)

col_main = bpy.data.collections.new("SurfClock_001_EditMode_Modeling")
scn.collection.children.link(col_main)

def make_mat(name, rgba, rough=0.35):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = rough
    m.diffuse_color = rgba
    return m

mat_clay = make_mat("Mat_Studio_Clay_Grey", (0.76, 0.77, 0.79, 1.0), 0.38)
mat_dial = make_mat("Mat_Dial_WarmWhite", (0.95, 0.95, 0.93, 1.0), 0.28)
mat_dark = make_mat("Mat_Tick_Charcoal", (0.10, 0.10, 0.11, 1.0), 0.45)
mat_orange = make_mat("Mat_Hand_SignalOrange", (0.98, 0.30, 0.04, 1.0), 0.28)

# Single unified mesh object that stays in EDIT MODE 100% of the time (zero mode switching = zero flashing!)
me = bpy.data.meshes.new("SurfClock_001_CAD_Mesh")
obj = bpy.data.objects.new("SurfClock_001_CAD_Model", me)
obj.data.materials.append(mat_clay)    # slot 0: outer body
obj.data.materials.append(mat_dial)    # slot 1: recessed dial face
obj.data.materials.append(mat_dark)    # slot 2: ticks & bores
obj.data.materials.append(mat_orange)  # slot 3: Braun pointer hands
col_main.objects.link(obj)

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def ramp(val, t0, t1):
    if val <= t0:
        return 0.0
    if val >= t1:
        return 1.0
    return smooth((val - t0) / (t1 - t0))

def build_progressive_edit_bmesh(bm, sec):
    bm.clear()

    # -------------------------------------------------------------------------
    # STEP 1 (0..22s): Start with 40x40x30mm Cube -> Select & Drag Width (184), Height (230), Depth (48)
    #   0..2s:   Initial cube, select Left/Right faces
    #   2..8s:   Drag X width 45 -> 184 mm
    #   8..10s:  Select Top/Bottom faces
    #   10..16s: Drag Z height 45 -> 230 mm
    #   16..18s: Select Front/Back faces
    #   18..22s: Drag Y depth 24 -> 48 mm
    # -------------------------------------------------------------------------
    wx = 45.0 + (184.0 - 45.0) * ramp(sec, 2.0, 8.0)
    hz = 45.0 + (230.0 - 45.0) * ramp(sec, 10.0, 16.0)
    dy = 24.0 + (48.0 - 24.0) * ramp(sec, 18.0, 22.0)

    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= wx
        v.co.y = (v.co.y + 0.5) * dy
        v.co.z *= hz
        v.select = False
    for e in bm.edges:
        e.select = False
    for f in bm.faces:
        f.material_index = 0
        f.select = False

    if sec < 22.0:
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            if sec < 8.5 and abs(f.normal.x) > 0.8:
                f.select = True
                for v in f.verts:
                    v.select = True
                for e in f.edges:
                    e.select = True
            elif 8.5 <= sec < 16.5 and abs(f.normal.z) > 0.8:
                f.select = True
                for v in f.verts:
                    v.select = True
                for e in f.edges:
                    e.select = True
            elif sec >= 16.5 and abs(f.normal.y) > 0.8:
                f.select = True
                for v in f.verts:
                    v.select = True
                for e in f.edges:
                    e.select = True
        return

    # -------------------------------------------------------------------------
    # STEP 2 (22..38s): Select the 4 Corner Edges & Slowly Bevel (R = 0 -> 9mm, segs = 1 -> 8)
    #   22..25s: Select the 4 corner edges one by one
    #   25..33s: Pull bevel offset 0.1 -> 9.0 mm
    #   33..38s: Increase bevel segments 1 -> 8
    # -------------------------------------------------------------------------
    bm.edges.ensure_lookup_table()
    corner_edges = [e for e in bm.edges if abs(e.verts[0].co.y - e.verts[1].co.y) > dy * 0.8]
    if sec < 25.0:
        n_sel = int(1 + 3.99 * ramp(sec, 22.0, 24.5))
        for idx_e, e in enumerate(corner_edges[:n_sel]):
            e.select = True
            for v in e.verts:
                v.select = True
        return

    bev_r = 0.15 + 8.85 * ramp(sec, 25.0, 33.0)
    bev_segs = 1 if sec < 33.0 else max(1, int(1 + 7 * ramp(sec, 33.0, 37.5)))
    res_bev = bmesh.ops.bevel(bm, geom=corner_edges, offset=bev_r, segments=bev_segs, profile=0.5, affect='EDGES')
    if sec < 38.0:
        for f in res_bev.get("faces", []):
            f.select = True
            for e in f.edges:
                e.select = True
            for v in f.verts:
                v.select = True
        return

    # -------------------------------------------------------------------------
    # STEP 3 (38..58s): Select Front Face -> Inset Bezel Wall (7mm) -> Extrude Dial Recess Inward (-4.0mm)
    #   38..40s: Select front face (glows orange)
    #   40..48s: Inset bezel wall 0.1 -> 7.0 mm
    #   48..50s: Pause with inner dial face selected
    #   50..58s: Extrude inner dial face inward 0.0 -> +4.0 mm along Y
    # -------------------------------------------------------------------------
    bm.faces.ensure_lookup_table()
    front_faces = [f for f in bm.faces if f.normal.y < -0.85]
    if sec < 40.0:
        for f in front_faces:
            f.select = True
            for e in f.edges:
                e.select = True
            for v in f.verts:
                v.select = True
        return

    inset_t = 0.15 + 6.85 * ramp(sec, 40.0, 48.0)
    bmesh.ops.inset_region(bm, faces=front_faces, thickness=inset_t, depth=0.0, use_boundary=True)
    bm.faces.ensure_lookup_table()
    inner_dial_faces = [
        f for f in bm.faces
        if f.normal.y < -0.85 and all(abs(v.co.x) < (wx * 0.5 - inset_t * 0.6) for v in f.verts)
    ]
    recess_y = 4.0 * ramp(sec, 50.0, 57.5)
    if recess_y > 0.01 and inner_dial_faces:
        bmesh.ops.translate(
            bm,
            vec=Vector((0.0, recess_y, 0.0)),
            verts=list({v for f in inner_dial_faces for v in f.verts}),
        )
    for f in inner_dial_faces:
        f.material_index = 1 if sec >= 50.0 else 0
    if sec < 58.0:
        for f in inner_dial_faces:
            f.select = True
            for e in f.edges:
                e.select = True
            for v in f.verts:
                v.select = True
        return

    # -------------------------------------------------------------------------
    # STEP 4 (58..76s): Model Upper (+25.3) & Lower (-78.2) Stepper Shaft Bosses & Center Hubs
    #   58..67s: Upper shaft ring appears at Z=+25.3 and extrudes out from Y=4.0 to Y=1.5
    #   67..76s: Lower shaft ring appears at Z=-78.2 and extrudes out from Y=4.0 to Y=1.5
    # -------------------------------------------------------------------------
    for is_upper, cz, t_start, t_end, hub_r in [
        (True, 25.3, 58.0, 67.0, 5.6),
        (False, -78.2, 67.0, 76.0, 4.8),
    ]:
        if sec < t_start:
            continue
        p_hub = ramp(sec, t_start + 1.2, t_end - 0.5)
        depth_h = 0.2 + 2.4 * p_hub
        ret_c = bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=24,
            radius1=hub_r, radius2=hub_r * 0.90, depth=depth_h
        )
        active_now = (t_start <= sec < t_end)
        for v in ret_c["verts"]:
            x0, y0, z0 = v.co.x, v.co.y, v.co.z
            v.co = Vector((x0, 4.0 - depth_h * 0.5 - z0, cz + y0))
            v.select = active_now
        for f in bm.faces:
            if all(v in ret_c["verts"] for v in f.verts):
                f.material_index = 3 if p_hub > 0.8 else 2
                f.select = active_now
                if active_now:
                    for e in f.edges:
                        e.select = True
    if sec < 76.0:
        return

    # -------------------------------------------------------------------------
    # STEP 5 (76..108s): Slowly Model the Semicircular Scale Ticks One by One
    #   76..94s:  21 upper beach arc ticks (-76° to +76° around Z=+25.3) extruded in place
    #   94..108s: 13 lower condition arc ticks (-68° to +68° around Z=-78.2) extruded in place
    # -------------------------------------------------------------------------
    u_ticks = (sec - 76.0) / 18.0
    for i in range(21):
        t_i = 76.0 + i * (18.0 / 21.0)
        if sec < t_i:
            break
        p_t = ramp(sec, t_i, t_i + 0.8)
        ang = math.radians(-76.0 + i * (152.0 / 20.0))
        is_maj = (i % 5 == 0)
        L = (7.2 if is_maj else 4.0) * p_t
        W = 1.6 if is_maj else 0.85
        R_mid = 48.0
        ret = bmesh.ops.create_cube(bm, size=1.0)
        is_latest = (t_i <= sec < t_i + 0.95) and (sec < 94.5)
        for v in ret["verts"]:
            lx = v.co.x * W
            ly = 3.7 - (v.co.y + 0.5) * (0.65 * p_t)
            lz = R_mid + v.co.z * L
            rx = lx * math.cos(ang) + lz * math.sin(ang)
            rz = -lx * math.sin(ang) + lz * math.cos(ang)
            v.co = Vector((rx, ly, 25.3 + rz))
            v.select = is_latest
        for f in bm.faces:
            if all(v in ret["verts"] for v in f.verts):
                f.material_index = 2
                f.select = is_latest
                if is_latest:
                    for e in f.edges:
                        e.select = True

    if sec >= 94.0:
        for i in range(13):
            t_i = 94.0 + i * (14.0 / 13.0)
            if sec < t_i:
                break
            p_t = ramp(sec, t_i, t_i + 0.8)
            ang = math.radians(-68.0 + i * (136.0 / 12.0))
            is_maj = (i % 6 == 0)
            L = (5.6 if is_maj else 3.2) * p_t
            W = 1.4 if is_maj else 0.75
            R_mid = 26.5
            ret = bmesh.ops.create_cube(bm, size=1.0)
            is_latest = (t_i <= sec < t_i + 1.05) and (sec < 108.5)
            for v in ret["verts"]:
                lx = v.co.x * W
                ly = 3.7 - (v.co.y + 0.5) * (0.65 * p_t)
                lz = R_mid + v.co.z * L
                rx = lx * math.cos(ang) + lz * math.sin(ang)
                rz = -lx * math.sin(ang) + lz * math.cos(ang)
                v.co = Vector((rx, ly, -78.2 + rz))
                v.select = is_latest
            for f in bm.faces:
                if all(v in ret["verts"] for v in f.verts):
                    f.material_index = 2
                    f.select = is_latest
                    if is_latest:
                        for e in f.edges:
                            e.select = True

    if sec < 108.0:
        return

    # -------------------------------------------------------------------------
    # STEP 6 (108..138s): Slowly Extrude & Taper the Upper & Lower Braun Pointer Hands
    #   108..117s: Extrude upper pointer blade out from hub (0 -> 44mm)
    #   117..123s: Taper upper pointer tip width (3.4mm -> 1.1mm) & extrude tail
    #   123..132s: Extrude lower pointer blade out from hub (0 -> 24mm)
    #   132..138s: Taper lower pointer tip width (2.8mm -> 1.0mm)
    # -------------------------------------------------------------------------
    # Upper hand
    p_u_ext = ramp(sec, 108.5, 117.0)
    p_u_tap = ramp(sec, 117.0, 122.5)
    # Gentle sweep during final inspection (160..180s)
    sweep_u = -36.0 * math.sin(math.pi * ramp(sec, 162.0, 178.0)) if sec >= 162.0 else 0.0
    ang_u = math.radians(38.0 + sweep_u)
    len_u = 2.0 + 42.0 * p_u_ext
    tail_u = 1.0 + 6.5 * p_u_tap
    ret_uh = bmesh.ops.create_cube(bm, size=1.0)
    active_u = (108.0 <= sec < 123.0)
    for v in ret_uh["verts"]:
        u_z = v.co.z + 0.5
        w_base = 3.2
        w_tip = 3.2 - 2.0 * p_u_tap
        w_cur = w_base * (1.0 - u_z) + w_tip * u_z
        lx = v.co.x * w_cur
        ly = 1.7 + v.co.y * 1.2
        lz = -tail_u + u_z * (len_u + tail_u)
        rx = lx * math.cos(ang_u) + lz * math.sin(ang_u)
        rz = -lx * math.sin(ang_u) + lz * math.cos(ang_u)
        v.co = Vector((rx, ly, 25.3 + rz))
        v.select = active_u and (u_z > 0.5)
    for f in bm.faces:
        if all(v in ret_uh["verts"] for v in f.verts):
            f.material_index = 3
            if active_u:
                f.select = any((v.co.z - 25.3) > 10.0 or abs(v.co.x) > 5.0 for v in f.verts)
                if f.select:
                    for e in f.edges:
                        e.select = True

    # Lower hand
    if sec >= 123.0:
        p_l_ext = ramp(sec, 123.5, 132.0)
        p_l_tap = ramp(sec, 132.0, 137.5)
        sweep_l = 28.0 * math.sin(math.pi * ramp(sec, 162.0, 178.0)) if sec >= 162.0 else 0.0
        ang_l = math.radians(-28.0 + sweep_l)
        len_l = 2.0 + 22.0 * p_l_ext
        tail_l = 1.0 + 4.5 * p_l_tap
        ret_lh = bmesh.ops.create_cube(bm, size=1.0)
        active_l = (123.0 <= sec < 138.0)
        for v in ret_lh["verts"]:
            u_z = v.co.z + 0.5
            w_base = 2.6
            w_tip = 2.6 - 1.5 * p_l_tap
            w_cur = w_base * (1.0 - u_z) + w_tip * u_z
            lx = v.co.x * w_cur
            ly = 1.7 + v.co.y * 1.2
            lz = -tail_l + u_z * (len_l + tail_l)
            rx = lx * math.cos(ang_l) + lz * math.sin(ang_l)
            rz = -lx * math.sin(ang_l) + lz * math.cos(ang_l)
            v.co = Vector((rx, ly, -78.2 + rz))
            v.select = active_l and (u_z > 0.5)
        for f in bm.faces:
            if all(v in ret_lh["verts"] for v in f.verts):
                f.material_index = 3
                if active_l:
                    f.select = True
                    for e in f.edges:
                        e.select = True

    if sec < 138.0:
        return

    # -------------------------------------------------------------------------
    # STEP 7 (138..162s): Orbit to Rear Face -> Inset Rear Wall, Extrude Cavity & Motor Mount Rings
    #   138..142s: Orbit to rear & select back face
    #   142..149s: Inset rear bezel wall (0.2 -> 6.0mm)
    #   149..156s: Extrude internal rear cavity inward (0 -> -34.0mm)
    #   156..162s: Extrude dual 28BYJ-48 stepper motor mounting rings & V7 ESP32 cradle rails
    # -------------------------------------------------------------------------
    bm.faces.ensure_lookup_table()
    rear_faces = [f for f in bm.faces if f.normal.y > 0.85 and any(v.co.y > 46.0 for v in f.verts)]
    if sec < 142.0:
        for f in rear_faces:
            f.select = True
            for e in f.edges:
                e.select = True
            for v in f.verts:
                v.select = True
        return

    ins_rear = 0.2 + 5.8 * ramp(sec, 142.0, 149.0)
    bmesh.ops.inset_region(bm, faces=rear_faces, thickness=ins_rear, depth=0.0, use_boundary=True)
    bm.faces.ensure_lookup_table()
    inner_rear = [
        f for f in bm.faces
        if f.normal.y > 0.85 and all(abs(v.co.x) < (wx * 0.5 - ins_rear * 0.6) for v in f.verts)
    ]
    cav_d = 34.0 * ramp(sec, 149.0, 156.0)
    if cav_d > 0.05 and inner_rear:
        bmesh.ops.translate(
            bm,
            vec=Vector((0.0, -cav_d, 0.0)),
            verts=list({v for f in inner_rear for v in f.verts}),
        )
    if sec < 156.0:
        for f in inner_rear:
            f.select = True
            for e in f.edges:
                e.select = True
            for v in f.verts:
                v.select = True
        return

    # Extrude dual 28BYJ-48 motor mount cradles & V7 ESP32 rails inside rear cavity
    p_m = ramp(sec, 156.0, 162.0)
    ring_h = 0.2 + 9.5 * p_m
    active_m = (156.0 <= sec < 162.5)
    for cz in (17.3, -70.2):
        ret_m = bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=28,
            radius1=16.0, radius2=16.0, depth=ring_h
        )
        for v in ret_m["verts"]:
            x0, y0, z0 = v.co.x, v.co.y, v.co.z
            v.co = Vector((x0, 14.0 + ring_h * 0.5 + z0, cz + y0))
            v.select = active_m
        for f in bm.faces:
            if all(v in ret_m["verts"] for v in f.verts):
                f.material_index = 3
                f.select = active_m
                if active_m:
                    for e in f.edges:
                        e.select = True

    for rx_off in (-15.0, 15.0):
        ret_r = bmesh.ops.create_cube(bm, size=1.0)
        for v in ret_r["verts"]:
            v.co.x = 51.0 + rx_off + v.co.x * 2.5
            v.co.y = 14.0 + (v.co.y + 0.5) * (7.5 * p_m)
            v.co.z = 28.0 + v.co.z * 52.0
            v.select = active_m
        for f in bm.faces:
            if all(v in ret_r["verts"] for v in f.verts):
                f.material_index = 3
                f.select = active_m

state = {"sec": 0.0, "initialized": False}
CYCLE_SECONDS = 180.0  # 3 full minutes per modeling cycle (slow, calm, deliberate)
DT = 0.04              # 25fps smooth updates

def live_editmode_step():
    # Enter EDIT mode ONCE and stay in EDIT mode forever (never toggle mode_set again -> zero flashing!)
    if not state["initialized"]:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (True, True, True)
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for s in area.spaces:
                        if s.type == 'VIEW_3D':
                            s.shading.type = 'SOLID'
                            s.shading.light = 'STUDIO'
                            s.shading.color_type = 'MATERIAL'
                            s.show_gizmo = True
                            s.show_gizmo_navigate = True
                            s.overlay.show_overlays = True
                            s.overlay.show_floor = True
                            s.overlay.show_cursor = True
                            s.overlay.show_stats = True
                            s.overlay.show_wireframes = True
                            s.overlay.wireframe_opacity = 0.55
        state["initialized"] = True

    sec = state["sec"] % CYCLE_SECONDS
    state["sec"] += DT

    bm = bmesh.from_edit_mesh(obj.data)
    build_progressive_edit_bmesh(bm, sec)
    bm.normal_update()
    bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)

    # Calm, slow designer camera movement & 3D cursor placement
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for s in area.spaces:
                    if s.type == 'VIEW_3D':
                        r3d = s.region_3d
                        r3d.view_perspective = 'PERSP'
                        if sec < 58.0:
                            # Calm front three-quarter angle while proportioning & beveling
                            u = sec / 58.0
                            r3d.view_location = Vector((0.0, 18.0, 0.0))
                            yaw = math.radians(-26.0 + 36.0 * u)
                            pitch = math.radians(73.0)
                            r3d.view_distance = 390.0
                            scn.cursor.location = Vector((0.0, 0.0, 0.0))
                        elif sec < 138.0:
                            # Closer front focus while modeling shaft hubs, radial ticks & pointer hands
                            u = (sec - 58.0) / 80.0
                            z_target = 25.3 if (sec < 67.0 or (76.0 <= sec < 94.0) or (108.0 <= sec < 123.0)) else -55.0
                            # Smoothly interpolate view_location Z
                            cur_z = r3d.view_location.z
                            r3d.view_location = Vector((0.0, 6.0, cur_z * 0.92 + (z_target * 0.35) * 0.08))
                            yaw = math.radians(10.0 - 24.0 * u)
                            pitch = math.radians(78.0)
                            r3d.view_distance = 320.0
                            scn.cursor.location = Vector((0.0, 3.8, 25.3 if z_target > 0 else -78.2))
                        elif sec < 162.0:
                            # Smooth, slow orbit to rear cavity to inset & extrude rear pocket + motor cradles
                            u = ramp(sec, 138.0, 143.0)
                            u_pan = (sec - 138.0) / 24.0
                            r3d.view_location = Vector((0.0, 22.0, 0.0))
                            yaw = math.radians(-14.0 + 178.0 * u + 20.0 * u_pan)
                            pitch = math.radians(74.0)
                            r3d.view_distance = 375.0
                            scn.cursor.location = Vector((0.0, 14.0, 17.3))
                        else:
                            # Slow turntable orbit back to front while hands gently sweep
                            u = ramp(sec, 162.0, 167.0)
                            u_orb = (sec - 162.0) / 18.0
                            r3d.view_location = Vector((0.0, 16.0, 0.0))
                            yaw = math.radians(184.0 + 150.0 * u + 20.0 * u_orb)
                            pitch = math.radians(76.0)
                            r3d.view_distance = 370.0
                        r3d.view_rotation = Euler((pitch, 0.0, yaw), 'XYZ').to_quaternion()

    return DT

bpy.app.timers.register(live_editmode_step, first_interval=0.4)
