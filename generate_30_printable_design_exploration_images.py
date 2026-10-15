#!/usr/bin/env python3
"""
Generates 30 High-Resolution Printable Modern Industrial Design Exploration Images
for the Surf Clock (Zero external brand or product names anywhere):
  - 5 Printable 6-Up Studio Presentation Boards (Board_1 to Board_5)
  - 1 Master 30-Concept Wall Poster (00_MASTER_30_DESIGN_EXPLORATIONS_POSTER.jpg)
  - 30 Individual Printable Concept Cards (Concept_01.jpg .. Concept_30.jpg)
  - 30 Clean Unlabelled Concept Cards (Clean_01.jpg .. Clean_30.jpg)
"""

import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_DIR = "/Users/jcolley/surf_clock/DESIGN_EXPLORATION_30_PRINTABLE_IMAGES"
CARDS_DIR = os.path.join(OUT_DIR, "INDIVIDUAL_CARDS_WITH_LABELS")
CLEAN_DIR = os.path.join(OUT_DIR, "INDIVIDUAL_CARDS_NO_TEXT")
ART_DIR = "/Users/jcolley/.gemini/jetski/brain/992bd51c-2ff0-4406-a5d4-01b10de896ab"
os.makedirs(CARDS_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

def load_font(size, bold=False):
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    )
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def clamp_rgb(rgb):
    return tuple(max(0, min(255, int(round(c)))) for c in rgb)

def scale_rgb(rgb, factor, add=0):
    return clamp_rgb((rgb[0] * factor + add, rgb[1] * factor + add, rgb[2] * factor + add))

def poly_superellipse(cx, cy, rx, ry, n_exp=3.0, segs=120):
    pts = []
    for i in range(segs):
        a = 2.0 * math.pi * i / segs
        ca, sa = math.cos(a), math.sin(a)
        x = cx + rx * math.copysign(abs(ca) ** (2.0 / n_exp), ca)
        y = cy + ry * math.copysign(abs(sa) ** (2.0 / n_exp), sa)
        pts.append((x, y))
    return pts

def poly_chamfer_rect(cx, cy, w, h, ch):
    hw, hh = w * 0.5, h * 0.5
    c = min(ch, hw * 0.7, hh * 0.7)
    return [
        (cx - hw + c, cy - hh),
        (cx + hw - c, cy - hh),
        (cx + hw,     cy - hh + c),
        (cx + hw,     cy + hh - c),
        (cx + hw - c, cy + hh),
        (cx - hw + c, cy + hh),
        (cx - hw,     cy + hh - c),
        (cx - hw,     cy - hh + c),
    ]

def poly_trapezoid(cx, cy, w_top, w_bot, h):
    hwt, hwb, hh = w_top * 0.5, w_bot * 0.5, h * 0.5
    return [
        (cx - hwt, cy - hh),
        (cx + hwt, cy - hh),
        (cx + hwb, cy + hh),
        (cx - hwb, cy + hh),
    ]

def poly_arch(cx, cy, w, h, segs=72):
    hw, hh = w * 0.5, h * 0.5
    r = hw
    y_arc_center = cy - hh + r
    pts = []
    for i in range(segs + 1):
        a = math.pi + math.pi * i / segs
        pts.append((cx + r * math.cos(a), y_arc_center + r * math.sin(a)))
    pts.append((cx + hw, cy + hh))
    pts.append((cx - hw, cy + hh))
    return pts

def draw_3d_extruded_shape(canvas, draw_fn, base_rgb, depth_dx=8, depth_dy=12, shadow_blur=22, bevel_px=4):
    """Draws a studio-lit 3D industrial body with soft cast shadow, 3D side extrusion wall,
    top-left specular highlight bevel, and main body surface.
    """
    W, H = canvas.size
    # 1. Soft directional studio cast shadow
    sh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh_layer)
    draw_fn(sh_draw, dx=depth_dx + 12, dy=depth_dy + 20, fill=(18, 20, 24, 92))
    draw_fn(sh_draw, dx=depth_dx + 4,  dy=depth_dy + 7,  fill=(15, 17, 20, 68))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    canvas.alpha_composite(sh_layer)

    # 2. 3D Side Extrusion Wall
    side_rgb = scale_rgb(base_rgb, 0.72, -8)
    steps = max(abs(depth_dx), abs(depth_dy), 1)
    d = ImageDraw.Draw(canvas)
    for s in range(steps, 0, -1):
        ox = depth_dx * s / steps
        oy = depth_dy * s / steps
        draw_fn(d, dx=ox, dy=oy, fill=(*side_rgb, 255))

    # 3. Top-left specular highlight rim
    hi_rgb = scale_rgb(base_rgb, 1.08, 18)
    sh_bevel_rgb = scale_rgb(base_rgb, 0.82, -5)
    draw_fn(d, dx=bevel_px * 0.5, dy=bevel_px * 0.5, fill=(*sh_bevel_rgb, 255))
    draw_fn(d, dx=-bevel_px * 0.4, dy=-bevel_px * 0.4, fill=(*hi_rgb, 255))

    # 4. Main front face
    draw_fn(d, dx=0, dy=0, fill=(*base_rgb, 255))

def draw_recessed_well(canvas, draw_fn, dial_rgb, rim_depth=6):
    """Draws a sunken instrument cavity with realistic top-left inner cast shadow and bottom-right highlight."""
    d = ImageDraw.Draw(canvas)
    outer_shadow = scale_rgb(dial_rgb, 0.66, -16)
    bottom_hi = scale_rgb(dial_rgb, 1.06, 14)
    draw_fn(d, dx=2, dy=2, fill=(*bottom_hi, 255))
    draw_fn(d, dx=-2, dy=-2, fill=(*outer_shadow, 255))
    draw_fn(d, dx=0, dy=0, fill=(*dial_rgb, 255))

    W, H = canvas.size
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    draw_fn(md, dx=0, dy=0, fill=255)

    inv = Image.new("RGBA", (W, H), (15, 18, 22, 95))
    cut = ImageDraw.Draw(inv)
    draw_fn(cut, dx=rim_depth, dy=rim_depth + 3, fill=(0, 0, 0, 0))
    inv = inv.filter(ImageFilter.GaussianBlur(radius=max(3, rim_depth)))

    clipped = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    clipped.paste(inv, (0, 0), mask)
    canvas.alpha_composite(clipped)

def draw_centered_text(draw, x, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw * 0.5, y - th * 0.5 - bbox[1] * 0.2), text, font=font, fill=fill)

def draw_surf_dial_graphics(
    canvas,
    b_cx, b_cy, b_r,
    c_cx, c_cy, c_r,
    ink_rgb,
    hand_rgb,
    sec_hand_rgb=None,
    dial_style="ticks",
    hand_style="baton",
    beach_deg=-30.0,
    cond_deg=38.0,
    compact_labels=False,
):
    """Draws the 5 Northern Beaches compass dial + Conditions sub-dial + 3D shadowed pointer hands."""
    if sec_hand_rgb is None:
        sec_hand_rgb = hand_rgb
    d = ImageDraw.Draw(canvas)
    f_beach = load_font(int(max(12, round(b_r * (0.142 if not compact_labels else 0.128)))), bold=True)
    f_cond  = load_font(int(max(11, round(c_r * (0.188 if not compact_labels else 0.175)))), bold=True)

    # 1. Upper Beach Dial Chapter Ring / Ticks / Arcs
    beaches = [
        ("LONG REEF",  -90.0, 0.0, -1.0),
        ("DEE WHY",    -30.0, 1.0, -0.35),
        ("CURL CURL",   30.0, 1.0,  0.35),
        ("FRESHIE",    150.0, -1.0, 0.35),
        ("QUEENSIE",  -150.0, -1.0, -0.35),
    ]

    if dial_style in ("arc_caliper", "crosshair", "rehaut_ring", "telemetry"):
        bbox = [b_cx - b_r, b_cy - b_r, b_cx + b_r, b_cy + b_r]
        if dial_style == "arc_caliper":
            d.arc(bbox, start=145, end=35, fill=(*ink_rgb, 255), width=max(3, int(b_r * 0.038)))
        elif dial_style == "rehaut_ring":
            d.ellipse(bbox, outline=(*ink_rgb, 110), width=max(2, int(b_r * 0.025)))
            for deg in range(0, 360, 10):
                rad = math.radians(deg)
                r0 = b_r * (0.90 if deg % 30 == 0 else 0.94)
                d.line(
                    [(b_cx + r0 * math.cos(rad), b_cy + r0 * math.sin(rad)),
                     (b_cx + b_r * math.cos(rad), b_cy + b_r * math.sin(rad))],
                    fill=(*ink_rgb, 180), width=max(2, int(b_r * 0.02))
                )
        elif dial_style == "crosshair":
            d.line([(b_cx - b_r * 0.85, b_cy), (b_cx + b_r * 0.85, b_cy)], fill=(*ink_rgb, 75), width=2)
            d.line([(b_cx, b_cy - b_r * 0.85), (b_cx, b_cy + b_r * 0.85)], fill=(*ink_rgb, 75), width=2)
            d.ellipse([b_cx - b_r * 0.55, b_cy - b_r * 0.55, b_cx + b_r * 0.55, b_cy + b_r * 0.55], outline=(*ink_rgb, 85), width=2)
        elif dial_style == "telemetry":
            for r_step in (0.65, 0.98):
                rr = b_r * r_step
                d.arc([b_cx - rr, b_cy - rr, b_cx + rr, b_cy + rr], start=140, end=40, fill=(*ink_rgb, 130), width=2)

    # Main 5 Beach Ticks + Sub-Ticks + Typography
    for b_name, deg, x_bias, y_bias in beaches:
        rad = math.radians(deg)
        if dial_style == "dots":
            px = b_cx + b_r * 0.92 * math.cos(rad)
            py = b_cy + b_r * 0.92 * math.sin(rad)
            dr = max(3.5, b_r * 0.048)
            d.ellipse([px - dr, py - dr, px + dr, py + dr], fill=(*ink_rgb, 255))
        elif dial_style != "minimal":
            r_in = b_r * 0.82
            r_out = b_r * 0.98
            d.line(
                [(b_cx + r_in * math.cos(rad), b_cy + r_in * math.sin(rad)),
                 (b_cx + r_out * math.cos(rad), b_cy + r_out * math.sin(rad))],
                fill=(*ink_rgb, 255), width=max(3, int(b_r * 0.045))
            )

        # Position beach name cleanly outside the chapter ring
        if abs(x_bias) < 0.1:
            tx = b_cx
            ty = b_cy - b_r * (1.24 if not compact_labels else 1.18)
        else:
            tx = b_cx + x_bias * b_r * (1.42 if not compact_labels else 1.28)
            ty = b_cy + y_bias * b_r * (1.14 if not compact_labels else 1.05)
        draw_centered_text(d, tx, ty, b_name, f_beach, (*ink_rgb, 255))

    if dial_style in ("ticks", "rehaut_ring", "telemetry"):
        for sub_deg in (-120, -60, 0, 180):
            rad = math.radians(sub_deg)
            r_in, r_out = b_r * 0.89, b_r * 0.97
            d.line(
                [(b_cx + r_in * math.cos(rad), b_cy + r_in * math.sin(rad)),
                 (b_cx + r_out * math.cos(rad), b_cy + r_out * math.sin(rad))],
                fill=(*ink_rgb, 210), width=max(2, int(b_r * 0.03))
            )

    # 2. Lower Conditions Sub-Dial (180° Semi-Circular Gauge Arc + NAH / WORTH IT? / YEAH)
    c_bbox = [c_cx - c_r, c_cy - c_r, c_cx + c_r, c_cy + c_r]
    arc_w = max(3, int(c_r * 0.055))
    d.arc(c_bbox, start=180, end=360, fill=(*ink_rgb, 255), width=arc_w)
    for c_deg, t_len in [(180, 0.18), (225, 0.13), (270, 0.18), (315, 0.13), (360, 0.18)]:
        rad = math.radians(c_deg)
        r0 = c_r * (1.0 - t_len)
        r1 = c_r * 0.99
        d.line(
            [(c_cx + r0 * math.cos(rad), c_cy + r0 * math.sin(rad)),
             (c_cx + r1 * math.cos(rad), c_cy + r1 * math.sin(rad))],
            fill=(*ink_rgb, 255), width=max(2, int(c_r * 0.048))
        )
    nah_mult = 1.30 if not compact_labels else 1.25
    yeah_mult = 1.34 if not compact_labels else 1.28
    draw_centered_text(d, c_cx - c_r * nah_mult,  c_cy - c_r * 0.04, "NAH",       f_cond, (*ink_rgb, 255))
    draw_centered_text(d, c_cx + c_r * yeah_mult, c_cy - c_r * 0.04, "YEAH",      f_cond, (*ink_rgb, 255))
    draw_centered_text(d, c_cx,                   c_cy + c_r * 0.35, "WORTH IT?", f_cond, (*ink_rgb, 255))

    # 3. Render 3D Cast-Shadowed Pointer Hands
    W, H = canvas.size
    hand_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_layer   = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hand_layer)
    sd = ImageDraw.Draw(sh_layer)

    def draw_one_hand(draw_ctx, cx, cy, length, tail, ang_deg, col, width, ox=0.0, oy=0.0):
        rad = math.radians(ang_deg)
        ux, uy = math.cos(rad), math.sin(rad)
        px, py = -uy, ux
        x_tail, y_tail = cx + ox - ux * tail, cy + oy - uy * tail
        x_tip,  y_tip  = cx + ox + ux * length, cy + oy + uy * length

        if hand_style == "tapered":
            w0 = width * 0.68
            w1 = width * 0.24
            poly = [
                (x_tail - px * w0, y_tail - py * w0),
                (x_tip  - px * w1, y_tip  - py * w1),
                (x_tip  + ux * width * 0.4, y_tip + uy * width * 0.4),
                (x_tip  + px * w1, y_tip  + py * w1),
                (x_tail + px * w0, y_tail + py * w0),
            ]
            draw_ctx.polygon(poly, fill=col)
        elif hand_style == "lollipop":
            draw_ctx.line([(x_tail, y_tail), (x_tip, y_tip)], fill=col, width=int(width * 0.85))
            lr = width * 1.15
            lx, ly = cx + ox + ux * (length * 0.68), cy + oy + uy * (length * 0.68)
            draw_ctx.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=col)
        elif hand_style == "Counterweight_Block":
            draw_ctx.line([(x_tail, y_tail), (x_tip, y_tip)], fill=col, width=int(width * 0.85))
            bw = width * 1.1
            poly_b = [
                (x_tail - px * bw, y_tail - py * bw),
                (x_tail + ux * (tail * 0.55) - px * bw, y_tail + uy * (tail * 0.55) - py * bw),
                (x_tail + ux * (tail * 0.55) + px * bw, y_tail + uy * (tail * 0.55) + px * bw),
                (x_tail + px * bw, y_tail + py * bw),
            ]
            draw_ctx.polygon(poly_b, fill=col)
        else:
            # Classic sculpted baton with rounded ends
            draw_ctx.line([(x_tail, y_tail), (x_tip, y_tip)], fill=col, width=int(width))
            r_end = width * 0.48
            draw_ctx.ellipse([x_tail - r_end, y_tail - r_end, x_tail + r_end, y_tail + r_end], fill=col)
            draw_ctx.ellipse([x_tip - r_end,  y_tip - r_end,  x_tip + r_end,  y_tip + r_end],  fill=col)

        # Center sculpted multi-tier hub cap
        r_hub = width * 1.48
        draw_ctx.ellipse([cx + ox - r_hub, cy + oy - r_hub, cx + ox + r_hub, cy + oy + r_hub], fill=col)
        if ox == 0.0 and oy == 0.0:
            r_in = r_hub * 0.52
            cap_col = scale_rgb(col[:3], 1.12, 16) + (255,)
            draw_ctx.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=cap_col)

    w_main = max(6, int(b_r * 0.095))
    w_cond = max(5, int(c_r * 0.115))
    draw_one_hand(sd, b_cx, b_cy, b_r * 0.84, b_r * 0.24, beach_deg, (15, 18, 22, 88), w_main, ox=5, oy=8)
    draw_one_hand(sd, c_cx, c_cy, c_r * 0.76, c_r * 0.22, -180 + cond_deg, (15, 18, 22, 88), w_cond, ox=4, oy=7)
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.alpha_composite(sh_layer)

    draw_one_hand(hd, b_cx, b_cy, b_r * 0.84, b_r * 0.24, beach_deg, (*hand_rgb, 255), w_main)
    draw_one_hand(hd, c_cx, c_cy, c_r * 0.76, c_r * 0.22, -180 + cond_deg, (*sec_hand_rgb, 255), w_cond)
    canvas.alpha_composite(hand_layer)

# -----------------------------------------------------------------------------
# 30 Original Modern Industrial Design Concepts (Zero External Brand Names!)
# -----------------------------------------------------------------------------

CONCEPTS = [
    (1,  "ANGLED DESK WEDGE",           "18° Tilted Desktop Trapezoid • Side-by-Side Twin Instrument Basins • Top Calibration Bar"),
    (2,  "LOUVERED ACOUSTIC TOTEM",     "Upper Compass Basin • Lower Horizontal Acoustic Louver Grill • Flank Thumbwheel Crown"),
    (3,  "STEPPED PLINTH CONSOLE",      "Raised Upper Compass Plateau (+6mm) • Recessed Lower Datum Terrace • 3 Tactile Keys"),
    (4,  "CYLINDRICAL DRUM MONOLITH",   "Ø168mm Pure Circular Drum • Integrated Tangential Cradle Foot • Razor-Thin 3mm Bezel"),
    (5,  "CANTILEVERED FLOATING FACE",  "Front White Baffle Cantilevered 8mm Forward Off Recessed Matte-Charcoal Core"),
    (6,  "OFF-CENTER REEL BILLET",      "Machined Billet Block • Oversized Ø108mm Off-Center Beach Wheel • 4 Corner Hex Bosses"),
    (7,  "MODULAR INSTRUMENT DECK",     "Low-Profile Landscape Deck • Twin Sunken Circular Wells • Machined Right Carry Loop"),
    (8,  "FOLDED-SHEET CHASSIS",        "Bent-Sheet Industrial Frame in Signal Orange • Corner Fastener Rivets • Recessed Baffle"),
    (9,  "SLIM VERTICAL PILLAR",        "Narrow 108×214mm Desktop Tower • Top Rotary Encoder Drums • Vertically Stacked Dials"),
    (10, "ARCHITECTURAL FIN CUBE",      "Asymmetric Split Cube • Left Vertical Brise-Soleil Fin Array • Right Stacked Dials"),
    (11, "SKELETONIZED BRIDGE SLAB",    "Exposed Dual Stepper Motor Mounting Rings • Routed Wire Conduit Channels • Technical Grid"),
    (12, "STADIUM CAPSULE BINNACLE",    "Full-Radius Stadium Pill Silhouette • Deep Conical Twin Portholes • Central Racetrack Rib"),
    (13, "ASYMMETRIC TELEMETRY DECK",   "Left Main Compass Window • Right Vertical Mechanical Telemetry Strip & Status Scale"),
    (14, "CHAMFERED OCTAGON HALO",      "Precision 8-Sided Octagonal Outer Casing • Deep Circular Amphitheater Step"),
    (15, "FACETED STEALTH PRISM",       "Wide 45° Architectural Perimeter Chamfers • Deeply Recessed Octagonal Dial Vault"),
    (16, "PERFORATED RING SQUARE",      "Soft-Cornered Wall Square • Concentric Micro-Perforated Ring Array • Bottom Cord Channel"),
    (17, "SUPERELLIPSE TACTILE PEBBLE", "Continuous Mathematical Lamé Curve (n=3.0) • Pillowed Bezel • Dished Dual Basins"),
    (18, "ORTHOGONAL BAFFLE GRID",      "Raised 1.8mm Architectural Cross-Fins Dividing Face Into 6 Proportional Geometric Bays"),
    (19, "EXTRUDED U-CHANNEL BEAM",     "Raw Architectural U-Channel Profile • Vertical Side Rails Projecting Past Top & Bottom"),
    (20, "BORDERLESS CRATER MONOLITH",  "Zero Outer Bezel Lip • Multi-Stepped Conical Craters Carved Directly Into Solid Block"),
    (21, "TWIN-COWL DASHBOARD POD",     "Two Sculpted Cylindrical Instrument Hoods Rising Proudly From a Unified Base Chassis"),
    (22, "SPLIT-LEVEL TURRET CONSOLE",  "Stepped Lower Conditions Deck Crowned by an Elevated Circular Upper Compass Turret"),
    (23, "OFFSET BUMPER CHRONOGRAPH",   "Protective Left Structural Guard Rail • Offset Right-Hand Dual Circular Instrument Pods"),
    (24, "PARABOLIC FUNNEL CUBE",       "Deep Rounded Square Shell • 45° Conical Parabolic Reflector Funnel Around Dual Dials"),
    (25, "STACKED GEOMETRIC TOTEM",     "Three Stacked Primitives: Fluted Rectangular Base + Narrow Neck Waist + Circular Disc Head"),
    (26, "STEPPED RANGEFINDER PLATE",   "Stadium-End Instrument Body • Stepped Upper Metal Shoulder • Knurled Bezel Rings"),
    (27, "BULKHEAD PORTHOLE BAROGRAPH", "8 Perimeter Socket-Cap Bosses • Deep Graduated Rehaut Ring • High-Vis Storm Needle"),
    (28, "TECTONIC SPLIT-DATUM TOTEM",  "Horizontal V-Groove Shadow Canyon Separating Proud Upper Plane & Recessed Lower Plane"),
    (29, "COCKPIT ALTIMETER SQUARE",    "Chamfered Instrument-Panel Square • 4 Corner Lock Bosses • Raised Center Compass Ring"),
    (30, "HARMONIC ARCH PORTAL",        "Pure Semi-Circular Arched Top Concentric With Upper Compass + Squared Conditions Base"),
]

def render_concept_tile(concept_id, width=900, height=1120, include_caption=True):
    """Renders a single high-res studio concept card at hero scale (filling ~75% of the studio tile)
    with zero label-to-ring overlaps and zero external brand names.
    """
    # Render the clock on a tightly framed 1140 x 1180 studio stage so the clock fills ~74% of the frame!
    SW, SH = 1140, 1180
    stage = Image.new("RGBA", (SW, SH), (224, 222, 217, 255))
    d = ImageDraw.Draw(stage)

    cx = SW // 2
    cy = SH // 2 - 4

    # Palette definitions
    WHITE   = (243, 241, 236)
    CREAM   = (236, 231, 220)
    ALAB    = (228, 226, 220)
    SILVER  = (196, 200, 205)
    SLATE   = (112, 118, 126)
    CHARC   = (44, 47, 52)
    OBSID   = (30, 32, 36)
    NAVY    = (46, 68, 94)
    ORANGE  = (236, 90, 36)
    YELLOW  = (238, 176, 34)
    COBALT  = (48, 112, 196)
    SAND    = (210, 203, 190)
    RED_OR  = (222, 58, 42)

    cid = concept_id

    if cid == 1:
        # 01: Angled Desk Wedge (Landscape side-by-side twin basins)
        pts_o = poly_trapezoid(cx, cy + 12, 760, 825, 500)
        pts_i = poly_trapezoid(cx, cy + 12, 706, 768, 446)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in pts_o], fill=fill), WHITE, 10, 18)
        d.rounded_rectangle([cx - 140, cy - 262, cx + 140, cy - 238], radius=8, fill=(*ORANGE, 255))
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in pts_i], fill=fill), ALAB, 8)
        for wcx, wr in [(cx - 178, 178), (cx + 190, 152)]:
            draw_recessed_well(stage, lambda dr, dx, dy, fill, wcx=wcx, wr=wr: dr.ellipse([wcx - wr + dx, cy + 14 - wr + dy, wcx + wr + dx, cy + 14 + wr + dy], fill=fill), WHITE, 6)
        draw_surf_dial_graphics(stage, cx - 178, cy + 18, 86, cx + 190, cy + 36, 72, CHARC, ORANGE, dial_style="ticks", hand_style="tapered", compact_labels=True)

    elif cid == 2:
        # 02: Louvered Acoustic Totem
        d.rounded_rectangle([cx + 286, cy - 190, cx + 318, cy - 70], radius=10, fill=(*SILVER, 255), outline=(*SLATE, 255), width=3)
        for ky in range(cy - 180, cy - 75, 10):
            d.line([(cx + 290, ky), (cx + 314, ky)], fill=(*SLATE, 255), width=2)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 295 + dx, cy - 395 + dy, cx + 295 + dx, cy + 395 + dy], radius=36, fill=fill), WHITE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 266 + dx, cy - 366 + dy, cx + 266 + dx, cy + 366 + dy], radius=24, fill=fill), ALAB, 8)
        for ly in range(cy + 48, cy + 348, 22):
            d.rounded_rectangle([cx - 244, ly, cx + 244, ly + 10], radius=4, fill=(*SLATE, 115))
        # Large circular white window for conditions dial so NAH & YEAH sit 100% inside the circle
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 148 + dx, cy + 198 - 148 + dy, cx + 148 + dx, cy + 198 + 148 + dy], fill=fill), WHITE, 6)
        draw_surf_dial_graphics(stage, cx, cy - 130, 126, cx, cy + 220, 72, CHARC, ORANGE, dial_style="ticks", beach_deg=-30, compact_labels=True)

    elif cid == 3:
        # 03: Stepped Plinth Console (Obsidian base + raised Chalk White upper plateau)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 310 + dx, cy - 395 + dy, cx + 310 + dx, cy + 395 + dy], radius=28, fill=fill), OBSID)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 278 + dx, cy - 362 + dy, cx + 278 + dx, cy + 88 + dy], radius=18, fill=fill), WHITE, 5, 8, shadow_blur=14)
        for bx, bcol in [(cx - 190, SLATE), (cx - 130, SLATE), (cx + 190, ORANGE)]:
            d.ellipse([bx - 18, cy + 115 - 18, bx + 18, cy + 115 + 18], fill=(*bcol, 255))
        draw_surf_dial_graphics(stage, cx, cy - 130, 124, cx, cy + 258, 82, CHARC, ORANGE, sec_hand_rgb=YELLOW, dial_style="arc_caliper", beach_deg=30)
        draw_surf_dial_graphics(stage, cx, cy - 13000, 10, cx, cy + 258, 82, WHITE, YELLOW, dial_style="minimal")

    elif cid == 4:
        # 04: Cylindrical Drum Monolith (Ø168mm pure circular drum on tangential cradle foot)
        foot = poly_trapezoid(cx, cy + 305, 330, 450, 130)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in foot], fill=fill), SLATE, 8, 12)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 360 + dx, cy - 360 + dy, cx + 360 + dx, cy + 360 + dy], fill=fill), WHITE, 10, 16)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 330 + dx, cy - 330 + dy, cx + 330 + dx, cy + 330 + dy], fill=fill), ALAB, 10)
        # Generous lower circular well so NAH / YEAH sit cleanly inside
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 142 + dx, cy + 158 - 142 + dy, cx + 142 + dx, cy + 158 + 142 + dy], fill=fill), WHITE, 6)
        draw_surf_dial_graphics(stage, cx, cy - 90, 122, cx, cy + 178, 68, CHARC, ORANGE, dial_style="rehaut_ring", beach_deg=-150, compact_labels=True)

    elif cid == 5:
        # 05: Cantilevered Floating Face Console
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 265 + dx, cy - 355 + dy, cx + 265 + dx, cy + 355 + dy], radius=20, fill=fill), OBSID, 12, 18)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 315 + dx, cy - 400 + dy, cx + 315 + dx, cy + 400 + dy], radius=16, fill=fill), WHITE, 8, 14, shadow_blur=22)
        d.rounded_rectangle([cx - 292, cy - 376, cx + 292, cy + 376], radius=10, outline=(*CHARC, 210), width=4)
        draw_surf_dial_graphics(stage, cx, cy - 115, 130, cx, cy + 225, 84, CHARC, ORANGE, dial_style="ticks", hand_style="tapered", beach_deg=-30)

    elif cid == 6:
        # 06: Off-Center Reel Billet Block
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 315 + dx, cy - 395 + dy, cx + 315 + dx, cy + 395 + dy], radius=44, fill=fill), SILVER)
        for sx in (cx - 265, cx + 265):
            for sy in (cy - 345, cy + 345):
                d.regular_polygon((sx, sy, 18), n_sides=6, rotation=30, fill=(*CHARC, 255), outline=(*WHITE, 200))
                d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=(*SILVER, 255))
        # Off-center circular well with r=235 centered at (cx - 32, cy - 95)
        w_cx, w_cy, w_r = cx - 32, cy - 95, 232
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([w_cx - w_r + dx, w_cy - w_r + dy, w_cx + w_r + dx, w_cy + w_r + dy], fill=fill), OBSID, 10)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 255 + dx, cy + 155 + dy, cx + 255 + dx, cy + 335 + dy], radius=22, fill=fill), WHITE, 7)
        draw_surf_dial_graphics(stage, w_cx, w_cy + 6, 110, cx, cy + 262, 74, WHITE, ORANGE, dial_style="telemetry", compact_labels=True, beach_deg=30)
        draw_surf_dial_graphics(stage, w_cx, w_cy - 8000, 10, cx, cy + 262, 74, CHARC, ORANGE, dial_style="minimal", compact_labels=True)

    elif cid == 7:
        # 07: Modular Instrument Deck (Landscape deck + right machined lanyard handle loop)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx + 295 + dx, cy - 185 + dy, cx + 405 + dx, cy + 185 + dy], radius=28, fill=fill), SILVER, 8, 12)
        d.rounded_rectangle([cx + 328, cy - 142, cx + 374, cy + 142], radius=14, fill=(224, 222, 217, 255))
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 405 + dx, cy - 240 + dy, cx + 320 + dx, cy + 240 + dy], radius=32, fill=fill), SILVER, 10, 14)
        d.line([(cx - 10, cy - 235), (cx - 10, cy + 235)], fill=(*SLATE, 160), width=3)
        # Left well r=174 at cx-198; Right well r=146 at cx+155
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 198 - 174 + dx, cy - 174 + dy, cx - 198 + 174 + dx, cy + 174 + dy], fill=fill), WHITE, 8)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx + 155 - 146 + dx, cy - 146 + dy, cx + 155 + 146 + dx, cy + 146 + dy], fill=fill), WHITE, 8)
        draw_surf_dial_graphics(stage, cx - 198, cy + 4, 86, cx + 155, cy + 20, 70, CHARC, COBALT, sec_hand_rgb=ORANGE, dial_style="crosshair", compact_labels=True)

    elif cid == 8:
        # 08: Folded-Sheet Industrial Chassis (Signal Orange bent flanges + recessed white baffle)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 315 + dx, cy - 400 + dy, cx + 315 + dx, cy + 400 + dy], radius=14, fill=fill), ORANGE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 275 + dx, cy - 360 + dy, cx + 275 + dx, cy + 360 + dy], radius=10, fill=fill), WHITE, 10)
        for sy in range(cy - 280, cy + 300, 70):
            d.rounded_rectangle([cx - 305, sy - 16, cx - 285, sy + 16], radius=4, fill=(*CHARC, 220))
            d.rounded_rectangle([cx + 285, sy - 16, cx + 305, sy + 16], radius=4, fill=(*CHARC, 220))
        for sx in (cx - 245, cx + 245):
            for sy in (cy - 330, cy + 330):
                d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=(*ORANGE, 255), outline=(*CHARC, 220), width=3)
        draw_surf_dial_graphics(stage, cx, cy - 115, 128, cx, cy + 225, 84, CHARC, CHARC, sec_hand_rgb=ORANGE, dial_style="ticks", hand_style="Counterweight_Block", beach_deg=-90)

    elif cid == 9:
        # 09: Slim Vertical Pillar (Narrow tower + 3 top rotary encoder drums)
        for ex, ecol in [(cx - 120, SLATE), (cx, ORANGE), (cx + 120, SLATE)]:
            d.rounded_rectangle([ex - 36, cy - 442, ex + 36, cy - 388], radius=8, fill=(*ecol, 255))
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 238 + dx, cy - 402 + dy, cx + 238 + dx, cy + 402 + dy], radius=34, fill=fill), SILVER)
        # Upper well r=204 at cy-145; Lower well r=154 at cy+220
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 204 + dx, cy - 145 - 204 + dy, cx + 204 + dx, cy - 145 + 204 + dy], fill=fill), OBSID, 8)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 154 + dx, cy + 220 - 154 + dy, cx + 154 + dx, cy + 220 + 154 + dy], fill=fill), OBSID, 8)
        draw_surf_dial_graphics(stage, cx, cy - 140, 98, cx, cy + 238, 72, WHITE, ORANGE, dial_style="rehaut_ring", compact_labels=True, beach_deg=150)

    elif cid == 10:
        # 10: Architectural Fin Cube (Left vertical fin array + Right stacked dials)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 355 + dx, cy - 355 + dy, cx + 355 + dx, cy + 355 + dy], radius=22, fill=fill), WHITE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 325 + dx, cy - 325 + dy, cx - 125 + dx, cy + 325 + dy], radius=10, fill=fill), CHARC, 6)
        for fx in range(cx - 310, cx - 130, 22):
            d.rectangle([fx, cy - 322, fx + 9, cy + 322], fill=(*WHITE, 255))
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 102 + dx, cy - 325 + dy, cx + 325 + dx, cy + 325 + dy], radius=14, fill=fill), ALAB, 8)
        draw_surf_dial_graphics(stage, cx + 112, cy - 95, 102, cx + 112, cy + 210, 68, CHARC, ORANGE, dial_style="ticks", compact_labels=True, beach_deg=-30)

    elif cid == 11:
        # 11: Skeletonized Bridge Slab (Exposed stepper bridges & routed wire conduits outside text zone)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 315 + dx, cy - 400 + dy, cx + 315 + dx, cy + 400 + dy], radius=48, fill=fill), OBSID)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 284 + dx, cy - 370 + dy, cx + 284 + dx, cy + 370 + dy], radius=36, fill=fill), CHARC, 9)
        # Outer technical frame & vertical conduit traces well outside the beach labels (at cx ± 242)
        d.rounded_rectangle([cx - 248, cy - 335, cx + 248, cy + 335], radius=28, outline=(*ORANGE, 175), width=4)
        for mcy, mr in [(cy - 115, 58), (cy + 225, 42)]:
            d.ellipse([cx - mr, mcy - mr, cx + mr, mcy + mr], outline=(*ORANGE, 185), width=3)
            d.ellipse([cx - mr * 0.65, mcy - mr * 0.65, cx + mr * 0.65, mcy + mr * 0.65], outline=(*SLATE, 180), width=2)
            for ex in (cx - mr - 10, cx + mr + 10):
                d.line([(ex - 8, mcy), (ex + 8, mcy)], fill=(*ORANGE, 175), width=3)
                d.ellipse([ex - 5, mcy - 5, ex + 5, mcy + 5], fill=(*SILVER, 220))
        draw_surf_dial_graphics(stage, cx, cy - 115, 122, cx, cy + 225, 78, WHITE, RED_OR, sec_hand_rgb=WHITE, dial_style="telemetry", hand_style="lollipop", compact_labels=True, beach_deg=-150)

    elif cid == 12:
        # 12: Stadium Capsule Binnacle (Pure R=275 stadium pill + twin deep conical portholes)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 275 + dx, cy - 425 + dy, cx + 275 + dx, cy + 425 + dy], radius=275, fill=fill), WHITE)
        d.rounded_rectangle([cx - 242, cy - 392, cx + 242, cy + 392], radius=242, outline=(*SILVER, 255), width=6)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 216 + dx, cy - 150 - 216 + dy, cx + 216 + dx, cy - 150 + 216 + dy], fill=fill), OBSID, 12)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 158 + dx, cy + 232 - 158 + dy, cx + 158 + dx, cy + 232 + 158 + dy], fill=fill), OBSID, 10)
        draw_surf_dial_graphics(stage, cx, cy - 145, 104, cx, cy + 248, 72, WHITE, ORANGE, dial_style="arc_caliper", hand_style="lollipop", compact_labels=True, beach_deg=30)

    elif cid == 13:
        # 13: Asymmetric Telemetry Deck (Deep Navy chassis + Left main window + Right telemetry strip)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 320 + dx, cy - 395 + dy, cx + 320 + dx, cy + 395 + dy], radius=24, fill=fill), NAVY)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 285 + dx, cy - 355 + dy, cx + 155 + dx, cy + 95 + dy], radius=18, fill=fill), WHITE, 8)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx + 178 + dx, cy - 355 + dy, cx + 285 + dx, cy + 95 + dy], radius=12, fill=fill), OBSID, 6)
        for ty_bar in range(cy - 325, cy + 75, 24):
            bar_col = ORANGE if ty_bar < cy - 140 else (YELLOW if ty_bar < cy - 20 else SLATE)
            d.rounded_rectangle([cx + 198, ty_bar, cx + 265, ty_bar + 10], radius=3, fill=(*bar_col, 255))
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 285 + dx, cy + 122 + dy, cx + 285 + dx, cy + 355 + dy], radius=18, fill=fill), WHITE, 8)
        draw_surf_dial_graphics(stage, cx - 65, cy - 125, 110, cx, cy + 255, 82, CHARC, ORANGE, dial_style="crosshair", compact_labels=True, beach_deg=-30)

    elif cid == 14:
        # 14: Chamfered Octagon Halo Ring
        oct_o = poly_chamfer_rect(cx, cy, 680, 780, 165)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in oct_o], fill=fill), OBSID)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 305 + dx, cy - 325 + dy, cx + 305 + dx, cy + 285 + dy], fill=fill), WHITE, 12)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 142 + dx, cy + 155 - 122 + dy, cx + 142 + dx, cy + 155 + 122 + dy], fill=fill), ALAB, 6)
        draw_surf_dial_graphics(stage, cx, cy - 85, 120, cx, cy + 172, 68, CHARC, ORANGE, dial_style="rehaut_ring", hand_style="tapered", compact_labels=True, beach_deg=-90)

    elif cid == 15:
        # 15: Faceted Stealth Prism (Wide 45-degree perimeter chamfers)
        p_out = poly_chamfer_rect(cx, cy, 650, 800, 95)
        p_in  = poly_chamfer_rect(cx, cy, 515, 665, 68)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in p_out], fill=fill), SLATE)
        for (x0, y0), (x1, y1) in zip(p_out, p_in):
            d.line([(x0, y0), (x1, y1)], fill=(*CHARC, 180), width=3)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in p_in], fill=fill), WHITE, 10)
        draw_surf_dial_graphics(stage, cx, cy - 110, 118, cx, cy + 205, 76, CHARC, ORANGE, dial_style="ticks", hand_style="tapered", compact_labels=True, beach_deg=150)

    elif cid == 16:
        # 16: Perforated Ring Square (Concentric micro-perforated ring array cleanly framing the compass!)
        d.rounded_rectangle([cx - 18, cy + 340, cx + 18, cy + 445], radius=6, fill=(*SILVER, 255))
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 350 + dx, cy - 360 + dy, cx + 350 + dx, cy + 350 + dy], radius=72, fill=fill), WHITE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 316 + dx, cy - 326 + dy, cx + 316 + dx, cy + 316 + dy], radius=56, fill=fill), ALAB, 7)
        # Concentric acoustic perforation dots outside the beach names (r=192, 208, 224) so zero text overlap!
        for r_ring, n_dots in [(190, 44), (206, 50), (222, 56)]:
            for k in range(n_dots):
                rad = 2.0 * math.pi * k / n_dots
                px = cx + r_ring * math.cos(rad)
                py = (cy - 92) + r_ring * math.sin(rad)
                d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=(*SLATE, 155))
        draw_surf_dial_graphics(stage, cx, cy - 92, 98, cx, cy + 215, 70, CHARC, ORANGE, dial_style="dots", compact_labels=True, beach_deg=-30)

    elif cid == 17:
        # 17: Superellipse Tactile Pebble (Lamé curve n=3.0)
        peb_o = poly_superellipse(cx, cy, 335, 410, n_exp=2.8)
        peb_i = poly_superellipse(cx, cy, 285, 360, n_exp=2.8)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in peb_o], fill=fill), SAND, 10, 16, bevel_px=8)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in peb_i], fill=fill), WHITE, 10)
        draw_surf_dial_graphics(stage, cx, cy - 105, 122, cx, cy + 205, 76, CHARC, RED_OR, dial_style="dots", hand_style="baton", beach_deg=30)

    elif cid == 18:
        # 18: Orthogonal Baffle Grid Frame (Raised cross-fins framing the dials without crossing text)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 320 + dx, cy - 400 + dy, cx + 320 + dx, cy + 400 + dy], radius=16, fill=fill), WHITE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 290 + dx, cy - 370 + dy, cx + 290 + dx, cy + 370 + dy], radius=10, fill=fill), ALAB, 8)
        for gy in (cy - 305, cy + 88):
            d.rectangle([cx - 290, gy - 5, cx + 290, gy + 5], fill=(*WHITE, 255), outline=(*SILVER, 220), width=2)
        for gx in (cx - 232, cx + 232):
            d.rectangle([gx - 5, cy - 370, gx + 5, cy + 370], fill=(*WHITE, 255), outline=(*SILVER, 220), width=2)
        draw_surf_dial_graphics(stage, cx, cy - 105, 114, cx, cy + 235, 78, CHARC, ORANGE, dial_style="crosshair", compact_labels=True, beach_deg=-30)

    elif cid == 19:
        # 19: Extruded U-Channel Beam (Projecting vertical side flanges)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rectangle([cx - 285 + dx, cy - 380 + dy, cx + 285 + dx, cy + 380 + dy], fill=fill), WHITE)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 328 + dx, cy - 420 + dy, cx - 276 + dx, cy + 420 + dy], radius=6, fill=fill), SILVER, 8, 12)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx + 276 + dx, cy - 420 + dy, cx + 328 + dx, cy + 420 + dy], radius=6, fill=fill), SILVER, 8, 12)
        d.rectangle([cx - 276, cy + 80, cx + 276, cy + 92], fill=(*SILVER, 255))
        draw_surf_dial_graphics(stage, cx, cy - 115, 128, cx, cy + 235, 82, CHARC, ORANGE, dial_style="ticks", beach_deg=-90)

    elif cid == 20:
        # 20: Borderless Dual-Crater Monolith (Multi-stepped conical craters sized so all text sits inside inner flat basin)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 320 + dx, cy - 405 + dy, cx + 320 + dx, cy + 405 + dy], radius=28, fill=fill), WHITE)
        for ccy, r_outer in [(cy - 125, 248), (cy + 225, 165)]:
            for factor, col_step in [(1.0, ALAB), (0.88, (218, 216, 210)), (0.76, WHITE)]:
                rr = r_outer * factor
                draw_recessed_well(stage, lambda dr, dx, dy, fill, rr=rr, ccy=ccy: dr.ellipse([cx - rr + dx, ccy - rr + dy, cx + rr + dx, ccy + rr + dy], fill=fill), col_step, 6)
        draw_surf_dial_graphics(stage, cx, cy - 120, 98, cx, cy + 242, 66, CHARC, ORANGE, dial_style="minimal", hand_style="tapered", compact_labels=True, beach_deg=-30)

    elif cid == 21:
        # 21: Twin-Cowl Dashboard Binnacle (Two bold cylindrical instrument hoods rising from base)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 320 + dx, cy - 405 + dy, cx + 320 + dx, cy + 405 + dy], radius=56, fill=fill), RED_OR)
        for hcy, hr in [(cy - 125, 236), (cy + 225, 162)]:
            draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill, hcy=hcy, hr=hr: dr.ellipse([cx - hr + dx, hcy - hr + dy, cx + hr + dx, hcy + hr + dy], fill=fill), RED_OR, 8, 14, shadow_blur=18)
            r_in = hr - 24
            draw_recessed_well(stage, lambda dr, dx, dy, fill, hcy=hcy, r_in=r_in: dr.ellipse([cx - r_in + dx, hcy - r_in + dy, cx + r_in + dx, hcy + r_in + dy], fill=fill), OBSID, 12)
        draw_surf_dial_graphics(stage, cx, cy - 120, 104, cx, cy + 242, 70, WHITE, WHITE, sec_hand_rgb=YELLOW, dial_style="arc_caliper", compact_labels=True, beach_deg=30)

    elif cid == 22:
        # 22: Split-Level Turret Console (Lower rectangular deck + tall upper circular turret)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 325 + dx, cy + 45 + dy, cx + 325 + dx, cy + 395 + dy], radius=38, fill=fill), CREAM)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 285 + dx, cy + 85 + dy, cx + 285 + dx, cy + 355 + dy], radius=24, fill=fill), WHITE, 8)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 270 + dx, cy - 405 + dy, cx + 270 + dx, cy + 135 + dy], fill=fill), OBSID, 10, 16)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 236 + dx, cy - 371 + dy, cx + 236 + dx, cy + 101 + dy], fill=fill), CHARC, 10)
        draw_surf_dial_graphics(stage, cx, cy - 130, 114, cx, cy + 242, 82, WHITE, ORANGE, dial_style="rehaut_ring", compact_labels=True, beach_deg=-150)
        draw_surf_dial_graphics(stage, cx, cy - 13000, 10, cx, cy + 242, 82, CHARC, ORANGE, dial_style="minimal")

    elif cid == 23:
        # 23: Offset Bumper Chronograph (Left protective guard rail + offset right circular pods)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 340 + dx, cy - 380 + dy, cx - 250 + dx, cy + 380 + dy], radius=18, fill=fill), ORANGE, 8, 12)
        for by in (cy - 220, cy + 220):
            d.rectangle([cx - 260, by - 36, cx - 200, by + 36], fill=(*SLATE, 255))
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 215 + dx, cy - 400 + dy, cx + 330 + dx, cy + 400 + dy], radius=68, fill=fill), OBSID)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 182 + dx, cy - 366 + dy, cx + 296 + dx, cy + 366 + dy], radius=52, fill=fill), WHITE, 9)
        draw_surf_dial_graphics(stage, cx + 58, cy - 115, 114, cx + 58, cy + 225, 76, CHARC, ORANGE, dial_style="telemetry", compact_labels=True, beach_deg=-30)

    elif cid == 24:
        # 24: Parabolic Funnel Cube (Amber Yellow outer cube + 45-degree conical reflector funnel)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 355 + dx, cy - 380 + dy, cx + 355 + dx, cy + 380 + dy], radius=48, fill=fill), YELLOW)
        for r_f, col_f in [(315, (245, 210, 110)), (284, CREAM), (254, WHITE)]:
            draw_recessed_well(stage, lambda dr, dx, dy, fill, r_f=r_f: dr.ellipse([cx - r_f + dx, cy - r_f + dy, cx + r_f + dx, cy + r_f + dy], fill=fill), col_f, 7)
        draw_surf_dial_graphics(stage, cx, cy - 68, 102, cx, cy + 142, 62, CHARC, OBSID, sec_hand_rgb=ORANGE, dial_style="ticks", compact_labels=True, beach_deg=30)

    elif cid == 25:
        # 25: Stacked Geometric Totem (Fluted base + Cylindrical waist + Circular head)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rectangle([cx - 125 + dx, cy + 40 + dy, cx + 125 + dx, cy + 150 + dy], fill=fill), COBALT, 6, 10)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 315 + dx, cy + 120 + dy, cx + 315 + dx, cy + 400 + dy], radius=20, fill=fill), OBSID)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 280 + dx, cy + 150 + dy, cx + 280 + dx, cy + 370 + dy], radius=14, fill=fill), WHITE, 8)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 280 + dx, cy - 415 + dy, cx + 280 + dx, cy + 145 + dy], fill=fill), WHITE, 10, 16)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 246 + dx, cy - 381 + dy, cx + 246 + dx, cy + 111 + dy], fill=fill), ALAB, 8)
        draw_surf_dial_graphics(stage, cx, cy - 130, 116, cx, cy + 278, 78, CHARC, ORANGE, sec_hand_rgb=COBALT, dial_style="arc_caliper", compact_labels=True, beach_deg=-90)

    elif cid == 26:
        # 26: Stepped Rangefinder Plate (Stadium camera-plate body + stepped silver upper shoulder)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 310 + dx, cy - 400 + dy, cx + 310 + dx, cy + 400 + dy], radius=140, fill=fill), OBSID)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 310 + dx, cy - 400 + dy, cx + 310 + dx, cy - 160 + dy], radius=95, fill=fill), SILVER, 4, 6, shadow_blur=10)
        d.ellipse([cx + 190 - 22, cy - 318 - 22, cx + 190 + 22, cy - 318 + 22], fill=(*RED_OR, 255))
        for cy_w, rw in [(cy - 98, 214), (cy + 220, 148)]:
            d.ellipse([cx - rw - 14, cy_w - rw - 14, cx + rw + 14, cy_w + rw + 14], fill=(*SILVER, 255))
            draw_recessed_well(stage, lambda dr, dx, dy, fill, cy_w=cy_w, rw=rw: dr.ellipse([cx - rw + dx, cy_w - rw + dy, cx + rw + dx, cy_w + rw + dy], fill=fill), WHITE, 8)
        draw_surf_dial_graphics(stage, cx, cy - 94, 104, cx, cy + 238, 70, CHARC, RED_OR, dial_style="rehaut_ring", compact_labels=True, beach_deg=-30)

    elif cid == 27:
        # 27: Bulkhead Porthole Barograph (8 socket bosses + deep graduated rehaut)
        sq_o = poly_superellipse(cx, cy, 335, 405, n_exp=3.6)
        sq_i = poly_superellipse(cx, cy, 276, 346, n_exp=3.6)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in sq_o], fill=fill), NAVY)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in sq_i], fill=fill), WHITE, 12)
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            bx = cx + 305 * math.cos(rad)
            by = cy + 375 * math.sin(rad)
            d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(*SILVER, 255), outline=(*OBSID, 255), width=3)
            d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(*OBSID, 255))
        draw_surf_dial_graphics(stage, cx, cy - 105, 118, cx, cy + 205, 76, CHARC, ORANGE, dial_style="rehaut_ring", hand_style="tapered", compact_labels=True, beach_deg=150)

    elif cid == 28:
        # 28: Tectonic Split-Datum Totem (Horizontal V-groove shadow canyon separating two offset planes)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 310 + dx, cy - 400 + dy, cx + 310 + dx, cy + 400 + dy], radius=24, fill=fill), CHARC)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 288 + dx, cy - 378 + dy, cx + 288 + dx, cy + 75 + dy], radius=16, fill=fill), WHITE, 6, 10, shadow_blur=14)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 288 + dx, cy + 98 + dy, cx + 288 + dx, cy + 378 + dy], radius=16, fill=fill), SILVER, 6)
        draw_surf_dial_graphics(stage, cx, cy - 135, 128, cx, cy + 250, 82, CHARC, ORANGE, dial_style="ticks", beach_deg=-30)

    elif cid == 29:
        # 29: Cockpit Altimeter Square (Chamfered square + 4 corner lock bosses + raised circular ring)
        c_sq = poly_chamfer_rect(cx, cy, 665, 760, 68)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in c_sq], fill=fill), OBSID)
        for sx in (cx - 266, cx + 266):
            for sy in (cy - 314, cy + 314):
                d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=(*SLATE, 255), outline=(*SILVER, 200), width=3)
                d.line([(sx - 12, sy - 12), (sx + 12, sy + 12)], fill=(*OBSID, 255), width=4)
        d.ellipse([cx - 242, cy - 342, cx + 242, cy + 142], fill=(*CHARC, 255), outline=(*SLATE, 220), width=5)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.ellipse([cx - 216 + dx, cy - 316 + dy, cx + 216 + dx, cy + 116 + dy], fill=fill), OBSID, 10)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.rounded_rectangle([cx - 220 + dx, cy + 150 + dy, cx + 220 + dx, cy + 332 + dy], radius=24, fill=fill), OBSID, 8)
        draw_surf_dial_graphics(stage, cx, cy - 96, 104, cx, cy + 258, 72, WHITE, ORANGE, sec_hand_rgb=YELLOW, dial_style="crosshair", hand_style="Counterweight_Block", compact_labels=True, beach_deg=30)

    elif cid == 30:
        # 30: Harmonic Arch Portal Totem (Semi-circular arched top concentric with upper compass)
        a_out = poly_arch(cx, cy, 620, 800)
        a_in  = poly_arch(cx, cy, 562, 742)
        draw_3d_extruded_shape(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in a_out], fill=fill), WHITE)
        draw_recessed_well(stage, lambda dr, dx, dy, fill: dr.polygon([(x + dx, y + dy) for x, y in a_in], fill=fill), ALAB, 10)
        d.line([(cx - 250, cy + 85), (cx + 250, cy + 85)], fill=(*SLATE, 120), width=3)
        draw_surf_dial_graphics(stage, cx, cy - 105, 130, cx, cy + 235, 84, CHARC, ORANGE, dial_style="arc_caliper", hand_style="tapered", beach_deg=-30)

    # Compose final card at 2x supersampling then downscale to (width, height)
    SS = 2
    W, H = width * SS, height * SS
    card = Image.new("RGBA", (W, H), (233, 231, 226, 255))
    cd = ImageDraw.Draw(card)

    pad = 16 * SS
    card_bottom = H - (168 * SS if include_caption else 16 * SS)
    box_w = W - 2 * pad
    box_h = card_bottom - pad

    stage_resized = stage.resize((box_w, box_h), Image.Resampling.LANCZOS)
    card.paste(stage_resized, (pad, pad))

    if include_caption:
        _, title, spec = CONCEPTS[concept_id - 1]
        f_title = load_font(34, bold=True)
        f_spec  = load_font(23, bold=False)
        cd.text((24 * SS, card_bottom + 20 * SS), f"CONCEPT {concept_id:02d}  —  {title}", font=f_title, fill=(216, 78, 28, 255))
        cd.text((24 * SS, card_bottom + 66 * SS), spec, font=f_spec, fill=(55, 58, 64, 255))

    out = card.resize((width, height), Image.Resampling.LANCZOS).convert("RGB")
    return out

def main():
    print("Rendering 30 Hero-Scale Printable Industrial Design Concept Images (Zero Brand Names)...")
    labeled_cards = []
    clean_cards   = []

    for cid, title, _ in CONCEPTS:
        slug = title.lower().replace(" ", "_").replace("-", "_")
        c_labeled = render_concept_tile(cid, width=900, height=1120, include_caption=True)
        c_clean   = render_concept_tile(cid, width=900, height=1000, include_caption=False)

        p_lab = os.path.join(CARDS_DIR, f"Concept_{cid:02d}_{slug}.jpg")
        p_cln = os.path.join(CLEAN_DIR, f"Clean_{cid:02d}_{slug}.jpg")
        c_labeled.save(p_lab, quality=94, dpi=(300, 300))
        c_clean.save(p_cln, quality=94, dpi=(300, 300))

        labeled_cards.append(c_labeled)
        clean_cards.append(c_clean)
        print(f"  [{cid:02d}/30] Saved {os.path.basename(p_lab)}")

    # Build 5 Printable 6-Up Studio Presentation Boards (3 cols x 2 rows)
    f_hdr = load_font(44, bold=True)
    f_sub = load_font(25, bold=False)

    for b_idx in range(5):
        c0 = b_idx * 6
        c1 = c0 + 6
        cw, ch = 900, 1120
        pad_x, pad_y = 28, 28
        top_bar = 145
        bw = pad_x + 3 * (cw + pad_x)
        bh = top_bar + 2 * (ch + pad_y)
        board = Image.new("RGB", (bw, bh), (233, 231, 226))
        bd = ImageDraw.Draw(board)
        bd.text((pad_x + 12, 32), f"SURF CLOCK — EARLY INDUSTRIAL DESIGN EXPLORATION (BOARD {b_idx+1} OF 5: CONCEPTS {c0+1:02d}–{c1:02d})", font=f_hdr, fill=(24, 26, 30))
        bd.text((pad_x + 12, 88), "Dual-Indicator Horological & Telemetry Form Studies  •  5 Northern Beaches Compass + Surf Conditions Gauge", font=f_sub, fill=(88, 92, 98))

        for k in range(6):
            r, c = divmod(k, 3)
            x = pad_x + c * (cw + pad_x)
            y = top_bar + r * (ch + pad_y)
            board.paste(labeled_cards[c0 + k], (x, y))

        b_path = os.path.join(OUT_DIR, f"Board_{b_idx+1}_Concepts_{c0+1:02d}_to_{c1:02d}.jpg")
        board.save(b_path, quality=94, dpi=(300, 300))
        shutil.copyfile(b_path, os.path.join(ART_DIR, os.path.basename(b_path)))
        print("Saved Printable 6-Up Board:", b_path)

    # Build Master 30-Concept Wall Poster (5 cols x 6 rows)
    tw, th = 660, 820
    px, py = 22, 22
    t_hdr = 160
    mw = px + 5 * (tw + px)
    mh = t_hdr + 6 * (th + py)
    master = Image.new("RGB", (mw, mh), (233, 231, 226))
    md = ImageDraw.Draw(master)
    f_mhdr = load_font(54, bold=True)
    f_msub = load_font(30, bold=False)
    md.text((px + 16, 36), "SURF CLOCK — 30 INDUSTRIAL DESIGN EXPLORATION CONCEPTS (COMPLETE ARCHIVE)", font=f_mhdr, fill=(24, 26, 30))
    md.text((px + 16, 102), "Early Silhouette, Chassis Architecture, Baffle & Dial Topology Studies  •  Long Reef / Queensie / Dee Why / Freshie / Curl Curl", font=f_msub, fill=(88, 92, 98))

    for idx, card in enumerate(labeled_cards):
        r, c = divmod(idx, 5)
        small = card.resize((tw, th), Image.Resampling.LANCZOS)
        master.paste(small, (px + c * (tw + px), t_hdr + r * (th + py)))

    m_path = os.path.join(OUT_DIR, "00_MASTER_30_DESIGN_EXPLORATIONS_POSTER.jpg")
    master.save(m_path, quality=93, dpi=(300, 300))
    shutil.copyfile(m_path, os.path.join(ART_DIR, "00_MASTER_30_DESIGN_EXPLORATIONS_POSTER.jpg"))
    print("Saved Master 30-Concept Poster:", m_path)

if __name__ == "__main__":
    main()
