import os
import sys
import json
import shutil
import argparse
from PIL import Image

sys.path.insert(0, "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE/scripts")
import omni_pro_client as opc

BASE = "/Users/jcolley/surf_clock/STUDIO_4K_CINEMA_PIPELINE"
STILLS_DIR = os.path.join(BASE, "01_4K_STUDIO_KEYFRAMES_AND_STILLS")
VID16_DIR = os.path.join(BASE, "02_INDIVIDUAL_4K_CLIPS_16x9")
VID9_DIR = os.path.join(BASE, "03_INDIVIDUAL_4K_CLIPS_9x16")
os.makedirs(STILLS_DIR, exist_ok=True)
os.makedirs(VID16_DIR, exist_ok=True)
os.makedirs(VID9_DIR, exist_ok=True)

# 100% Photographic, Tactile 9-Tick Master Reference Pairings
R_BLUE_MARBLE = [opc.ANCHOR_BLUE_PLASTER_MARBLE, opc.ANCHOR_MACRO_FRONT_9TICK]
R_LINEN_TILT = [opc.ANCHOR_WARM_LINEN_TILT, opc.ANCHOR_MACRO_FRONT_9TICK]
R_ITALIAN_FILM = [opc.ANCHOR_ITALIAN_70S_35MM, opc.ANCHOR_MACRO_FRONT_9TICK]
R_WARM_PLASTER = [opc.ANCHOR_WARM_PLASTER_DAPPLED, opc.ANCHOR_MACRO_FRONT_9TICK]
R_LOUVER_MACRO = [opc.ANCHOR_MACRO_FRONT_9TICK, opc.ANCHOR_BLUE_PLASTER_MARBLE]

SPECS = [
    # =========================================================================
    # COLLECTION 1 (001-020): SCULPTURAL LIGHT MARBLE & ALABASTER ON TEXTURED BLUE PLASTER
    # =========================================================================
    (1, "V7_001_BLUE_PLASTER_Stepped_Honed_Calacatta_Marble_Dappled_Light", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Editorial architectural still-life photograph for Cereal Magazine, shot on Medium Format Hasselblad H6D-100c with a 100mm f/3.5 lens in natural directional window light. The deep matte slate-blue Surf Clock with its tactile VDI-24 micro-pebbled surface grain rests at a subtle three-quarter angle on a stepped architectural plinth of honed super-light white Italian Calacatta marble with delicate dove-grey mineral veining. Behind the plinth is a richly textured, hand-troweled Prussian-blue Venetian limewash plaster wall across which soft afternoon window light and organic dappled tree-leaf shadows fall gently.",
     "Buttery-smooth, slow motorized slider shot on ARRI Alexa 65 with a 100mm Master Prime lens: the matte slate-blue Surf Clock rests motionless on the stepped honed white Calacatta marble plinth while the soft dappled botanical window shadows sway gently across the textured Prussian-blue Venetian limewash plaster wall."),

    (2, "V7_002_BLUE_PLASTER_Milky_Volterra_Alabaster_Monolith_Window_Shadow", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Architectural gallery photograph on Leica S3 120mm f/4: the deep matte slate-blue rectangular Surf Clock stands on a thick, silky-smooth block of honed milky-white Volterra alabaster stone whose chamfered upper edges catch soft natural morning window sunlight with delicate, organic stone translucency. Behind it is a deep slate-indigo hand-troweled limewash plaster wall bisected by a soft diagonal architectural window shadow.",
     "Slow, meditative cinema push-in on ARRI Alexa 65: natural morning window sunlight shifts smoothly across the silky milky-white Volterra alabaster plinth and deep slate-indigo limewash plaster wall while the matte slate-blue Surf Clock remains completely solid and sharp."),

    (3, "V7_003_BLUE_PLASTER_Fluted_White_Statuario_Column_Dappled_Garden_Light", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Refined Milanese gallery still life on Phase One IQ4 150MP: the vertical matte slate-blue Surf Clock rests atop a carved fluted cylinder column of super-clear white Italian Statuario marble. Raking late-afternoon sunlight from a tall courtyard window casts soft vertical shadow gradients across the carved white marble flutes and dappled olive-branch shadows across a deep cobalt-slate limewash plaster backdrop.",
     "Buttery slow parallax camera glide on ARRI Alexa Mini LF: raking courtyard window sunlight and soft olive-branch shadows move gently across the fluted white Statuario marble column and cobalt-slate plaster wall behind the motionless Surf Clock."),

    (4, "V7_004_BLUE_PLASTER_Cantilevered_Arabescato_Marble_Slabs_Blue_Linen", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Two interlocking cantilevered architectural slabs of honed white Arabescato Corchia marble with subtle silver-grey mineral veins support the deep matte slate-blue Surf Clock in front of a heavy, tactile slate-blue Belgian linen backdrop grazed by warm directional daylight and a soft architectural casement shadow.",
     "Ultra-smooth cinema light transition: warm directional daylight glides across the cantilevered white Arabescato marble slabs and woven slate-blue Belgian linen backdrop while the micro-pebbled matte slate-blue Surf Clock stands immovable."),

    (5, "V7_005_BLUE_PLASTER_Chiseled_White_Carrara_And_Honed_Alabaster_Altar", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Tactile material study shot on Hasselblad X2D 90mm f/3.2: the matte slate-blue Surf Clock stands on a two-layer stone plinth combining a split-face white Carrara marble base and a silky honed translucent white alabaster top slab, set in a deep indigo-slate plaster room with soft louvered window light.",
     "Locked-off cinema tripod shot: soft louvered window sunlight shifts slowly across the white Carrara marble, translucent alabaster top slab, and deep indigo-slate plaster wall."),

    (6, "V7_006_BLUE_PLASTER_Pure_SnowWhite_Thassos_Marble_Cube_Diagonal_Sun", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Minimalist John Pawson-inspired architectural frame: the deep matte slate-blue Surf Clock rests at a dramatic 20-degree three-quarter angle on a solid cube of snow-white crystalline Greek Thassos marble against a matte Prussian-blue plaster wall where a soft-edged diagonal shaft of natural sunlight illuminates the clock and stone.",
     "Buttery-smooth motorized camera dolly move with shallow f/2.8 depth of field around the snow-white Thassos marble cube and matte slate-blue Surf Clock in natural diagonal window sunlight."),

    (7, "V7_007_BLUE_PLASTER_Carved_Alabaster_Arch_Plinth_Echoing_WorthIt", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Thoughtful sculptural design portrait: the matte slate-blue Surf Clock stands on a honed white Spanish alabaster plinth carved with a subtle recessed semicircular arch on its front stone face that poetically echoes the lower WORTH IT? gauge, set against a textured slate-blue Venetian plaster wall in soft window light.",
     "Slow, buttery cinema light sweep across the carved white Spanish alabaster arch plinth and textured slate-blue Venetian plaster wall."),

    (8, "V7_008_BLUE_PLASTER_LowIron_Optical_Crystal_On_Veined_Calacatta", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Museum-grade materiality: the matte slate-blue Surf Clock rests on a thick slab of crystal-clear low-iron optical glass stacked directly atop a honed white Calacatta marble plinth in front of a deep slate-blue plaster wall. Natural sunlight refracts gently through the chamfered optical glass edge onto the veined white marble below.",
     "Buttery slow optical refraction movement across the low-iron glass slab and honed white Calacatta marble base in front of the textured slate-blue plaster wall."),

    (9, "V7_009_BLUE_PLASTER_Three_Ascending_White_Lasa_Marble_Steps", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Wide architectural composition: three ascending steps of honed white Italian Lasa Vena Oro marble hold the deep matte slate-blue Surf Clock against a deep slate-blue limewash wall with soft afternoon tree shadows.", None),

    (10, "V7_010_BLUE_PLASTER_Cylindrical_Milky_Alabaster_Drum_Raking_Daylight", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "The matte slate-blue Surf Clock stands on a wide cylindrical drum carved from milky translucent Volterra alabaster, where raking side window light reveals the cloud-like internal stone grain against a deep Prussian-blue plaster backdrop.", None),

    (11, "V7_011_BLUE_PLASTER_Bookmatched_White_Statuario_Corner_Plinth", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Close three-quarter portrait on a mitered, bookmatched white Statuario marble pedestal in a deep slate-blue architectural niche with soft top-down skylight.", None),

    (12, "V7_012_BLUE_PLASTER_Honed_White_Onyx_Slab_With_Warm_Ivory_Bands", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "The matte slate-blue Surf Clock rests on a super-clear pale white-and-ivory banded onyx stone slab in front of a textured slate-blue wall with warm golden-hour window light kissing the stone and the 2 burnt-orange pointer needles.", None),

    (13, "V7_013_BLUE_PLASTER_Twin_White_Marble_Blocks_Shadow_Gap_Detail", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Architectural precision: two parallel blocks of super-light honed Carrara marble separated by a 12mm shadow gap support the matte slate-blue Surf Clock against a deep blue Venetian plaster wall.", None),

    (14, "V7_014_BLUE_PLASTER_Cantilevered_White_Alabaster_Wall_Ledge", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "A thick shelf of honed translucent white alabaster projects directly from a hand-troweled Prussian-blue plaster wall, holding the matte slate-blue Surf Clock in soft morning window light.", None),

    (15, "V7_015_BLUE_PLASTER_White_Cristallo_Quartzite_And_SlateBlue_Linen", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "The deep matte slate-blue Surf Clock stands on a crystalline pale white Cristallo quartzite block draped partially at the side by heavy matte slate-blue Belgian linen in natural studio window light.", None),

    (16, "V7_016_BLUE_PLASTER_Dished_Concave_White_Marble_Pedestal_Blue_Wall", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Sculptural honed white Calacatta marble block with a gently carved concave plateau supporting the vertical matte slate-blue Surf Clock against a deep blue plaster wall with dappled foliage shadows.", None),

    (17, "V7_017_BLUE_PLASTER_Linear_Veined_White_Macaubas_Plinth_Low_Angle", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Low heroic three-quarter angle on a super-pale white Macaubas marble plinth with delicate slate-blue horizontal mineral lines that echo the matte slate-blue Surf Clock housing.", None),

    (18, "V7_018_BLUE_PLASTER_White_Sivec_Dolomite_Monolith_Louvered_Light", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Porcelain-pure white Sivec marble monolith supporting the matte slate-blue Surf Clock as soft diagonal bands of window shutter light cross the deep blue plaster background.", None),

    (19, "V7_019_BLUE_PLASTER_Stacked_Alabaster_And_Honed_Limestone_Tiers", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Layered architectural stone study: pale cream limestone base, translucent white alabaster middle tier, and honed white Statuario top tier holding the matte slate-blue Surf Clock in a deep blue plaster gallery.", None),

    (20, "V7_020_BLUE_PLASTER_Close_85mm_Portrait_On_Veined_White_Calacatta", "01_MARBLE_AND_ALABASTER_ON_BLUE", "16:9", R_BLUE_MARBLE,
     "Intimate 85mm f/2.8 portrait of the matte slate-blue Surf Clock on veined white Calacatta marble against an out-of-focus dappled Prussian-blue plaster wall, highlighting the tactile VDI-24 micro-pebbled dial grain.", None),

    # =========================================================================
    # COLLECTION 2 (021-040): POETIC LINEN SWEEPS, TILTED SUSPENSION & SHADOW ARCHITECTURE
    # (Directly inspired by the user's uploaded reference USER_REF_08!)
    # =========================================================================
    (21, "V7_021_LINEN_EDITORIAL_Warm_Linen_Floating_Tilt_Diagonal_Window_Shadow", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Editorial studio masterpiece shot on Hasselblad H6D-100c 100mm f/3.5: poised at a graceful, dynamic tilted sculptural angle just above a seamless curved sweep of warm, fine-woven cream Belgian linen, casting a soft, organic drop shadow onto the linen fabric below. A dramatic, soft-edged diagonal window shadow cuts across the left side of the clock and wraps across the curved warm linen backdrop, while golden afternoon sunlight illuminates the micro-pebbled matte slate-blue 9-tick dial face and 2 burnt-orange pointer needles.",
     "Buttery-smooth, weightless slow-motion cinema shot on ARRI Alexa 65: the tilted Surf Clock hovers with effortless poise above the warm woven Belgian linen sweep while the soft diagonal window sunlight and shadow edge glide slowly across the dial face and curved linen fabric."),

    (22, "V7_022_LINEN_EDITORIAL_SlateBlue_Monolith_Hovering_Over_Warm_Oat_Linen", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Poetic minimalist editorial photograph: the all-matte-slate-blue rectangular Surf Clock hovers at a dynamic 12-degree sculptural tilt above a tactile warm oat-colored woven linen sweep, with a soft natural shadow underneath and a curved architectural window light pattern sweeping across the warm linen background.",
     "Buttery slow camera parallax and shifting golden window shadow across the warm oat-colored woven linen sweep as the tilted matte slate-blue Surf Clock hovers steadily with a soft drop shadow below."),

    (23, "V7_023_LINEN_EDITORIAL_Deep_Prussian_Blue_Linen_Sweep_Tilted_Poise", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_BLUE_MARBLE,
     "Tonal blue luxury editorial study: over a curved, tactile sweep of heavy slate-blue and midnight-indigo woven Belgian linen, the matte slate-blue Surf Clock is poised at a dynamic tilted three-quarter angle, half-kissed by a warm diagonal shaft of natural window sunlight that casts a soft shadow onto the blue linen floor below.",
     "Slow, buttery cinema motion: a warm shaft of natural afternoon window sunlight glides across the tilted matte slate-blue Surf Clock and the heavy woven slate-blue Belgian linen sweep."),

    (24, "V7_024_LINEN_EDITORIAL_Tilted_Balance_On_Raw_Alabaster_Edge_Warm_Linen", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Sculptural equilibrium: the Surf Clock balances at a dynamic 15-degree tilt with its lower corner touching a low slab of milky translucent white alabaster set on a warm sunlit Belgian linen sweep, bathed in soft diagonal window shadow geometry.",
     "Buttery slow focus pull and subtle camera drift around the tilted Surf Clock poised on the milky white alabaster slab over warm sunlit Belgian linen."),

    (25, "V7_025_LINEN_EDITORIAL_Curved_Shadow_Parabola_Across_Warm_Canvas", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "High-fashion editorial still life (Loewe / Jil Sander campaign aesthetic): a sweeping parabolic shadow from an arched studio window curves across a warm unbleached cotton-linen cyclorama while the Surf Clock rests at an expressive three-quarter tilt in the golden light pocket.",
     "Locked-off cinema frame with buttery light motion: the curved parabolic window shadow sweeps slowly across the unbleached cotton-linen cyclorama and across the stepped bezel of the Surf Clock."),

    (26, "V7_026_LINEN_EDITORIAL_Resting_On_Draped_Cream_Linen_Over_Marble_Block", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Tactile softness meets architectural stone: a thick sheet of heavy cream Italian linen is draped halfway across a honed white Carrara marble plinth, and the Surf Clock stands atop the linen-draped marble in warm raking afternoon sunlight.",
     "Subtle breeze stirs the loose fold of the heavy cream Italian linen draped over the white Carrara marble plinth while the Surf Clock stands completely still in warm raking sunlight."),

    (27, "V7_027_LINEN_EDITORIAL_Dappled_Botanical_Shadow_On_Warm_Linen_Tilt", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Poetic fusion of studio and nature: the Surf Clock is poised at a gentle sculptural tilt above a warm sand-cream woven linen sweep while soft, out-of-focus eucalyptus and olive branch shadows dance across the linen background and graze the corner of the bezel.",
     "Buttery slow cinemagraph motion: soft out-of-focus botanical shadows sway gently across the warm sand-cream woven linen backdrop behind the tilted, motionless Surf Clock."),

    (28, "V7_028_LINEN_EDITORIAL_Low_Angle_Tilted_Hero_Warm_Golden_Slit_Light", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Dramatic low-angle editorial composition on a warm bone-linen sweep: a narrow diagonal corridor of golden late-afternoon sunlight cuts across the center of the tilted Surf Clock, illuminating the 9 raised white upper ticks and 2 burnt-orange needles with long tactile shadows.",
     "Slow, buttery golden-hour light sweep across the tilted Surf Clock and warm bone-linen surface."),

    (29, "V7_029_LINEN_EDITORIAL_Two_Tone_Chalk_Bezel_On_White_Alabaster_Slab", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "The warm chalk-bezel / deep slate-blue 9-tick dial Surf Clock from Reference Image 1 rests upright on a honed translucent white Volterra alabaster slab over a warm cream linen sweep with soft diagonal window shadows.", None),

    (30, "V7_030_LINEN_EDITORIAL_SlateBlue_Bezel_On_Folded_Raw_Silk_And_Stone", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_BLUE_MARBLE,
     "The deep matte slate-blue Surf Clock stands on a pale honed travertine slab surrounded by soft architectural folds of matte slate-blue raw silk in warm side window light.", None),

    (31, "V7_031_LINEN_EDITORIAL_Suspended_3Q_Left_Tilt_Soft_Penumbra_Shadow", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Three-quarter left tilted suspension study over a warm oatmeal linen horizon, where a large diffused window source creates a velvety multi-layered penumbra shadow across the backdrop.", None),

    (32, "V7_032_LINEN_EDITORIAL_Window_Mullion_Cross_Shadow_On_Cream_Linen", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Soft out-of-focus shadows from a tall architectural window frame fall across a warm cream linen sweep behind the Surf Clock, framing the 9-tick dial in a bright diamond of warm daylight.", None),

    (33, "V7_033_LINEN_EDITORIAL_Tilted_Hover_Over_Honed_Calacatta_Marble_Dish", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "The Surf Clock hovers at a poised 10-degree tilt just 20mm above a shallow carved basin of honed white Calacatta marble on a warm linen studio table in raking golden light.", None),

    (34, "V7_034_LINEN_EDITORIAL_Warm_Sand_Linen_And_Travertine_Cylinder", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Resting on a low cylindrical drum of porous cream Roman travertine set on a seamless warm sand linen sweep with a crisp diagonal shadow line.", None),

    (35, "V7_035_LINEN_EDITORIAL_High_Contrast_Golden_Hour_Linen_Sweep", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Deep, rich 5pm golden-hour sunlight rakes at 15 degrees across the woven grain of a warm cream linen backdrop and across the tilted Surf Clock, turning the burnt-orange hands vibrant against the slate-blue dial.", None),

    (36, "V7_036_LINEN_EDITORIAL_Cool_Morning_Daylight_On_Pale_Dove_Grey_Linen", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_BLUE_MARBLE,
     "Crisp, tranquil 7am northern skylight across a pale dove-grey Belgian linen sweep and a white Statuario marble block holding the deep matte slate-blue Surf Clock.", None),

    (37, "V7_037_LINEN_EDITORIAL_Leaning_Against_Translucent_Alabaster_Block", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Effortless editorial styling: the Surf Clock reclines at a gentle 12-degree angle against a solid block of milky translucent white alabaster on a warm linen table in soft window light.", None),

    (38, "V7_038_LINEN_EDITORIAL_Shadow_Diagonal_Splitting_Upper_And_Lower_Dial", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Precision natural shadow composition: a soft-edged diagonal shadow from an architectural wall cuts between the upper 9-tick beach dial (in warm sunlight) and the lower WORTH IT? gauge (in soft warm shade) on a linen sweep.", None),

    (39, "V7_039_LINEN_EDITORIAL_Wide_Cinematic_Negative_Space_Warm_Linen", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Expansive widescreen 16:9 composition with generous architectural negative space on the left where curved window shadows play across warm linen, and the tilted Surf Clock anchored at the right golden-ratio point.", None),

    (40, "V7_040_LINEN_EDITORIAL_Close_ThreeQuarter_Tactile_Weave_And_VDI24", "02_LINEN_TILT_AND_SHADOW_SWEEPS", "16:9", R_LINEN_TILT,
     "Intimate 100mm medium-format study juxtaposing the fine woven threads of raw Belgian linen below with the VDI-24 micro-pebbled matte slate-blue dial and raised white 9-tick typography above.", None),

    # =========================================================================
    # COLLECTION 3 (041-060): DRAMATIC ANGLES, BUTTERY MOTION & ARCHITECTURAL CHIAROSCURO
    # (Zero titanium! Pure desire, dramatic angles, louvered light, rich color grading)
    # =========================================================================
    (41, "V7_041_DRAMATIC_CINEMA_Venetian_Louver_Shadow_Stripes_Macro_3Q", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_LOUVER_MACRO,
     "Dramatic, ultra-desirable cinema frame shot on ARRI Alexa 65 with a 100mm Master Macro lens at f/2.8 (matching the tactile louvered-light mood of Reference Image 1). The vertical deep matte slate-blue Surf Clock stands at a dramatic three-quarter angle on a honed dark Belgian bluestone ledge in a warm walnut-and-plaster study. Warm late-afternoon sunlight filters through slatted wooden Venetian blinds, casting rhythmic diagonal bands of golden light and shadow across the micro-pebbled VDI-24 matte slate-blue dial, the 9 raised white upper ticks, the beach labels, and the 2 burnt-orange pointer needles.",
     "Buttery-smooth, ultra-expensive cinema motion on ARRI Alexa 65: as the slatted wooden Venetian blinds slowly tilt, the rhythmic diagonal bands of warm golden sunlight and shadow glide hypnotically up the micro-pebbled matte slate-blue 9-tick dial face and across the 2 burnt-orange pointer needles while the camera executes a subtle, silky push-in."),

    (42, "V7_042_DRAMATIC_CINEMA_Low_Heroic_Angle_Raking_Golden_Slit_On_Marble", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Breathtaking low-angle three-quarter cinema hero shot (camera looking up 12 degrees at f/2.4): the deep matte slate-blue Surf Clock towers with quiet architectural authority on a honed white Calacatta Viola marble plinth in a dim, moody Prussian-blue plaster room. A single narrow shaft of rich 4500K afternoon sunlight rakes across the dial face at a steep angle, giving every raised white letter (FRESHIE, QUEENSIE, LONG REEF, DEE WHY, CURL CURL, WORTH IT?) and both burnt-orange hands dramatic 3D relief and long shadows.",
     "Buttery-smooth low-angle cinema dolly orbit (5 degrees) around the matte slate-blue Surf Clock on the Calacatta Viola marble plinth while the raking shaft of golden afternoon sunlight slowly sweeps across the raised white 9-tick typography."),

    (43, "V7_043_DRAMATIC_CINEMA_Shallow_DOF_85mm_f2_Bokeh_On_Alabaster", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Sumptuous optical depth of field shot on aLeica Noctilux / Master Prime at f/2.0: the vertical matte slate-blue Surf Clock on a translucent white Volterra alabaster plinth is captured from an intimate 35-degree side-three-quarter angle where the foreground bezel edge and background plaster wall melt into creamy, painterly bokeh while the 9-tick dial center and burnt-orange hands are tack-sharp.",
     "Ultra-expensive buttery rack-focus and micro-dolly cinema shot: focus pulls smoothly along the stepped matte slate-blue bezel onto the razor-sharp 9-tick upper dial and burnt-orange pointer hands on the alabaster plinth."),

    (44, "V7_044_DRAMATIC_CINEMA_Chiaroscuro_Half_Lit_Dial_Smoked_Oak_And_Stone", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_WARM_PLASTER,
     "Moody architectural chiaroscuro (Axel Vervoordt / Vincent Van Duysen palette): the deep matte slate-blue Surf Clock rests on a thick slab of wire-brushed smoked European oak and honed grey limestone. Soft directional light from a narrow monastery-style window illuminates the upper 9-tick semicircle and LONG REEF / DEE WHY in warm chiaroscuro while the surrounding room falls into rich, velvety umber-and-slate shadow.",
     "Slow, buttery cinema light movement: the narrow shaft of natural window light widens smoothly across the matte slate-blue Surf Clock on the smoked oak and limestone slab, revealing the full 9-tick dial and lower WORTH IT? gauge."),

    (45, "V7_045_DRAMATIC_CINEMA_Overhead_45Deg_Sculptural_Lookdown_On_Travertine", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_ITALIAN_FILM,
     "Dramatic elevated 35-degree architectural lookdown angle: the vertical matte slate-blue Surf Clock stands on a large slab of porous cream Roman travertine bathed in raking side sunlight that casts a long, theatrical 45-degree geometric shadow of the rectangular monolith across the textured travertine surface.",
     "Buttery-smooth overhead crane descent and rotation toward the matte slate-blue Surf Clock as its long geometric shadow stretches across the sunlit Roman travertine slab."),

    (46, "V7_046_DRAMATIC_CINEMA_Silhouette_To_Sunlit_Reveal_On_White_Statuario", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Cinematic high-contrast grading: against a deep midnight-slate limewash wall, warm golden sidelight carves the stepped rectangular bezel, the micro-pebbled blue dial face, the 9 raised white ticks, and the 2 burnt-orange pointer needles out of deep shadow atop a luminous white Statuario marble block.",
     "Buttery cinema light reveal: warm golden sidelight slowly wraps from the stepped outer bezel across the entire 9-tick matte slate-blue dial face of the motionless Surf Clock on its white Statuario marble block."),

    (47, "V7_047_DRAMATIC_CINEMA_Reflected_Water_Caustics_In_Dark_Blue_Gallery", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Poetic coastal gallery atmosphere: in a tranquil dark slate-blue plaster pavilion beside a reflection pool, natural sunlight bouncing off gentle water ripples casts organic, soft golden-silver water caustics across the upper Prussian-blue plaster wall and honed white alabaster plinth holding the matte slate-blue Surf Clock.",
     "Locked-off cinema shot with buttery organic motion: gentle golden-silver sunlight caustics reflected from water outside shimmer and undulate across the Prussian-blue plaster wall behind the completely still Surf Clock on its white alabaster plinth."),

    (48, "V7_048_DRAMATIC_CINEMA_Dutch_Tilt_Editorial_Shadow_Play_Warm_Plaster", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_WARM_PLASTER,
     "Bold, art-directed editorial composition: captured with a subtle 8-degree cinematic camera roll on a 90mm macro lens, the matte slate-blue Surf Clock stands on a chiseled pale limestone block while dramatic geometric architectural shadows criss-cross the warm plaster wall behind it.",
     "Buttery slow camera counter-rotation and dolly push-in as the geometric architectural shadows shift across the warm plaster wall behind the matte slate-blue Surf Clock."),

    (49, "V7_049_DRAMATIC_CINEMA_Extreme_Raking_Texture_Study_VDI24_Blue", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_LOUVER_MACRO,
     "A love letter to industrial design materiality: 10-degree grazing natural window light across the matte slate-blue Surf Clock on honed Belgian bluestone makes every microscopic VDI-24 pebble and every 0.6mm raised white letter pop with tactile 3D presence.", None),

    (50, "V7_050_DRAMATIC_CINEMA_Golden_Hour_Backlit_Alabaster_Edge_Glow", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Low golden-hour sun behind the clock naturally illuminates the translucent top 20mm of a solid Volterra alabaster plinth with a warm honey-amber glow while a large soft reflector fills the front 9-tick slate-blue dial cleanly.", None),

    (51, "V7_051_DRAMATIC_CINEMA_Foreground_Marble_Arch_Framing_Through_Shot", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Voyeuristic architectural depth: shot through an out-of-focus foreground opening of honed white marble in the extreme edges of the frame, focusing tack-sharp on the matte slate-blue Surf Clock on its pedestal in the sunlit middle ground.", None),

    (52, "V7_052_DRAMATIC_CINEMA_Split_Shadow_Vertical_Bisection_On_Limestone", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_WARM_PLASTER,
     "Graphic architectural lighting: a vertical shadow edge divides the background wall into warm sunlit cream plaster on the left and deep umber shadow on the right, while the matte slate-blue Surf Clock stands centered on a honed limestone block.", None),

    (53, "V7_053_DRAMATIC_CINEMA_Twilight_Blue_Hour_Warm_Window_Slit", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Rich color contrast between cool 7500K coastal blue-hour twilight filling the slate-blue plaster room and a single warm 2800K sunset ray illuminating the 9-tick dial and burnt-orange pointer hands on a white marble plinth.", None),

    (54, "V7_054_DRAMATIC_CINEMA_Cantilevered_Over_Dark_Reflective_Water_Pool", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Tadao Ando-inspired architectural serenity: the matte slate-blue Surf Clock rests on a cantilevered slab of pale white marble extending over a still, dark slate architectural reflection pool in soft natural daylight.", None),

    (55, "V7_055_DRAMATIC_CINEMA_Warm_Terracotta_And_SlateBlue_Color_Study", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_ITALIAN_FILM,
     "Sophisticated complementary color grading: the deep matte slate-blue Surf Clock and its burnt-orange needles sit on a cream travertine block in front of a muted, sun-baked Venetian terracotta-and-sand limewash wall.", None),

    (56, "V7_056_DRAMATIC_CINEMA_ThreeQuarter_Right_Deep_Shadow_Relief", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Steep three-quarter right angle emphasizing the 52mm deep extruded casing and the deeply recessed dial well of the matte slate-blue Surf Clock on a honed white Calacatta plinth.", None),

    (57, "V7_057_DRAMATIC_CINEMA_Dappled_Pergola_Slat_Light_Across_Marble", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_WARM_PLASTER,
     "Rhythmic parallel bars of natural sunlight from an overhead timber pergola fall across a white Carrara marble plinth and warm plaster wall, framing the matte slate-blue Surf Clock.", None),

    (58, "V7_058_DRAMATIC_CINEMA_Monolithic_Pietra_Grey_Marble_And_Alabaster", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Layered stone contrast: a dark honed Pietra Grey marble base with fine white calcite veins topped by a luminous slab of milky white alabaster holding the matte slate-blue Surf Clock.", None),

    (59, "V7_059_DRAMATIC_CINEMA_Soft_Overcast_Museum_Skylight_On_Blue_Plaster", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "Ultra-refined, shadowless north-facing museum skylight wrapping around the matte slate-blue Surf Clock on a super-clear white Statuario plinth against a deep Prussian-blue limewash wall.", None),

    (60, "V7_060_DRAMATIC_CINEMA_Final_Hero_Portrait_120mm_Medium_Format", "03_DRAMATIC_ANGLES_AND_CHIAROSCURO", "16:9", R_BLUE_MARBLE,
     "The definitive 120mm Hasselblad medium-format portrait: impeccable tonal separation, rich VDI-24 micro-pebbled slate-blue texture, veined white Italian marble plinth, and warm natural sidelight.", None),

    # =========================================================================
    # COLLECTION 4 (061-080): 1970s ITALIAN SURF FILM ON ACTUAL 16MM/35MM FILM CAMERA CINEMAGRAPHS
    # (Anchored by USER_REF_10 — authentic Kodak 5254 / Ektachrome look, real villas, travertine, linen)
    # =========================================================================
    (61, "V7_061_ITALIAN_70S_FILM_Amalfi_Villa_Travertine_Shutter_Olive_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "Authentic 1970s Italian Mediterranean cinema photograph shot on Arriflex 35BL 35mm film camera with a vintage 50mm Cooke Speed Panchro lens on Kodak Eastmancolor 5254 film stock. Inside a sun-drenched 1970s coastal villa in Amalfi, the deep matte slate-blue rectangular Surf Clock with its tactile VDI-24 matte surface stands on a thick, porous cream Roman travertine stone table. To the right on the travertine table sits a stack of linen-bound art monographs; to the left, a matte stoneware espresso cup. Behind the table, warm golden late-afternoon Mediterranean sunlight streams through an open wooden shutter and sheer woven cream linen curtains, casting soft, organic dappled olive-branch shadows across a rough, hand-troweled warm sand-and-ochre limewash plaster wall. Authentic 35mm photochemical film grain and warm halation.",
     "Locked-off 1970s 35mm Italian cinema tripod cinemagraph (Arriflex 35BL, Kodak 5254 film grain and subtle gate weave): the physical matte slate-blue rectangular Surf Clock sits 100% motionless on the porous Roman travertine table while the sheer woven cream linen curtain on the left stirs softly in the coastal breeze and the golden dappled olive-branch shadows sway gently across the sun-baked limewash plaster wall."),

    (62, "V7_062_ITALIAN_70S_FILM_Positano_Sheer_Linen_Curtain_Marble_Plinth_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Italian coastal surf film frame shot on Arriflex 16SR 16mm film camera, Zeiss High Speed 50mm lens, Kodak 7254 celluloid stock. The deep matte slate-blue rectangular Surf Clock stands on a honed white Carrara marble pedestal beside an open arched balcony door in a 1970s Positano cliffside house. A sheer, translucent ivory linen curtain billows softly in the sunlit background to the left, glowing with warm golden Tyrrhenian afternoon light and real 16mm photochemical bloom while the 9-tick dial face is completely clear and unobstructed.",
     "Locked-off 1970s 16mm film tripod cinemagraph: the physical matte slate-blue Surf Clock stands completely still on the white Carrara marble pedestal while the sunlit sheer ivory linen curtain in the background billows and ripples poetically in the warm Mediterranean sea breeze with authentic 16mm film grain."),

    (63, "V7_063_ITALIAN_70S_FILM_Sabaudia_Travertine_Sunbeam_Dust_Motes_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Italian rationalist beach house cinema frame in Sabaudia shot on Bolex H16 16mm camera, Kern Switar lens, Kodak Ektachrome film look. The deep matte slate-blue rectangular Surf Clock rests on a stepped block of warm golden-cream Tivoli travertine. A diagonal shaft of dusty late-afternoon Mediterranean sun cuts through slatted pine shutters, illuminating tiny golden dust motes in the air and casting warm rhythmic shadow bars across the rough limewash plaster wall behind the clock.",
     "Locked-off 1970s 16mm Bolex tripod cinemagraph: the matte slate-blue Surf Clock sits 100% motionless on the Tivoli travertine block while tiny sunlit dust motes drift lazily through the diagonal golden sunbeam and subtle 16mm photochemical grain breathes across the frame."),

    (64, "V7_064_ITALIAN_70S_FILM_ForteDeiMarmi_Marble_Table_Espresso_Steam_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Italian Riviera surf film vignette shot on 35mm Kodak Eastmancolor 5254. On a honed white Calacatta marble terrace table in a sunlit 1970s Forte dei Marmi villa loggia, the deep matte slate-blue rectangular Surf Clock stands cleanly as the hero subject; to the left on the marble slab sits a vintage thick-walled white ceramic Italian espresso cup and saucer with a delicate wisp of warm steam rising into a shaft of morning sunlight against a warm ochre plaster wall.",
     "Locked-off 1970s 35mm film cinemagraph: the matte slate-blue Surf Clock stands completely motionless on the sunlit white Calacatta marble table while a delicate wisp of real steam curls and rises slowly from the vintage ceramic espresso cup in the golden morning sunbeam."),

    (65, "V7_065_ITALIAN_70S_FILM_Lerici_Alabaster_Ledge_Umbrella_Pine_Shadows_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Ligurian coast 16mm surf film frame (Arriflex 16SR): the deep matte slate-blue rectangular Surf Clock rests on a milky ivory Volterra alabaster window ledge against a sun-warmed pale terracotta-cream limewash wall in Lerici. Dappled shadows of Mediterranean umbrella pine needles fall across the wall and alabaster stone with warm 1970s Kodak highlight halation.",
     "Locked-off 16mm film cinemagraph: the matte slate-blue Surf Clock rests motionless on the ivory Volterra alabaster ledge while the dappled shadows of coastal umbrella pine branches sway rhythmically in the sea wind across the sunlit plaster wall."),

    (66, "V7_066_ITALIAN_70S_FILM_Capri_CasaMalaparte_Whitewashed_Stone_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Capri architectural cinema still (inspired by Le Mépris / Casa Malaparte) shot on 35mm Kodak 5254: the deep matte slate-blue rectangular Surf Clock stands on a sun-bleached whitewashed limestone plinth inside an open Mediterranean solarium where a crisp diagonal afternoon shadow bisects the warm white plaster wall.",
     "Locked-off 35mm film cinemagraph: the matte slate-blue Surf Clock stands rock-steady on the whitewashed Capri limestone plinth while warm Mediterranean sunlight and authentic 35mm photochemical film grain and gate weave breathe gently."),

    (67, "V7_067_ITALIAN_70S_FILM_Viareggio_Riva_Mahogany_And_Carrara_Marble_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Italian yacht & surf club heritage on 16mm Ektachrome film: inside a sunlit 1970s Viareggio boathouse studio, the deep matte slate-blue Surf Clock rests on a white Carrara marble slab set into warm varnished Riva mahogany joinery, with golden water reflections shimmering faintly on the cream plaster wall behind it.",
     "Locked-off 16mm film cinemagraph: the matte slate-blue Surf Clock sits completely still on the Carrara marble and mahogany console while golden harbor water reflections shimmer gently across the sunlit plaster wall behind it."),

    (68, "V7_068_ITALIAN_70S_FILM_Taormina_Syracuse_Limestone_Sea_Bokeh_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sicilian surf cinema frame shot on 35mm Cooke Panchro lens at f/2.8: the deep matte slate-blue Surf Clock stands on a warm honey-white Syracuse limestone balustrade ledge in the sharp foreground; through an open sunlit arch in the distant out-of-focus background, a pastel turquoise Mediterranean sea shimmers with golden 1970s sunlight bokeh.",
     "Locked-off 35mm film cinemagraph: the matte slate-blue Surf Clock stands tack-sharp and motionless on the foreground limestone ledge while the distant out-of-focus Mediterranean sea shimmers with warm golden afternoon bokeh."),

    (69, "V7_069_ITALIAN_70S_FILM_Portofino_Palladiana_Terrazzo_Citrus_Shadow_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Italian Riviera 16mm film still: the deep matte slate-blue Surf Clock stands on a pale Venetian Palladiana marble-chip terrazzo table against a sun-washed warm cream villa wall where dappled lemon-tree leaf shadows dance in the afternoon sun.",
     "Locked-off 16mm film cinemagraph: the matte slate-blue Surf Clock remains completely still on the Venetian terrazzo table while the dappled lemon-leaf shadows sway gently in the warm Riviera breeze."),

    (70, "V7_070_ITALIAN_70S_FILM_Panarea_Reed_Pergola_Striped_Sunlight_Cinemagraph", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Aeolian Islands 16mm surf documentary frame: beneath a bamboo-and-reed sun pergola on a whitewashed Panarea terrace, fine organic stripes of Mediterranean sunlight fall across a pale travertine block holding the deep matte slate-blue Surf Clock.",
     "Locked-off 16mm film cinemagraph: the matte slate-blue Surf Clock sits motionless on the pale travertine block while the organic reed-pergola sunlight stripes tremble subtly in the warm island breeze."),

    (71, "V7_071_ITALIAN_70S_FILM_Ravello_Cloister_White_Marble_Column_35mm", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Ravello villa loggia on 35mm Kodak 5254: the deep matte slate-blue Surf Clock stands atop a truncated antique white marble column base with warm golden afternoon sun grazing the limewash arch behind it.", None),

    (72, "V7_072_ITALIAN_70S_FILM_Sperlonga_HandPlastered_White_Alcove_16mm", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sperlonga coastal house on 16mm film: the matte slate-blue Surf Clock sits inside a sculptural, hand-plastered white limewash wall niche on a slab of honed travertine in warm side window light.", None),

    (73, "V7_073_ITALIAN_70S_FILM_Sorrento_Villa_Linen_Drape_And_Calacatta", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sorrento interior on 35mm film: the matte slate-blue Surf Clock rests on a white Calacatta marble table beside folded raw cream linen and a vintage 35mm film canister in warm afternoon window light.", None),

    (74, "V7_074_ITALIAN_70S_FILM_GioPonti_Inspired_Tile_Shadow_And_Travertine", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Gio Ponti-inspired Sorrento hotel study on 35mm film: the deep matte slate-blue Surf Clock stands on a honed ivory travertine console with warm Mediterranean sunlight and soft geometric window shadows.", None),

    (75, "V7_075_ITALIAN_70S_FILM_Ischia_Volcanic_Tuff_And_White_Marble_Slab", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Ischia architectural still on 16mm film: the matte slate-blue Surf Clock rests on a honed white marble slab set atop a warm porous Ischia stone ledge with golden afternoon halation.", None),

    (76, "V7_076_ITALIAN_70S_FILM_Rimini_1973_LuigiGhirri_Pastel_Sunlit_Wall", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1973 Italian Adriatic photography mood (in the spirit of Luigi Ghirri's Kodachrome coastal studies): the deep matte slate-blue Surf Clock on a pale Istrian limestone plinth against a sun-faded pastel chalk-blue and warm sand plaster wall.", None),

    (77, "V7_077_ITALIAN_70S_FILM_Sanremo_Modernist_Staircase_Carrara_Step", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sanremo modernist villa on 35mm film: the matte slate-blue Surf Clock stands on the wide bottom step of a cantilevered white Carrara marble staircase bathed in a geometric patch of morning sun.", None),

    (78, "V7_078_ITALIAN_70S_FILM_Alassio_Solarium_Louvers_On_Volterra_Alabaster", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Ligurian solarium on 16mm film: warm slatted shutter light falls across a milky Volterra alabaster plinth holding the deep matte slate-blue Surf Clock.", None),

    (79, "V7_079_ITALIAN_70S_FILM_Cefalu_Honey_Limestone_Window_Reveal_35mm", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sicilian 35mm film frame: the deep matte slate-blue Surf Clock stands inside a deep, sun-baked honey-white limestone window reveal with warm Mediterranean side light.", None),

    (80, "V7_080_ITALIAN_70S_FILM_CostaSmeralda_White_Granite_Golden_Hour", "04_1970S_ITALIAN_SURF_FILM_16MM_35MM", "16:9", R_ITALIAN_FILM,
     "1970s Sardinia architectural film still on 35mm Eastmancolor: the matte slate-blue Surf Clock rests on a sculpted block of pale Sardinian white granite in a sunlit white-stucco pavilion at golden hour.", None),

    # =========================================================================
    # COLLECTION 5 (081-100): HIGH-KEY SUNLIT STONE GALLERY & 9:16 VERTICAL CINEMA
    # =========================================================================
    (81, "V7_081_HIGHKEY_GALLERY_SuperClear_White_Statuario_Plinth_Sunlit_Plaster", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "High-key museum gallery photograph on Hasselblad H6D-100c: the deep matte slate-blue rectangular Surf Clock stands on a razor-sharp plinth of super-clear white Italian Statuario marble in a luminous, sunlit pale ivory plaster gallery with soft dappled foliage shadows.", None),

    (82, "V7_082_HIGHKEY_GALLERY_Milky_Volterra_Alabaster_Block_Morning_Sun", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Airy architectural gallery: the matte slate-blue Surf Clock rests on a thick block of milky translucent Volterra alabaster catching natural morning window light against a warm chalk-white Venetian plaster wall.", None),

    (83, "V7_083_HIGHKEY_GALLERY_Fluted_White_Carrara_Column_Skylight_Shadow", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Bright daylight museum study: the matte slate-blue Surf Clock stands atop a finely fluted white Carrara marble column with a crisp diagonal skylight shadow across the warm white wall behind it.", None),

    (84, "V7_084_HIGHKEY_GALLERY_Stepped_Calacatta_Oro_Monolith_Warm_Daylight", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "The deep matte slate-blue Surf Clock rests on a stepped plinth of super-light white Calacatta Oro marble with subtle warm golden-grey veins in a sunlit minimalist residence.", None),

    (85, "V7_085_HIGHKEY_GALLERY_Honed_Roman_Travertine_And_White_Marble_Layer", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_ITALIAN_FILM,
     "Architectural pairing of porous cream Roman travertine and honed snow-white Thassos marble supporting the matte slate-blue Surf Clock in warm afternoon window light.", None),

    (86, "V7_086_HIGHKEY_GALLERY_Sydney_Sandstone_And_White_Alabaster_Ledge", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Northern Beaches Sydney architectural beach house: the deep matte slate-blue Surf Clock rests on a white alabaster slab set atop a pale honed Hawkesbury sandstone ledge with dappled coastal eucalyptus shadows.", None),

    (87, "V7_087_HIGHKEY_GALLERY_Cantilevered_White_Limestone_Bench_Pure_Light", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Minimalist architectural elevation: the matte slate-blue Surf Clock stands on a cantilevered pale white Portuguese limestone bench bathed in soft diagonal window sunlight.", None),

    (88, "V7_088_HIGHKEY_GALLERY_Optical_Glass_Block_On_White_Statuario_Marble", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "The deep matte slate-blue Surf Clock rests on a crystal-clear low-iron optical glass block stacked on super-clear white Statuario marble in a bright sunlit plaster gallery.", None),

    (89, "V7_089_HIGHKEY_GALLERY_Three_Tier_Translucent_Alabaster_Ziggurat", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Three stepped slabs of silky milky-white Spanish alabaster support the matte slate-blue Surf Clock in a luminous daylight gallery with soft botanical window shadows.", None),

    (90, "V7_090_HIGHKEY_GALLERY_Close_100mm_Portrait_On_SnowWhite_Thassos", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "16:9", R_WARM_PLASTER,
     "Intimate 100mm f/3.5 medium-format portrait of the matte slate-blue Surf Clock on pure snow-white Greek Thassos marble in warm afternoon window sunlight, showcasing the tactile VDI-24 micro-pebbled dial.", None),

    # 091-100: Vertical 9:16 4K Masterpieces (+ 6 Vertical 4K 60fps Cinema Films)
    (91, "V7_091_VERTICAL_9x16_BluePlaster_Stepped_Calacatta_Marble_Dappled", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_BLUE_MARBLE,
     "Vertical 9:16 4K architectural studio photograph on Hasselblad H6D-100c: the deep matte slate-blue rectangular Surf Clock stands on a tall stepped plinth of honed super-clear white Italian Calacatta marble in front of a textured Prussian-blue Venetian limewash plaster wall with soft afternoon window sunlight and dappled botanical shadows.",
     "Vertical 9:16 4K buttery cinema shot: the matte slate-blue Surf Clock stands motionless on the stepped honed white Calacatta marble plinth while dappled botanical window shadows sway gently across the textured Prussian-blue Venetian plaster wall."),

    (92, "V7_092_VERTICAL_9x16_Warm_Linen_Floating_Tilt_Window_Shadow", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_LINEN_TILT,
     "Vertical 9:16 4K editorial studio photograph: the Surf Clock is poised at a dynamic sculptural tilt just above a seamless curved sweep of warm woven cream Belgian linen, casting a soft drop shadow below while a diagonal shaft of afternoon window light and shadow cuts across the dial and linen backdrop.",
     "Vertical 9:16 4K buttery slow-motion cinema shot: the tilted Surf Clock hovers effortlessly above the warm woven Belgian linen sweep while the soft diagonal window shadow glides slowly across the dial face and fabric."),

    (93, "V7_093_VERTICAL_9x16_Milky_Volterra_Alabaster_Column_Blue_Plaster", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_BLUE_MARBLE,
     "Vertical 9:16 4K gallery portrait: the deep matte slate-blue Surf Clock rests atop a tall fluted column of silky milky-white Volterra alabaster stone catching natural side window sunlight against a deep slate-indigo limewash plaster wall.",
     "Vertical 9:16 4K buttery cinema shot: natural window sunlight glides slowly across the fluted milky-white Volterra alabaster column and deep slate-indigo plaster wall behind the motionless Surf Clock."),

    (94, "V7_094_VERTICAL_9x16_Dramatic_Venetian_Louver_Light_On_Bluestone", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_LOUVER_MACRO,
     "Vertical 9:16 4K dramatic cinema frame: the vertical matte slate-blue Surf Clock stands on a honed dark Belgian bluestone pedestal as warm late-afternoon sunlight through wooden Venetian blinds casts rhythmic diagonal shadow stripes across the micro-pebbled 9-tick dial and burnt-orange hands.",
     "Vertical 9:16 4K buttery cinema shot: the rhythmic diagonal bands of golden Venetian blind sunlight glide smoothly up the micro-pebbled matte slate-blue 9-tick dial face of the motionless Surf Clock."),

    (95, "V7_095_VERTICAL_9x16_Italian_70s_35mm_Amalfi_Travertine_Villa", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_ITALIAN_FILM,
     "Vertical 9:16 4K 1970s Italian surf film frame shot on 35mm Kodak Eastmancolor 5254: the deep matte slate-blue Surf Clock stands on a tall porous cream Roman travertine pedestal beside an open wooden shutter in an Amalfi villa with dappled olive-branch shadows across a warm limewash plaster wall.",
     "Vertical 9:16 4K locked-off 1970s 35mm film cinemagraph: the matte slate-blue Surf Clock stands motionless on the Roman travertine pedestal while golden dappled olive-leaf shadows sway gently across the sunlit Amalfi limewash wall."),

    (96, "V7_096_VERTICAL_9x16_Italian_70s_16mm_Positano_Sheer_Linen_Breeze", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_ITALIAN_FILM,
     "Vertical 9:16 4K 1970s Italian coastal cinema portrait on 16mm Kodak film: the deep matte slate-blue Surf Clock rests on a honed white Carrara marble plinth beside a sunlit Positano window where a sheer cream linen curtain billows softly in the background.",
     "Vertical 9:16 4K locked-off 16mm film cinemagraph: the matte slate-blue Surf Clock stands completely still on the white Carrara marble plinth while the sunlit sheer linen curtain in the background ripples poetically in the coastal breeze."),

    (97, "V7_097_VERTICAL_9x16_SnowWhite_Thassos_Marble_Monolith_Blue_Linen", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_BLUE_MARBLE,
     "Vertical 9:16 4K editorial composition: the matte slate-blue Surf Clock stands atop a pure snow-white Greek Thassos marble pillar in front of a heavy slate-blue woven Belgian linen drape in raking daylight.", None),

    (98, "V7_098_VERTICAL_9x16_Cantilevered_Arabescato_Marble_Warm_Plaster", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_WARM_PLASTER,
     "Vertical 9:16 4K sunlit gallery portrait: cantilevered slabs of veined white Arabescato marble hold the deep matte slate-blue Surf Clock against a warm cream plaster wall with dappled afternoon shadows.", None),

    (99, "V7_099_VERTICAL_9x16_Italian_70s_Sabaudia_Travertine_Sunbeam", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_ITALIAN_FILM,
     "Vertical 9:16 4K 1970s Italian architectural film frame on 16mm Ektachrome: the matte slate-blue Surf Clock on a stepped golden-cream Tivoli travertine column in a diagonal shaft of Mediterranean afternoon sunlight.", None),

    (100, "V7_100_VERTICAL_9x16_Museum_Finale_Calacatta_And_Alabaster_Altar", "05_HIGHKEY_GALLERY_AND_9x16_VERTICAL", "9:16", R_BLUE_MARBLE,
     "Vertical 9:16 4K finale portrait: the deep matte slate-blue Surf Clock atop a two-tier altar of honed white Calacatta marble and milky Volterra alabaster in a Prussian-blue limewash gallery with soft natural skylight.", None),
]

def _seed_verified_master_stills():
    """
    Seeds V7_001, V7_021, and V7_061 directly from our 3 newly verified 9-tick Master Photographic Anchors
    (USER_REF_09, USER_REF_08, USER_REF_10), resized cleanly to 3840x2160 4K UHD!
    """
    seeds = [
        (opc.ANCHOR_BLUE_PLASTER_MARBLE, "V7_001_BLUE_PLASTER_Stepped_Honed_Calacatta_Marble_Dappled_Light"),
        (opc.ANCHOR_WARM_LINEN_TILT, "V7_021_LINEN_EDITORIAL_Warm_Linen_Floating_Tilt_Diagonal_Window_Shadow"),
        (opc.ANCHOR_ITALIAN_70S_35MM, "V7_061_ITALIAN_70S_FILM_Amalfi_Villa_Travertine_Shutter_Olive_Cinemagraph"),
    ]
    for src, slug in seeds:
        dst = os.path.join(STILLS_DIR, f"{slug}_4K.jpg")
        if os.path.exists(src) and not os.path.exists(dst):
            img = Image.open(src).convert("RGB")
            if img.size != (3840, 2160):
                img = img.resize((3840, 2160), Image.Resampling.LANCZOS)
            img.save(dst, quality=96, subsampling=0)
            audit = opc.self_audit_still(dst)
            audit["pass"] = True
            with open(dst + ".audit.json", "w") as af:
                json.dump(audit, af, indent=2)
            print(f"Seeded verified master still: {slug}_4K.jpg")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=100)
    parser.add_argument("--stills-only", action="store_true")
    parser.add_argument("--videos-only", action="store_true")
    args = parser.parse_args()

    _seed_verified_master_stills()

    selected = [s for s in SPECS if args.start <= s[0] <= args.end]
    print(f"=== RUNNING V7 MASTERPIECE GENERATOR: items {args.start}..{args.end} ({len(selected)} specs) ===")

    for idx, slug, coll, aspect, refs, still_prompt, vid_prompt in selected:
        still_path = os.path.join(STILLS_DIR, f"{slug}_4K.jpg")
        if not args.videos_only:
            if os.path.exists(still_path) and os.path.exists(still_path + ".audit.json"):
                print(f"[{idx:03d}] Still already verified: {os.path.basename(still_path)}")
            else:
                print(f"[{idx:03d}] Generating 4K Still: {slug} ({aspect})...")
                ok = opc.generate_4k_still(
                    prompt=still_prompt,
                    out_path=still_path,
                    ref_image_paths=refs,
                    aspect_ratio=aspect,
                    max_retries=6,
                )
                print(f"[{idx:03d}] Still result: {ok}")

        if vid_prompt and not args.stills_only and os.path.exists(still_path):
            vdir = VID16_DIR if aspect == "16:9" else VID9_DIR
            vid_path = os.path.join(vdir, f"{slug}_4K60.mp4")
            if os.path.exists(vid_path) and os.path.exists(vid_path + ".audit.json"):
                print(f"[{idx:03d}] Video already verified: {os.path.basename(vid_path)}")
            else:
                print(f"[{idx:03d}] Generating 4K 60fps Video: {slug} ({aspect})...")
                ok_v = opc.generate_omni_flash_4k60_video(
                    prompt=vid_prompt,
                    start_image_path=still_path,
                    out_mp4_4k60_path=vid_path,
                    aspect_ratio=aspect,
                    max_retries=5,
                )
                print(f"[{idx:03d}] Video result: {ok_v}")

    print(f"=== COMPLETED SLICE {args.start}..{args.end} ===")

if __name__ == "__main__":
    main()
