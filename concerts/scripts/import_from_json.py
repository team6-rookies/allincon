import os
import json
import django
from datetime import datetime

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allincon.settings')
django.setup()

from concerts.models import Concert, Location, Site

# JSON 파일 경로
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'C:\Users\XNOTE\DjangoProjects\allincon\concerts_data.json')

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    title = item['title']
    date = item['date']
    location_name = item['location']
    site_name = item['site']
    
    current_year = datetime.now().year

    def ensure_full_date(d):
        d = d.strip()
        if len(d.split('.')) == 2:  # 예: '4.25'
            return f"{current_year}.{d}"
        return d

    # 날짜 처리
    if ' ~ ' in date:
        start_str, end_str = date.split(' ~ ')
        start_date = datetime.strptime(ensure_full_date(start_str), '%Y.%m.%d')
        end_date = datetime.strptime(ensure_full_date(end_str), '%Y.%m.%d')
    else:
        single_date = ensure_full_date(date)
        start_date = end_date = datetime.strptime(single_date, '%Y.%m.%d')

    # Location, Site 객체 가져오기 또는 생성
    location_obj, _ = Location.objects.get_or_create(name=location_name)
    site_obj, _ = Site.objects.get_or_create(name=site_name)

    # 이미 저장된 Concert는 생략
    if not Concert.objects.filter(title=title, start_date=start_date, location=location_obj).exists():
        Concert.objects.create(
            title=title,
            start_date=start_date,
            end_date=end_date,
            location=location_obj,
            site=site_obj
        )
        print(f"{title} 저장 완료")
    else:
        print(f"{title} 이미 존재함")
