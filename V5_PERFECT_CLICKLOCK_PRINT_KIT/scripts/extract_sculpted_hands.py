import trimesh

hands = trimesh.load("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/5a_SinglePair_Standard_2.2mm_SteppedBase_Hands_PrusaMINI.stl")
parts = hands.split(only_watertight=False)
# Part 0 is Face-Up Sculpted Upper Beach Hand (hub at X=-24.0, Y=0.0, pointing along +Y, closed crown cap at Z=+4.20)
# Part 2 is Face-Up Sculpted Lower Conditions Hand (hub at X=-9.0, Y=0.0, pointing along +Y, closed crown cap at Z=+4.20)
h_up = parts[0].copy()
h_up.apply_translation([24.0, 0.0, 0.0])
h_up.export("/tmp/hand_upper_centered.stl")

h_lo = parts[2].copy()
h_lo.apply_translation([9.0, 0.0, 0.0])
h_lo.export("/tmp/hand_lower_centered.stl")
print("Exported Face-Up Sculpted Hands with closed crown caps!")
