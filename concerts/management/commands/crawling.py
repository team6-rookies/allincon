from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from concerts.models import Location, Concert, Site

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y.%m.%d').date()
    except ValueError:
        print(f"날짜 파싱 오류: '{date_str}'")
        return None

class Command(BaseCommand):
    help = '티켓링크에서 콘서트 정보를 스크래핑하여 데이터베이스에 저장합니다.'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('콘서트 정보 스크래핑 및 저장을 시작합니다...'))
        url = "https://www.ticketlink.co.kr/performance/14"
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Whale/4.31.304.16 Safari/537.36'
        options_webdriver = webdriver.ChromeOptions()
        options_webdriver.add_argument(f'user-agent={user_agent}')
        options_webdriver.add_argument('--headless')
        options_webdriver.add_argument("--disable-gpu")
        scraped_count = 0
        created_count = 0
        updated_count = 0
        current_site_name = "티켓링크"
        try:
            source_site_obj, ss_created = Site.objects.get_or_create(name=current_site_name)
            if ss_created:
                self.stdout.write(self.style.SUCCESS(f"출처 사이트 '{current_site_name}' 레코드를 생성했습니다."))
            else:
                self.stdout.write(f"출처 사이트 '{current_site_name}' 레코드를 사용합니다.")
        except Exception as e:
            raise CommandError(f"출처 사이트 '{current_site_name}' 처리 중 오류 : {e}")

        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options_webdriver) as driver:
            driver.get(url)
            wait = WebDriverWait(driver, 15)
            last_height = driver.execute_script("return document.body.scrollHeight")
            print("스크롤을 내리는 중...")
            processed_keys = set() # (title, location_name, start_date_str) 튜플 저장

            while True:
                target_item_selector = "section.common_section.section_list_region div.product_grid_item"
                current_items = []
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.common_section.section_list_region")))
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, target_item_selector)))
                current_items = driver.find_elements(By.CSS_SELECTOR, target_item_selector)
                print(f"Found {len(current_items)} items in target section.")
                new_items_in_cycle = 0

                for item_div in current_items:
                    #공연이름
                    title_span = item_div.find_element(By.CSS_SELECTOR, ".product_title")
                    title = title_span.text.strip()
                    
                    #공연장
                    place = "정보 없음"
                    place_span = item_div.find_element(By.CSS_SELECTOR, ".product_place")
                    place = place_span.text.strip()
                    period_text = ""

                    #시작, 끝 날짜
                    start_date_str, end_date_str = None, None
                    try:
                        period_span = item_div.find_element(By.CSS_SELECTOR, ".product_period")
                        period_text = period_span.text.strip()
                        if "~" in period_text:
                            dates = period_text.split("~")
                            start_date_str = dates[0].strip()
                            end_date_str = dates[1].strip()
                        elif period_text:
                            start_date_str = end_date_str = period_text
                    except NoSuchElementException: # 정보 없을시 PASS
                            pass
                    
                    #정보 누락시 건너뛰기
                    if not title or not place or place == "정보 없음":
                        continue
                    processing_key = (title, place, start_date_str)
                    if processing_key in processed_keys:
                        continue # 이미 이 사이클에서 처리한 항목
                    processed_keys.add(processing_key)
                    new_items_in_cycle += 1
                    
                    location_obj, created = Location.objects.get_or_create(name=place)
                    if created:
                        print(f"  -> 새 공연장을 추가합니다. {place}")
                    parsed_start_date = parse_date(start_date_str)
                    parsed_end_date = parse_date(end_date_str)
                    concert_obj, created = Concert.objects.update_or_create(
                        title=title,
                        location=location_obj,
                        start_date=parsed_start_date,
                        defaults={ #업데이트할 필드들
                            'end_date': parsed_end_date,
                            'source' : source_site_obj,
                            }
                        )
                    scraped_count += 1
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                
                #스크롤 내리기
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                scroll_wait_time = 3
                time.sleep(scroll_wait_time)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    time.sleep(5)
                    final_height = driver.execute_script("return document.body.scrollHeight")
                    if final_height == last_height:
                        print("스크롤을 끝까지 내렸습니다.")
                        break
                    else:
                        last_height = final_height
                else:
                    last_height = new_height
        print(f"전체 스크랩 수는 {scraped_count}입니다.")
        print(f"새로 추가된 콘서트 수는 {created_count}입니다.")
        print(f"이미 있던 콘서트 수는 {updated_count}입니다.")
        print("완료")


