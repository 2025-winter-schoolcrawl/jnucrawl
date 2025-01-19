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