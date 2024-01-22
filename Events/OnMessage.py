import sqlite3
import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/BadwordsFilter.sqlite")
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        self.database.execute(f"CREATE TABLE IF NOT EXISTS '{message.guild.id}' (word TEXT)")
        data = self.database.execute(f"SELECT word FROM '{message.guild.id}'").fetchall()
        if data == []:
            return
        
        else:
            for word in data:
                if word[0] in message.content:
                    await message.delete()
                    return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessage(bot))