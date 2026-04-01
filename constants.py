G=6.674e-11
MASS_T = 1.34518e23
RAD_T = 2575000.0
RHO_0   = 4.9
H_SCALE = 20600.0
MASS_P  = 318.0          # mass                    (kg)
A_CAP = 5.73           # capsule cross-section   (m²)  — from 2.7 m diameter
 
# Drag coefficient × area for each descent phase.
# We combine C_D and A into one number (called C_D × A, or "CDA") because
# what appears in the drag force equation is always the product of the two.
CDA_PHASE0 = 1.50 * A_CAP           # Phase 0: capsule only, no parachute
CDA_PHASE1 = 0.55 * (A_CAP + 54.1) # Phase 1: main parachute (8.3 m diameter)
CDA_PHASE2 = 0.55 * (A_CAP +  7.1) # Phase 2: stabiliser drogue (3 m diameter)
H_DEPLOY_MAIN   = 160000  # main chute deploys at 160 km altitude
H_DEPLOY_DROGUE =  15000  # drogue takes over  at  15 km altitude