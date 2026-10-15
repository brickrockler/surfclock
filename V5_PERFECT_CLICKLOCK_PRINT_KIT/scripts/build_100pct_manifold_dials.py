import bpy
import bmesh
import math
import sys
sys.path.insert(0, "/Users/jcolley/surf_clock")
import build_v3_dial_faces_fast as bdf

def create_box_obj(name, x0, x1, y0, y1, z0, z1):
    bm = bmesh.new()
    verts = [
        bm.verts.new((x0, y0, z0)), bm.verts.new((x1, y0, z0)),
        bm.verts.new((x1, y1, z0)), bm.verts.new((x0, y1, z0)),
        bm.verts.new((x0, y0, z1)), bm.verts.new((x1, y0, z1)),
        bm.verts.new((x1, y1, z1)), bm.verts.new((x0, y1, z1)),
    ]
    for f in [(0,3,2,1), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (3,0,4,7)]:
        bm.faces.new([verts[i] for i in f])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def create_cone_obj(name, cx, cy, r1, r2, z0, z1, segs=64):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r1, radius2=r2, depth=(z1 - z0))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(cx, cy, 0.5 * (z0 + z1)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# 1. Build a 100% Manifold, Watertight Base Plate in Blender (221.5 x 175.5 x 2.40 mm, ZERO corner notches!)
bpy.ops.wm.read_factory_settings(use_empty=True)
base = create_box_obj("DialBase", -110.75, 110.75, -87.75, 87.75, 0.00, 2.40)
holes = []
for hname, hcx, hcy in [("Upper", -25.30, 0.0), ("Lower", 78.20, 0.0)]:
    holes.append(create_cone_obj(f"Chamfer_{hname}", hcx, hcy, 4.65, 3.90, -0.05, 0.70, segs=64))
    holes.append(create_cone_obj(f"Bore_{hname}", hcx, hcy, 3.90, 3.90, 0.65, 2.50, segs=64))

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = holes[0]
for o in holes:
    o.select_set(True)
bpy.ops.object.join()
all_holes = bpy.context.view_layer.objects.active

mod = base.modifiers.new(name="CutHoles", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = all_holes
bpy.context.view_layer.objects.active = base
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(all_holes, do_unlink=True)

bm = bmesh.new()
bm.from_mesh(base.data)
bmesh.ops.triangulate(bm, faces=bm.faces)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
non_mf = sum(1 for e in bm.edges if not e.is_manifold)
print("Clean Base Plate: verts=", len(bm.verts), "faces=", len(bm.faces), "non_manifold=", non_mf)

base_tris = []
for f in bm.faces:
    v = [tuple(vert.co) for vert in f.verts]
    base_tris.append((v[0], v[1], v[2]))
bm.free()

# Override make_clean_chamfered_dial_plate_tris with our 100% manifold base_tris!
bdf.make_clean_chamfered_dial_plate_tris = lambda *a, **kw: list(base_tris)

# Now rebuild all 3 dials and check watertightness of every component!
bdf.build_custom_dial_stl(
    ["LONG REEF", "QUEENSIE", "DEE WHY", "FRESHIE", "CURL CURL"],
    [
        "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2a_Dial_Face_NORTHERN_BEACHES_Queensie_M600_at_Z2.6mm_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl",
    ],
    label="2a Northern Beaches (Queensie)"
)
bdf.build_custom_dial_stl(
    ["BONDI", "MANLY", "BRONTE", "TAMARAMA", "MAROUBRA"],
    [
        "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2b_Dial_Face_SYDNEY_ICONS_Bondi_Bronte_M600_at_Z2.6mm_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/2_Dial_Face_V3_SYDNEY_ICONS_Bondi_Bronte_PrusaMK4.stl",
    ],
    label="2b Sydney Icons"
)
bdf.build_custom_dial_stl(
    ["BONDI", "TAMARAMA", "BRONTE", "COOGEE", "MAROUBRA"],
    [
        "/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/2c_Dial_Face_EASTERN_SUBURBS_Bondi_Coogee_M600_at_Z2.6mm_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
        "/Users/jcolley/surf_clock/2_Dial_Face_V3_EASTERN_SUBURBS_Bondi_Bronte_Coogee_PrusaMK4.stl",
    ],
    label="2c Eastern Suburbs"
)
