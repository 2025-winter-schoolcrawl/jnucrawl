import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 접근 활성화
intents.members = True  # 멤버 정보 접근 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("안녕하세요! 저는 디스코드 봇입니다. 😊")

bot.run(TOKEN)
