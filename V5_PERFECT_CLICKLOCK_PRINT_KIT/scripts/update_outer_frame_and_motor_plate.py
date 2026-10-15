import bpy
import bmesh
import math
import os

# ---------------------------------------------------------------------------
# PART 1: Update 1_Outer_Frame Corner Pillars (Shorter & Easier to Wedge/Snap)
# ---------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
orig_frame = "/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl"
bpy.ops.wm.stl_import(filepath=orig_frame)
frame = bpy.context.selected_objects[0]
frame.name = "Outer_Frame_ShortPillars"

def make_bm_obj(name, bm):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# First, remove the old bulky 10.3x10.3mm corner pillars inside the cavity
# from Z = 6.20 mm to Z = 49.02 mm, while preserving the outer cavity walls
# (|X| >= 111.30, |Y| >= 88.30) and the R=0.60mm cavity corner fillet!
# Wait: at the cavity corner (111.30, 88.30), the cavity wall has R=0.60mm fillet
# centered at (110.70, 87.70). If we cut out [100.0 .. 111.30] x [77.0 .. 88.30]
# with R=0.60mm outer corner at (111.30, 88.30) from Z = 6.20 to Z = 49.00,
# let's see: it cleanly removes the old pillar flush with the inner wall!
cut_objs = []
add_objs = []

for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # Create a cutter block that matches the inner cavity corner (|X|<=111.30, |Y|<=88.30, R=0.60 at outer corner)
        # from |X| = 99.0 to 111.30, |Y| = 76.0 to 88.30, Z = 6.20 to 49.00
        bm = bmesh.new()
        pts_2d = []
        # Outer corner fillet at (110.70, 87.70) with R = 0.60
        cx_f, cy_f, r_f = 110.70, 87.70, 0.60
        pts_2d.append((99.0, 76.0))
        pts_2d.append((111.30, 76.0))
        for i in range(17):
            ang = (0.5 * math.pi) * (i / 16.0)
            pts_2d.append((cx_f + r_f * math.cos(ang), cy_f + r_f * math.sin(ang)))
        pts_2d.append((99.0, 88.30))
        
        # Apply signs sx, sy
        signed_pts = [(sx * px, sy * py) for px, py in pts_2d]
        if sx * sy < 0:
            signed_pts = list(reversed(signed_pts))
        
        z0, z1 = 6.20, 49.00
        v_bot = [bm.verts.new((px, py, z0)) for px, py in signed_pts]
        v_top = [bm.verts.new((px, py, z1)) for px, py in signed_pts]
        bm.faces.new(list(reversed(v_bot)))
        bm.faces.new(v_top)
        n = len(signed_pts)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([v_bot[i], v_bot[j], v_top[j], v_top[i]])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        cut_objs.append(make_bm_obj(f"CutOldPillar_{sx}_{sy}", bm))

        # Now build the new SHORTER, EASY-WEDGE corner pillar!
        # What makes it super easy to wedge the Dial Plate (±111.0 x ±88.0 x 2.4mm) in from the back?
        # 1) Front retaining catch starts at Z = 6.65 mm (giving 0.25mm axial clearance behind Z=4.00..6.40mm dial plate!)
        # 2) At Z = 6.65 mm, it is a compact 45-degree corner triangular/chamfered catch extending from
        #    the corner (111.30, 88.30) inward to 107.20 on X and 84.20 on Y (so the diagonal edge goes from
        #    (107.20, 88.30) to (111.30, 84.20), midpoint at (109.25, 86.25) -> only 1.75mm x 1.75mm (2.5mm diagonal)
        #    overlap with the (111.0, 88.0) corner of the Dial Plate at Z = 6.65 mm!).
        # 3) From Z = 6.65 mm to Z = 9.50 mm, it slopes smoothly out to a compact 6.0mm x 6.0mm chamfered pillar
        #    (extending from (105.30, 88.30) to (111.30, 82.30) with a slight outer bulge to (106.8, 83.8) -> max 4.2mm
        #    overlap with the Dial Plate corner instead of 10.0mm!).
        # 4) It maintains this slim profile all the way up to Z = 49.00 mm, providing a rock-solid Z = 49.00 mm
        #    corner shelf for the Back Cover!
        def make_pillar_section(z_bot, z_top, d_bot, d_top, bulge_bot, bulge_top, tag):
            bm_p = bmesh.new()
            # Polygon in Q1:
            # Corner at (111.35, 88.35) (overlapping into wall by 0.05mm for clean boolean union, clipped at outer boundary)
            # Wait: to avoid protruding outside the inner wall, let's trace the exact R=0.60mm corner at (110.70, 87.70)!
            def get_loop(d, bulge):
                loop = []
                # Start at top wall (111.30 - d, 88.30)
                # Diagonal beveled inner face with smooth midpoint bulge:
                p_top = (111.30 - d, 88.30)
                p_right = (111.30, 88.30 - d)
                # 5 points along the rounded-bevel inner face from p_right to p_top:
                for k in range(9):
                    t = k / 8.0
                    # linear from p_right to p_top, pushed inward (toward -X, -Y) by sin(pi*t)*bulge
                    lx = p_right[0] * (1.0 - t) + p_top[0] * t - bulge * math.sin(math.pi * t)
                    ly = p_right[1] * (1.0 - t) + p_top[1] * t - bulge * math.sin(math.pi * t)
                    loop.append((lx, ly))
                # Now trace along the corner wall back to p_right via the R=0.60 corner fillet
                for i in range(8, -1, -1):
                    ang = (0.5 * math.pi) * (i / 8.0)
                    loop.append((110.70 + 0.62 * math.cos(ang), 87.70 + 0.62 * math.sin(ang)))
                return loop

            l_bot = get_loop(d_bot, bulge_bot)
            l_top = get_loop(d_top, bulge_top)
            s_bot = [(sx * px, sy * py) for px, py in l_bot]
            s_top = [(sx * px, sy * py) for px, py in l_top]
            if sx * sy < 0:
                s_bot = list(reversed(s_bot))
                s_top = list(reversed(s_top))
            vb = [bm_p.verts.new((px, py, z_bot)) for px, py in s_bot]
            vt = [bm_p.verts.new((px, py, z_top)) for px, py in s_top]
            bm_p.faces.new(list(reversed(vb)))
            bm_p.faces.new(vt)
            m = len(vb)
            for i in range(m):
                j = (i + 1) % m
                bm_p.faces.new([vb[i], vb[j], vt[j], vt[i]])
            bmesh.ops.recalc_face_normals(bm_p, faces=bm_p.faces)
            return make_bm_obj(tag, bm_p)

        # Lower snap-catch ramp: Z = 6.65 .. 9.50 mm
        # At Z = 6.65 mm: d = 4.20 mm, bulge = 0.60 mm -> midpoint at (108.6, 85.6), which overlaps the (111.0, 88.0) dial corner by 2.4mm x 2.4mm!
        # At Z = 9.50 mm: d = 5.60 mm, bulge = 1.00 mm -> midpoint at (107.5, 84.5), which overlaps the dial corner by 3.5mm x 3.5mm (vs 10.0mm before!)
        add_objs.append(make_pillar_section(6.65, 9.50, 4.20, 5.60, 0.60, 1.00, f"PillarRamp_{sx}_{sy}"))
        # Main shaft up to Z = 49.00 mm: d = 5.60 mm, bulge = 1.00 mm
        add_objs.append(make_pillar_section(9.50, 49.00, 5.60, 5.60, 1.00, 1.00, f"PillarShaft_{sx}_{sy}"))

# Apply Boolean DIFFERENCE to remove old pillars
bpy.ops.object.select_all(action='DESELECT')
for o in cut_objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = cut_objs[0]
bpy.ops.object.join()
all_cuts = bpy.context.active_object

mod_d = frame.modifiers.new(name="RemoveOldPillars", type='BOOLEAN')
mod_d.operation = 'DIFFERENCE'
mod_d.solver = 'EXACT'
mod_d.object = all_cuts
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod_d.name)
bpy.data.objects.remove(all_cuts, do_unlink=True)

# Apply Boolean UNION to add new shorter pillars
bpy.ops.object.select_all(action='DESELECT')
for o in add_objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = add_objs[0]
bpy.ops.object.join()
all_adds = bpy.context.active_object

mod_u = frame.modifiers.new(name="AddShortPillars", type='BOOLEAN')
mod_u.operation = 'UNION'
mod_u.solver = 'EXACT'
mod_u.object = all_adds
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier=mod_u.name)
bpy.data.objects.remove(all_adds, do_unlink=True)

# Clean and verify manifoldness
bm = bmesh.new()
bm.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
bmesh.ops.triangulate(bm, faces=bm.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
non_m = [e for e in bm.edges if not e.is_manifold]
print(f"Updated 1_Outer_Frame: verts={len(bm.verts)}, faces={len(bm.faces)}, non_manifold={len(non_m)}")
bm.to_mesh(frame.data)
bm.free()

bpy.ops.object.select_all(action='DESELECT')
frame.select_set(True)
frame_paths = [
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
]
for p in frame_paths:
    bpy.ops.wm.stl_export(filepath=p, export_selected_objects=True)
    print("Exported:", p)

# ---------------------------------------------------------------------------
# PART 2: Ensure 3_Motor_Mount_Plate Clears Both Old & New Corner Pillars
# ---------------------------------------------------------------------------
for mp_src, mp_dsts in [
    (
        "/tmp/stl_backups/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/3_Motor_Mount_Plate_V3_ESP32_WiderClips_PilotHoles_PrusaMK4.stl",
        ],
    ),
    (
        "/tmp/stl_backups/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/3_Motor_Mount_Plate_V3_SCREWLESS_PrusaMK4.stl",
        ],
    ),
]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath=mp_src)
    mp = bpy.context.selected_objects[0]
    mp_cuts = []
    # Cut 10.3x10.3mm corner notches (|X| > 100.80, |Y| > 77.80) just like 3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4NEW.stl
    # so the motor plate drops straight in past ANY outer frame (old or new)!
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx * 106.5, sy * 83.5, 2.5))
            c = bpy.context.active_object
            c.scale = (11.4, 11.4, 10.0)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            mp_cuts.append(c)
    bpy.ops.object.select_all(action='DESELECT')
    for o in mp_cuts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = mp_cuts[0]
    bpy.ops.object.join()
    all_mp_cuts = bpy.context.active_object

    mod_mp = mp.modifiers.new(name="CornerNotches", type='BOOLEAN')
    mod_mp.operation = 'DIFFERENCE'
    mod_mp.solver = 'EXACT'
    mod_mp.object = all_mp_cuts
    bpy.context.view_layer.objects.active = mp
    bpy.ops.object.modifier_apply(modifier=mod_mp.name)
    bpy.data.objects.remove(all_mp_cuts, do_unlink=True)

    bm_m = bmesh.new()
    bm_m.from_mesh(mp.data)
    bmesh.ops.remove_doubles(bm_m, verts=bm_m.verts, dist=1e-4)
    bmesh.ops.triangulate(bm_m, faces=bm_m.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
    bmesh.ops.recalc_face_normals(bm_m, faces=bm_m.faces)
    non_m2 = [e for e in bm_m.edges if not e.is_manifold]
    print(f"Updated {os.path.basename(mp_src)}: verts={len(bm_m.verts)}, faces={len(bm_m.faces)}, non_manifold={len(non_m2)}")
    bm_m.to_mesh(mp.data)
    bm_m.free()

    bpy.ops.object.select_all(action='DESELECT')
    mp.select_set(True)
    for dst in mp_dsts:
        bpy.ops.wm.stl_export(filepath=dst, export_selected_objects=True)
        print("Exported:", dst)
