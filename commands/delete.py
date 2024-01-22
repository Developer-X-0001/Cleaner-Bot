import config
import discord

from discord.ext import commands
from discord import app_commands
from Interface.Buttons.ErrorReportButton import ErrorReportView
from Interface.Buttons.CategoryDeleteButtons import CategoryDeleteButtons
from discord.app_commands.checks import has_permissions, bot_has_permissions

class Delete(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    delete_group = app_commands.Group(name="delete", description="Delete unnecassry channel or roles")

    @delete_group.command(name="channel", description="Delete unnecessary channels")
    @app_commands.describe(channel="The channel you want to delete.")
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await channel.delete()
        await interaction.response.send_message(content=f"{config.CLEAN_EMOJI} Deleted **#{channel}**", ephemeral=True)
        return
        
    @channel.error
    async def channel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Channels)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Channels)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete channel", error_msg=error), ephemeral=True)
            return
        
    @delete_group.command(name="thread", description="Delete unnecessary thread")
    @app_commands.describe(thread="The thread you want to delete.")
    @bot_has_permissions(manage_threads=True)
    @has_permissions(manage_threads=True)
    async def thread(self, interaction: discord.Interaction, thread: discord.Thread):
        await thread.delete()
        await interaction.response.send_message(content=f"{config.CLEAN_EMOJI} Deleted **#{thread}**", ephemeral=True)
        return
        
    @thread.error
    async def thread_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Threads)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Threads)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete thread", error_msg=error), ephemeral=True)
            return

    @delete_group.command(name="role", description="Delete unnecessary roles")
    @app_commands.describe(role="The role you want to delete.")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        if role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, your role position is lower than (**@{role.name}**) role to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
            
        elif role >= interaction.guild.me.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, my role postion lower than (**@{role.name}**) role to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return

        await role.delete()
        
        await interaction.response.send_message(content=f"{config.CLEAN_EMOJI} Deleted **{role}**", ephemeral=True)
        return
        
    @role.error
    async def role_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Roles)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Roles)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete role", error_msg=error), ephemeral=True)
            return

    @delete_group.command(name="nickname", description="Delete/Reset someone's nickname to their default username.")
    @app_commands.describe(user="The user who's nickname you want to delete.")
    @bot_has_permissions(manage_nicknames=True)
    @has_permissions(manage_nicknames=True)
    async def nickname(self, interaction: discord.Interaction, user: discord.Member):
        nick = user.display_name
        name = user.name
        if nick == name:
            await interaction.response.send_message(f"{config.WARN_EMOJI} Oops! {user.mention} doesn't have any nickname.", ephemeral=True)
            return
        if nick != name:
            await user.edit(nick=None)
            await interaction.response.send_message(f"{config.DONE_EMOJI} Success! {user.mention}'s nickname has been removed.", ephemeral=True)
            return
        
    @nickname.error
    async def nick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Nicknames)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Nicknames)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete nickname", error_msg=error), ephemeral=True)
            return
    
    @delete_group.command(name="emoji", description="Delete unwanted emojis from the server.")
    @app_commands.describe(emoji="The emoji you want to delete.")
    @bot_has_permissions(manage_emojis=True)
    @has_permissions(manage_emojis=True)
    async def emoji(self, interaction: discord.Interaction, emoji: str):
        try:
            emoji_id = discord.PartialEmoji.from_str(emoji).id
            if interaction.client.get_emoji(emoji_id).guild.id == interaction.guild.id:
                emoji = interaction.client.get_emoji(emoji_id)
                await emoji.delete()
                await interaction.response.send_message(f"{config.DONE_EMOJI} Success! The specified emoji has been deleted.", ephemeral=True)
                return
            
            if interaction.client.get_emoji(emoji_id).guild.id != interaction.guild.id:
                await interaction.response.send_message(f"{config.ERROR_EMOJI} Oops! The specified emoji doesn't belong to this server/guild.", ephemeral=True)
                return
            
        except:
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Oops! I can't locate that emoji.", ephemeral=True)
            return
    
    @emoji.error
    async def emoji_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Emojis and Stickers)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Emojis and Stickers)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete emoji", error_msg=error), ephemeral=True)
            return

    @delete_group.command(name="category", description="Delete unwanted categories including their channels.")
    @app_commands.describe(category="The category you want to delete.")
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def category(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        await interaction.response.defer(ephemeral=True)
        index = 0
        channel_names = ""
        for channel in category.channels:
            index += 1
            channel_names += f"{index}. {channel.name}\n"
        
        embed = discord.Embed(description=f"**Deleting 📁{category.name}:**\nFollowing channels will be deleted\n```{channel_names}```\n{config.WARN_EMOJI} **Confirmation Required**", color=discord.Color.orange())
        embed.set_footer(text="This action can't be reversed! Confirm at your own risk")

        await interaction.followup.send(embed=embed, view=CategoryDeleteButtons(category))
        return

    @category.error
    async def category_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, you are missing **(Manage Channels)** permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} Missing Permissions, I'm missing **(Manage Channels)** permission to process this command.", color=discord.Color.red()), ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete category", error_msg=error), ephemeral=True)
            return
    
async def setup(bot: commands.Cog) -> None:
    await bot.add_cog(
        Delete(bot))