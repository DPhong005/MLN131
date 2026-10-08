from pathlib import Path
import json, re, urllib.request, urllib.parse, time
from PIL import Image, ImageOps
from io import BytesIO

ROOT = Path(__file__).resolve().parent.parent
ITEMS = [
 (1, 'Marx engels.JPG', 'Tượng Mác và Ăngghen tại Berlin', 'Jenli', 'Public domain', 'https://creativecommons.org/publicdomain/mark/1.0/'),
 (2, 'Mercedes-Benz-Vietnam factory workers management.jpg', 'Công nhân và quản lý tại nhà máy Mercedes-Benz Việt Nam', 'namisito', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
 (3, '11-01-2025 Line 1 Ho Chi Minh City metro for Ben Thanh Station 10.jpg', 'Đô thị TP.HCM nhìn từ tuyến metro số 1', 'Xuanphuocle', 'CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
 (4, 'National Assembly Building of Vietnam 2.jpg', 'Nhà Quốc hội Việt Nam tại Hà Nội', 'Christophe95', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
 (5, 'Agriculture in Vietnam with farmers.jpg', 'Nông nghiệp và người nông dân Việt Nam', 'Dennis G. Jarvis', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/'),
 (6, 'Hmong women with traditional costume.jpg', 'Phụ nữ H’Mông mặc trang phục truyền thống tại Bắc Hà', 'DTH-BD-NVT', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
 (7, "Black H'mong family – Grandmother, mother, grandson- Sapa Vietnam.JPG", 'Gia đình H’Mông ba thế hệ tại Sa Pa', 'Hanay', 'CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
]
def get(url):
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'CNXHLearningWebsite/2.0 (educational photo import)'})
   with urllib.request.urlopen(req,timeout=60) as response:return response.read()
  except Exception:
   if attempt==3:raise
   time.sleep(3*(attempt+1))
records=[]
folder=ROOT/'assets/illustrations/generated'
for id,title,alt,author,license,license_url in ITEMS:
 page='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(title.replace(' ','_'))
 destination=folder/f'chapter-{id}-photo.webp'
 html=get(page).decode('utf-8')
 match=re.search(r'class="fullImageLink"[^>]*>\s*<a href="([^"]+)"',html)
 if not match:raise RuntimeError(f'Original image link missing: {title}')
 original=match[1].replace('&amp;','&')
 if not destination.exists():
  image=ImageOps.exif_transpose(Image.open(BytesIO(get(original)))).convert('RGB')
  image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
  image.save(destination,quality=88,method=6)
 records.append(dict(chapterId=id,title=alt,author=author,license=license,licenseUrl=license_url,sourceUrl=page,originalUrl=original,image='/assets/illustrations/generated/'+destination.name,changes='Thu nhỏ và chuyển sang WebP; khung thẻ cắt ảnh bằng CSS.'))
 print(f'Imported chapter {id}',flush=True)
(ROOT/'data/photoCredits.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
