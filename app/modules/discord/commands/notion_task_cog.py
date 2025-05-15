import discord
from discord.ext import commands, tasks

# サジェスト参照用
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.notion.notion_task_fetcher import NotionTaskFetcher
    from modules.gemini.gemini_client import GeminiClient

class NotionTaskCog(commands.Cog):
    def __init__(self, bot: commands.Bot, notion_task_fetcher: "NotionTaskFetcher", gemini_client: "GeminiClient", CHANNEL_ID: int):
        self.bot = bot
        self.notion_client = notion_task_fetcher
        self.gemini_client = gemini_client
        self.channel_id = CHANNEL_ID
        self.channel = None
        print("NotionTaskCog initialized")  # 初期化確認用

        # タスクを開始
        self.notify_deadline.start()

    # 1日ごとに監視して実行
    @tasks.loop(hours=24)
    async def notify_deadline(self):
        try:
            REMIND_DAYS = [1, 3, 7]

            for days in REMIND_DAYS:
                deadline_tasks = await self.notion_client.fetch_deadline_tasks(days)
                print(f"deadline_tasks: {deadline_tasks}")  # debug

                for task in deadline_tasks:
                    task_name = task.get("Name", "Unknown")
                    message = f"締切日まであと{days}日後の'{task_name}'という名前のタスクがあることをユーザーに伝えてあげてください"

                    response = await self.gemini_client.talk(message)
                    self.channel = await self.bot.fetch_channel(self.channel_id)
                    await self.channel.send(response)

        except Exception as e:
            print(f"error: {e}")
        
async def setup(bot, notion_task_fetcher, gemini_client, CHANNEL_ID):
    await bot.add_cog(NotionTaskCog(bot, notion_task_fetcher, gemini_client, int(CHANNEL_ID)))