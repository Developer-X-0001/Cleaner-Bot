import config
import discord
import sqlite3

from discord import app_commands
from discord.ext import commands
from Interface.Buttons.HelpButtons import HelpButtons, HelpButtonsWithNotif

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")

    @app_commands.command(name="help", description="Get a list of available commands")
    async def help(self, interaction: discord.Interaction):
        data = self.database.execute("SELECT status FROM NotificationView WHERE user_id = ?", (interaction.guild.id,)).fetchone()
        if data is None:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(content=f"{config.NOTIFICATION_EMOJI} **You have an unread notification!**", embed=resp_embed, view=HelpButtonsWithNotif(), ephemeral=True)
            return
        else:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=HelpButtons(), ephemeral=True)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Help(bot))