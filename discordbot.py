import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import signal
import sys
        
# === CustomBot 클래스 정의 ===
class CustomBot(commands.Bot):
    async def setup_hook(self):
        """봇 초기화 시 자동 공지 작업 등록"""
        self.loop.create_task(auto_send_notices())
        
# === 환경 변수 및 봇 설정 ===
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 접근 활성화
intents.members = True          # 멤버 정보 접근 활성화
bot = CustomBot(command_prefix="!", intents=intents)

# === URL 및 역할/채널 매핑 설정 ===
role_emoji_map = {
    "📚": {
        "role": "전남대학교 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_1")), 
        "url": "https://www.jnu.ac.kr/WebApp/web/HOM/COM/Board/board.aspx?boardID=5&bbsMode=list&cate=0",
        "multi_page": True  # 전남대학교 공지는 다중 페이지 처리 필요
    },
    "🖥️": {
        "role": "공과대학 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_2")), 
        "url": "https://eng.jnu.ac.kr/eng/7343/subview.do",
        "multi_page": False
    },
    "💻": {
        "role": "소프트웨어공학과 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_3")), 
        "url": "https://sw.jnu.ac.kr/sw/8250/subview.do",
        "multi_page": False
    },
    "⚡": {
        "role": "전자컴퓨터공학부 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_4")), 
        "url": "https://eceng.jnu.ac.kr/eceng/20079/subview.do",
        "multi_page": False
    },
    "🤖": {
        "role": "AI융합대학 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_5")), 
        "url": "https://cvg.jnu.ac.kr/cvg/3608/subview.do",
        "multi_page": False
    },
    "🧠": {
        "role": "인공지능학부 공지", 
        "channel_id": int(os.getenv("CHANNEL_ID_6")), 
        "url": "https://aisw.jnu.ac.kr/aisw/518/subview.do",
        "multi_page": False
    }
}

# === 공지사항 관리 관련 변수 ===
txt_file = "crawl.txt"
today = datetime.now()
threshold_date = today - timedelta(days=2)

# === 공지사항 처리 함수 ===
def load_existing_notices(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file)

def save_new_notices(file_path, notices):
    with open(file_path, "a", encoding="utf-8") as file:
        for notice in notices:
            file.write(f"{notice['date']}|{notice['source']}|{notice['title']}\n")

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
            base_url = "/".join(url.split('/')[:3])  # Extract base URL (e.g., https://sw.jnu.ac.kr)
            link = base_url + link_tag['href']

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
            date_td = row.find_all('td', class_='under')[-2]
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

# === 디스코드 봇 이벤트 및 명령어 ===
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    """이모지 클릭 시 역할 부여"""
    if user.bot:
        return

    emoji = str(reaction.emoji)
    data = role_emoji_map.get(emoji)
    if data:
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name=data["role"])
        if role:
            await user.add_roles(role)
            # await user.send(f"{data['role']} 역할이 부여되었습니다!")
            
@bot.event
async def on_reaction_remove(reaction, user):
    """이모지 제거 시 역할 제거"""
    if user.bot:
        return

    emoji = str(reaction.emoji)
    data = role_emoji_map.get(emoji)
    if data:
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name=data["role"])
        if role:
            await user.remove_roles(role)
            # await user.send(f"{data['role']} 역할이 제거되었습니다!")

@bot.command()
async def 공지(ctx):
    """해당 채널에 연결된 사이트의 공지사항만 출력"""
    channel_id = ctx.channel.id
    data = next((data for data in role_emoji_map.values() if data["channel_id"] == channel_id), None)

    if not data:
        await ctx.send("이 채널에 연결된 공지사항이 없습니다!")
        return

    existing_notices = load_existing_notices(txt_file)
    if data.get("multi_page"):
        new_notices = fetch_notices_multi_page(data["url"], data["role"], existing_notices)
    else:
        new_notices = fetch_notices(data["url"], data["role"], existing_notices)

    if new_notices:
        save_new_notices(txt_file, new_notices)
        for notice in new_notices:
            await ctx.send(f"{notice['title']}\n[링크 보기]({notice['link']})")
    else:
        await ctx.send("새로운 공지사항이 없습니다!")
        
        
# === 채널별 자동 공지 전송 기능 ===
async def wait_until_exact_minute():
    """정각(00분)까지 대기"""
    now = datetime.now()
    # 다음 정각(00분) 시간 계산
    next_minute = (now + timedelta(minutes=5)).replace(second=0, microsecond=0)
    wait_time = (next_minute - now).total_seconds()
    print(f"현재 시간: {now}, 정각까지 대기 시간: {wait_time}초")
    await asyncio.sleep(wait_time)
    
async def auto_send_notices():
    """정각에 공지사항 전송"""
    await bot.wait_until_ready()
    print("자동 공지 대기 중...")
    await wait_until_exact_minute()  # 정각까지 대기
    print(f"자동 공지 실행 시작: {datetime.now()}")

    for emoji, data in role_emoji_map.items():
        channel = bot.get_channel(data["channel_id"])
        if not channel:
            print(f"채널 ID {data['channel_id']}를 찾을 수 없습니다.")
            continue

        existing_notices = load_existing_notices(txt_file)
        if data.get("multi_page"):
            new_notices = fetch_notices_multi_page(data["url"], data["role"], existing_notices)
        else:
            new_notices = fetch_notices(data["url"], data["role"], existing_notices)

        if new_notices:
            save_new_notices(txt_file, new_notices)
            for notice in new_notices:
                await channel.send(f"{notice['title']}\n[링크 보기]({notice['link']})")
    print(f"자동 공지 실행 완료: {datetime.now()}")
    await bot.close()  # 실행 완료 후 봇 종료



# 종료 핸들러 추가
def handle_exit(signum, frame):
    print(f"프로세스 종료 시간: {datetime.now()}")
    sys.exit(0)

# SIGTERM(종료 신호) 처리
signal.signal(signal.SIGTERM, handle_exit)

# === 봇 실행 코드 ===
if __name__ == "__main__":
    print(f"프로세스 시작 시간: {datetime.now()}")
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("프로세스가 수동으로 종료되었습니다.")
    finally:
        print(f"프로세스 종료 시간: {datetime.now()}")