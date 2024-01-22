import config
import asyncio
import discord

from discord.ext import commands
from discord import app_commands
from Interface.Buttons.ErrorReportButton import ErrorReportView
from Interface.Buttons.CategoryPurgeButtons import CategoryPurgeButtons

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    purge_group = app_commands.Group(name="purge", description="re-create channel or a whole category of channels")

    @purge_group.command(name="channel", description="Recreates current or mentioned channel")
    @app_commands.describe(channel="The channel you want to re-create.")
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel=None):
        if channel is None:
            await interaction.response.defer()
            try:
                await interaction.followup.send(f"{config.WARN_EMOJI} {interaction.user.mention} has initiated a {config.NUKE_EMOJI} **Nuke!**")
                await asyncio.sleep(5)
                await interaction.channel.send(f"{config.BLAST_EMOJI} Nuking.....")
                position = interaction.channel.position
                await interaction.channel.delete(reason=f"{interaction.user} invoked Purge command")
                chnl = await interaction.channel.clone(reason=f"{interaction.user} invoked Purge command")
                await chnl.move(category=interaction.channel.category, beginning=True, offset=position)
                return

            except Exception as error:
                await interaction.followup.send(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge channel", error_msg=error))
                return
        else:
            await interaction.response.defer(ephemeral=True)
            try:
                await interaction.followup.send(f"{config.BLAST_EMOJI} The mentioned channel will be nuked in a while")
                await channel.send(f"{config.WARN_EMOJI} {interaction.user.mention} has initiated a {config.NUKE_EMOJI} **Nuke!**")
                await asyncio.sleep(5)
                await channel.send(f"{config.BLAST_EMOJI} Nuking.....")
                position = channel.position
                print(position)
                await channel.delete(reason=f"{interaction.user} invoked Purge command")
                chnl = await channel.clone(reason=f"{interaction.user} invoked Purge command")
                await chnl.move(category=interaction.channel.category, beginning=True, offset=position)
                await interaction.edit_original_message(content=f"{config.DONE_EMOJI} Nuke Successful")
                return

            except Exception as error:
                await interaction.followup.send(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge channel", error_msg=error))
                return
    
    @channel.error
    async def channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(content=f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing (Manage Channels) permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge channel", error_msg=error), ephemeral=True)
            return
    
    @purge_group.command(name="category", description="Recreates current")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def category(self, interaction: discord.Interaction):
        old_category = interaction.channel.category.id
        global cat
        cat = self.bot.get_channel(old_category)
        await interaction.response.send_message(f"{config.WARN_EMOJI} This command will re-create the current category.\nAre you sure about this?", ephemeral=True, view=CategoryPurgeButtons())
        return
    
    @category.error
    async def category_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(content=f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing (Manage Channels) permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge category", error_msg=error), ephemeral=True)
            return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Purge(bot))