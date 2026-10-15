import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

img = cv2.imread("/Users/jcolley/.gemini/jetski/brain/ad8e6e93-9a00-4c65-9fc3-25a2be0e07eb/.user_uploaded/media_1791866899748.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img_rgb.shape

fig, ax = plt.subplots(figsize=(12, 8), dpi=180)
ax.imshow(img_rgb[int(h*0.18):int(h*0.48), int(w*0.42):int(w*1.00)])
ax.grid(True, color='yellow', alpha=0.5, lw=0.6)
ax.minorticks_on()
ax.grid(True, which='minor', color='cyan', alpha=0.25, lw=0.4)
plt.tight_layout()
plt.savefig("/tmp/uln2003_grid_measure.png", dpi=180)
