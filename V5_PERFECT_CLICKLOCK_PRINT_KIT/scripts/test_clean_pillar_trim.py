import bpy
import bmesh
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
orig_frame = "/tmp/stl_backups/1_Outer_Frame_MATTE_WHITE_PrusaMK4.stl"
bpy.ops.wm.stl_import(filepath=orig_frame)
frame = bpy.context.selected_objects[0]

def make_bm_obj(name, bm):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# 1. Fill old corner holes (at +/-104.50, +/-81.50, Z = 6.40..49.00) AND the floating pyramid bottom (Z = 6.40..11.20)
# Wait: in the original STL, between Z = 6.40 and Z = 11.20, the corner pillar had a 4-sided pyramid detached from the wall!
# Let's union a clean corner block from Z = 6.65 to Z = 49.00 anchored solidly to the corner walls (overlapping slightly into the wall by 0.4mm, i.e. up to 111.70 and 88.70, which is well inside the outer wall at 115.0 and 92.0!),
# after first cutting away the old inner pillar from Z = 6.00 to Z = 49.50 inside |X| <= 111.15, |Y| <= 88.15!
# WAIT: Why did our previous cut have non-manifold edges? ONLY because we tried to match the R=0.60 wall fillet!
# The frame wall is 3.70 mm thick (|X| = 111.30 .. 115.00, |Y| = 88.30 .. 92.00)!
# So if our new pillar extends to |X| = 112.00, |Y| = 89.00 (0.70 mm embedded inside the solid outer wall!) and Z = 6.65 .. 49.00,
# and our cutter removes the old pillar inside |X| <= 111.20, |Y| <= 88.20 from Z = 6.00 .. 49.05,
# let's see what happens!
bm_check = bmesh.new()
bm_check.from_mesh(frame.data)
non_m_orig = [e for e in bm_check.edges if not e.is_manifold]
print("Original frame non_manifold edges:", len(non_m_orig))
bm_check.free()

cut_objs = []
add_objs = []

for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # Cutter: removes everything of the old pillar inside |X| in [98.0 .. 111.32], |Y| in [75.0 .. 88.32], Z in [6.00 .. 49.05]
        # Wait: to avoid coplanarity with |X|=111.30, |Y|=88.30, let's let the cutter cut up to |X|=111.80, |Y|=88.80 from Z=6.00 to Z=49.05
        # ONLY where |X| > 100.5 and |Y| > 77.5, AND THEN add back the clean wall + shorter corner pillar from Z=6.00 to Z=49.05!
        # Even simpler: why not ONLY cut the inner part of the old pillar (without touching the wall at 111.30 or 88.30)?
        # Wait: in the old pillar, at Z = 6.40..11.20, the pyramid slopes away from the wall.
        # If we:
        # Step A: Union a solid corner filler from Z = 6.65 to Z = 49.00 that fills the gap between the pyramid and the wall (embedded to 112.0, 89.0) AND fills the old Ø2.85mm hole!
        # Step B: Subtract a clean diagonal cutter from Z = 6.00 to Z = 50.00 that trims the bottom below Z = 6.65 AND trims the inner protrusion along a smooth 45-degree bevel!
        
        # Let's build Step A (Solid Corner Pillar Block anchored in the wall from Z = 6.65 to Z = 48.98):
        # Wait: why did Z = 49.00 create non-manifold edges earlier? Because Z = 49.00 was coplanar with the existing Z = 49.00 face!
        # If our filler block goes from Z = 6.65 to Z = 49.00, and our diagonal cutter cuts from Z = 5.50 to Z = 50.00,
        # then any coplanar face at Z = 49.00 inside the cut region is completely sliced away by the Z = 5.50..50.00 cutter!
        bm_fill = bmesh.new()
        pts_fill = [
            (sx * 100.80, sy * 77.80),
            (sx * 112.00, sy * 77.80),
            (sx * 112.00, sy * 89.00),
            (sx * 100.80, sy * 89.00),
        ]
        if sx * sy < 0:
            pts_fill = list(reversed(pts_fill))
        vb = [bm_fill.verts.new((px, py, 6.65)) for px, py in pts_fill]
        vt = [bm_fill.verts.new((px, py, 49.00)) for px, py in pts_fill]
        bm_fill.faces.new(list(reversed(vb)))
        bm_fill.faces.new(vt)
        for i in range(4):
            j = (i + 1) % 4
            bm_fill.faces.new([vb[i], vb[j], vt[j], vt[i]])
        bmesh.ops.recalc_face_normals(bm_fill, faces=bm_fill.faces)
        add_objs.append(make_bm_obj(f"FillCorner_{sx}_{sy}", bm_fill))

        # Step B1: Bottom slot cutter from Z = 5.50 to Z = 6.65 (trims the old Z=6.40..6.65 pyramid tip, staying inside |X|<=111.00, |Y|<=88.00 so it never touches the walls!)
        bm_bot = bmesh.new()
        pts_bot = [
            (sx * 100.00, sy * 77.00),
            (sx * 111.00, sy * 77.00),
            (sx * 111.00, sy * 88.00),
            (sx * 100.00, sy * 88.00),
        ]
        if sx * sy < 0:
            pts_bot = list(reversed(pts_bot))
        vb2 = [bm_bot.verts.new((px, py, 5.50)) for px, py in pts_bot]
        vt2 = [bm_bot.verts.new((px, py, 6.65)) for px, py in pts_bot]
        bm_bot.faces.new(list(reversed(vb2)))
        bm_bot.faces.new(vt2)
        for i in range(4):
            j = (i + 1) % 4
            bm_bot.faces.new([vb2[i], vb2[j], vt2[j], vt2[i]])
        bmesh.ops.recalc_face_normals(bm_bot, faces=bm_bot.faces)
        cut_objs.append(make_bm_obj(f"CutBot_{sx}_{sy}", bm_bot))

        # Step B2: Diagonal bevel cutter from Z = 6.00 to Z = 50.00 that makes the corner pillar MUCH SHORTER!
        # Instead of sticking out to (101.0, 78.0) (10.3mm x 10.3mm), we slice off everything inside the 45-degree plane
        # passing from (105.50, 88.50) to (111.50, 82.50) (so the pillar only extends 5.8mm along each wall and 2.9mm diagonally from the corner!),
        # AND with a front lead-in chamfer from Z = 6.65 to Z = 9.50!
        # Let's do the main diagonal cut (Z = 6.00 to 50.00):
        bm_diag = bmesh.new()
        # Polygon in Q1 that covers (98, 75) up to the diagonal line from (105.50, 89.50) to (112.50, 82.50)
        # Wait: if it goes to 89.50 and 112.50, it would cut into the outer wall!
        # So we clip the polygon at x = 111.30 and y = 88.30? NO, to avoid coplanarity with x = 111.30 and y = 88.30,
        # notice that the old pillar ONLY sticks out along X in [101.0 .. 111.30] and Y in [78.0 .. 88.30]!
        # Where the old pillar meets the wall at y = 88.30 (for x in 101.0..105.5) and x = 111.30 (for y in 78.0..82.5),
        # if we keep a 5.8mm x 5.8mm square pillar [105.50 .. 111.30] x [82.50 .. 88.30] with a rounded inner corner at (105.50, 82.50),
        # wait: why did the old pillar touch the wall at x = 101.0..105.5? Because the old pillar started at x = 101.0!
        # If our FillCorner only fills [105.50 .. 112.00] x [82.50 .. 89.00], and we cut the old pillar for x < 105.50 or y < 82.50,
        # let's check where the old pillar touched the wall for x < 105.50: ONLY from Z = 11.20 to Z = 49.00!
        pass
