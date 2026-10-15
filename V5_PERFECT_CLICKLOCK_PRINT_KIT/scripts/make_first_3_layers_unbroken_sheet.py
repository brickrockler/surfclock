with open("/tmp/build_audited_v5_all_parts_low_esp32.py") as f:
    code = f.read()

# 1. Remove the tiny 1.6mm pilot holes completely (solid Ø3.84mm motor ear pegs are stronger and have zero tiny circles!)
code = code.replace(
    'sub_objs.append(create_cyl_obj(f"Sub_{mname}_Pilot_{sy}", x_can, sy * 17.50, 0.80, -1.0, 8.0, segs=24))',
    '# Solid Ø3.84mm motor ear pegs (no tiny pilot hole needed!)'
)

# 2. Start all internal board relief pockets at Z = 0.60 mm (Layer 4) instead of Z = -1.0 mm!
#    That way Layers 1, 2, and 3 (Z = 0.00 to 0.60 mm) print as ONE UNBROKEN CONTINUOUS SHEET across the bed!
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Cut_TopWin", -96.0, -50.0, -74.0, 74.0, 4.0, -1.0, 5.0, segs_corner=8))',
    'sub_objs.append(create_rounded_rect_obj("Cut_TopWin", -96.0, -50.0, -74.0, 74.0, 4.0, 0.60, 5.0, segs_corner=8))'
)
code = code.replace(
    '2.0, -1.0, 3.8, segs_corner=6',
    '2.0, 0.60, 3.8, segs_corner=6'
)
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_L", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc - 13.10, esp_yc - 8.60, 1.8, -1.0, 5.0, segs_corner=6))',
    'sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_L", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc - 13.10, esp_yc - 8.60, 1.8, 0.60, 5.0, segs_corner=6))'
)
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_R", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc + 8.60, esp_yc + 13.10, 1.8, -1.0, 5.0, segs_corner=6))',
    'sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_R", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc + 8.60, esp_yc + 13.10, 1.8, 0.60, 5.0, segs_corner=6))'
)
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Sub_Bay2_Vent", b2_x0 + 4.0, b2_x1 - 4.0, b2_yc - 12.0, b2_yc + 12.0, 3.0, -1.0, 5.0, segs_corner=6))',
    'sub_objs.append(create_rounded_rect_obj("Sub_Bay2_Vent", b2_x0 + 4.0, b2_x1 - 4.0, b2_yc - 12.0, b2_yc + 12.0, 3.0, 0.60, 5.0, segs_corner=6))'
)

with open("/tmp/build_audited_v5_all_parts_low_esp32.py", "w") as f:
    f.write(code)
