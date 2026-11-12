from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent


def source(name):
    return Image.open(ROOT / f'{name}-original.png').convert('RGBA')


def transparent(image, colors):
    image = image.copy()
    image.putdata([(0, 0, 0, 0) if pixel[:3] in colors else pixel for pixel in image.getdata()])
    return image


def save(image, name):
    image.save(ROOT / f'{name}.png', optimize=True)


players_source = source('players')
players = Image.new('RGBA', (1024, 512))
for row, y in enumerate([9, 74, 139, 204, 277, 342, 407, 472]):
    for col in range(16):
        x = col * 65 + 1
        cell = transparent(players_source.crop((x, y, x + 64, y + 64)), {(28, 102, 145), (0, 47, 87)})
        players.paste(cell, (col * 64, row * 64))
save(players, 'players')


def pack_frames(image, regions, cell_size, anchor, key_colors):
    atlas = Image.new('RGBA', (cell_size[0] * len(regions), cell_size[1]))
    bounds = []
    for index, region in enumerate(regions):
        frame = transparent(image.crop(region), key_colors)
        frame = frame.crop(frame.getbbox())
        x = anchor[0] - frame.width // 2
        y = anchor[1] - frame.height
        atlas.paste(frame, (index * cell_size[0] + x, y))
        bounds.append([x, y, frame.width, frame.height])
    return atlas, bounds


enemies, enemy_bounds = pack_frames(
    source('enemies'),
    [(1, 12, 25, 52), (26, 12, 50, 52), (50, 12, 69, 52),
     (69, 12, 91, 52), (91, 12, 116, 52), (116, 12, 141, 52), (91, 12, 116, 52)],
    (40, 48), (20, 44), {(0, 47, 87), (0, 0, 0)},
)
save(enemies, 'enemies')

effects = Image.new('RGBA', (160, 40))
for index, region in enumerate([(214, 874, 232, 905), (233, 874, 264, 905), (265, 874, 289, 905), (290, 874, 306, 905)]):
    frame = transparent(players_source.crop(region), {(0, 0, 0), (82, 14, 0), (0, 47, 87)})
    frame = frame.crop(frame.getbbox())
    effects.paste(frame, (index * 40 + (40 - frame.width) // 2, (40 - frame.height) // 2))
save(effects, 'effects')

pickups = Image.new('RGBA', (224, 24))
weapons_source = source('weapons')
for index in range(7):
    x = index * 25 + 1
    frame = transparent(weapons_source.crop((x, 1, x + 24, 17)), {(0, 47, 87), (0, 0, 0)})
    frame = frame.crop(frame.getbbox())
    pickups.paste(frame, (index * 32 + (32 - frame.width) // 2, (24 - frame.height) // 2))
save(pickups, 'pickups')
save(transparent(source('turrets'), {(0, 61, 8)}), 'turrets')

titles = source('titles')
title = titles.crop((0, 0, 256, 240))
title.putdata([(0, 0, 0, 255) if p[:3] in {(221, 0, 255), (117, 0, 135)} else p for p in title.getdata()])
title.paste(titles.crop((32, 496, 224, 576)), (32, 64))
title.paste(titles.crop((0, 312, 256, 344)), (0, 200))
menu = title.crop((32, 144, 128, 192))
menu.putdata([(173, 173, 173, 255) if p[:3] == (255, 255, 255) else p for p in menu.getdata()])
title.paste(menu, (32, 144))
save(title, 'title')
save(transparent(titles.crop((132, 400, 148, 416)), {(221, 0, 255), (0, 0, 0)}), 'cursor')

info = {'players': {'cell': [64, 64], 'anchor': [32, 50], 'swimAnchor': [32, 42]},
        'enemies': {'cell': [40, 48], 'anchor': [20, 44], 'bounds': enemy_bounds}}
(ROOT / 'sprites.json').write_text(json.dumps(info, separators=(',', ':')))
preview = Image.new('RGB', (1024, 720), '#24302a')
preview.paste(players, (0, 0), players)
preview.paste(enemies, (0, 536), enemies)
preview.paste(effects, (320, 540), effects)
preview.paste(pickups, (520, 548), pickups)
preview.paste(title.resize((128, 120), Image.Resampling.NEAREST), (800, 528))
save(preview, 'sprites-inspection')
print('Prepared original players, enemies, explosions, pickups, turrets and title.')
