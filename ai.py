import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# 웹 페이지 URLs
urls = [
    {"url": "https://cvg.jnu.ac.kr/cvg/3608/subview.do", "source": "AI융합대학"},
    {"url": "https://aisw.jnu.ac.kr/aisw/518/subview.do", "source": "인공지능학부"}
]

# 파일 경로
txt_file = "crawl.txt"

# 오늘 날짜 및 기준 날짜 계산
today = datetime.now()
threshold_date = today - timedelta(days=40)

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
            file.write(f"{notice['date']}|{notice['title']}|{notice['link']}\n")

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
                notice_key = f"{date_text}|{title}|{link}"
                if notice_key not in existing_notices:
                    new_notices.append({
                        'title': title,
                        'date': date_text,
                        'link': link,
                        'source': source
                    })
                    notices.append(notice_key)

    return new_notices

# 기존 공지사항 로드
existing_notices = load_existing_notices(txt_file)

# 모든 URL에서 공지사항 수집
all_notices = []
all_new_notices = []
for entry in urls:
    new_notices = fetch_notices(entry['url'], entry['source'], existing_notices)
    all_new_notices.extend(new_notices)

# 새로운 공지사항 저장
if all_new_notices:
    save_new_notices(txt_file, all_new_notices)

# 결과 출력
if all_new_notices:
    print("새로운 공지사항:")
    for notice in all_new_notices:
        print(f"[{notice['source']}] {notice['title']}")
        print(f"- {notice['link']}")
else:
    print("새로운 공지사항이 없습니다.")
