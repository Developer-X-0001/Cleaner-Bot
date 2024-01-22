import config
import discord

from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Show's bot latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        latency = round(self.bot.latency * 1000)

        if latency < 150:
            if latency < 75:
                await interaction.followup.send(f"{config.LATENCY_EMOJI} **Bot Latency:** {config.SIGNAL_5_EMOJI} `{latency}`ms", ephemeral=True)
                return
            else:
                await interaction.followup.send(f"{config.LATENCY_EMOJI} **Bot Latency:** {config.SIGNAL_4_EMOJI} `{latency}`ms", ephemeral=True)
                return

        if latency > 150:
            if latency > 300:
                await interaction.followup.send(f"{config.LATENCY_EMOJI} **Bot Latency:** {config.SIGNAL_1_EMOJI} `{latency}`ms", ephemeral=True)
                return
            if latency > 225:
                await interaction.followup.send(f"{config.LATENCY_EMOJI} **Bot Latency:** {config.SIGNAL_2_EMOJI} `{latency}`ms", ephemeral=True)
                return
            else:
                await interaction.followup.send(f"{config.LATENCY_EMOJI} **Bot Latency:** {config.SIGNAL_3_EMOJI}`{latency}`ms", ephemeral=True)
                return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Ping(bot))