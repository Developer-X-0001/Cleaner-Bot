import discord

from discord.ext import commands
from discord import app_commands
from Interface.Modals.BugReportModal import BugReport

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Experiencing Issues? Report it to us!")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugReport())
        return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Report(bot))