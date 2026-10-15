# Real 28BYJ-48 Stepper Motor Datasheet Z-Dimensions (measured from the front face of the Ø28mm motor can):
# - Front of Ø28mm metal can = 0.00 mm datum (sits against the motor pocket floor of 3_Motor_Mount_Plate)
# - Mounting ears: flush with front of metal can (0.00 mm to -0.80 mm metal thickness) -> wait!
#   STOP AND CHECK THIS ON A REAL 28BYJ-48 STEPPER MOTOR!!
#   Where are the metal mounting ears located along the Z axis of a 28BYJ-48 stepper motor?!
#   THE METAL MOUNTING EARS ARE AT THE FRONT FACE OF THE MOTOR CAN (THE SHAFT SIDE), NOT THE BACK SIDE!!
#   Wait: let's check our motor mount pocket in 3_Motor_Mount_Plate:
#   - In 3_Motor_Mount_Plate:
#     - The bottom of 3_Motor_Mount_Plate (Z_plate = 0.00 mm) touches the back of 2_Dial_Face!
#     - Sub_CanPocket floor is at Z_plate = 2.00 mm!
#     - The ear bosses (Add_Ear) top surface is at Z_plate = 5.00 mm?!
#     WAIT A SECOND!! WHY ARE THE EAR BOSSES AT Z_plate = 5.00 mm IF THEPOCKET FLOOR IS AT Z_plate = 2.00 mm?!
#     LOOK AT ZOOM 2 AND ZOOM 3 OF THE USER'S PHOTO (/tmp/uln2003_grid_measure.png)!!

print("Checking 28BYJ-48 ear height vs can floor in /tmp/uln2003_grid_measure.png!")
