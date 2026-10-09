from pathlib import Path
from PIL import Image
import json, sys

root = Path(__file__).resolve().parent.parent
paths = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
credits_path = root / 'data/photoCredits.json'
credits = json.loads(credits_path.read_text(encoding='utf-8'))
for key, source in paths.items():
    i = int(key)
    im = Image.open(source).convert('RGBA')
    if im.getchannel('A').getextrema()[0] == 255:
        raise ValueError(f'Case {i} has no transparent background')
    bbox = im.getchannel('A').getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        im = im.crop((max(0,x0-12),max(0,y0-12),min(im.width,x1+12),min(im.height,y1+12)))
    im.thumbnail((1000,1000), Image.Resampling.LANCZOS)
    name = f'case-{i}-photo-cutout.webp'
    im.save(root / 'assets/illustrations/generated' / name, quality=92, method=6)
    record = next(x for x in credits if x.get('id') == f'case-{i}')
    record.update(cutoutImage='/assets/illustrations/generated/'+name, cutoutWidth=im.width, cutoutHeight=im.height)
    record['cutoutChanges'] = 'Tách nền bằng công cụ chỉnh ảnh, giữ chủ thể của ảnh nguồn; dùng trong khối tình huống ở trang chương.'
    print(name, im.size)
credits_path.write_text(json.dumps(credits,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
