import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

img = cv2.imread("/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/.user_uploaded/media_1791866899748.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img_rgb.shape

fig, axes = plt.subplots(1, 3, figsize=(18, 7), dpi=150)
# 1. ESP32 + USB-C + bottom-left corner
axes[0].imshow(img_rgb[int(h*0.40):int(h*0.88), int(w*0.10):int(w*0.60)])
axes[0].set_title("Zoom 1: ESP32-S3 & USB-C Collision")
# 2. Upper ULN2003 boards + Upper Motor
axes[1].imshow(img_rgb[int(h*0.18):int(h*0.55), int(w*0.40):int(w*1.00)])
axes[1].set_title("Zoom 2: ULN2003 Cradles & Upper Stepper")
# 3. Lower Stepper + Bottom Wall + Corner Posts
axes[2].imshow(img_rgb[int(h*0.45):int(h*0.95), int(w*0.40):int(w*1.00)])
axes[2].set_title("Zoom 3: Lower Stepper, Wires & Bottom Wall")
plt.tight_layout()
plt.savefig("/tmp/photo_audit_zooms.png", dpi=150)
