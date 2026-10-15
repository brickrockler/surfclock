# Surf Clock V3 — Complete PrusaSlicer Settings & Assembly Manual

All **V3 STL files** in `FINAL_PRINT_FILES/` are **100% watertight (`is_watertight = True`, `0` non-manifold edges)**, pre-centered, and pre-oriented flat on the build plate for your **2× Prusa MK4** and **1× Prusa MINI** printers.

---

## 1. Dial Faceplate (`2_Dial_Face_WHITE_then_BLACK_at_Z2.6mm_PrusaMK4.stl`) — Prusa MK4
* **What Changed in V3:**
  * **`QUEENSIE` $\rightarrow$ `QUEENSIE`**: Shortened from 11 tiny letters to 8 full-size (`4.45 mm`) letters matching `DEE WHY` and `FRESHIE` (an optional reinforced `QUEENSIE` version is also saved as `2_OPTIONAL_Dial_Face_QUEENSIE_Reinforced_PrusaMK4.stl`).
  * **2-Perimeter Unbreakable Strokes + Flared White Root Pedestal (`Z = 2.40..2.58 mm`)**: Every letter stroke is widened to `0.90–0.92 mm` (2 full closed nozzle perimeter loops) sitting on a `1.18–1.20 mm` flared white pedestal shoulder on Layer 13 (`Z = 2.40..2.58 mm`). This prevents PrusaSlicer from ironing underneath the letters and gives the Black PLA a rough, wide 3-line foundation pad to fuse into.
  * **Smooth, String-Free, Friction-Free `Ø7.80 mm` Hand Shaft Holes**: Replaced the old 90° mid-air counterbore step (which caused white bridging strings across the holes) with a smooth `Ø7.80 mm` cylindrical bore and a 45° self-supporting backside lead-in chamfer (`0.50 mm` radial clearance all around the `Ø6.80 mm` one-piece hand base = **zero friction**).

* **Exact PrusaSlicer Settings (Critical for Unbreakable Letters):**
  * **Profile:** `0.20mm STRUCTURAL` (or `0.20mm QUALITY`), `0.4 mm` nozzle
  * **Perimeter Generator:** `Arachne` (Default in PrusaSlicer — ensures 2 continuous closed perimeter loops inside every `0.90 mm` letter stroke)
  * **Ironing:** **OFF** (Recommended! Leaving Ironing OFF keeps the `Z = 2.40..2.58 mm` white layer hot and micro-textured so the black letters fuse permanently. If you ever enable Ironing, choose **`Topmost surface only`**, NEVER `All top surfaces`.)
  * **Color Change (`M600`):** Slice at `0.20 mm`, drag the orange layer slider to **`Z = 2.60 mm` (Layer 14)**, and click the **`+`** icon:
    * `Z = 0.00 – 2.58 mm` (Layers 1–13): **Matte White PLA** (prints the base plate + the flared white letter pedestal on Layer 13)
    * `Z = 2.60 – 3.16 mm` (Layers 14–16): **Matte Black PLA** (prints 3 solid black layers of 2-perimeter letters, ticks & gauge arc)
  * **Slow Down & Boost Heat for the Letters (Optional Height Range Modifier `Z = 2.40 – 3.20 mm`):**
    * Right-click part $\rightarrow$ `Add range` (`2.40` to `3.20 mm`) $\rightarrow$ set **External perimeters speed: `20 mm/s`**, **Small perimeters speed: `15 mm/s`**, and **Nozzle temperature: `220 °C`** so the black PLA melts deeply into the white pedestal.

---

## 2. Motor Housing Plate (`3_Motor_Mount_Plate_ORANGE_or_WHITE_PrusaMK4.stl`) — Prusa MK4
* **What Changed in V3:**
  * **Bottom-Left ESP32 Snap Cradle (`30.20 × 58.00 mm`):** Dedicated bottom cradle with `9.50 mm` elevated PCB ledges, two deep through-troughs for downward-pointing male header pins, 4 corner snap-hooks, and open bottom USB-C cable exit.
  * **Bottom-Right Universal ESP32 / LiPo Battery / Mini-Breadboard Snap Bay (`38.20 × 56.00 mm`):** Stepped inner `30.20 mm` ledges + `38.20 mm` outer bay with 4 snap-clips.
  * **Wider Microcontroller / ULN2003 Clips (`+1.10 mm` per side = `33.20 × 37.20 mm`):** Expanded by `+2.20 mm` in both X and Y with `1.20 mm` corner PCB standoffs for underside solder pins.
  * **`Ø1.55 mm` Self-Tapping Screw Pilot Holes:** Replaced the oversized holes with precision `Ø1.55 mm` pilot holes + `Ø2.80 mm` conical starter dimples for M2 / M2.2 / `#2` self-tapping screws, and lowered the motor ear seat by `1.80 mm` so the metal shafts reach further through the dial.
  * **9 Wide L-Bridge / Omega Cable Tunnels:** Wide `14.0 × 10.5 × 7.0 mm` cable guides with `4.0 mm` side entry slots and 45° self-supporting roofs.

* **PrusaSlicer Settings:**
  * **Profile:** `0.20mm STRUCTURAL`, **Perimeters:** `3`, **Infill:** `20% Grid` or `Gyroid`, **Supports:** **`None` (OFF)** (all clips and L-bridge tunnels are 45° self-supporting).

---

## 3. V4 "Finished-Top" One-Piece Extended Braun Hands — Prusa MINI
* **Why V3 Printed With an Unfinished Top & What Changed in V4:**
  1. **Removed the Stair-Stepped Pitched Roof & 3-Tier Grooves:** V3 had a shallow sloped roof (`Z = 3.40..4.23 mm`) and a 3-tier grooved hub that sliced into 5 narrow stair-stepped layers (`1.5 mm → 0.15 mm` wide) that couldn't be ironed. V4 replaces that with a **100% Coplanar, Dead-Flat Monolithic Braun Top Plane** across the entire blade, circular hub cap (`Ø10.40 mm` / `Ø9.40 mm`), and tail, with smooth `R = 1.50 mm` tangent fillets and `>= 2.00 mm` (`5×` nozzle width) rounded baton tips.
  2. **Fixed the Cradle Tip-Droop Bug:** In V3, the peel-away cradle accidentally sloped down from `Z = 1.96 mm` at the hub to `Z = 1.27 mm` at the tip (leaving a `0.93 mm` mid-air gap at the tip that curled upward during printing). In V4, the cradle is a **100% constant-height horizontal shelf (`Z = 2.00 mm`)** all the way past the tip (`0.20 mm` uniform gap everywhere).
  3. **Built-In `Ø6.80 mm` Shaft Extender Stem + `1.20 mm` Solid Top Cap:** Drops straight into the `Ø7.80 mm` V3 dial hole (`0.50 mm` radial clearance = zero friction) with a `28BYJ-48` `5.20 × 3.16 mm` keyed D-bore backed by **6 solid unbroken layers (`1.20 mm`)** of orange PLA.

* **Which Hand File to Print (`FINAL_PRINT_FILES/`):**
  * **Option 1 (`5a_OPTION1_FaceUp_FlatIronedTop_Extended_Hands_PrusaMINI.stl` — ~7 min print):**
    * **Printed Face-Up** (`2.20 mm` built-in extender on bottom + fixed constant-height flat peel-away cradle).
    * Because the entire top surface at `Z = 4.00 mm` is **one single dead-flat horizontal plane**, turning on **PrusaSlicer Ironing (`Topmost surface only`)** buffs the entire hand from tip to hub to tail in one uninterrupted pass into a smooth, finished surface!
  * **Option 2 (`5b_OPTION2_FaceDown_SmoothBedTop_Extended_Hands_PrusaMINI.stl` — ~6 min print):**
    * **Printed Face-Down directly on the PEI build plate** (`Z = 0.00 mm` on the bed IS the visible front surface of the hand, and the built-in `2.40 mm` shaft extender grows straight UP in `+Z`).
    * Needs **ZERO cradle and ZERO supports**! Peel off the bed and flip over onto the motor shaft so the **smooth PEI-molded `Z = 0.00 mm` bottom layer** becomes the visible top surface of the hand!
  * **Combined Standard Plate (`5a_SinglePair_Standard_2.2mm_SteppedBase_Hands_PrusaMINI.stl` — ~12 min print):**
    * Contains **BOTH Option 1 (Left) and Option 2 (Right)** on one plate so you can print both at once and pick your favorite finish!
  * **Master 4-Pair Fitting Pack (`5_Pointer_Hands_MATTE_ORANGE_PrusaMINI.stl`):**
    * Includes Both Option 1 (Face-Up) and Option 2 (Face-Down) in **Standard (`2.2–2.4 mm`)** and **Deep-Reach (`3.4–3.6 mm`)** extender lengths.

* **PrusaSlicer Settings for V4 Hands (Prusa MINI):**
  * **Profile:** `0.15mm QUALITY` or `0.20mm QUALITY` (`0.4 mm` nozzle)
  * **Supports:** **`None` (OFF)**
  * **Perimeters:** **`3`**
  * **Top Fill Pattern:** **`Monotonic Lines`**
  * **Ironing (Recommended for Option 1 Face-Up / Combined Plate):** Enable **Ironing $ightarrow$ `Topmost surface only`** (`15%` flow rate, `0.10 mm` spacing) so the nozzle irons the dead-flat `Z = 4.00 mm` top plane into a glass-smooth sheet!

---

## 4. "Corflute" Fluted Architectural Back Cover (`4_Back_Cover_TRANSPARENT_or_WHITE_PrusaMK4.stl`) — Prusa MK4
* **What Changed in V3:**
  * Replaced the flat `3.0 mm` slab (which printed with diagonal 45° cross-hatch infill) with a true 3D-modeled **Corflute / Architectural Reeded Panel**: a `0.60 mm` continuous optical skin (`Z = 0.00..0.60 mm`) topped by **49 parallel vertical Corflute ribs (`0.88 mm` wide = 2 nozzle perimeters, at `3.20 mm` pitch)** running vertically down the clock (`Z = 0.60..3.00 mm`).
  * Because the skin is 3 bottom layers thick and every vertical rib is exactly 2 perimeters wide (`0.88 mm`), PrusaSlicer generates **0% diagonal 45° infill** across the entire fluted field!

* **PrusaSlicer Settings for Pure Parallel Vertical Corflute Striations:**
  * **Profile:** `0.20mm QUALITY` or `0.20mm STRUCTURAL`
  * **Perimeters:** **`3`**
  * **Solid Layers:** **Bottom: `3`**, **Top: `3`**
  * **Bottom Fill Pattern:** **`Aligned Rectilinear`**
  * **Fill Angle:** **`0°`** (aligns the `Z = 0.00..0.60 mm` translucent base skin lines vertically right along the 49 Corflute ribs!)
  * **Supports:** **`None` (OFF)**
