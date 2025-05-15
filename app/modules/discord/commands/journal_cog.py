import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from modules.gemini.gemini_client import GeminiClient

class JournalCog(commands.Cog):
    def __init__(self, bot: commands.Bot, gemini_client: "GeminiClient", GUILD_ID, CHANNEL_ID):
        self.bot = bot
        self.gemini_client = gemini_client
        self.guild_id = GUILD_ID
        self.channel_id = CHANNEL_ID
        self.start_time = None
        self.status = False  # 日記作成起動中はTrue

    @app_commands.command(name="create_journal", description="Geminiとの対話で日記を作成")
    async def create_journal(self, interaction: discord.Interaction):
        try:
            message = await interaction.response.send_message("Coming soon...")

        except Exception as e:
            print(f"Failed create journal: {e}")
            

    async def cog_load(self):
        self.bot.tree.add_command(self.create_journal, guild=discord.Object(id=self.guild_id))

async def setup(bot, gemini_client, GUILD_ID, CHANNEL_ID):
    await bot.add_cog(JournalCog(bot, gemini_client, GUILD_ID, CHANNEL_ID))