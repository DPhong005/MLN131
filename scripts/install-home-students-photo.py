from pathlib import Path
from PIL import Image
import json, sys

root = Path(__file__).resolve().parent.parent
source = Path(sys.argv[1])
image = Image.open(source).convert('RGBA')
if image.getchannel('A').getextrema()[0] == 255:
    raise ValueError('Ảnh chưa có nền trong suốt')
image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
name = 'hero-students-getty-cutout.webp'
image.save(root / 'assets/illustrations/generated' / name, quality=92, method=6)
credits_path = root / 'data/photoCredits.json'
credits = json.loads(credits_path.read_text(encoding='utf-8'))
credits = [item for item in credits if item.get('id') != 'home-students']
credits.append(dict(id='home-students', title='Nhóm sinh viên châu Á trước trường đại học',
    author='Getty Images',
    sourceUrl='https://unsplash.com/photos/cheerful-young-asian-university-students-standing-in-front-of-entrance-of-building-1h794xBEIl8',
    license='Unsplash+ — bản xem trước do người dùng cung cấp, còn watermark',
    licenseUrl='https://unsplash.com/plus/license',
    image='/assets/illustrations/generated/' + name, width=image.width, height=image.height,
    changes='Tách nền bằng công cụ chỉnh ảnh; giữ watermark trên phần ảnh được giữ lại.'))
credits_path.write_text(json.dumps(credits, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
app_path = root / 'js/app.js'
app = app_path.read_text(encoding='utf-8')
app = app.replace('/assets/illustrations/generated/hero-cutout-v2.webp', '/assets/illustrations/generated/' + name)
app = app.replace('width="1536" height="1024" fetchpriority="high" alt="Con người, lao động và cộng đồng kết nối qua tri thức"',
    f'width="{image.width}" height="{image.height}" fetchpriority="high" alt="Nhóm sinh viên châu Á giao lưu trước trường đại học"')
app_path.write_text(app, encoding='utf-8')
print(name, image.size)
