import config
import discord

from discord.ext import commands
from discord import app_commands
from discord.app_commands.errors import MissingPermissions
from Interface.Buttons.ErrorReportButton import ErrorReportView
from Interface.Buttons.PermissionUpdateButton import PermissionUpdateButton

class Permissions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="check_permissions", description="Check if the bot has all required permissions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def perm_check(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{config.LOADING_EMOJI} Initiating Permission Check", ephemeral=True)
        me = interaction.guild.get_member(self.bot.user.id)
        manage_roles = f"{config.ERROR_EMOJI} Manage Roles"
        manage_channels = f"{config.ERROR_EMOJI} Manage Channels"
        manage_nicknames = f"{config.ERROR_EMOJI} Manage Nicknames"
        manage_emojis_and_stickers = f"{config.ERROR_EMOJI} Manage Emojis and Stickers"
        read_messages = f"{config.ERROR_EMOJI} Read Messages"
        send_messages = f"{config.ERROR_EMOJI} Send Messages"
        send_messages_in_threads = f"{config.ERROR_EMOJI} Send Messages in Threads"
        manage_messages = f"{config.ERROR_EMOJI} Manage Messages"
        manage_threads = f"{config.ERROR_EMOJI} Manage Threads"
        embed_links = f"{config.ERROR_EMOJI} Embed Links"
        read_message_history = f"{config.ERROR_EMOJI} Read Message History"
        use_external_emojis = f"{config.ERROR_EMOJI} Use External Emojis"
        use_external_stickers = f"{config.ERROR_EMOJI} Use External Stickers"
        counter = 0
        if me.guild_permissions.manage_roles:
            manage_roles = f"{config.DONE_EMOJI} Manage Roles"
            counter += 1
        if me.guild_permissions.manage_channels:
            manage_channels = f"{config.DONE_EMOJI} Manage Channels"
            counter += 1
        if me.guild_permissions.manage_nicknames:
            manage_nicknames = f"{config.DONE_EMOJI} Manage Nicknames"
            counter += 1
        if me.guild_permissions.manage_emojis_and_stickers:
            manage_emojis_and_stickers = f"{config.DONE_EMOJI} Manage Emojis and Stickers"
            counter += 1
        if me.guild_permissions.read_messages:
            read_messages = f"{config.DONE_EMOJI} Read Messages"
            counter += 1
        if me.guild_permissions.send_messages:
            send_messages = f"{config.DONE_EMOJI} Send Messages"
            counter += 1
        if me.guild_permissions.send_messages_in_threads:
            send_messages_in_threads = f"{config.DONE_EMOJI} Send Messages in Threads"
            counter += 1
        if me.guild_permissions.manage_messages:
            manage_messages = f"{config.DONE_EMOJI} Manage Messages"
            counter += 1
        if me.guild_permissions.manage_threads:
            manage_threads = f"{config.DONE_EMOJI} Manage Threads"
            counter += 1
        if me.guild_permissions.embed_links:
            embed_links = f"{config.DONE_EMOJI} Embed Links"
            counter += 1
        if me.guild_permissions.read_message_history:
            read_message_history = f"{config.DONE_EMOJI} Read Message History"
            counter += 1
        if me.guild_permissions.use_external_emojis:
            use_external_emojis = f"{config.DONE_EMOJI}  Use External Emojis"
            counter += 1
        if me.guild_permissions.use_external_stickers:
            use_external_stickers = f"{config.DONE_EMOJI} Use External Stickers"
            counter += 1
        
        if counter == 13:
            embed = discord.Embed(
                title="Permission Check Report",
                description=f"{manage_roles}\n{manage_channels}\n{manage_nicknames}\n{manage_emojis_and_stickers}\n{read_messages}\n{send_messages}\n{send_messages_in_threads}\n{manage_messages}\n{manage_threads}\n{embed_links}\n{read_message_history}\n{use_external_emojis}\n{use_external_stickers}\n\n{config.DONE_EMOJI} All permissions are granted!",
                color=discord.Color.magenta()
            )
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
                
            await interaction.edit_original_response(content=None, embed=embed)
            return
        
        if counter != 13:
            embed = discord.Embed(
                title="Permission Check Report",
                description=f"{manage_roles}\n{manage_channels}\n{manage_nicknames}\n{manage_emojis_and_stickers}\n{read_messages}\n{send_messages}\n{send_messages_in_threads}\n{manage_messages}\n{manage_threads}\n{embed_links}\n{read_message_history}\n{use_external_emojis}\n{use_external_stickers}\n\n{config.WARN_EMOJI} Missing permissions found!",
                color=discord.Color.magenta()
            )
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
                
            embed.set_footer(text="Click the button below, to re-invite the bot without kicking")
            await interaction.edit_original_response(content=None, embed=embed, view=PermissionUpdateButton())
            return
    
    @perm_check.error
    async def perm_chec_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing (Administrator) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/check_permissions", error_msg=error), ephemeral=True)
            return
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Permissions(bot))