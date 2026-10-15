# Surf Clock — V5 "Click-Lock" Edition (Complete Fresh Print Kit & Exact PrusaSlicer Settings)

This folder (`V5_PERFECT_CLICKLOCK_PRINT_KIT/`) contains **only the final, audited V5 Click-Lock STL files** engineered so the entire clock drops straight together and clicks into place by hand with **zero bending, zero corner posts, and zero screws**.

---

## 1. Files Included in This Folder (What to Print)

You need **5 parts total** (pick **one** Dial Face `2a`/`2b`/`2c` and **one** Back Cover `4a`/`4b`):

| Part # | File Name | Printer | Recommended Filament (TE / Braun Palette) | Est. Time |
| :--- | :--- | :--- | :--- | :--- |
| **Part 1** | `1_Outer_Frame_ClickLock_PrusaMK4.stl` | **Prusa MK4 #1** | Matte Cool Light Grey (`RAL 7035`) or Matte White PLA | ~3h 15m |
| **Part 2** *(Pick 1)* | `2a_Dial_Face_NORTHERN_BEACHES_Queensie_M600_at_Z2.6mm_PrusaMK4.stl`<br>`2b_Dial_Face_SYDNEY_ICONS_Bondi_Bronte_M600_at_Z2.6mm_PrusaMK4.stl`<br>`2c_Dial_Face_EASTERN_SUBURBS_Bondi_Coogee_M600_at_Z2.6mm_PrusaMK4.stl` | **Prusa MK4 #2** | Base (`Z = 0.0–2.4 mm`): Matte White or Cool Light Grey PLA<br>Text (`M600` swap at **`Z = 2.60 mm`**): Matte Black PLA | ~1h 35m |
| **Part 3** | `3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl` | **Prusa MK4 #2** *(after Dial)* | Matte Orange (`TE Hero Accent`) or Matte Charcoal PLA | ~1h 50m |
| **Part 4** *(Pick 1)* | `4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl` *(Best for Translucent)*<br>`4b_Back_Cover_BRAUN_LOUVERED_HiddenClips_PrusaMK4.stl` *(Best for Opaque)* | **Prusa MK4 #1** *(or #2)* | `4a`: Translucent / Natural Clear PLA or PETG<br>`4b`: Matte Cool Light Grey or Matte White PLA | ~1h 10m |
| **Part 5** | `5_Pointer_Hands_Skinny_Capped_PrusaMINI.stl` | **Prusa MINI** | Matte Orange (`Beach Hand`) / Matte Black (`Conditions Hand`) | ~18m |

---

## 2. Exact PrusaSlicer Settings for Each File

### Global Baseline (All Parts)
- **Printer Profile:** `Original Prusa MK4 Input Shaper 0.4 nozzle` (Parts 1–4) / `Original Prusa MINI+ Input Shaper 0.4 nozzle` (Part 5)
- **Filament Profile:** `Generic PLA` or `Prusament PLA` (`215°C` first layer / `210°C` other layers, `60°C` bed)
- **Build Plate:** **Satin Powder-Coated PEI Sheet** (gives the authentic Teenage Engineering matte micro-texture on all exterior faces)
- **Supports:** **`None` (`Every single part is 100% self-supporting — NEVER enable supports!`)**
- **Brim:** **`No`** (`Disable Skirt/Brim on Parts 1–4 so they fit within the 250 × 210 mm MK4 build area`)

---

### PART 1: `1_Outer_Frame_ClickLock_PrusaMK4.stl`
> **Orientation:** Already oriented **Front Bezel Face-Down (`Z = 0.0 mm` on the print bed)**. Do not rotate X or Y.

- **Print Settings Preset:** `0.20mm STRUCTURAL @MK4 IS`
- **Layer Height:** `0.20 mm` (First layer: `0.20 mm`)
- **Perimeters (Walls):** **`4`** *(Ensures rock-solid outer walls and crisp `45°` internal click-lock ramps)*
- **Top / Bottom Solid Layers:** `5` Top / `5` Bottom
- **Bottom Fill Pattern:** **`Monotonic Lines`** *(Creates a uniform directional grain across the front bezel rim)*
- **Infill:** `15%` **`Gyroid`**
- **Seam Position:** **`Rear`** *(Hides the Z-seam along the bottom/rear edge)*
- **Skirt / Brim:** **Loops: `0`**, **Brim width: `0 mm`** *(Required so the `230 × 184 mm` frame fits the MK4 bed with zero clipping)*
- **Supports:** **`None`** *(All internal corner seats and click-lock flanges are angled at `45°` for zero-support printing)*

---

### PART 2: `2a` / `2b` / `2c_Dial_Face_..._M600_at_Z2.6mm_PrusaMK4.stl`
> **Orientation:** Already oriented **Flat on Back (`Z = 0.0 mm` on bed, raised 3D lettering on top at `Z = 2.40–3.16 mm`)**.

- **Print Settings Preset:** `0.20mm STRUCTURAL @MK4 IS`
- **Layer Height:** `0.20 mm` (First layer: `0.20 mm`)
- **Wall Generator:** **`Arachne`** *(Critical for razor-sharp DIN/Braun lettering strokes and sub-dial tick marks)*
- **Perimeters:** `3`
- **Top / Bottom Solid Layers:** `5` Top / `4` Bottom
- **Top Fill Pattern:** **`Monotonic Lines`**
- **Ironing:**
  - **Enable Ironing:** **`Enabled`**
  - **Ironing Type:** **`All top surfaces`** *(Irons both the flat `Z = 2.40 mm` dial face AND the `Z = 3.16 mm` tops of the letters so they look screen-printed!)*
  - **Flow rate:** `15%`
  - **Spacing between ironing passes:** `0.10 mm`
- **Infill:** `20%` **`Grid`** or **`Rectilinear`**
- **Skirt / Brim:** **Loops: `0`**, **Brim width: `0 mm`**
- **Exact Two-Color Filament Swap (`M600`):**
  1. Slice the plate at `0.20 mm` layer height.
  2. In the Preview vertical layer slider on the right, drag down to **`Z = 2.60 mm` (Layer 13)** — this is the very first layer where the raised letters and arc appear above the flat `2.40 mm` dial face.
  3. Click the orange **`+`** icon at **`Z = 2.60 mm`** to insert a **Color Change (`M600`)**.
  4. Start the print with **Matte White** (or **Cool Light Grey**) PLA; when the MK4 beeps at `Z = 2.60 mm`, swap to **Matte Black** PLA.

---

### PART 3: `3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl`
> **Orientation:** Already oriented **Flat Base-Down (`Z = 0.0 mm` on bed, clips and ESP32 pedestal pointing UP)**.

- **Print Settings Preset:** `0.20mm STRUCTURAL @MK4 IS`
- **Layer Height:** `0.20 mm`
- **Wall Generator:** **`Arachne`**
- **Perimeters:** **`4`** *(Makes the 10 perimeter leaf-spring click-tabs, ULN2003 snap-clips, motor ear snap-clips, and raised `Z = 16.5 mm` ESP32-S3 H-bridge pedestal strong and resilient)*
- **Top / Bottom Solid Layers:** `5` Top / `4` Bottom
- **Infill:** `20%` **`Gyroid`**
- **Skirt / Brim:** **Loops: `0`**, **Brim width: `0 mm`**
- **Supports:** **`None`** *(Even the side wire-access windows on the raised ESP32 pedestal bridge cleanly across `14 mm` with zero supports)*

---

### PART 4A (Recommended for Translucent Back): `4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl`
> **Orientation:** Already oriented **Outside Face-Down (`Z = 0.0 mm` on Satin PEI bed, 10 hidden internal snap-clips pointing UP)**.

- **Print Settings Preset:** `0.20mm STRUCTURAL @MK4 IS`
- **Filament:** **Translucent / Natural Clear PLA or PETG**
- **Layer Height:** `0.20 mm`
- **Perimeters:** `3`
- **How to Get the Even Teenage Engineering "Frosted Ice" Diffusion:**
  - **Top Solid Layers:** `0` *(or set Top/Bottom to `100% Aligned Rectilinear` infill at `45°` only, NOT crisscross!)*
  - **Best Method in PrusaSlicer:**
    - Set **Top Solid Layers = `5`**, **Bottom Solid Layers = `5`**, **Infill = `100%`**, and set **Fill Pattern / Top Fill / Bottom Fill = `Aligned Rectilinear`** with **Fill Angle = `0°` (or `90°`)** so every single internal layer of the `2.0 mm` optical window runs in the **exact same direction** instead of creating a diagonal crosshatch grid!
    - **Extrusion Multiplier (Flow):** `1.02` (`102%` — eliminates tiny air micro-bubbles between extrusion lines for clear optical glow).
    - **Print Speed (Solid Infill & First Layer):** Slow down to **`35 mm/s`** for crystal-consistent translucency.
- **Skirt / Brim:** **Loops: `0`**, **Brim width: `0 mm`**
- **Supports:** **`None`**

### PART 4B (If Printing Opaque Back): `4b_Back_Cover_BRAUN_LOUVERED_HiddenClips_PrusaMK4.stl`
- Same settings as **Part 1 (`0.20mm STRUCTURAL`, `3` Perimeters, `15% Gyroid`, `Loops: 0`, `Supports: None`)**.

---

### PART 5: `5_Pointer_Hands_Skinny_Capped_PrusaMINI.stl`
> **Orientation:** Already oriented **Flat Base-Down (`Z = 0.0 mm` on bed, capped top pointing UP)**.

- **Print Settings Preset:** `0.12mm DETAIL` or `0.15mm STRUCTURAL @MINI IS`
- **Layer Height:** **`0.12 mm`** *(or `0.15 mm`)*
- **Wall Generator:** **`Arachne`**
- **Perimeters:** **`4`** *(Solidifies the thin tapered needle blades and the `5.18 × 3.12 mm` keyed `28BYJ-48` shaft bore)*
- **Infill:** `100% Rectilinear`
- **Ironing:** **`Enabled` (`All top surfaces`, `15%` flow)** *(Gives the top surface of the hands a smooth molded finish)*
- **Supports:** **`None`**

---

## 3. Zero-Screw, Zero-Bend Assembly Sequence (60 Seconds)

1. **Snap Electronics onto `3_Motor_Mount_Plate` (Outside the Clock on Your Desk First!):**
   - **2× `28BYJ-48` Stepper Motors:** Push both motors straight down into the upper and lower figure-8 pockets (`Z = 2.0 mm` coplanar floor). The `Ø3.84 mm` ear pegs pass through the metal ear holes and the side ear clips click over the metal ears—locking both motors with zero screws.
   - **2× `ULN2003` Driver Boards:** Snap onto the 4 bare corner pads in the Upper-Left and Upper-Right (or Mid-Right) cradles; the `-2.0 mm` bottom clip and split top corner clips click over the PCB edges with all solder pins hanging freely in the enlarged `27.6 × 31.6 mm` under-board cutout.
   - **Freenove `ESP32-S3-WROOM` Board:** Plug your female DuPont jumper wires onto the bottom pins (they have `16.5 mm` of clearance inside the open side trenches!), drop the Freenove PCB onto the raised `Z = 16.5 mm` central H-bridge pedestal (`with the top antenna tab extending through the 20.4 mm top opening`), and click it under the 4 side clips.
   - **USB-C Cable:** Plug your right-angle or straight USB-C cable into `USB-UART` (or `USB-OTG`)—you now have **`51.8 mm` (`> 2 inches`)** of wide-open space below the port—and tuck the cord through the two bottom USB-C cable arches toward the bottom-center exit.
2. **Drop `2_Dial_Face` Straight Into `1_Outer_Frame`:**
   - Lay `1_Outer_Frame` face-down on your table.
   - Drop `2_Dial_Face` face-down into the back of the frame—thanks to the hidden corner and edge reliefs, it falls **100% straight down to the front bezel lip (`Z = 4.0 mm`) under gravity alone with zero bending**.
3. **Click `3_Motor_Mount_Plate` Straight Down Behind `2_Dial_Face`:**
   - Align the two motor shafts with the two dial holes and push `3_Motor_Mount_Plate` straight down.
   - In the final `4 mm`, the **10 compliant leaf-spring perimeter tabs** slide down the `45°` flanged frame ramps and **CLICK** under the `Z = 9.45 mm` snap catches—locking both the dial face and motor plate tightly in place with zero screws.
4. **Click `4_Back_Cover` Flush Into the Rear Rim:**
   - Route the USB-C cord through the bottom-center slot and press `4_Back_Cover` into the rear rim (`Z = 49.0–52.0 mm`).
   - Its 4 corners rest dead-flush on the `45°` rear corner seats at `Z = 49.0 mm`, while the **10 hidden internal cantilever clips** on the inside of the cover click into the internal frame catches at `Z = 47.0 mm`—leaving a **100% seamless, slot-free, screw-free rear face**.
5. **Press `5_Pointer_Hands` Onto the Protruding Shafts:**
   - Turn the clock face-up and press the keyed Beach Hand and Conditions Needle onto the two `28BYJ-48` shafts (which now protrude `+3.0 mm` further out the front of the dial face thanks to the coplanar motor ear seats).

---

## 4. Crucial Tip if Using "Fuzzy Skin" on `1_Outer_Frame`

If you want that bead-blasted / powder-coated Teenage Engineering texture on the outside of `1_Outer_Frame_ClickLock_PrusaMK4.stl`:

1. **DO NOT enable global `Fuzzy skin: Outside walls` in Print Settings!**
   - **Why:** Between `Z = 43.0 mm` and `Z = 52.0 mm`, the bottom USB-C slot cuts through the wall, turning the closed rectangular ring into a "C" shape. If you turn on global `Outside walls` fuzzy skin, PrusaSlicer treats the **inside rear rim (`Z = 43–52 mm`)** as part of the outside wall and puts fuzzy bumps onto the internal `4_Back_Cover` snap-catches and seating ledge!
2. **Instead, use `Paint-on Fuzzy Skin` (`Smart Fill`) on ONLY the 4 Outer Vertical Sides:**
   - Select `1_Outer_Frame_ClickLock_PrusaMK4.stl` on the plater.
   - Click the **Paint-on Fuzzy Skin** icon on the left toolbar (or press `F` / select Fuzzy Skin brush) $\rightarrow$ choose **Smart fill**.
   - Click **only the 4 flat exterior side walls** (Top, Bottom, Left, Right outer faces). Leave the front bezel bevel and the entire interior unpainted.
   - Then go to **Print Settings $\rightarrow$ Layers and perimeters $\rightarrow$ Fuzzy skin** (leave the dropdown set to `None` so it only applies where painted!) and set the **TE Micro-Texture values**:
     - **Fuzzy skin thickness:** **`0.10 mm`** *(Default `0.30 mm` looks like rough stucco; `0.10 mm` looks like bead-blasted anodized aluminum / powder coat)*
     - **Fuzzy skin point distance:** **`0.30 mm`** *(Default `0.80 mm` is too coarse; `0.30 mm` creates a tight, fine matte grain)*

---

## 5. Exact Settings for `3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl`
*(Note: Make sure to reload `3_Motor_Mount_Plate_ClickLock_Audited_PrusaMK4.stl` from disk — the tall ESP32 archway is 100% removed and replaced with the sleek low-profile `Z = 9.5 mm` V3 cradle moved up `41 mm` for USB-C clearance, with `0.0 mm²` of flat overhangs!)*

* **Printer Profile:** `Original Prusa MK4 Input Shaper 0.4 nozzle`
* **Print Settings Preset:** `0.20mm STRUCTURAL @MK4IS` (or `0.20mm SPEED @MK4IS`)
* **Filament:** Matte White PLA, Cool Light Grey PLA, or Braun Orange PLA (`Generic PLA @PGIS` / `Prusament PLA @PGIS`)
* **Build Plate:** Satin PEI or Textured PEI
* **Orientation:** Flat on its back (`Z = 0.0 mm` flat bottom touching the bed; motor rings and board clips facing UP)
* **Layer Height:** `0.20 mm` (First layer: `0.20 mm`)
* **Perimeters (Walls):** **`3`** *(3 perimeters makes the 10 perimeter click-lock leaf springs, the 28BYJ-48 ear snap-clips, and the ULN2003/ESP32 latches 100% solid flexible spring-beams so they flex and click without snapping)*
* **Solid Layers:** **Top: `4`** | **Bottom: `4`**
* **Infill:** **`15%` `Gyroid`** or **`15%` `Rectilinear`**
* **Supports:** **`None`** (Every clip and wire guide now has a `45°` self-supporting underside ramp — `0` flat overhangs!)
* **Brim:** **`No`**
* **Fuzzy Skin:** **`Off`** *(Keep Fuzzy Skin OFF on the Motor Mount Plate so the motors, PCBs, and perimeter click-tabs slide and snap with glass-smooth tolerances)*

---

## 6. Exact Settings for an Awesome See-Through Back in **Transparent PETG**
**File:** `4a_Back_Cover_PURE_FLAT_TRANSLUCENT_HiddenClips_PrusaMK4.stl` *(recommended for clearest view of internals)* or `4b_Back_Cover_BRAUN_LOUVERED_HiddenClips_PrusaMK4.stl`

Normal slicing traps tiny air tunnels between crisscrossing `45°` layers, which turns Transparent PETG milky white instead of see-through. To get a **crystal-clear / Teenage Engineering smoked-glass look** where you can clearly see the ESP32-S3 LEDs, rainbow ribbon cables, and gold 28BYJ-48 motors inside, use this exact Prusa "Glass PETG" recipe:

### A. Build Sheet Choice (Crucial for PETG!)
* **For Clear / Glossy See-Through Window:** Use the **Smooth PEI Sheet** with a quick wipe of **Windex** (or a thin layer of glue stick / hairspray) as a release agent *(never print PETG on bare Smooth PEI cleaned with IPA, or it welds too tightly)*.
* **For Frosted "Ice-Glass" Diffused Window (hides fingerprints & diffuses the red/green LEDs beautifully):** Use the **Satin Powder-Coated Sheet** (no glue stick needed — PETG releases cleanly on Satin PEI once cooled!).

### B. Orientation
* Place **FLAT on the bed** (`Z = 0.0 mm` outer rear face touching the build plate; the 10 hidden snap-clips pointing UP from `Z = 3.0 to 5.8 mm`).

### C. The "Optical See-Through PETG" Slicer Settings (in PrusaSlicer)
1. **Printer & Preset:** `Original Prusa MK4 Input Shaper 0.4 nozzle` -> **`0.20mm STRUCTURAL @MK4IS`**
2. **Filament Preset:** `Generic PETG @PGIS` or `Prusament PETG @PGIS`
   * **Filament -> Extrusion Multiplier:** **`1.03`** *(3% intentional slight over-extrusion squeezes out all microscopic air pockets between adjacent lines)*
   * **Filament -> Nozzle Temperature:** **`245 °C`** (First layer) / **`250 °C`** (Other layers) *(slightly hotter helps layers fuse into a single clear optical sheet)*
   * **Filament -> Bed Temperature:** **`85 °C`** (First layer) / **`90 °C`** (Other layers)
   * **Filament -> Cooling:** **Keep fan always on: `OFF`** | **Min/Max Fan Speed: `0%` to `20%`** *(ONLY enable fan `40%` for Bridges/Overhangs so the 10 little snap-clips at `Z = 3.0–5.8 mm` print crisply while the `0–3.0 mm` window cools slowly and stays glassy clear!)*
3. **Print Settings -> Layers and Perimeters:**
   * **Layer Height:** `0.20 mm` (First layer: `0.20 mm`)
   * **Perimeters:** **`3`** *(keeps the 10 hidden snap-clips strong and springy)*
   * **Horizontal Shells -> Solid Layers:**
     * **Top: `1`** | **Bottom: `1`** *(Avoids 8 crisscrossing solid layers that create a cloudy crosshatch grid!)*
4. **Print Settings -> Infill (THE SECRET TO SEE-THROUGH PETG):**
   * **Fill density:** **`100%`**
   * **Fill pattern:** **`Aligned Rectilinear`** *(CRITICAL: Unlike normal Rectilinear which alternates `+45° / -45°` and creates a cloudy screen-door grid, **`Aligned Rectilinear`** lays every single layer down in the **exact same parallel direction**, acting like an optical fresnel lens you can see right through!)*
   * **Fill angle:** **`0°`** (or **`90°`** — aligns the lines cleanly with the rectangular frame instead of diagonal)
5. **Print Settings -> Speed (Slow Down the Window Layers!):**
   * **First layer speed:** **`20 mm/s`**
   * **Solid infill / Infill speed:** **`30 mm/s`** *(Printing the `100% Aligned Rectilinear` window slowly at `30 mm/s` prevents micro-bubbles from forming in the PETG melt zone)*
6. **Supports & Brim:** **`None`** (and **Fuzzy Skin: `Off`**)
