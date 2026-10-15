#!/usr/bin/env python3
import os
import sys
import json
import importlib.util

SCRIPT_DIR = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts"
sys.path.insert(0, SCRIPT_DIR)

import omni_pro_client as opc

spec = importlib.util.spec_from_file_location(
    "film_mastering",
    os.path.join(SCRIPT_DIR, "49_world_class_film_mastering.py")
)
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
OUT_DIR = os.path.join(BASE, "raw_renders", "v6_film_explorations", "v6_agent_02")
os.makedirs(OUT_DIR, exist_ok=True)

ING_07 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_07_WARM_CREAM_STUDIO_9TICK_4K.jpg")
ING_02 = os.path.join(opc.GOLDEN_DIR, "INGREDIENT_02_THREE_QUARTER_LEFT_9TICK_4K.jpg")
REF_03 = os.path.join(opc.USER_REF_DIR, "USER_REF_03_WarmCream_Architectural_Studio.png")

REFS = [ING_07, ING_02, REF_03]

still_01_path = os.path.join(OUT_DIR, "V6_A02_STILL_01_Levitating_Sunlit_Cream_Studio_4K.jpg")
prompt_01 = (
    "Surreal, hyper-clean high-fashion industrial design editorial photograph shot on Kodak Vision3 50D 35mm film with a Cooke Speed Panchro 50mm lens at f/2.0: "
    "the exact deep matte slate-blue rectangular Braun/Dieter Rams Surf Forecast Instrument (184 x 230 x 52 mm, hardcover art monograph scale) effortlessly floating and levitating in mid-air "
    "exactly 8cm above a bright sunlit warm-cream honed travertine stone shelf against a bright, airy sun-drenched chalk-ivory and warm-cream Venetian limewash plaster wall. "
    "Zero wires, zero stands, zero supports—pure gravity-defying architectural levitation casting a soft, authentic floating ambient shadow directly onto the warm cream travertine surface underneath. "
    "Bathed in luminous golden morning Australian coastal sunlight streaming from the side, with soft out-of-focus dappled eucalyptus leaf shadows and dreamy foreground bokeh. "
    "Crisp focus on the recessed matte slate-blue dial face showing the upper semicircle with strictly 9 white radial ticks on the top arc (8 to 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
    "100% blank smooth matte blue plastic at the bottom of the upper circle (5, 6, 7 o'clock), 1 long burnt-orange needle on the upper dial, and 1 short burnt-orange needle on the lower WORTH IT? (NAH / YEAH) gauge."
)

still_02_path = os.path.join(OUT_DIR, "V6_A02_STILL_02_BrightAiry_Cream_Alcove_FloatingWall_4K.jpg")
prompt_02 = (
    "Bright, airy sunlit warm-cream architectural alcove study shot on 35mm Kodak Vision3 250D film with a Zeiss Super Speed 50mm lens at f/2.0: "
    "the deep matte slate-blue rectangular Surf Forecast Instrument (184 x 230 x 52 mm) cleanly flush wall-mounted inside a recessed minimal warm-cream limewash plaster architectural niche, "
    "captured in crisp three-quarter morning sunlight. Striking high-key editorial contrast between the rich dark marine slate-blue VDI-24 matte bead-blasted housing (#2D3E5E) and the luminous, "
    "sun-drenched warm chalk-cream plaster wall. Subtle golden highlight bloom and gossamer sunlight bands drifting across the warm cream alcove, with soft out-of-focus coastal botanicals in the foreground corner. "
    "Razor-sharp typography and dial geometry: strictly 9 raised white radial tick marks on the top arc only (8 to 4 o'clock: FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL), "
    "100% blank smooth matte slate-blue plastic at 5, 6, and 7 o'clock, and strictly 2 burnt-orange pointer needles total (1 upper, 1 lower on WORTH IT? NAH/YEAH)."
)

print("=== Generating STILL 01 ===")
opc.generate_4k_still(prompt_01, still_01_path, REFS, aspect_ratio="16:9", max_retries=5)
audit_01 = opc.self_audit_still(still_01_path)
print("FINAL AUDIT STILL 01:", json.dumps(audit_01))

print("=== Generating STILL 02 ===")
opc.generate_4k_still(prompt_02, still_02_path, REFS, aspect_ratio="16:9", max_retries=5)
audit_02 = opc.self_audit_still(still_02_path)
print("FINAL AUDIT STILL 02:", json.dumps(audit_02))

# Apply film mastering to both stills (both airy_cream_sunlit_cinema and orchid_35mm_250D_warm)
s01_airy = still_01_path.replace("_4K.jpg", "_MASTER_AiryCream_4K.jpg")
s01_orchid = still_01_path.replace("_4K.jpg", "_MASTER_Orchid35mm_4K.jpg")
fm.apply_film_look_to_still(still_01_path, s01_airy, preset="airy_cream_sunlit_cinema")
fm.apply_film_look_to_still(still_01_path, s01_orchid, preset="orchid_35mm_250D_warm")

s02_airy = still_02_path.replace("_4K.jpg", "_MASTER_AiryCream_4K.jpg")
s02_orchid = still_02_path.replace("_4K.jpg", "_MASTER_Orchid35mm_4K.jpg")
fm.apply_film_look_to_still(still_02_path, s02_airy, preset="airy_cream_sunlit_cinema")
fm.apply_film_look_to_still(still_02_path, s02_orchid, preset="orchid_35mm_250D_warm")

audit_s01_airy = opc.self_audit_still(s01_airy)
audit_s01_orchid = opc.self_audit_still(s01_orchid)
audit_s02_airy = opc.self_audit_still(s02_airy)
audit_s02_orchid = opc.self_audit_still(s02_orchid)
print("AUDIT STILL 01 AIRY:", json.dumps(audit_s01_airy))
print("AUDIT STILL 01 ORCHID:", json.dumps(audit_s01_orchid))
print("AUDIT STILL 02 AIRY:", json.dumps(audit_s02_airy))
print("AUDIT STILL 02 ORCHID:", json.dumps(audit_s02_orchid))
