import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# 웹 페이지 URLs
urls = [
    {"url": "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=5&bbsMode=list&cate=0", "source": "전남대학교 공지사항"},
    {"url": "https://eng.jnu.ac.kr/eng/7343/subview.do", "source": "공과대학"},
    {"url": "https://sw.jnu.ac.kr/sw/8250/subview.do", "source": "소프트웨어공학과"},
    {"url": "https://eceng.jnu.ac.kr/eceng/20079/subview.do", "source": "전자컴퓨터공학부"},
    {"url": "https://cvg.jnu.ac.kr/cvg/3608/subview.do", "source": "AI융합대학"},
    {"url": "https://aisw.jnu.ac.kr/aisw/518/subview.do", "source": "인공지능학부"}
]

# 파일 경로
txt_file = "crawl.txt"

# 오늘 날짜 및 기준 날짜 계산
today = datetime.now()
threshold_date = today - timedelta(days=2)

# 기존 공지사항 불러오기
def load_existing_notices(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file)

# 새로운 공지사항 저장하기
def save_new_notices(file_path, notices):
    with open(file_path, "a", encoding="utf-8") as file:
        for notice in notices:
            file.write(f"{notice['date']}|{notice['source']}|{notice['title']}\n")

# 공지사항 추출 함수
def fetch_notices(url, source, existing_notices):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    notices = []
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    new_notices = []

    for row in rows:
        date_td = row.find('td', class_='td-date')
        title_td = row.find('td', class_='td-subject')
        link_tag = title_td.find('a') if title_td else None

        if date_td and title_td and link_tag:
            date_text = date_td.text.strip()
            title_parts = [part.strip() for part in title_td.stripped_strings]
            title = " ".join(title_parts)
            link = url.split('/subview.do')[0] + link_tag['href']

            # 날짜 파싱
            try:
                notice_date = datetime.strptime(date_text, "%Y.%m.%d")
            except ValueError:
                continue

            # 날짜 비교 후 필터링
            if threshold_date <= notice_date <= today:
                notice_key = f"{date_text}|{source}|{title}"
                if notice_key not in existing_notices:
                    new_notices.append({
                        'title': title,
                        'date': date_text,
                        'link': link,
                        'source': source
                    })
                    notices.append(notice_key)

    return new_notices

# 전남대학교 공지사항 처리 함수 (다중 페이지 지원)
def fetch_notices_multi_page(base_url, source, existing_notices, max_pages=3):
    new_notices = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tbody = soup.find('tbody')
        if not tbody:
            print(f"tbody 태그를 찾을 수 없습니다. URL: {url}")
            continue

        rows = tbody.find_all('tr')

        for row in rows:
            # 날짜 및 제목 찾기
            date_td = row.find_all('td', class_='under')[-2]  # 마지막 <td class="under">가 날짜
            title_td = row.find('td', class_='title')
            link_tag = title_td.find('a') if title_td else None

            if date_td and title_td and link_tag:
                date_text = date_td.text.strip()
                title_parts = [part.strip() for part in title_td.stripped_strings]
                title = " ".join(title_parts)
                link = "https://www.jnu.ac.kr" + link_tag['href']
                
                # 날짜 파싱
                try:
                    notice_date = datetime.strptime(date_text, "%Y-%m-%d")
                except ValueError:
                    continue

                # 날짜 비교 후 필터링
                if threshold_date <= notice_date <= today:
                    notice_key = f"{date_text}|{source}|{title}"
                    if notice_key not in existing_notices:
                        new_notices.append({
                            'title': title,
                            'date': date_text,
                            'link': link,
                            'source': source
                        })

    return new_notices

# 기존 공지사항 로드
existing_notices = load_existing_notices(txt_file)

# 모든 URL에서 공지사항 수집
all_notices = []
all_new_notices = []

for entry in urls:
    if "cate" in entry['url']:
        new_notices = fetch_notices_multi_page(entry['url'], entry['source'], existing_notices)
    else:
        new_notices = fetch_notices(entry['url'], entry['source'], existing_notices)
    all_new_notices.extend(new_notices)

# 새로운 공지사항 저장
if all_new_notices:
    save_new_notices(txt_file, all_new_notices)

# 결과 출력
if all_new_notices:
    for notice in all_new_notices:
        print(f"[{notice['source']}] {notice['title']}")
        print(f"- {notice['link']}")
else:
    print("새로운 공지사항이 없습니다.")
