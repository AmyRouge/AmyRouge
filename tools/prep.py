import glob, io, os, base64, json
from PIL import Image
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
out = {}
def b64(data): return base64.b64encode(data).decode()
# --- video frames: crop around the character, every frame of the wave window
frames = sorted(glob.glob(S + '/frames/*.png'))
fr = []
for f in frames:
    im = Image.open(f).convert('RGB').crop((330, 0, 990, 720)).resize((330, 360), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=62, optimize=True, progressive=True)
    fr.append(b64(buf.getvalue()))
out['frames'] = fr
print('frames', len(fr), sum(len(x) for x in fr) // 1024, 'KB b64')
def png(im, colors=None):
    if colors:
        im = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True); return b64(buf.getvalue())
pt = Image.open(S + '/point_full.png')
pt = pt.resize((round(pt.width * 760 / pt.height), 760), Image.LANCZOS)
out['point'] = png(pt, 255); out['point_size'] = pt.size
idf = Image.open(S + '/id_full.png')
ill = idf.resize((round(idf.width * 520 / idf.height), 520), Image.LANCZOS)
out['laptop'] = png(ill, 255); out['laptop_size'] = ill.size
# portrait: square crop around the face (coords in id_full space)
face = idf.crop((180, 0, 1000, 820)).resize((360, 360), Image.LANCZOS)
out['face'] = png(face, 255); out['face_size'] = face.size
for k in ('point', 'laptop', 'face'): print(k, out[k + '_size'], len(out[k]) // 1024, 'KB b64')
json.dump(out, open(S + '/assets.json', 'w'))
face.save(S + '/face_chk.png')
