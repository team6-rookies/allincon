import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allincon.settings")
django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytz
from datetime import datetime
from concerts.models import Concert, Location, Site

# 자동 스크롤 기능
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 날짜 포맷 변환 함수 (timezone-aware)
def format_date(date_string):
    try:
        seoul_tz = pytz.timezone("Asia/Seoul")
        dt = datetime.strptime(date_string, "%Y.%m.%d")
        return seoul_tz.localize(dt)
    except Exception as e:
        print(f"날짜 포맷 에러: {e}")
        return None
    
# 출처 사이트 저장
site_instance, created = Site.objects.get_or_create(name="멜론티켓")

# 크롤링 URL
url = "https://ticket.melon.com/concert/index.htm?genreType=GENRE_CON"

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get(url)
    driver.implicitly_wait(5)
    scroll_to_bottom(driver)

    concerts = driver.find_elements(By.CSS_SELECTOR, "#perf_poster > li")
    print(f'총 {len(concerts)}개의 공연을 찾았습니다.\n')

    for concert in concerts:
        try:
            title_elem = concert.find_elements(By.CLASS_NAME, "tit")
            location_elem = concert.find_elements(By.CLASS_NAME, "location")
            date_elem = concert.find_elements(By.CLASS_NAME, "day")

            # 요소가 없는 경우 패스
            # if not (title_elem and location_elem and date_elem):
            #     continue

            title = title_elem[0].text.strip()
            location = location_elem[0].text.strip()
            raw_date = date_elem[0].text.strip()

            # 날짜 나누기
            if "-" in raw_date:
                start_date, end_date = [d.strip() for d in raw_date.split("-")]
            else:
                start_date = end_date = raw_date

            start_date = format_date(start_date)
            end_date = format_date(end_date)

            if not start_date or not end_date:
                continue

            # 장소 모델 연결
            location_instance, created = Location.objects.get_or_create(name=location)

            # 콘서트 저장
            concert_exists = Concert.objects.filter(
                title=title,
                location=location_instance,
                start_date=start_date,
                end_date=end_date,
                site=site_instance
            ).exists()
            
            if not concert_exists:
                Concert.objects.create(
                    title=title,
                    location=location_instance,
                    start_date=start_date,
                    end_date=end_date,
                    site=site_instance
                )
                print(f'{title} 저장 완료 \n출처: {site_instance.name}\n')
                print(f'공연명: {title}')
                print(f'공연장소: {location}')
                print(f'시작일: {start_date}')
                print(f'종료일: {end_date}')
                print(f'{"-"*50}')
            else:
                print(f'{title} 이미 존재하므로 저장 생략')
        except Exception as e:
            print(f'처리 중 오류 발생')






