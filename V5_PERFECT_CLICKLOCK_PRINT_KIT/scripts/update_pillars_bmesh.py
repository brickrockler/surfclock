import bpy
import bmesh
import math
import os

for src, dsts in [
    (
        "/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl",
        ],
    ),
    (
        "/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
        [
            "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
            "/Users/jcolley/surf_clock/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl",
        ],
    ),
]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.stl_import(filepath=src)
    obj = bpy.context.selected_objects[0]

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)

    for v in bm.verts:
        ax, ay, z = abs(v.co.x), abs(v.co.y), v.co.z
        if 6.30 <= z <= 49.05 and 95.0 < ax <= 111.32 and 72.0 < ay <= 88.32:
            if ax >= 110.65 and ay >= 87.65:
                if z < 15.0:
                    v.co.z = z + 0.45
                continue
            sx = 1.0 if v.co.x > 0 else -1.0
            sy = 1.0 if v.co.y > 0 else -1.0
            dx = max(0.0, 111.30 - ax)
            dy = max(0.0, 88.30 - ay)
            # At the bottom tip (z == 6.40), pull it even closer into the corner (scale 0.35 -> ~1.9mm from wall)
            # so the lead-in ramp slopes smoothly from the corner outward as Z goes from 6.85 to 11.65 mm!
            scale_xy = 0.35 if z < 7.0 else 0.54
            new_ax = 111.30 - dx * scale_xy
            new_ay = 88.30 - dy * scale_xy
            v.co.x = sx * new_ax
            v.co.y = sy * new_ay
            if z < 15.0:
                v.co.z = z + 0.45

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    non_m = [e for e in bm.edges if not e.is_manifold]
    print(f"Updated {os.path.basename(src)}: verts={len(bm.verts)}, faces={len(bm.faces)}, non_manifold={len(non_m)}")
    bm.to_mesh(obj.data)
    bm.free()

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    for dst in dsts:
        bpy.ops.wm.stl_export(filepath=dst, export_selected_objects=True)
        print("  Exported:", dst)
