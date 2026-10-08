from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json,urllib.request,re
from PIL import Image
root=Path(__file__).resolve().parent.parent
items=[
 ('game-decode',30708395,'close-up-of-colorful-puzzle-pieces-on-a-table','Mảnh ghép giải đố'),
 ('game-mindmap',6914034,'sticky-notes-on-the-wall','Bảng ghi chú kết nối ý tưởng'),
 ('game-verify',12719256,'close-up-shot-of-a-magnifying-glass-on-top-of-papers','Kính lúp và tài liệu nghiên cứu'),
 ('game-hotseat',35335992,'professional-conference-with-audience-listening-to-speaker','Khán giả lắng nghe tại hội trường'),
 ('case-1',32526073,'students-studying-in-a-library-setting','Sinh viên học trong thư viện'),
 ('case-2',8973132,'machinery-in-factory','Người lao động vận hành máy móc'),
 ('case-3',13919144,'city-buildings-under-construction','Công trình đô thị đang xây dựng'),
 ('case-4',8068161,'people-having-a-discussion-at-the-office','Trao đổi ý kiến trong cuộc họp'),
 ('case-5',4975362,'elderly-farmer-collecting-vegetables-on-farm','Người nông dân thu hoạch rau'),
 ('case-6',7972975,'group-of-students-studying-together-outdoors','Nhóm sinh viên trao đổi ngoài trời'),
 ('case-7',4868311,'woman-cleaning-room-with-children','Chia sẻ công việc chăm sóc nhà cửa'),
 ('article-1',16420457,'a-group-of-students-sitting-in-a-library-and-studying','Thảo luận tài liệu học tập'),
 ('article-2',31212936,'worker-in-a-textile-factory-operating-machinery','Công nhân và dây chuyền dệt'),
 ('article-3',5504725,'construction-in-city','Quá trình xây dựng đô thị'),
 ('article-4',8297652,'business-people-discussing-about-documents','Thảo luận và xem xét tài liệu'),
 ('article-5',8730179,'people-discussing-on-documents','Phối hợp công việc qua trao đổi'),
 ('article-6',5676744,'group-of-people-studying-together','Học tập cùng một nhóm đa dạng'),
 ('article-7',8507664,'a-family-preparing-food-in-the-kitchen','Gia đình nhiều thế hệ cùng chuẩn bị bữa ăn'),
]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:return r.read()
def save(item):
 id,num,slug,title=item
 url=f'https://images.pexels.com/photos/{num}/pexels-photo-{num}.jpeg?auto=compress&cs=tinysrgb&w=1200'
 im=Image.open(BytesIO(get(url))).convert('RGB');im.thumbnail((1200,1200));name=id+'-photo.webp';im.save(root/'assets/illustrations/generated'/name,quality=88)
 print(id,flush=True)
 return dict(id=id,title=title,author='Pexels — thông tin tác giả tại trang ảnh gốc',sourceUrl=f'https://www.pexels.com/photo/{slug}-{num}/',license='Pexels License',licenseUrl='https://www.pexels.com/license/',image='/assets/illustrations/generated/'+name,width=im.width,height=im.height,changes='Thu nhỏ và chuyển sang WebP; ảnh minh họa chủ đề, không phải ảnh ghi lại tình huống giả định.')
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(save,items))
p=root/'data/photoCredits.json';old=json.loads(p.read_text(encoding='utf-8'));ids={x['id'] for x in records};old=[x for x in old if x.get('id') not in ids];p.write_text(json.dumps(old+records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
