import config
import discord

from discord import app_commands
from discord.ext import commands
from Interface.Embeds.NotificationEmbed import notification_embed

class News(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="news", description="Check latest news or messages sent by the developers.")
    async def news(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=notification_embed, ephemeral=True)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        News(bot))