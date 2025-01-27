import runpy
import requests
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 0. 카카오 엑세스 토큰 발급, 재발급
def set_token(script_path):
    # 스크립트의 경로 객체 생성
    script_path = Path(script_path)

    try:
        # 서브 프로세스로 스크립트 실행
        result = subprocess.run(
            ['python', str(script_path)],
            capture_output=True,   # 표준 출력과 표준 에러를 캡처
            text=True              # 출력을 문자열로 처리
        )

        # 반환 코드 확인
        if result.returncode == 0:
            print("스크립트가 성공적으로 실행되었습니다.")
        else:
            print(f"스크립트 실행 중 오류 발생. 반환 코드: {result.returncode}")

    except Exception as e:
        print(f"에러: 서브 프로세스 실행 중 예외 발생 - {e}")


# 1. 크롤러 실행후 전역변수 추출(새로운 공지사항)
def convert_notice_to_text(notice):
    return f"[{notice['source']}] {notice['title']}"

# 2. 내게 쓰기
def send_myself(message_text, link):
    with open(r"for_kakao\kakao_code.json", "r") as fp:
        tokens = json.load(fp)

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":message_text,
            "link":{
                "web_url": link,
                "mobile_web_url": link
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    # response.status_code
    # print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


def main():
    # 0. 토큰 세팅
    set_token(r"for_kakao/get_my_token.py")

    # 1. 크롤러 실행후 새로 갱신된 공지사항 추출 (새로운 공지사항이 있으면 crawl.txt에 기록)
    mod_vars = runpy.run_path("basic_webcrawler.py")

    # 2. all_new_notices 추출
    all_new_notices = mod_vars.get("all_new_notices", [])
    if not all_new_notices:
        print("새로운 공지사항이 없습니다.")
        return

    # 3. 각 공지사항을 개별적으로 전송
    for notice in all_new_notices:
        message_text = convert_notice_to_text(notice)
        link = notice['link']
        send_myself(message_text, link)

    current_time = datetime.now().strftime("[%m/%d %H:%M] ")
    send_myself(current_time + "최신 크롤링 결과를 모두 보고했습니다", "")
    print("모든 새로운 공지사항을 카카오톡으로 전송했습니다.")
    

if __name__ == "__main__":
    main()
