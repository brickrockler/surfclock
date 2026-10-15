import trimesh
import numpy as np

# Keep full dial for white base, and extract ONLY raised black lettering (z_min >= 2.54) shifted +0.04mm in Z
dial = trimesh.load("/Users/jcolley/surf_clock/FINAL_PRINT_FILES/2_Dial_Face_V3_QUEENSIE_Reinforced_PrusaMK4.stl")
dial.export("/tmp/dial_base_white.stl")

tris = dial.vertices[dial.faces]
z_min = tris[:, :, 2].min(axis=1)
mask_black = z_min >= 2.52
dial_black = dial.submesh([np.where(mask_black)[0]], append=True)
dial_black.apply_translation([0.0, 0.0, 0.04])
dial_black.export("/tmp/dial_text_black.stl")
print(f"Exported full dial_base_white ({len(dial.faces)} faces) & dial_text_black ({len(dial_black.faces)} faces)")
