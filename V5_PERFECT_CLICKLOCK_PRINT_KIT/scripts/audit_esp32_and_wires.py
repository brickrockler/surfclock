# Let's verify every dimension of the Freenove ESP32-S3-WROOM board in the user's photo
# Looking at the photo:
# - Silkscreen: "FREENOVE www.freenove.com v1.0", dual USB-C ports at bottom ("USB-UART" on left, "USB-OTG" on right)
# - Standard Freenove ESP32-S3-WROOM PCB dimensions:
#   Width = 28.0 mm (or 28.5 mm), Length = 51.0 to 52.5 mm (20 pins per side at 2.54mm pitch = 48.26mm pin span + ~3.5mm ends = 52.0mm)
# - In the user's photo, the Freenove ESP32-S3 is sitting inside the ESP32 cradle:
#   Our cradle in 3_Motor_Mount_Plate has:
#     esp_y0, esp_y1 = -68.10, -37.90 -> inner width = 30.20 mm!
#     Wait: look closely at the user's photo at the left and right edges of the Freenove ESP32-S3 board!
#     In the photo, the Freenove ESP32-S3 board is ~28.0 mm wide inside a 30.20 mm wide cradle!
#     Look at the right edge of the black Freenove PCB in the photo:
#     The right clips (ESP_ClipY1) barely catch the edge if the board shifts left because 30.20 mm - 28.0 mm = 2.20 mm of side-to-side play!
#     Wait: let's measure the pixel width vs length of the Freenove ESP32-S3 PCB and cradle in the user's photo!

import cv2
import numpy as np

img = cv2.imread("/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/.user_uploaded/media_1791866899748.jpg")
print("Photo resolution:", img.shape)
