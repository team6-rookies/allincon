# allincon

Allincon - 사이트 별 콘서트 크롤링 및 웹 사이트 구성

# 프로젝트 소개
인터파크, 멜론, 티켓링크 등의 콘서트 예매 사이트에서 정보를 수집하여,
공연 일정, 장소, 예매처를 한눈에 확인하고 검색할 수 있는 플랫폼입니다.

# 프로젝트 개요
프로그래머스 데이터 엔지니어링 6회차 1차 프로젝트 
본 프로젝트는 Selenium을 활용해 티켓 사이트에서 콘서트 정보를 크롤링하고, 
Django를 기반으로 콘서트 정보를 시각화 및 조회할 수 있는 웹 서비스를 구축하는 데 목적이 있습니다.

# 프로젝트 개발 기간
2025.04.18 ~ 2025.04.24

# 팀원
- 조원서
- 장현우 
- 박범수
- 최정우
- 김미연

# 주요 기능
- 키워드 검색으로 콘서트 정보 보기
- 모든 콘서트 목록 보기
- 장소별 콘서트 보기
- 특정 장소 콘서트에 대한 세부 내용 보기
- 월 별 콘서트 보기

# 사용 기술
- 데이터 수집: Selenium (동적 웹 크롤링)
- 백엔드: Django, Django REST Framework (DRF)
- 데이터 저장: Django ORM (models), SQLite (기본 설정)
- API 직렬화: DRF의 Serializer
- 프론트엔드: Django Template

# 데이터 수집
Selenium – 각 사이트 별 콘서트 정보 크롤링
-> JSON 저장 후 API POST로 Django DB에 저장

# 데이터 구조 및 모델
> Concert 모델
title
start_date / end_date
location (ForeignKey)
site (ForeignKey)

> Location 모델
name
address (optional)
max_people (optional)

> Site 모델
name

# 데이터 처리 흐름
1. Selenium을 사용해 티켓 사이트에서 콘서트 정보 수집
2. 수집한 데이터는 JSON 형식으로 가공 및 저장
3. JSON 데이터를 Django REST API에 전송하여 DB에 저장
4. DRF 기반 API를 통해 저장된 콘서트 데이터를 외부에 제공
5. Django 템플릿을 활용한 웹 페이지에서 콘서트 정보 조회 및 검색

# 페이지 구성
- 메인 페이지 (검색창, 전체보기, 장소목록)
- 콘서트 목록 페이지
- 장소 목록 및 상세 페이지
- 콘서트 상세 페이지

# 설치 및 실행 방법
```bash
git clone https://github.com/team6-rookies/allincon.git
cd allincon
python manage.py runserver
```

# 협업 
GitHub를 사용해 팀원들과 협업 

