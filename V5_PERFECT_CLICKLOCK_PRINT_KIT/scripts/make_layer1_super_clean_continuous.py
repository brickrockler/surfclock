with open("/tmp/build_audited_v5_all_parts_low_esp32.py") as f:
    code = f.read()

# Remove Cut_MidWin and Cut_BotLeftWin completely so the nozzle sweeps long unbroken lines across the plate on Layer 1!
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Cut_MidWin", 14.0, 38.0, -18.0, 18.0, 3.0, -1.0, 5.0, segs_corner=8))',
    '# Removed Cut_MidWin for unbroken Layer 1 sweeps'
)
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Cut_BotLeftWin", 68.0, 89.0, -68.0, -36.0, 4.0, -1.0, 5.0, segs_corner=8))',
    '# Removed Cut_BotLeftWin (the exact hole in the user photo!) for unbroken Layer 1 sweeps'
)

with open("/tmp/build_audited_v5_all_parts_low_esp32.py", "w") as f:
    f.write(code)

with open("/tmp/upgrade_dials_motorplate_backcover_clicklock.py") as f:
    u_code = f.read()

# Make the 10 FlexSlots start at Z = 0.60 mm (Layer 4) instead of -1.0 mm, so Layer 1-3 has ZERO perimeter slots to snag!
u_code = u_code.replace(
    'flex_cuts.append(add_box_obj(f"FlexSlotY_{sy}_{xc}", xc - 8.5, xc + 8.5, y_slot_c - 0.9, y_slot_c + 0.9, -1.0, 10.0))',
    'flex_cuts.append(add_box_obj(f"FlexSlotY_{sy}_{xc}", xc - 8.5, xc + 8.5, y_slot_c - 0.9, y_slot_c + 0.9, 0.60, 10.0))'
)
u_code = u_code.replace(
    'flex_cuts.append(add_box_obj(f"FlexSlotX_{sx}_{yc}", x_slot_c - 0.9, x_slot_c + 0.9, yc - 8.5, yc + 8.5, -1.0, 10.0))',
    'flex_cuts.append(add_box_obj(f"FlexSlotX_{sx}_{yc}", x_slot_c - 0.9, x_slot_c + 0.9, yc - 8.5, yc + 8.5, 0.60, 10.0))'
)

with open("/tmp/upgrade_motorplate_only.py", "w") as f:
    # Keep only the motorplate section so it runs in 1 second without touching dials
    idx = u_code.index("# 2. ADD COMPLIANT PERIMETER CLICK-FLEX SLOTS")
    idx_end = u_code.index("# 3. UPGRADE 4_BACK_COVER")
    f.write("import bpy\nimport bmesh\n\ndef add_box_obj(name, x0, x1, y0, y1, z0, z1):\n    cx, cy, cz = 0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1)\n    sx, sy, sz = (x1-x0), (y1-y0), (z1-z0)\n    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))\n    obj = bpy.context.active_object\n    obj.name = name\n    obj.scale = (sx, sy, sz)\n    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)\n    return obj\n\n" + u_code[idx:idx_end])
