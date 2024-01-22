import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

class OnGuildRemove(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.database.execute("DELETE FROM GuildSettings WHERE guild_id = ?", (guild.id,)).connection.commit()
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnGuildRemove(bot))