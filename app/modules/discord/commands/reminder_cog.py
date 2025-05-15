import discord
from discord import app_commands
from discord.ext import commands, tasks

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.reminder.reminder_manager import ReminderManager
    from modules.gemini.gemini_client import GeminiClient

class ReminderCog(commands.Cog):
    def __init__(self, bot: commands.Bot, reminder_manager: "ReminderManager", gemini_client: "GeminiClient", GUILD_ID, CHANNEL_ID):
        self.bot = bot
        self.reminder_manager = reminder_manager
        self.gemini_client = gemini_client
        self.guild_id = GUILD_ID
        self.channel_id = CHANNEL_ID
        self.channel = None

        self.monitor_reminder.start()

        print("ReminderCog initialized")  # 初期化確認用
        
    @app_commands.command(name="set_reminder", description="リマインダーを設定")
    async def set_reminder(self, interaction: discord.Interaction, task_name: str, time_str: str):
        try:
            self.reminder_manager.add_reminder(task_name, time_str)
            response = await self.gemini_client.talk(f"[system_message: ユーザーに{task_name}を{time_str}にリマインドすることを伝えてください。]")
            await interaction.response.send_message(response)

        except Exception as e:
            print(f"コマンドが動作しませんでした: {e}")

    @tasks.loop(seconds=1)
    async def monitor_reminder(self):
        try:
            # ここループしちゃうからifでどうにかする
            task_name = await self.reminder_manager.monitor_reminder()

            if task_name is not None:
                response = await self.gemini_client.talk(f"[system_message: ユーザーに{task_name}の時間になったことを知らせてください]")
                self.channel = await self.bot.fetch_channel(self.channel_id)
                await self.channel.send(response)
                self.reminder_manager.dalete_task(task_name)

        except Exception as e:
            print(f"Failed monitor_reminder: {e}")
    
    async def cog_load(self):
        self.bot.tree.add_command(self.set_reminder, guild=discord.Object(id=self.guild_id))

async def setup(bot, reminder_manager, gemini_client, GUILD_ID, CHANNEL_ID):
    await bot.add_cog(ReminderCog(bot, reminder_manager, gemini_client, GUILD_ID, CHANNEL_ID))