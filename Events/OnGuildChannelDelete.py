import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

class OnGuildChannelDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.TextChannel):
        data = self.database.execute("SELECT audit_channel FROM GuildSettings WHERE guild_id = ?", (channel.guild.id,)).fetchone()
        if data is None:
            return
        
        else:
            if channel.id == data[0]:
                self.database.execute("UPDATE GuildSettings SET audit_channel = NULL WHERE guild_id = ?", (channel.guild.id,)).connection.commit()
                return
            
            else:
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnGuildChannelDelete(bot))