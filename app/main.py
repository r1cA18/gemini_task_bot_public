import asyncio
import discord
from discord.ext import commands
import config.settings as KEY
from config.logging import setup_logging

from core.dispatcher import Dispatcher

# logging設定
setup_logging()

# DiscordBOTの制御
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
dispatcher = Dispatcher()

# 起動時
@bot.event
async def on_ready():
    try:
        guild = discord.Object(KEY.GUILD_ID)
        if not guild:
            print(f"ギルドID {KEY.GUILD_ID} が見つかりません")
        
        # Debug ---
        # print("\n=== デバッグ情報 ===")
        # print(f"読み込まれているコグ: {list(bot.cogs.keys())}")  # コグの一覧
        # print(f"コマンドツリーの状態: {[cmd.name for cmd in bot.tree.get_commands()]}")  # 現在のコマンド
        
        await bot.tree.sync(guild=guild)

        # Debug ---
        # print(f"同期されたコマンド: {[cmd.name for cmd in commands]}")
        
        print(f"{bot.user} (ID: {bot.user.id}) が起動したよ！")

    except Exception as e:
        print(f"スラッシュコマンドの同期に失敗しました: {e}")

# Cogの読み込み関数
async def load_cogs():
    try:
        from modules.discord.commands import reminder_cog
        from modules.discord.commands import gemini_cog
        from modules.discord.commands import notion_task_cog
        from modules.discord.commands import journal_cog

        await reminder_cog.setup(bot, dispatcher.get_reminder_manager(), dispatcher.get_gemini(), KEY.GUILD_ID, KEY.CHANNEL_ID)
        await gemini_cog.setup(bot, dispatcher.get_gemini(), KEY.CHANNEL_ID)
        await notion_task_cog.setup(bot, dispatcher.get_notion_task_fetcher(), dispatcher.get_gemini(), KEY.CHANNEL_ID)
        await journal_cog.setup(bot, dispatcher.get_gemini(), KEY.GUILD_ID, KEY.CHANNEL_ID)
        
        # Debug
        print(f"読み込まれているコグ: {list(bot.cogs.keys())}")

    except Exception as e:
        print(f"コグの読み込みに失敗しました: {e}")

# メイン処理
async def main():
    await load_cogs()
    await bot.start(token=KEY.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())