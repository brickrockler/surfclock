import bpy
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath="/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl")
back = bpy.context.selected_objects[0]

# Create a 45-degree beveled internal window pocket from Z = 1.00 mm to Z = 3.10 mm
# Outer window frame stays 3.00 mm thick around the perimeter (|X| > 98.0 or |Y| > 75.0)
# Inside |X| < 98.0, |Y| < 75.0, it tapers at 45 degrees down to a crystal-clear 1.00 mm (4-layer) optical window!
bm = bmesh.new()
x_top, y_top, z_top = 98.0, 75.0, 3.05
x_bot, y_bot, z_bot = 95.95, 72.95, 1.00

vt = [
    bm.verts.new((-x_top, -y_top, z_top)),
    bm.verts.new(( x_top, -y_top, z_top)),
    bm.verts.new(( x_top,  y_top, z_top)),
    bm.verts.new((-x_top,  y_top, z_top)),
]
vb = [
    bm.verts.new((-x_bot, -y_bot, z_bot)),
    bm.verts.new(( x_bot, -y_bot, z_bot)),
    bm.verts.new(( x_bot,  y_bot, z_bot)),
    bm.verts.new((-x_bot,  y_bot, z_bot)),
]
bm.faces.new(vt)
bm.faces.new(list(reversed(vb)))
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new([vb[i], vb[j], vt[j], vt[i]])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
m_cut = bpy.data.meshes.new("WinCut")
bm.to_mesh(m_cut)
bm.free()
o_cut = bpy.data.objects.new("WinCut", m_cut)
bpy.context.collection.objects.link(o_cut)

mod = back.modifiers.new(name="CutClearWindow", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.solver = 'EXACT'
mod.object = o_cut
bpy.context.view_layer.objects.active = back
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(o_cut, do_unlink=True)

bm_b = bmesh.new()
bm_b.from_mesh(back.data)
bmesh.ops.remove_doubles(bm_b, verts=bm_b.verts, dist=1e-4)
bmesh.ops.triangulate(bm_b, faces=bm_b.faces)
bmesh.ops.recalc_face_normals(bm_b, faces=bm_b.faces)
non_mf = sum(1 for e in bm_b.edges if not e.is_manifold)
vol = bm_b.calc_volume() / 1000.0
print(f"4c Fast Clear-Window Back Cover: verts={len(bm_b.verts)}, faces={len(bm_b.faces)}, non_manifold={non_mf}, volume={vol:.1f} cm^3")
bm_b.to_mesh(back.data)
bm_b.free()

bpy.ops.object.select_all(action='DESELECT')
back.select_set(True)
bpy.ops.wm.stl_export(
    filepath="/Users/jcolley/surf_clock/V5_PERFECT_CLICKLOCK_PRINT_KIT/4c_Back_Cover_FAST_1HR_CLEAR_WINDOW_PrusaMK4.stl",
    export_selected_objects=True,
    ascii_format=False
)
