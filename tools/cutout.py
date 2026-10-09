import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
src, out = sys.argv[1], sys.argv[2]
crop = tuple(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
excl = tuple(int(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 else None
im = Image.open(src).convert('RGB')
if crop: im = im.crop(crop)
a = np.asarray(im).astype(int)
v = a.mean(2); sat = a.max(2) - a.min(2)
checker = (sat < 14) & (((v > 66) & (v < 100)) | ((v > 118) & (v < 156)) | ((sat < 10) & (v >= 100) & (v <= 118)))
# 1) outer background: flood from border
flood = checker.copy()
if excl:   # near the neon glow: anything that isn't the white sticker border is background
    R = np.zeros_like(flood); R[excl[1]:excl[3], excl[0]:excl[2]] = True
    flood = np.where(R, ~((v > 195) & (sat < 50)), flood)
lab, n = nd.label(flood)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# 2) enclosed checker pockets (strict rule): contain both tones
labc, nc = nd.label(checker)
idx = range(1, nc + 1)
sz = nd.sum(checker, labc, idx); dk = nd.sum(checker & (v < 100), labc, idx); lt = nd.sum(checker & (v > 118), labc, idx)
pockets = np.isin(labc, [i + 1 for i in range(nc) if sz[i] > 400 and dk[i] > 80 and lt[i] > 80])
fg = nd.binary_opening(~bg, iterations=2)
lab2, n2 = nd.label(fg)
keep = 1 + int(np.argmax(nd.sum(fg, lab2, range(1, n2 + 1))))
fg = nd.binary_fill_holes(lab2 == keep) & ~pockets
fg = nd.binary_erosion(fg, iterations=1)
alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
rgba = im.copy(); rgba.putalpha(alpha)
rgba = rgba.crop(rgba.getbbox()); rgba.save(out); print(out, rgba.size)
