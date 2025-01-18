import os
import requests
from bs4 import BeautifulSoup
import datetime


def crawl_jnu_titles():
    url = "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=5&bbsMode=list&cate=0&page=1"
    f_name = "./전남대 공지사항.txt"
    now = datetime.datetime.now()
    # formatted_date = "[" + now.strftime("%Y-%m-%d") + "]"
    formatted_time = "[" + now.strftime("%H:%M") + "]"

    # 1) 이전에 저장된 제목들을 읽어 set으로 관리하기
    #    파일이 없으면 처음 실행으로 간주 (old_titles = set())
    old_titles = set()
    if os.path.exists(f_name):
        with open(f_name, 'r', encoding='utf-8') as f:
            # 파일에 들어 있는 각 줄을 그대로 old_titles에 추가
            # (줄 포맷이 "[번호]타이틀"이므로, 그대로 비교)
            for line in f:
                line = line.strip()
                if line:  # 빈 줄이 아니라면
                    old_titles.add(line)

    # 2) 웹 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request Error! Status Code: {response.status_code}")
        return

    # 3) BeautifulSoup 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    title_elements = soup.select("td.title a")

    # 4) 새로 얻은 타이틀들을 list로 만들고, set으로도 변환
    new_titles_list = []
    for idx, element in enumerate(title_elements, 1):
        title_text = element.get_text(strip=True)
        # 파일에 기록할 형식: [번호]제목
        # 번호가 계속 바뀔 수 있으니, 더 신뢰도 있게 비교하려면 title_text만 쓰거나 URL도 같이 쓰는 방법도 있음
        line = f"[{idx}]{title_text}"
        new_titles_list.append(line)

    # 5) 새로 추가된 항목만 추출: set(new_titles_list) - old_titles
    #    단, new_titles_list는 리스트지만, 겹치는 항목 구분을 위해 set 변환
    new_titles_set = set(new_titles_list)
    diff = new_titles_set - old_titles  # old_titles에 없는 항목만

    # diff가 비어있지 않다면(새로운 공지사항이 있다면), 파일에 append
    if diff:
        with open(f_name, 'a', encoding='utf-8') as f:
            for line in new_titles_list:
                if line in diff:
                    f.write("=======process on=======" + "\n" +  formatted_time + line + "\n")
                    print("<new>" + formatted_time + line)  # 새로 추가된 라인만 print
    else:
        # 새로 추가된 내용이 없으면 안내 메시지
        print(formatted_time + "신규 공지사항이 없습니다.")


if __name__ == "__main__":
    crawl_jnu_titles()