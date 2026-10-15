# 1. Standard Freenove ESP32-S3-WROOM (FNK0085 / v1.0) dimensions & datasheet check:
# The Freenove ESP32-S3-WROOM CAM board has 2x20 pin headers (20 pins * 2.54mm = 50.8mm header length).
# Total PCB length = 66.0 mm (or 65.0 mm) if it's the 21/22-pin version, or let's count the pins in Zoom 1!
# Wait: let's count the pins along the left header of the Freenove ESP32-S3 board in Zoom 1!

import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

img = cv2.imread("/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/.user_uploaded/media_1791866899748.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img_rgb.shape

fig, ax = plt.subplots(figsize=(8, 10), dpi=180)
ax.imshow(img_rgb[int(h*0.41):int(h*0.72), int(w*0.18):int(w*0.52)])
ax.grid(True, color='cyan', alpha=0.4, lw=0.6)
plt.tight_layout()
plt.savefig("/tmp/freenove_closeup.png", dpi=180)
