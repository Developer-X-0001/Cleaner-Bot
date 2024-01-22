import discord
import sqlite3
import config

from discord import app_commands
from discord.ext import commands
from discord.ui import View, button, Button
from Interface.Buttons.ChangelogButtons import ChangelogButtons, ChangelogButtonsWithNotif

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")

    @app_commands.command(name="changelog", description="See what's new")
    async def changelog(self, interaction: discord.Interaction):
        data = self.database.execute("SELECT status FROM NotificationView WHERE user_id = ?", (interaction.user.id,)).fetchone()
        if data is None:
            resp_embed = discord.Embed(
                title="Where do you want to receive the changelog?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(content=f"{config.NOTIFICATION_EMOJI} **You have an unread notification!**", embed=resp_embed, view=ChangelogButtonsWithNotif(), ephemeral=True)
            return
        else:
            resp_embed = discord.Embed(
                title="Where do you want to receive the changelog?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=ChangelogButtons(), ephemeral=True)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Changelog(bot))