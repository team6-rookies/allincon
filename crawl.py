import requests
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

TARGET_URL = "https://www.ticketlink.co.kr/performance/14"
API_ENDPOINT = "http://127.0.0.1:8000/api/concerts/upload/"
CURRENT_SOURCE_NAME = "티켓링크"

def parse_date_str(date_str):
    if not date_str:
        return None
    try:
        dt_obj = datetime.strptime(date_str, '%Y.%m.%d')
        return dt_obj.strftime('%Y-%m-%d')
    except ValueError:
        print(f"날짜 파싱 오류 (문자열 변환): '{date_str}'")
        return None

def run_scraper():
    print('콘서트 정보 스크래핑을 시작합니다...')
    options_webdriver = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Whale/4.31.304.16 Safari/537.36'
    options_webdriver.add_argument(f'user-agent={user_agent}')
    options_webdriver.add_argument('--headless')
    options_webdriver.add_argument("--disable-gpu")
    options_webdriver.add_argument("--window-size=1920,1080")
    all_scraped_data = []
    processed_keys = set()

    try:
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options_webdriver) as driver:
            driver.get(TARGET_URL)
            wait = WebDriverWait(driver, 15)
            last_height = driver.execute_script("return document.body.scrollHeight")
            print('스크롤을 내리는 중...')

            while True:
                target_item_selector = "section.common_section.section_list_region div.product_grid_item"
                current_items = []

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.common_section.section_list_region")))
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, target_item_selector)))
                    current_items = driver.find_elements(By.CSS_SELECTOR, target_item_selector)
                    print(f"{len(current_items)}개의 자료를 찾았습니다.")
                except TimeoutException:
                    print("요소 로딩 시간 초과.")
                except Exception as e:
                    print(f"요소 검색 중 오류: {e}")

                for item_div in current_items:
                    try:
                        title_span = item_div.find_element(By.CSS_SELECTOR, ".product_title")
                        title = title_span.text.strip()

                        place = None
                        try:
                            place_span = item_div.find_element(By.CSS_SELECTOR, ".product_place")
                            place = place_span.text.strip()
                            if not place: place = None
                        except NoSuchElementException: pass

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
                        except NoSuchElementException: pass

                        if not title or not place:
                            continue

                        processing_key = (title, place, start_date_str)
                        if processing_key in processed_keys:
                            continue
                        processed_keys.add(processing_key)

                        formatted_start_date = parse_date_str(start_date_str)
                        formatted_end_date = parse_date_str(end_date_str)

                        payload = {
                            'title': title,
                            'location': place,
                            'source': CURRENT_SOURCE_NAME,
                            'start_date': formatted_start_date,
                            'end_date': formatted_end_date,
                        }

                        payload = {k: v for k, v in payload.items() if v is not None}
                        all_scraped_data.append(payload)
                    except Exception as item_err:
                        print(f"아이템 처리 중 오류 발생: {item_err}")
                        continue

                print('아래로 스크롤합니다...')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                try:
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        time.sleep(5)
                        final_height = driver.execute_script("return document.body.scrollHeight")
                        if final_height == last_height:
                            print('페이지 끝에 도달했습니다.')
                            break
                        else: last_height = final_height
                    else: last_height = new_height
                except Exception as scroll_err:
                    print(f"스크롤 높이 확인 중 오류: {scroll_err}")
                    break

        print("-" * 30)
        print(f"총 {len(all_scraped_data)} 개의 고유 콘서트 데이터 스크랩 완료.")
        if all_scraped_data:
            print("API 서버로 데이터 전송 시작...")
            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(API_ENDPOINT, json=all_scraped_data, headers=headers, timeout=30)
                if response.status_code == 201:
                    print(f"  성공: 데이터가 성공적으로 생성되었습니다. 응답: {response.json()}")
                elif response.status_code == 400:
                    print(f"  실패 또는 부분 성공: API 서버에서 오류 발생. 상태코드: {response.status_code}")
                    try:
                        print(f"  오류 내용: {response.json()}")
                    except requests.exceptions.JSONDecodeError:
                        print(f"  오류 내용 (텍스트): {response.text[:500]}...")
                else:
                    print(f"  실패: 예상치 못한 응답. 상태코드: {response.status_code}, 내용: {response.text[:-1]}...")
            except requests.exceptions.RequestException as req_err:
                print(f"  오류: API 서버로 데이터 전송 중 오류 발생: {req_err}")
            print("데이터 전송 완료.")
        else:
            print("전송할 데이터가 없습니다.")
        print("-" * 30)

    except Exception as e:
        print(f"스크래핑 중 심각한 오류 발생: {e}")
    finally:
        print("-" * 30)
        print(f"스크래핑 완료.")
        print("-" * 30)

if __name__ == "__main__":
    run_scraper()