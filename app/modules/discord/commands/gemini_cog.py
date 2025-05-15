import discord
from discord.ext import commands

# サジェスト参照用
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.gemini.gemini_client import GeminiClient

class GeminiCog(commands.Cog):
    def __init__(self, bot: commands.Bot, gemini_client: "GeminiClient", CHANNEL_ID: int):
        self.bot = bot
        self.client = gemini_client
        self.channel_id = CHANNEL_ID
        print("GeminiCog initialized")  # 初期化確認用
    
    @commands.Cog.listener()
    async def on_message(self, message):
        #  ボット自身のメッセージは無視
        if message.author.bot:
            return

        print(f"message.channel.id: {message.channel.id}, self.channel_id: {self.channel_id}")

        # チャンネル内のユーザーのメッセージに対して応答
        if message.channel.id == self.channel_id:
            user_input = message.content
            try:
                response = await self.client.talk(user_input)
                print(f"response: {response}")
                await message.channel.send(response)
            except Exception as e:
                print(f"Geminiの応答に失敗しました: {e}")
                await message.channel.send("応答に失敗しました")

async def setup(bot, gemini_client, CHANNEL_ID):
    await bot.add_cog(GeminiCog(bot, gemini_client, int(CHANNEL_ID)))