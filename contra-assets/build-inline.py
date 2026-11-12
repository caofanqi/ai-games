from pathlib import Path
import base64
import json
import re

ROOT = Path(__file__).resolve().parent
html_path = ROOT.parent / 'contra.html'
html = html_path.read_text()
assets = {name: 'data:image/png;base64,' + base64.b64encode((ROOT / f'{name}.png').read_bytes()).decode()
          for name in ['jungle', 'players', 'enemies', 'effects', 'pickups', 'turrets', 'title', 'cursor']}
data = {'ASSET_DATA': assets, 'LEVEL': json.loads((ROOT / 'level.json').read_text()),
        'SPRITE_INFO': json.loads((ROOT / 'sprites.json').read_text())}
for name, value in data.items():
    declaration = f'const {name} = ' + json.dumps(value, separators=(',', ':')) + ';'
    html, count = re.subn(rf'const {name}\s*=\s*\{{.*?\}};', lambda match: declaration, html, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Missing embedded declaration: {name}')
html_path.write_text(html)
print(f'Embedded {len(assets)} original images; standalone HTML: {html_path.stat().st_size:,} bytes')
