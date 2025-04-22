import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

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

# 날짜 포맷 변환 함수 (string 그대로 저장, 시간대 필요 없음)
def format_date(date_string):
    try:
        dt = datetime.strptime(date_string, "%Y.%m.%d")
        return dt.strftime("%Y-%m-%d") 
    except Exception as e:
        print(f"날짜 포맷 에러: {e}")
        return None

# 크롤링 URL
url = "https://ticket.melon.com/concert/index.htm?genreType=GENRE_CON"

concert_list = []

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

            concert_list.append({
                "title": title,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "site": "멜론티켓"
            })

        except Exception as e:
            print(f'처리 중 오류 발생: {e}')

# JSON 파일로 저장
with open("melonpbs.json", "w", encoding="utf-8") as f:
    json.dump(concert_list, f, ensure_ascii=False, indent=2)

print("melonpbs.json 파일로 저장 완료!")
