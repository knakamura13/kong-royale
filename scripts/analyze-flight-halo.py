# Inspect a frozen caption with full text, shadow only, and neither; this is not a WCAG verdict.
import json
from pathlib import Path
from PIL import Image, ImageChops

out = Path(__file__).resolve().parent.parent
meta = json.loads((out / 'flight-halo.json').read_text())
full = Image.open(out / 'flight-halo-text.png').convert('RGB')
shadow = Image.open(out / 'flight-halo-shadow-only.png').convert('RGB')
scene = Image.open(out / 'flight-halo-background.png').convert('RGB')
fg = (255, 248, 231)
if meta['dpr'] != 1 or meta['color'] != 'rgb(255, 248, 231)' or full.size != shadow.size or full.size != scene.size:
    raise ValueError('Unexpected screenshot geometry or foreground')
def lum(rgb):
    return sum(w * (v / 255 / 12.92 if v / 255 <= .04045 else ((v / 255 + .055) / 1.055) ** 2.4)
               for v, w in zip(rgb, (.2126, .7152, .0722)))
def ratio(rgb):
    a, b = lum(fg), lum(rgb)
    return (max(a, b) + .05) / (min(a, b) + .05)
r = meta['rect']
core = {(x, y) for y in range(int(r['y']), int(r['y'] + r['h']) + 1)
        for x in range(int(r['x']), int(r['x'] + r['w']) + 1) if full.getpixel((x, y)) == fg}
if not core:
    raise ValueError('No exact-color pixels')
ring = {(x + dx, y + dy) for x, y in core for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if (x + dx, y + dy) not in core}
def stats(points):
    rs = sorted(ratio(shadow.getpixel(pt)) for pt in points)
    return {'count': len(rs), 'min': rs[0], 'median': rs[len(rs)//2], 'max': rs[-1],
            'below_4_5': sum(v < 4.5 for v in rs)}
result = {'method': 'compare CSS foreground to the shadow-only capture at exact-color glyph pixels and their immediate four-neighbor ring',
          'limit': 'ring is constructed from exact foreground pixels, not true glyph outlines; it includes antialias and interior pixels. No halo-width or conformance conclusion.',
          'full_vs_scene_bbox': ImageChops.difference(full, scene).getbbox(),
          'shadow_vs_scene_bbox': ImageChops.difference(shadow, scene).getbbox(),
          'core': stats(core), 'neighbor_ring': stats(ring)}
(out / 'flight-halo-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
