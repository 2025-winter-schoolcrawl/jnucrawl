# basic_webcrawl.py

## 개요
`basic_webcrawl.py`는 여러 대학 및 학부 웹사이트에서 공지사항을 크롤링하고, 중복을 제거하여 새로운 공지사항만을 출력 및 저장하는 Python 스크립트입니다. 이 스크립트는 BeautifulSoup를 사용하여 웹 페이지를 파싱하며, 공지사항 데이터를 효율적으로 관리할 수 있습니다.

## 주요 기능
1. **공지사항 크롤링**:
   - 여러 URL에서 공지사항 데이터를 가져옵니다.
   - 공지사항의 날짜, 출처, 제목, 링크를 추출합니다.

2. **중복 검사**:
   - 기존 공지사항을 `crawl.txt` 파일에서 불러옵니다.
   - 이미 저장된 공지사항과 비교하여 중복을 제거합니다.

3. **결과 저장**:
   - 새로운 공지사항만 `crawl.txt` 파일에 저장합니다.
   - 저장 형식: `날짜 | 출처 | 제목`

4. **출력**:
   - 새로운 공지사항만 콘솔에 출력합니다.
   - 출력 형식: `[출처] 제목` 및 링크

## 추가된 사이트
- **전남대학교 공지사항**:
  - 전남대학교의 주요 공지사항 크롤링을 지원하며, 여러 페이지에 걸친 데이터를 수집합니다.

## 파일 설명
- **`crawl.txt`**:
  - 기존 공지사항 데이터가 저장되는 파일입니다.
  - 각 공지사항은 `날짜 | 출처 | 제목` 형식으로 저장됩니다.

## 사용 방법
1. **필요한 라이브러리 설치**:
   ```bash
   pip install requests beautifulsoup4
   ```

2. **스크립트 실행**:
   ```bash
   python basic_webcrawl.py
   ```

3. **결과 확인**:
   - 새로운 공지사항은 터미널에 출력됩니다.
   - 중복되지 않은 공지사항만 `crawl.txt`에 저장됩니다.

## 전송 매체 선택
- 디스코드를 이용한다면 `discordbot.py` 를 실행하세요.
- 카카오톡을 이용한다면 `for_kakao/config.py` 정보를 설정한뒤 `kakaotalkbot_myself.py` 를 실행하세요. 토큰 정보 설정은 별도의 [가이드라인](https://pastoral-mind-1b3.notion.site/189f09124a9880338650ff955c098a6c){:target="_blank"}을 참조하세요.

## 주의사항
- 일부 웹사이트는 `robots.txt` 파일에 의해 크롤링이 제한될 수 있으니, 사이트 정책을 준수하세요.
- 전남대학교 공지사항은 다중 페이지를 처리하도록 구현되어 있으며, 기본적으로 최대 3페이지를 크롤링합니다. 페이지 수는 코드에서 `max_pages` 변수로 조정할 수 있습니다.

## 확장 가능성
- 추가 웹사이트를 크롤링하려면 `urls` 리스트에 URL과 출처 정보를 추가하면 됩니다.
- 더 많은 날짜 조건이나 필터링 조건을 적용하려면 `threshold_date`와 관련된 코드를 수정할 수 있습니다.
