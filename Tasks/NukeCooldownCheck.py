import sqlite3
import datetime
from discord.ext import commands, tasks

class NukeCooldownCheck(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nuke_cooldown_check.start()
        self.database = sqlite3.connect("./Databases/Data.sqlite")

    @tasks.loop(seconds=1)
    async def nuke_cooldown_check(self):
        await self.bot.wait_until_ready()
        data = self.database.execute("SELECT guild_id, nuke_cooldown FROM GuildSettings").fetchall()
        if data == []:
            return
        else:
            for entry in data:
                guild = self.bot.get_guild(entry[0])
                time = datetime.datetime.fromtimestamp(entry[1]).strftime("%Y-%m-%d")
                now_time = datetime.datetime.now().strftime("%Y-%m-%d")

                if now_time >= time:
                    self.database.execute("UPDATE GuildSettings SET nuke_cooldown = 0 WHERE guild_id = ?", (guild.id,)).connection.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        NukeCooldownCheck(bot))