import requests
import config
import json
from pathlib import Path


url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = config.rest_api_key
redirect_uri = config.redirect_uri
authorize_code = config.authorize_code


# 토큰 신규 발급
def get_new_token():
    # 토큰 신규 발급 요청 준비
    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open(r".\kakao_code.json","w") as fp:
        json.dump(tokens, fp)


# 토큰 갱신
def refresh_classic_token(refresh_value):
    # 토큰 갱신 요청 준비
    data = {
        'grant_type': 'refresh_token',
        'client_id': rest_api_key,
        'refresh_token': refresh_value,
    }
    # 갱신 요청후 응답에서 access_token만 추출
    response = requests.post(url, data=data)
    response_data = response.json()
    new_access_token = response_data.get("access_token")

    if new_access_token:
        # access_token 업데이트
        data["access_token"] = new_access_token
        # JSON 파일 경로 객체로 변환
        json_file = Path(r"./kakao_code.json")
        # JSON 파일에 저장
        try:
            with json_file.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("access_token이 성공적으로 업데이트되었습니다.")
            return True
        except Exception as e:
            print(f"에러: JSON 파일 쓰기 실패 - {e}")
            return False


# 토큰 정보 확인
def read_token():
    # JSON 파일의 경로
    json_file_path = r".\kakao_code.json"
    # JSON 파일 열기 및 데이터 로드
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # refresh 값을 변수에 저장
    refresh_token = data['refresh_token']
    return refresh_token


def main():
    file_path = Path(r".\kakao_code.json")

    # 토큰 파일이 존재한다면 토큰 갱신
    if file_path.exists():
        refresh_token = read_token()
        refresh_classic_token(refresh_token)

    # 토큰 파일이 존재하지 않는다면 토큰 발급
    else:
        get_new_token()


if __name__ == "__main__":
    main()