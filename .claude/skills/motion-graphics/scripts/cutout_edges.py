"""Recorta un objeto/persona generado sobre blanco puro y deja alfa real.

Uso: python3 -I cutout_edges.py entrada.png salida.png TAMAÑO [umbral=236] [saturación=14] [erosión=3] [anillo=0]
Borra solo el blanco CONECTADO al borde (un colorkey blanco también borraría los brillos del objeto).
Ropa clara / pelo con halo: python3 -I cutout_edges.py in.png out.png 900 250 6 3 4
"""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

src, dst, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
thr = int(sys.argv[4]) if len(sys.argv) > 4 else 236
sat = int(sys.argv[5]) if len(sys.argv) > 5 else 14
ero = int(sys.argv[6]) if len(sys.argv) > 6 else 3
ring = int(sys.argv[7]) if len(sys.argv) > 7 else 0

im = Image.open(src).convert("RGB")
w0, h0 = im.size
im = im.resize((size, round(size * h0 / w0)), Image.LANCZOS)
a = np.asarray(im).astype(np.int16)
h, w, _ = a.shape
near = (a.min(axis=2) >= thr) & ((a.max(axis=2) - a.min(axis=2)) <= sat)
bg = np.zeros((h, w), bool)
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if near[y, x] and not bg[y, x]:
            bg[y, x] = True; q.append((y, x))
for y in range(h):
    for x in (0, w - 1):
        if near[y, x] and not bg[y, x]:
            bg[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not bg[ny, nx]:
            bg[ny, nx] = True; q.append((ny, nx))
if ring:
    # quita píxeles claros y poco saturados en un anillo fino alrededor del fondo (halo)
    grown = np.asarray(Image.fromarray(bg.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(ring * 2 + 1))) > 0
    light = (a.min(axis=2) >= 200) & ((a.max(axis=2) - a.min(axis=2)) <= 30)
    bg = bg | (grown & light)
alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(ero)).filter(ImageFilter.GaussianBlur(1.2))
out = im.convert("RGBA"); out.putalpha(alpha); out.save(dst)
print("ok", dst, round(bg.mean(), 3))
