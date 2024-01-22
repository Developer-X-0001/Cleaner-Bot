import config
import sqlite3
import discord
import datetime

from discord.ext import commands

class OnMessageEdit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        
        time = round(datetime.datetime.now().timestamp())
        
        data = self.database.execute("SELECT audit_channel FROM GuildSettings WHERE guild_id = ?", (before.guild.id,)).fetchone()
        if data is None:
            return

        else:
            channel = self.bot.get_channel(data[0])
            if channel:
                embed = discord.Embed(
                    title="Message Edited!",
                    description=f"{config.TIME_EMOJI} **Time:** <t:{time}:f>\
                        \n{config.USER_EMOJI} **Author:** {before.author.name if not before.author.global_name else before.author.global_name}\
                        \n{config.CHANNEL_EMOJI} **Channel:** {before.channel.mention}\
                        \n{config.MSG_EMOJI} **Message Contents**\nOriginal: {before.content}\nEdited: {after.content}",
                    color=discord.Color.magenta()
                ).set_footer(
                    text="Attachements aren't supported yet."
                )
                
                await channel.send(embed=embed)
                return

            else:
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessageEdit(bot))