import os
from dotenv import load_dotenv
from pathlib import Path

# 環境変数の読み込み
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# API KEY
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# Notion
NOTION_DATABASE_ID_Zettelkasten = os.getenv("NOTION_DATABASE_ID_Zettelkasten")
NOTION_DATABASE_ID_TASKS = os.getenv("NOTION_DATABASE_ID_TASKS")
NOTION_DATABASE_ID_JOURNAL = os.getenv("NOTION_DATABASE_ID_JOURNAL")
NOTION_DATABASE_ID_TEST = os.getenv("NOTION_DATABASE_ID_TEST")

# Discord
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")