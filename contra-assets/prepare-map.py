from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
original = Image.open(ROOT / 'jungle-original.png').convert('RGB').crop((512, 0, 3840, 240))
world = original.copy()


def copy_background(target, source):
    x, y, width, height = target
    sx, sy = source
    world.paste(original.crop((sx, sy, sx + width, sy + height)), (x, y))


for target, source in [
    ((240, 80, 32, 36), (208, 80)),
    ((288, 80, 32, 36), (208, 80)),
    ((352, 80, 32, 36), (208, 80)),
    ((304, 176, 32, 36), (464, 176)),
    ((624, 176, 32, 36), (464, 176)),
    ((1264, 80, 32, 36), (1200, 80)),
    ((1328, 92, 24, 20), (1232, 92)),
    ((1520, 48, 32, 32), (1488, 48)),
    ((1552, 48, 16, 32), (1488, 48)),
    ((2352, 112, 32, 24), (2320, 112)),
    ((2352, 136, 16, 16), (2384, 136)),
    ((2368, 136, 16, 16), (2384, 136)),
    ((2320, 88, 32, 16), (2288, 88)),
    ((2320, 200, 16, 16), (2304, 200)),
    ((2336, 200, 16, 16), (2352, 200)),
]:
    copy_background(target, source)

draw = ImageDraw.Draw(world)
draw.rectangle((0, 0, world.width, 15), fill=(0, 0, 0))
draw.rectangle((240, 56, 271, 71), fill=(0, 0, 0))
draw.rectangle((1120, 88, 1151, 103), fill=(0, 0, 0))
world.save(ROOT / 'jungle.png', optimize=True)

greens = {(0, 148, 0), (128, 208, 16)}
platforms = []
for y in range(68, 229, 16):
    spans = []
    for x in range(0, 3216, 8):
        green_pixels = sum(
            original.getpixel((xx, yy)) in greens
            for yy in range(y, y + 4)
            for xx in range(x, x + 8)
        )
        if green_pixels >= 28:
            if spans and x - spans[-1][1] <= 8:
                spans[-1][1] = x + 8
            else:
                spans.append([x, x + 8])
    for left, right in spans:
        platforms.append({'x': left, 'y': y, 'w': right - left, 'kind': 'ground'})

platforms.extend([
    {'x': 768, 'y': 116, 'w': 128, 'kind': 'bridge'},
    {'x': 1056, 'y': 116, 'w': 128, 'kind': 'bridge'},
    {'x': 2304, 'y': 212, 'w': 64, 'kind': 'ground'},
    {'x': 3200, 'y': 212, 'w': 64, 'kind': 'ground'},
])
platforms.sort(key=lambda item: (item['y'], item['x']))
level = {
    'width': 3328,
    'height': 240,
    'platforms': platforms,
    'turrets': [
        {'x': 1248, 'y': 144, 'type': 'gun'},
        {'x': 1632, 'y': 112, 'type': 'gun'},
        {'x': 1824, 'y': 112, 'type': 'gun'},
        {'x': 2048, 'y': 144, 'type': 'wall'},
        {'x': 2176, 'y': 48, 'type': 'wall'},
        {'x': 2752, 'y': 112, 'type': 'wall'},
        {'x': 2976, 'y': 176, 'type': 'gun'},
        {'x': 3104, 'y': 176, 'type': 'gun'},
    ],
    'supplyBoxes': [
        {'x': 320, 'y': 144, 'weapon': 'M'},
        {'x': 1568, 'y': 144, 'weapon': 'F'},
        {'x': 2272, 'y': 176, 'weapon': 'S'},
    ],
    'flyingSupplies': [
        {'x': 256, 'y': 64, 'weapon': 'S'},
        {'x': 1136, 'y': 96, 'weapon': 'S'},
        {'x': 2336, 'y': 96, 'weapon': 'R'},
        {'x': 2336, 'y': 208, 'weapon': 'B'},
    ],
}
(ROOT / 'level.json').write_text(json.dumps(level, ensure_ascii=False, separators=(',', ':')))

preview = world.crop((0, 0, 768, 240)).resize((1536, 480), Image.Resampling.NEAREST)
preview.save(ROOT / 'jungle-clean-inspection.png')
print(f'Prepared original map: {world.width} x {world.height}; {len(platforms)} collision surfaces')
