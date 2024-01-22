import config
import sqlite3
import discord
import datetime

from discord.ext import commands
from discord import app_commands
from Interface.Buttons.NukeButtons import NukeButtons

class Nuke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")

    @app_commands.command(name="nuke", description="This is a dangerous command, your whole server will be wiped")
    async def nuke(self, interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner_id:
            await interaction.response.defer(ephemeral=True)
            data = self.database.execute("SELECT nuke_cooldown FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
            if data is None:
                embed=discord.Embed(
                    title="Server Nuke Command",
                    description="This command will completely wipe everything in your server except server members. Make sure that you are aware of what you are going to do, this action cannot be undone!\n\n**ARE YOU SURE ABOUT THIS?**",
                    color=discord.Color.magenta()
                )
                embed.set_footer(text="This command can be used once per 15 days.")
                embed.set_thumbnail(url=config.CLEANER_ICON)

                await interaction.followup.send(embed=embed, view=NukeButtons())
                return
            
            else:
                now_time = datetime.datetime.now()
                future_time = datetime.datetime.fromtimestamp(data[0])
                timeleft = future_time - now_time

                embed=discord.Embed(
                    title="Server Nuke Command On Cooldown",
                    description=f"You can't use this command at the moment, please try again after the cooldown.\n**Time Left:** {timeleft.days} days\n\n{config.CLEANER_EMOJI} **Cleaner Premium** is required!\nUpgrade to **Cleaner Premium**, to use this commands without any cooldowns.\nPrice **0.99$/mo**",
                    color=discord.Color.magenta()
                )
                embed.set_footer(text="This command can be used once per 15 days.")
                embed.set_thumbnail(url=config.CLEANER_ICON)

                await interaction.followup.send(embed=embed)
                return
        else:
            await interaction.response.send_message(content=f"{config.ERROR_EMOJI} Huh? only **Server Owner** can invoke this command!", ephemeral=True)
            return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Nuke(bot))