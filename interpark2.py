import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json

# Selenium WebDriver 설정
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 사이트 접속
url = 'https://tickets.interpark.com/contents/genre/concert'
driver.get(url)

# 전체 탭 클릭 대기 후 클릭
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="전체"]'))).click()

# 페이지가 완전히 로드될 때까지 대기
time.sleep(2)

# 콘서트 정보를 저장할 리스트
concerts = []

# 원하는 콘서트 수량
target_concerts = 100

# 중복 없이 콘서트 정보를 수집하기 위한 변수
collected_titles = set()

# 스크롤 반복하며 콘서트 목록 수집
while len(concerts) < target_concerts:
    # 페이지의 콘서트 항목들이 로드되기를 기다림
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul[class^="TicketItem_contentsWrap"]'))
    )

    # 콘서트 항목들을 찾기
    elements = driver.find_elements(By.CSS_SELECTOR, 'ul[class^="TicketItem_contentsWrap"]')

    # 콘서트 정보 추출
    for el in elements:
        if len(concerts) >= target_concerts:  # 100개 이상 되면 멈추기
            break
        try:
            # 정확한 클래스명에 맞춰 추출
            title = el.find_element(By.CLASS_NAME, "TicketItem_goodsName__Ju76j").text
            date = el.find_element(By.CLASS_NAME, "TicketItem_playDate__5ePr2").text
            location = el.find_element(By.CLASS_NAME, "TicketItem_placeName__ls_9C").text
            
            # 이미 수집한 콘서트 정보는 제외
            if title not in collected_titles:
                collected_titles.add(title)

                concerts.append({
                    'title': title,
                    'date': date,
                    'location': location,
                    'site': 'Interpark'  # 'Interpark'라는 name을 바로 넣으면, Django가 자동으로 site_id = 1로 처리
                })
        except Exception as e:
            print(f"정보 추출 실패: {e}")

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 수집된 콘서트 정보 출력
print(f"총 {len(concerts)}개의 콘서트 정보를 수집했습니다.")
for concert in concerts:
    print(concert)

# 드라이버 종료
driver.quit()

# JSON 파일로 저장
json_path = 'concerts_data.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(concerts, f, ensure_ascii=False, indent=4)

print(f"콘서트 데이터를 {json_path}에 저장했습니다.")