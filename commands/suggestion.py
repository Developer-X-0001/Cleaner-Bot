import discord

from discord.ext import commands
from discord import app_commands
from Interface.Modals.SuggestionModal import SubSuggestion

class Suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggestion", description="Got an Idea? share with us!")
    async def suggest(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SubSuggestion())
        return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Suggestion(bot))