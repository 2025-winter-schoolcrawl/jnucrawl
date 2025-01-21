import requests
import json
import os


# 카카오톡 토큰 발행 및 저장
def get_token_and_store():
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = '[당신의 api 키를 입력하세요]'
    redirect_uri = '[등록한 리디렉션 url을 입력하세요]'
    authorize_code = '[카카오로부터 발급받은 코드를 입력하세요]'

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }

    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "kakao_code.json")

    # JSON 파일로 토큰 저장
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(tokens, fp)

    # JSON 파일에서 토큰 다시 읽기
    with open(json_path, "r", encoding="utf-8") as fp:
        loaded_tokens = json.load(fp)

    print(loaded_tokens["access_token"])


def main():
    get_token_and_store()


if __name__ == "__main__":
    main()