import discord
from discord import app_commands
from discord.ext import commands

class OnRawReactionAdd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == "🗑️":
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.delete()
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnRawReactionAdd(bot))