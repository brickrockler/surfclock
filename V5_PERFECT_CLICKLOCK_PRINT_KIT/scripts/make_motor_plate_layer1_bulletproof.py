with open("/tmp/build_audited_v5_all_parts_low_esp32.py") as f:
    code = f.read()

# 1. Remove Sub_ESP_CenterWin so the middle of the ESP32 cradle is ONE wide 17.2mm solid bar on Layer 1 (instead of two skinny 3mm ribbons that peel up!)
code = code.replace(
    'sub_objs.append(create_rounded_rect_obj("Sub_ESP_CenterWin", esp_x0 + 3.0, esp_x1 - 3.0, esp_yc - 5.60, esp_yc + 5.60, 2.2, -1.0, 5.0, segs_corner=6))',
    '# Removed Sub_ESP_CenterWin so Layer 1 has a wide 17.2mm solid bed-adhesion pad instead of two skinny ribbons!'
)

# 2. Start the 4 tiny Ø1.6mm motor ear pilot holes at Z = 0.60 mm instead of Z = -1.0 mm so Layer 1-3 never prints tiny 1.6mm circles that catch on the nozzle!
code = code.replace(
    'create_cyl_obj(f"Sub_{mname}_EarPilot_{sy}", x_can, sy * 17.50, 0.80, -1.0, 7.0, segs=24)',
    'create_cyl_obj(f"Sub_{mname}_EarPilot_{sy}", x_can, sy * 17.50, 0.80, 0.60, 7.0, segs=24)'
)

with open("/tmp/build_audited_v5_all_parts_low_esp32.py", "w") as f:
    f.write(code)
