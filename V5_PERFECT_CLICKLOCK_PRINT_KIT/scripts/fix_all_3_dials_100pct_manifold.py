import sys
sys.path.insert(0, "/Users/jcolley/surf_clock")
import math
import trimesh
import build_v3_dial_faces_fast as bdf

# Fix 1: Make make_clean_chamfered_dial_plate_tris 100% watertight by connecting every radial ray segment on the outer perimeter
#        and burying z_root = 2.30 mm slightly into the 2.40 mm base plate so there are zero coplanar z=2.40 face collisions!
def make_clean_watertight_dial_plate_tris(
    half_x=110.75,
    half_y=87.75,
    z0=0.00,
    z1=2.40,
    hole1=(-25.30, 0.0),
    hole2=(78.20, 0.0),
    r_back=4.60,
    r_front=3.90,
    z_chamfer=0.70
):
    tris = []
    x_split = 26.0
    zones = [
        (-half_x, x_split, -half_y, half_y, hole1[0], hole1[1], "left"),
        (x_split,  half_x, -half_y, half_y, hole2[0], hole2[1], "right"),
    ]
    segs = 72
    # Guarantee exact shared angles at the 4 corners of each zone!
    for x_min, x_max, y_min, y_max, hcx, hcy, side in zones:
        corner_angles = [
            math.atan2(y_max - hcy, x_max - hcx),
            math.atan2(y_max - hcy, x_min - hcx),
            math.atan2(y_min - hcy, x_min - hcx),
            math.atan2(y_min - hcy, x_max - hcx),
        ]
        # Add regular angles plus exact corner angles
        angs = sorted(set(
            [round((2.0 * math.pi * i / segs) % (2.0 * math.pi), 8) for i in range(segs)] +
            [round(a % (2.0 * math.pi), 8) for a in corner_angles]
        ))
        n_a = len(angs)
        rect_pts = []
        for a in angs:
            ca, sa = math.cos(a), math.sin(a)
            tx = (x_max - hcx) / ca if ca > 1e-9 else ((x_min - hcx) / ca if ca < -1e-9 else 1e9)
            ty = (y_max - hcy) / sa if sa > 1e-9 else ((y_min - hcy) / sa if sa < -1e-9 else 1e9)
            t = min(tx, ty)
            px = round(hcx + ca * t, 5)
            py = round(hcy + sa * t, 5)
            rect_pts.append((px, py))

        for i in range(n_a):
            i1 = (i + 1) % n_a
            a0, a1 = angs[i], angs[i1]
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)
            rx0, ry0 = rect_pts[i]
            rx1, ry1 = rect_pts[i1]

            fx0, fy0 = round(hcx + r_front * c0, 5), round(hcy + r_front * s0, 5)
            fx1, fy1 = round(hcx + r_front * c1, 5), round(hcy + r_front * s1, 5)
            bdf.add_quad(tris, (fx0, fy0, z1), (rx0, ry0, z1), (rx1, ry1, z1), (fx1, fy1, z1))

            bx0, by0 = round(hcx + r_back * c0, 5), round(hcy + r_back * s0, 5)
            bx1, by1 = round(hcx + r_back * c1, 5), round(hcy + r_back * s1, 5)
            bdf.add_quad(tris, (bx1, by1, z0), (rx1, ry1, z0), (rx0, ry0, z0), (bx0, by0, z0))

            bdf.add_quad(tris, (bx0, by0, z0), (bx1, by1, z0), (fx1, fy1, z_chamfer), (fx0, fy0, z_chamfer))
            bdf.add_quad(tris, (fx0, fy0, z_chamfer), (fx1, fy1, z_chamfer), (fx1, fy1, z1), (fx0, fy0, z1))

            # Close outer perimeter wall segment directly between (rx0, ry0) and (rx1, ry1)
            bdf.add_quad(tris, (rx0, ry0, z0), (rx1, ry1, z0), (rx1, ry1, z1), (rx0, ry0, z1))
    return tris

bdf.make_clean_chamfered_dial_plate_tris = make_clean_watertight_dial_plate_tris

# Also wrap make_stepped_stadium_stroke_bed and make_stepped_arc_extrusion_portrait so z_root = 2.30 (buried 0.1mm in plate)
orig_stroke = bdf.make_stepped_stadium_stroke_bed
def clean_stroke(xp0, yp0, xp1, yp1, width, z_root=2.30, z_ped=2.58, z_top=3.16, flare_extra=0.28, cap_segs=10):
    raw = orig_stroke(xp0, yp0, xp1, yp1, width, z_root=z_root, z_ped=z_ped, z_top=z_top, flare_extra=flare_extra, cap_segs=cap_segs)
    # Round vertices to 5 decimals so every triangle shares exact vertex coordinates!
    clean = []
    for p1, p2, p3 in raw:
        q1 = tuple(round(v, 5) for v in p1)
        q2 = tuple(round(v, 5) for v in p2)
        q3 = tuple(round(v, 5) for v in p3)
        if q1 != q2 and q2 != q3 and q1 != q3:
            clean.append((q1, q2, q3))
    return clean

orig_arc = bdf.make_stepped_arc_extrusion_portrait
def clean_arc(cx_p, cy_p, r_in, r_out, deg_start, deg_end, z_root=2.30, z_ped=2.58, z_top=3.16, flare_side=0.14, segs=72):
    raw = orig_arc(cx_p, cy_p, r_in, r_out, deg_start, deg_end, z_root=z_root, z_ped=z_ped, z_top=z_top, flare_side=flare_side, segs=segs)
    clean = []
    for p1, p2, p3 in raw:
        q1 = tuple(round(v, 5) for v in p1)
        q2 = tuple(round(v, 5) for v in p2)
        q3 = tuple(round(v, 5) for v in p3)
        if q1 != q2 and q2 != q3 and q1 != q3:
            clean.append((q1, q2, q3))
    return clean

bdf.make_stepped_stadium_stroke_bed = clean_stroke
bdf.make_stepped_arc_extrusion_portrait = clean_arc

# Rebuild all 3 Dial Faces directly into V5_PERFECT_CLICKLOCK_PRINT_KIT and FINAL_PRINT_FILES!
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
