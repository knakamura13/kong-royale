# Estimate glyph-edge contrast from a separately rendered mask and the frozen shadow-only frame.
import json
from pathlib import Path
from PIL import Image, ImageChops

out = Path(__file__).resolve().parent.parent
meta = json.loads((out / 'flight-glyph.json').read_text())
images = {n: Image.open(out / f'flight-glyph-{n}.png').convert('RGB') for n in ('text','background','shadow-only','mask')}
full, scene, shadow, mask = (images[n] for n in ('text','background','shadow-only','mask'))
fg = (255, 248, 231)
if meta['dpr'] != 1 or meta['color'] != 'rgb(255, 248, 231)' or len({i.size for i in images.values()}) != 1:
    raise ValueError('Unexpected image geometry or text color')
def luminance(rgb):
    return sum(w * (v/255/12.92 if v/255 <= .04045 else ((v/255+.055)/1.055)**2.4)
               for v,w in zip(rgb,(.2126,.7152,.0722)))
def ratio(rgb):
    a,b=luminance(fg),luminance(rgb)
    return (max(a,b)+.05)/(min(a,b)+.05)
r=meta['rect']
# Use only pixels whose full pixel square lies inside the black mask rectangle.
x0,y0=int(r['x'])+1,int(r['y'])+1
x1,y1=int(r['x']+r['w']),int(r['y']+r['h'])
results=[]
for threshold in (64,128,192,254):
    glyph={(x,y) for y in range(y0,y1) for x in range(x0,x1) if min(mask.getpixel((x,y)))>=threshold}
    ring={(x+dx,y+dy) for x,y in glyph for dx,dy in ((0,1),(0,-1),(1,0),(-1,0))
          if (x+dx,y+dy) not in glyph and x0<=x+dx<x1 and y0<=y+dy<y1}
    if not ring: raise ValueError('Empty glyph edge')
    vals=sorted((ratio(shadow.getpixel(pt)),pt) for pt in ring)
    results.append({'threshold':threshold,'glyph_pixels':len(glyph),'edge_pixels':len(ring),
                    'minimum_ratio':vals[0][0],'minimum_coordinate':vals[0][1],
                    'median_ratio':vals[len(vals)//2][0],'below_4_5':sum(v[0]<4.5 for v in vals)})
result={'method':'Separate white-on-black mask with text shadow disabled; threshold grayscale for glyph coverage, then compare CSS foreground against shadow-only composite at four-neighbor pixels outside the mask.',
        'limitations':'One rendered frame at DPR 1. Grayscale thresholds approximate antialiased glyph boundaries; the external ring is not an authoritative vector outline or a WCAG conformance test. Threshold sensitivity is reported.',
        'text_vs_background_bbox':ImageChops.difference(full,scene).getbbox(),
        'shadow_vs_background_bbox':ImageChops.difference(shadow,scene).getbbox(),
        'results':results}
(out/'flight-glyph-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
