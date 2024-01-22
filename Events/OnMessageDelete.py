import config
import sqlite3
import discord
import datetime

from discord.ext import commands

class OnMessageDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        
        time = round(datetime.datetime.now().timestamp())

        data = self.database.execute("SELECT audit_channel FROM GuildSettings WHERE guild_id = ?", (message.guild.id,)).fetchone()
        if data is None:
            return
        
        else:
            channel = message.guild.get_channel(data[0])
            if channel:
                embed = discord.Embed(
                    title="Message Deleted!",
                    description=f"{config.TIME_EMOJI} **Time:** <t:{time}:f>\
                        \n{config.USER_EMOJI} **Author:** {message.author.name if not message.author.global_name else message.author.global_name}\
                        \n{config.CHANNEL_EMOJI} **Channel:** {message.channel.mention}\
                        \n{config.MSG_EMOJI} **Message Content:** {message.content}",
                    color=discord.Color.magenta()
                ).set_footer(
                    text="Attachements aren't supported yet."
                )
                
                await channel.send(embed=embed)
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessageDelete(bot))