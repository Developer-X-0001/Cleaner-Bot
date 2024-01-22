import config
import discord

from discord.ext import commands, tasks
from Functions.FormatNumber import format_large_number

class UpdateStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_channels.start()

    @tasks.loop(minutes=30)
    async def update_channels(self):
        latency_channel = self.bot.get_channel(config.LATENCY_CHANNEL_ID)
        server_count_channel = self.bot.get_channel(config.SERVERCOUNT_CHANNEL_ID)
        shard_count_channel = self.bot.get_channel(config.SHARDCOUNT_CHANNEL_ID)
        member_count_channel = self.bot.get_channel(config.MEMBERCOUNT_CHANNEL_ID)

        await latency_channel.edit(name=f"Cleaner Latency: {round(self.bot.latency * 1000)}ms")
        await server_count_channel.edit(name=f"Server Count: {len(self.bot.guilds)}")
        await shard_count_channel.edit(name=f"Shard Count: {self.bot.shard_count}")
        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count

        await member_count_channel.edit(name=f"Member Count: {format_large_number(total_members)}")

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateStats(bot))