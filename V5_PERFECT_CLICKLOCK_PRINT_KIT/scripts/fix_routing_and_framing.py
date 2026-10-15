with open("/Users/jcolley/surf_clock/render_real_3d_stl_chapters.py", "r") as f:
    code = f.read()

# 1. Tighten dial shaft holes to 5.6 x 5.6 mm so the Ø9.0mm hand hubs completely cover them in ch04/ch05!
old_holes = '''for sx0, sx1, sy0, sy1 in [
    (-110.8, -30.5, -87.8, 87.8),
    (-20.1,   73.0, -87.8, 87.8),
    ( 83.4,  110.8, -87.8, 87.8),
    (-30.5,  -20.1, -87.8, -5.2),
    (-30.5,  -20.1,   5.2, 87.8),
    ( 73.0,   83.4, -87.8, -5.2),
    ( 73.0,   83.4,   5.2, 87.8),
]:'''

new_holes = '''for sx0, sx1, sy0, sy1 in [
    (-110.8, -28.1, -87.8, 87.8),
    (-22.5,   75.4, -87.8, 87.8),
    ( 81.0,  110.8, -87.8, 87.8),
    (-28.1,  -22.5, -87.8, -2.8),
    (-28.1,  -22.5,   2.8, 87.8),
    ( 75.4,   81.0, -87.8, -2.8),
    ( 75.4,   81.0,   2.8, 87.8),
]:'''

assert old_holes in code, "old_holes not found"
code = code.replace(old_holes, new_holes, 1)

# 2. Route all wires strictly along the solid orange bridges & C-clips (zero motor collisions, zero window crossings!)
old_w_block = '''# 1) Motor 5-pin orthogonal ribbon leads (exiting blue motor block -> spine rib -> straight into inner white JST socket!)
w_mot_up = make_ortho_wire("W_Mot_Up", [
    (-5.5, 0.0, 16.5),
    (-5.5, -23.5, 11.8),
    (-30.0, -23.5, 11.8),
    (-30.0, -38.5, 14.8),
], mat_w_mot, radius=1.25)

w_mot_lo = make_ortho_wire("W_Mot_Lo", [
    (58.5, 0.0, 16.5),
    (58.5, 23.5, 11.8),
    (26.0, 23.5, 11.8),
    (26.0, 38.5, 14.8),
], mat_w_mot, radius=1.25)

# 2) Upper IN1-IN4 -> GPIO 4, 5, 6, 7 (parallel orthogonal ribbon along Y=-23.5 spine channel under C-clips!)
w_up_sig1 = make_ortho_wire("W_Up_Sig1", [
    (-16.5, -45.0, 14.5),
    (-2.0, -45.0, 11.5),
    (-2.0, -23.0, 11.5),
    (60.0, -23.0, 11.5),
    (60.0, -41.0, 16.8),
], mat_w_cyan, radius=0.82)

w_up_sig2 = make_ortho_wire("W_Up_Sig2", [
    (-16.5, -47.5, 14.5),
    (0.0, -47.5, 11.5),
    (0.0, -24.8, 11.5),
    (64.0, -24.8, 11.5),
    (64.0, -41.0, 16.8),
], mat_w_teal, radius=0.82)

# 3) Lower IN1-IN4 -> GPIO 15, 16, 17, 18 (routed along right spine Y=+25.5 through C-clip -> bottom solid bridge X=95.5 -> ESP32!)
w_lo_sig1 = make_ortho_wire("W_Lo_Sig1", [
    (39.5, 45.0, 14.5),
    (48.5, 45.0, 11.5),
    (48.5, 24.5, 11.5),
    (94.5, 24.5, 11.5),
    (94.5, -26.5, 11.5),
    (74.0, -26.5, 11.5),
    (74.0, -41.0, 16.8),
], mat_w_amber, radius=0.82)

w_lo_sig2 = make_ortho_wire("W_Lo_Sig2", [
    (39.5, 47.5, 14.5),
    (50.5, 47.5, 11.5),
    (50.5, 26.2, 11.5),
    (96.2, 26.2, 11.5),
    (96.2, -28.2, 11.5),
    (78.0, -28.2, 11.5),
    (78.0, -41.0, 16.8),
], mat_w_orange, radius=0.82)

# 4) 5V VBUS (Red) & GND (Dark Slate) orthogonal power bus along left spine -> ESP32 -> bottom bridge -> right spine!
w_pwr_5v = make_ortho_wire("W_Pwr_5V", [
    (-16.5, -51.0, 14.5),
    (2.2, -51.0, 11.2),
    (2.2, -21.2, 11.2),
    (86.0, -21.2, 11.2),
    (86.0, -41.0, 16.8),
    (86.0, -21.2, 11.2),
    (97.8, -21.2, 11.2),
    (97.8, 28.0, 11.2),
    (52.5, 28.0, 11.2),
    (52.5, 51.0, 11.2),
    (39.5, 51.0, 14.5),
], mat_w_red, radius=0.85)

w_pwr_gnd = make_ortho_wire("W_Pwr_GND", [
    (-16.5, -53.2, 14.5),
    (4.0, -53.2, 11.0),
    (4.0, -19.5, 11.0),
    (90.0, -19.5, 11.0),
    (90.0, -41.0, 16.8),
    (90.0, -19.5, 11.0),
    (99.5, -19.5, 11.0),
    (99.5, 29.8, 11.0),
    (54.5, 29.8, 11.0),
    (54.5, 53.2, 11.0),
    (39.5, 53.2, 14.5),
], mat_w_gnd, radius=0.85)'''

new_w_block = '''# 1) Motor 5-pin orthogonal ribbon leads (exiting blue motor block -> spine rib -> straight into inner white JST socket!)
w_mot_up = make_ortho_wire("W_Mot_Up", [
    (-5.5, 0.0, 16.5),
    (-5.5, -24.5, 11.8),
    (-30.0, -24.5, 11.8),
    (-30.0, -38.5, 14.8),
], mat_w_mot, radius=1.20)

w_mot_lo = make_ortho_wire("W_Mot_Lo", [
    (55.5, 0.0, 16.5),
    (53.0, 0.0, 12.0),
    (53.0, 31.5, 12.0),
    (26.0, 31.5, 12.0),
    (26.0, 38.5, 14.8),
], mat_w_mot, radius=1.20)

# 2) Upper IN1-IN4 -> GPIO 4, 5, 6, 7 (parallel orthogonal ribbon along Y=-23.5 spine channel under C-clips!)
w_up_sig1 = make_ortho_wire("W_Up_Sig1", [
    (-16.5, -45.0, 14.5),
    (-1.5, -45.0, 11.5),
    (-1.5, -22.5, 11.5),
    (58.0, -22.5, 11.5),
    (58.0, -41.0, 16.8),
], mat_w_cyan, radius=0.78)

w_up_sig2 = make_ortho_wire("W_Up_Sig2", [
    (-16.5, -47.2, 14.5),
    (0.2, -47.2, 11.5),
    (0.2, -24.2, 11.5),
    (62.0, -24.2, 11.5),
    (62.0, -41.0, 16.8),
], mat_w_teal, radius=0.78)

# 3) Lower IN1-IN4 -> GPIO 15, 16, 17, 18 (routed along right spine Y=+26.5 -> solid upper-mid bridge X=+4.5 -> left spine Y=-26.0 -> ESP32!)
w_lo_sig1 = make_ortho_wire("W_Lo_Sig1", [
    (39.5, 45.0, 14.5),
    (48.5, 45.0, 11.5),
    (48.5, 25.5, 11.5),
    (4.0,  25.5, 11.5),
    (4.0, -25.8, 11.5),
    (72.0, -25.8, 11.5),
    (72.0, -41.0, 16.8),
], mat_w_amber, radius=0.78)

w_lo_sig2 = make_ortho_wire("W_Lo_Sig2", [
    (39.5, 47.2, 14.5),
    (50.2, 47.2, 11.5),
    (50.2, 27.2, 11.5),
    (5.8,  27.2, 11.5),
    (5.8, -27.5, 11.5),
    (76.0, -27.5, 11.5),
    (76.0, -41.0, 16.8),
], mat_w_orange, radius=0.78)

# 4) 5V VBUS (Red) & GND (Dark Slate) orthogonal power bus along spine & upper-mid bridge
w_pwr_5v = make_ortho_wire("W_Pwr_5V", [
    (-16.5, -50.5, 14.5),
    (2.0, -50.5, 11.2),
    (2.0, -29.2, 11.2),
    (84.0, -29.2, 11.2),
    (84.0, -41.0, 16.8),
    (84.0, -29.2, 11.2),
    (7.5, -29.2, 11.2),
    (7.5,  28.8, 11.2),
    (51.8, 28.8, 11.2),
    (51.8, 50.5, 11.2),
    (39.5, 50.5, 14.5),
], mat_w_red, radius=0.80)

w_pwr_gnd = make_ortho_wire("W_Pwr_GND", [
    (-16.5, -52.8, 14.5),
    (3.5, -52.8, 11.0),
    (3.5, -31.0, 11.0),
    (88.0, -31.0, 11.0),
    (88.0, -41.0, 16.8),
    (88.0, -31.0, 11.0),
    (9.2, -31.0, 11.0),
    (9.2,  30.5, 11.0),
    (53.5, 30.5, 11.0),
    (53.5, 52.8, 11.0),
    (39.5, 52.8, 14.5),
], mat_w_gnd, radius=0.80)'''

assert old_w_block in code, "old_w_block not found"
code = code.replace(old_w_block, new_w_block, 1)

# 3. In ch05, pull the camera back slightly so the entire 184x230mm portrait monolith frame has generous studio breathing room!
old_ch05_cam = '''        cx = 24.0 * math.sin(0.22 * t)
        cy = -405.0 + 14.0 * math.cos(0.15 * t)
        cz = 6.0 + 8.0 * math.sin(0.18 * t)
        set_cam_look((cx, cy, cz), (0.0, 0.0, -2.0), lens=60.0)'''

new_ch05_cam = '''        cx = 22.0 * math.sin(0.22 * t)
        cy = -465.0 + 12.0 * math.cos(0.15 * t)
        cz = 8.0 + 6.0 * math.sin(0.18 * t)
        set_cam_look((cx, cy, cz), (0.0, 0.0, 0.0), lens=54.0)'''

assert old_ch05_cam in code, "old_ch05_cam not found"
code = code.replace(old_ch05_cam, new_ch05_cam, 1)

with open("/Users/jcolley/surf_clock/render_real_3d_stl_chapters.py", "w") as f:
    f.write(code)
print("Patched routing and ch05 framing")
