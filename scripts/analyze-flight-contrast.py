# Compare a frozen frame with and without the subtitle, using its CSS foreground color.
import json
from pathlib import Path
from PIL import Image, ImageChops

out = Path(__file__).resolve().parent.parent
info = json.loads((out / 'flight-contrast.json').read_text())
visible = Image.open(out / 'flight-contrast-text.png').convert('RGB')
background = Image.open(out / 'flight-contrast-background.png').convert('RGB')
if visible.size != background.size or info['dpr'] != 1:
    raise ValueError('Expected equal-sized DPR 1 screenshots')
foreground = (255, 248, 231)
if info['color'] != 'rgb(255, 248, 231)':
    raise ValueError('Foreground changed; update the analysis')
def luminance(rgb):
    vals = [v / 255 for v in rgb]
    return sum(weight * (v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4)
               for v, weight in zip(vals, (.2126, .7152, .0722)))
def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)
rect = info['rect']
rows = []
for y in range(max(0, int(rect['y'])), min(visible.height, int(rect['y'] + rect['h']) + 1)):
    for x in range(max(0, int(rect['x'])), min(visible.width, int(rect['x'] + rect['w']) + 1)):
        if visible.getpixel((x, y)) == foreground:
            bg = background.getpixel((x, y))
            rows.append((contrast(foreground, bg), x, y, bg))
if not rows:
    raise ValueError('No exact foreground pixels found')
rows.sort()
result = {'method': 'CSS foreground versus same-coordinate captured underlying scene at exact foreground pixels; excludes antialias pixels and does not assess the shadow as a potential halo',
          'difference_bbox': ImageChops.difference(visible, background).getbbox(),
          'foreground': foreground, 'exact_foreground_pixels': len(rows),
          'minimum': {'ratio': rows[0][0], 'x': rows[0][1], 'y': rows[0][2], 'background': rows[0][3]},
          'median_ratio': rows[len(rows) // 2][0], 'maximum_ratio': rows[-1][0],
          'pixels_below_4_5': sum(r[0] < 4.5 for r in rows)}
(out / 'flight-contrast-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
