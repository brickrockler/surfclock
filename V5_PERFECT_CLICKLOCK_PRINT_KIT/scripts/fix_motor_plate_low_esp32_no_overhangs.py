with open("/tmp/build_audited_v5_all_parts.py") as f:
    code = f.read()

old_sec5_start = code.index("# 5. Audited Freenove ESP32-S3-WROOM Cradle")
old_sec5_end = code.index("# 6. Bottom-Right Spare / Battery / Breadboard Bay")

new_sec5 = """# 5. Sleek Low-Profile Freenove ESP32-S3-WROOM Cradle — MOVED UP 41 mm, ZERO ARCHWAYS!
#    - Identical low-profile height to your original V3 cradle (PCB rests at Z = 9.50 mm, low solid side walls at Z = 11.20 mm),
#      sitting flat on the Z = 0..3.0 mm base plate with two pin-row slots and a center window — NO elevated archway!
#    - Moved UP 41.0 mm (esp_x0 = +2.00 mm to esp_x1 = +59.50 mm, esp_yc = -51.00 mm) so you have 51.80 mm of wide-open
#      runway below the USB-C ports!
esp_x0, esp_x1 = 2.00, 59.50
esp_yc = -51.00
esp_y0, esp_y1 = esp_yc - 14.35, esp_yc + 14.35  # 28.70 mm inner width for Freenove ESP32-S3 PCB
z_esp_shelf = 9.50  # Exact same low-profile 9.50 mm PCB shelf height as your original V3 cradle!

# Cut two pin-row slots (for the two header rows at esp_yc ± 11.4 mm) and center weight-saving window through the Z=0..3mm plate
sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_L", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc - 13.80, esp_yc - 8.60, 1.8, -1.0, 5.0, segs_corner=6))
sub_objs.append(create_rounded_rect_obj("Sub_ESP_PinSlot_R", esp_x0 + 1.5, esp_x1 - 1.5, esp_yc + 8.60, esp_yc + 13.80, 1.8, -1.0, 5.0, segs_corner=6))
sub_objs.append(create_rounded_rect_obj("Sub_ESP_CenterWin", esp_x0 + 3.0, esp_x1 - 3.0, esp_yc - 5.60, esp_yc + 5.60, 2.2, -1.0, 5.0, segs_corner=6))

# Solid Low-Profile Side Guide Walls from Z = 2.50 to 11.20 mm (ZERO archways, ZERO bridges!)
# With an internal Z = 9.50 mm step (1.15 mm wide) that the PCB edges rest on!
add_objs.append(create_box_obj("ESP_WallY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0 - 2.20, esp_y0, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_WallY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))
# Internal PCB support ledges (Z = 2.50 to 9.50 mm, 1.15 mm wide along the inside of both walls, clearing the pin rows!)
add_objs.append(create_box_obj("ESP_LedgeY0", esp_x0 - 2.2, esp_x1 + 2.2, esp_y0, esp_y0 + 1.15, 2.50, z_esp_shelf))
add_objs.append(create_box_obj("ESP_LedgeY1", esp_x0 - 2.2, esp_x1 + 2.2, esp_y1 - 1.15, esp_y1, 2.50, z_esp_shelf))

# Top End-Stop Shoulders at esp_x0 (with 20.4 mm open center for the Freenove antenna tab!)
add_objs.append(create_box_obj("ESP_TopStop_L", esp_x0 - 2.20, esp_x0, esp_y0 - 2.20, esp_yc - 10.20, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_TopStop_R", esp_x0 - 2.20, esp_x0, esp_yc + 10.20, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))

# Bottom End-Stop Shoulders at esp_x1 (catching the outer corners while leaving 25.1 mm wide-open for BOTH USB-C plugs!)
add_objs.append(create_box_obj("ESP_BotStop_L", esp_x1, esp_x1 + 2.20, esp_y0 - 2.20, esp_y0 + 1.80, 2.50, z_esp_shelf + 1.70))
add_objs.append(create_box_obj("ESP_BotStop_R", esp_x1, esp_x1 + 2.20, esp_y1 - 1.80, esp_y1 + 2.20, 2.50, z_esp_shelf + 1.70))

# 4 Low-Profile 45-Degree Snap-Latch Clips on the Side Walls (Z = 9.50 to 12.30 mm)
for cx0, cx1 in [(esp_x0 + 6.0, esp_x0 + 14.0), (esp_x1 - 14.0, esp_x1 - 6.0)]:
    pts_esp_y0 = [
        (esp_y0 - 2.20, z_esp_shelf),
        (esp_y0, z_esp_shelf),
        (esp_y0, z_esp_shelf + 1.65),
        (esp_y0 + 0.55, z_esp_shelf + 2.20),
        (esp_y0 + 0.55, z_esp_shelf + 2.50),
        (esp_y0 - 0.30, z_esp_shelf + 3.10),
        (esp_y0 - 2.20, z_esp_shelf + 3.10),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY0_{cx0}", cx0, cx1, pts_esp_y0))
    pts_esp_y1 = [
        (esp_y1, z_esp_shelf),
        (esp_y1 + 2.20, z_esp_shelf),
        (esp_y1 + 2.20, z_esp_shelf + 3.10),
        (esp_y1 + 0.30, z_esp_shelf + 3.10),
        (esp_y1 - 0.55, z_esp_shelf + 2.50),
        (esp_y1 - 0.55, z_esp_shelf + 2.20),
        (esp_y1, z_esp_shelf + 1.65),
    ]
    add_objs.append(create_prism_profile_x(f"ESP_ClipY1_{cx0}", cx0, cx1, pts_esp_y1))

"""

code = code[:old_sec5_start] + new_sec5 + code[old_sec5_end:]

# Also make the cable arches 45-degree self-supporting so there are ZERO flat overhangs!
old_cables = """def make_cable_arch_x(name, x0, x1, yc, side_sign):
    s = side_sign
    yz = [
        (yc - s * 5.2, 2.5),
        (yc - s * 2.6, 2.5),
        (yc - s * 2.6, 5.8),
        (yc - s * 0.6, 7.8),
        (yc + s * 3.2, 7.8),
        (yc + s * 4.0, 6.8),
        (yc + s * 5.0, 6.8),
        (yc + s * 5.0, 8.8),
        (yc + s * 4.0, 9.6),
        (yc - s * 5.2, 9.6),
    ]
    if s < 0:
        yz = list(reversed(yz))
    return create_prism_profile_x(name, x0, x1, yz)

def make_cable_arch_y(name, y0, y1, xc, side_sign):
    s = side_sign
    xz = [
        (xc - s * 5.2, 2.5),
        (xc - s * 2.6, 2.5),
        (xc - s * 2.6, 5.8),
        (xc - s * 0.6, 7.8),
        (xc + s * 3.2, 7.8),
        (xc + s * 4.0, 6.8),
        (xc + s * 5.0, 6.8),
        (xc + s * 5.0, 8.8),
        (xc + s * 4.0, 9.6),
        (xc - s * 5.2, 9.6),
    ]
    if s > 0:
        xz = list(reversed(xz))
    return create_prism_profile_y(name, y0, y1, xz)"""

new_cables = """def make_cable_arch_x(name, x0, x1, yc, side_sign):
    s = side_sign
    yz = [
        (yc - s * 5.2, 2.5),
        (yc - s * 2.6, 2.5),
        (yc - s * 2.6, 4.4),
        (yc + s * 1.4, 8.4),
        (yc + s * 2.6, 7.2),
        (yc + s * 3.6, 8.2),
        (yc + s * 3.6, 9.4),
        (yc - s * 5.2, 9.4),
    ]
    if s < 0:
        yz = list(reversed(yz))
    return create_prism_profile_x(name, x0, x1, yz)

def make_cable_arch_y(name, y0, y1, xc, side_sign):
    s = side_sign
    xz = [
        (xc - s * 5.2, 2.5),
        (xc - s * 2.6, 2.5),
        (xc - s * 2.6, 4.4),
        (xc + s * 1.4, 8.4),
        (xc + s * 2.6, 7.2),
        (xc + s * 3.6, 8.2),
        (xc + s * 3.6, 9.4),
        (xc - s * 5.2, 9.4),
    ]
    if s > 0:
        xz = list(reversed(xz))
    return create_prism_profile_y(name, y0, y1, xz)"""

assert old_cables in code, "old_cables not found"
code = code.replace(old_cables, new_cables)

with open("/tmp/build_audited_v5_all_parts_low_esp32.py", "w") as f:
    f.write(code)
print("Successfully wrote /tmp/build_audited_v5_all_parts_low_esp32.py")
