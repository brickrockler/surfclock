import bpy
import bmesh
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

def add_box(name, x0, x1, y0, y1, z0, z1):
    cx, cy, cz = 0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1)
    sx, sy, sz = (x1-x0), (y1-y0), (z1-z0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

def add_cyl(name, cx, cy, z0, z1, r, vertices=48):
    cz = 0.5*(z0+z1)
    h = z1 - z0
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=h, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    return obj

def bool_op(target, cutters, op='DIFFERENCE'):
    for c in cutters:
        mod = target.modifiers.new(name=f"{op}_{c.name}", type='BOOLEAN')
        mod.operation = op
        mod.solver = 'EXACT'
        mod.object = c
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(c, do_unlink=True)

# -------------------------------------------------------------------------
# Build Split-Zone 1_Outer_Frame (removes dead middle pillar shaft Z=11.0..38.0mm,
# keeps front dial/motor seat & adds 45-deg self-supporting rear corner tabs at Z=38..49mm)
# -------------------------------------------------------------------------
bpy.ops.wm.stl_import(filepath="/tmp/stl_backups/1_Outer_Frame_V3_Tiny_Corner_Pilot_Holes_PrusaMK4.stl")
frame = bpy.context.selected_objects[0]
frame.name = "OuterFrame_V4_SplitZone"

cutters = []
unions = []
for sx in (-1.0, 1.0):
    for sy in (-1.0, 1.0):
        # Cut away the middle corner post between Z = 10.2 mm and Z = 38.0 mm
        # while leaving the outer wall (|X| >= 111.30, |Y| >= 88.30) completely untouched!
        x0 = 98.0 if sx > 0 else -111.28
        x1 = 111.28 if sx > 0 else -98.0
        y0 = 75.0 if sy > 0 else -88.28
        y1 = 88.28 if sy > 0 else -75.0
        cutters.append(add_box(f"CutMidPost_{sx}_{sy}", x0, x1, y0, y1, 10.20, 49.50))

        # Add clean 45-degree self-supporting rear corner boss (Z = 37.0 to 49.0 mm)
        # Tapering out from the wall at Z=37.0mm to a 6.0x6.0mm corner pad at Z=43..49mm
        bx0 = 105.30 if sx > 0 else -111.35
        bx1 = 111.35 if sx > 0 else -105.30
        by0 = 82.30 if sy > 0 else -88.35
        by1 = 88.35 if sy > 0 else -82.30
        boss = add_box(f"RearBoss_{sx}_{sy}", bx0, bx1, by0, by1, 37.00, 49.00)
        # Bevel the bottom inner edge at 45 degrees so it prints with zero supports!
        bm = bmesh.new()
        bm.from_mesh(boss.data)
        ix = 105.30 if sx > 0 else -105.30
        iy = 82.30 if sy > 0 else -82.30
        for v in bm.verts:
            if abs(v.co.z - 37.00) < 0.05:
                if abs(v.co.x - ix) < 0.05 or abs(v.co.y - iy) < 0.05:
                    v.co.x = 111.25 if sx > 0 else -111.25
                    v.co.y = 88.25 if sy > 0 else -88.25
        bm.normal_update()
        bm.to_mesh(boss.data)
        bm.free()
        unions.append(boss)

        # Tiny 1.8mm pilot hole in the rear boss (Z = 39.0 to 49.5 mm) at (107.8, 84.8)
        cutters.append(add_cyl(f"RearPilot_{sx}_{sy}", sx*107.80, sy*84.80, 39.00, 49.50, 0.90, 24))

bool_op(frame, cutters, 'DIFFERENCE')
bool_op(frame, unions, 'UNION')

bm = bmesh.new()
bm.from_mesh(frame.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
non_man = sum(1 for e in bm.edges if not e.is_manifold)
print(f"OuterFrame_V4_SplitZone: verts={len(bm.verts)}, faces={len(bm.faces)}, non_manifold={non_man}")
bm.to_mesh(frame.data)
bm.free()

for path in [
    "/Users/jcolley/surf_clock/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
    "/Users/jcolley/surf_clock/FINAL_PRINT_FILES/1_Outer_Frame_V4_SplitZone_OpenCavity_PrusaMK4.stl",
]:
    bpy.ops.object.select_all(action='DESELECT')
    frame.select_set(True)
    bpy.context.view_layer.objects.active = frame
    bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True)
    print("Exported:", path)
