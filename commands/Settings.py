import config
import sqlite3
import discord

from discord import app_commands
from discord.ext import commands
from Interface.Buttons.ResetButtons import ResetButtons
from Interface.Buttons.AuditButtons import AuditButtons
from Interface.Buttons.AmountButtons import AmountButtons
from Interface.Buttons.ErrorReportButton import ErrorReportView

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.database = sqlite3.connect("./Databases/Data.sqlite")
        self.badwords_db = sqlite3.connect("./Databases/BadwordsFilter.sqlite")
        self.bot = bot

    settings = app_commands.Group(name="settings", description="shows the bot settings for the current server")

    @settings.command(name="default_pins", description="Assign a default pin deletion check, either Keep or Delete")
    @app_commands.describe()
    @app_commands.choices(default=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def pins(self, interaction: discord.Interaction, default: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT default_pins FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()

        if default.value == "delete":
            if data is None:
                self.database.execute("INSERT INTO GuildSettings VALUES (?, 5, NULL, 0, ?, ?)", (interaction.guild.id, 'delete', 'inactive',)).connection.commit()
                await interaction.followup.send(content=f"{config.DONE_EMOJI} Default pins check condition is set to **Delete**, your pinned messages will be deleted.")
                return
            else:
                self.database.execute("UPDATE GuildSettings SET default_pins = ? WHERE guild_id = ?", ('delete', interaction.guild.id,)).connection.commit()
                await interaction.followup.send(content=f"{config.DONE_EMOJI} Default pins check condition has been updated to **Delete**, your pinned messages will be deleted.")
                return
        
        if default.value == "keep":
            if data is None:
                self.database.execute("INSERT INTO GuildSettings VALUES (?, 5, NULL, 0, ?, ?)", (interaction.guild.id, 'keep', 'inactive',)).connection.commit()
                await interaction.followup.send(content=f"{config.DONE_EMOJI} Default pins check condition is set to **Keep**, now your pinned messages won't be deleted.")
                return
            else:
                self.database.execute("UPDATE GuildSettings SET default_pins = ? WHERE guild_id = ?", ('keep', interaction.guild.id,)).connection.commit()
                await interaction.followup.send(content=f"{config.DONE_EMOJI} Default pins check condition has been updated to **Keep**, now your pinned messages won't be deleted.")
                return

    @pins.error
    async def pins_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/settings default_pins", error_msg=error), ephemeral=True)
            return

    @settings.command(name="audit_channel", description="Assign a channel for Message logs")
    @app_commands.describe(channel="The channel where you want get the logs.")
    @app_commands.checks.has_permissions(administrator=True)
    async def audit(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT audit_channel FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        
        if data is None:
            try:
                self.database.execute("INSERT INTO GuildSettings VALUES (?, 5, ?, 0, ?, ?)", (interaction.guild.id, channel.id, 'delete', 'inactive',)).connection.commit()
                await interaction.followup.send(f"{config.DONE_EMOJI} Successfully assigned {channel.mention} for Message Logs.")
                await channel.send(f"**{interaction.user}** has set this channel for Message Logs.")
                return
            
            except discord.errors.Forbidden:
                await interaction.followup.send(f"{config.ERROR_EMOJI} Sorry, I'm unable to send messages in {channel.mention}.")
                return
        
        if data[0] == channel.id:
            await interaction.followup.send(f"{config.ERROR_EMOJI} The mentioned channel is already assigned for audit logging")
            return

        else:
            prv_chnl = interaction.guild.get_channel(data[0])
            embed = discord.Embed(
                title="Old Audit Channel Detected!",
                description="I've noticed that, an audit channel for this server is already set. Would you like to replace it with new one?",
                color= discord.Color.magenta()
            )
            await interaction.followup.send(embed=embed, view=AuditButtons(previous_channel=prv_chnl, new_channel=channel), ephemeral=True)
            return
    
    @audit.error
    async def audit_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/settings audit_channel", error_msg=error), ephemeral=True)
            return

    @settings.command(name="default_amount", description="Change default message cleaning amount")
    @app_commands.describe(amount="The amount you want to set as default cleaning amount.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_amount(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount > 100:
            await interaction.followup.send(content=f"{config.ERROR_EMOJI} Default amount can't be greater than `100`!")
            return
        if amount == 0:
            await interaction.followup.send(content=f"{config.ERROR_EMOJI} Default amount can't be zero!")
            return
        if amount < 0:
            await interaction.followup.send(content=f"{config.ERROR_EMOJI} Default amount can't lower than zero!")
            return
        else:
            data = self.database.execute("SELECT default_amount FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
            if data is None:
                self.database.execute("INSERT INTO GuildSettings VALUES (?, ?, NULL, 0, ?, ?)", (interaction.guild.id, amount, 'delete', 'inactive',)).connection.commit()
                await interaction.followup.send(f"{config.DONE_EMOJI} Default cleaning amount is now set to `{amount}`")
                return
            
            if data[0] == amount:
                await interaction.followup.send(f"{config.ERROR_EMOJI} Default cleaning amount is already set to `{amount}`")
                return
                
            else:
                embed = discord.Embed(
                    title="Default Amount Detected!",
                    description=f"I've noticed that, a default amount for this server is already set to `{data[0]}`. Would you like to replace it with `{amount}`?",
                    color= discord.Color.magenta()
                )
                await interaction.followup.send(embed=embed, view=AmountButtons(new_amount=amount), ephemeral=True)
                return
    
    @set_amount.error
    async def set_amount_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/settings default_amount", error_msg=error), ephemeral=True)
            return

    @settings.command(name="reset", description="This command will reset every variable set in Cleaner#8788")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="⚠️ Warning",
            color=discord.Color.magenta(),
            description=f"{config.WARN_EMOJI} This command will reset all the settings for this server!\nAre you sure about this?"
        ), view=ResetButtons(), ephemeral=True)
        return
    
    @reset.error
    async def reset_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/settings reset", error_msg=error), ephemeral=True)
            return

    @settings.command(name="show", description="Shows the current bot configuration for the current server")
    @app_commands.checks.has_permissions(administrator=True)
    async def show(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT default_amount, audit_channel, default_pins FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
    
        if data[1] is None:
            audit_data = "None"

        else:
            audit_data = self.bot.get_channel(data[1]).mention
        
        if data[0] is None:
            amount_data = "5 (Not Configured)"
        else:
            amount_data = data[0]
        
        if data[2] is None:
            pins_data = "Delete"
        else:
            pins_data = str(data[2]).capitalize()

        badwords = len(self.badwords_db.execute(f"SELECT words FROM '{interaction.guild.id}'").fetchall())

        embed = discord.Embed(
            title=f"Cleaner Configuration for {interaction.guild.name}",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url=config.CLEANER_ICON)
        embed.add_field(name="Audit Channel", value=f"{audit_data}", inline=False)
        embed.add_field(name="Default Cleaning Amount", value=f"{amount_data}", inline=False)
        embed.add_field(name="Default Pins Condition", value=f"{pins_data}", inline=False)
        embed.add_field(name="Blacklisted Words", value=badwords, inline=False)

        await interaction.followup.send(embed=embed)
        return
    
    @show.error
    async def show_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/settings show", error_msg=error), ephemeral=True)
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Settings(bot))