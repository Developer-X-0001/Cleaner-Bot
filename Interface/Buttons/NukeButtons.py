import config
import sqlite3
import asyncio
import discord
import datetime

from discord.ui import View, button, Button
from discord import app_commands

class NukeButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="nuke_yes")
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def nuke_yes(self, interaction: discord.Interaction, button: Button):
        time = (len(interaction.guild.channels) + len(interaction.guild.roles) + len(interaction.guild.categories)) * 2
        if time > 3600:
            hours = time//3600
            minutes = time%3600//60
            seconds = time%3600%60%60
            eta = f"{hours} hours, {minutes} minutes and {seconds} seconds"

        if 3600 > time > 60:
            minutes = time%3600//60
            seconds = time%3600%60%60
            eta = f"{minutes} minutes and {seconds} seconds"
        
        if 60 > time:
            seconds = time%3600%60%60
            eta = f"{seconds} seconds"

        embed = discord.Embed(
            title="Confirm the Nuke",
            description="By pressing the confirm button, you are agreeing that:\n\n・**Channels** will be deleted\n・**Categories** will be deleted\n・**Roles** will be deleted\n\nYou can still deny this nuke....",
            color=discord.Color.magenta()
        )
        embed.set_footer(text=f"The process will take about {eta} approx.")
        embed.set_thumbnail(url=config.CLEANER_ICON)

        await interaction.response.edit_message(content=None, embed=embed, view=NukeConfirm())
        return
    
    @button(label="No", style=discord.ButtonStyle.red, custom_id="nuke_no")
    async def nuke_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", embed=None, view=None)
        return
    
class NukeConfirm(View):
    def __init__(self):
        self.database = sqlite3.connect("./Databases/Data.sqlite")
        super().__init__(timeout=None)
    
    @button(label="Confirm", style=discord.ButtonStyle.green, custom_id="nuke_confirm")
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def nuke_confirm(self, interaction: discord.Interaction, button: Button):
        now_time = datetime.datetime.now()
        cooldown = datetime.timedelta(days=15)
        future_time = now_time + cooldown
        self.database.execute(
            '''
                INSERT INTO GuildSettings VALUES (
                    ?, 5, NULL, ?, ?, ?
                ) ON CONFLICT (
                    guild_id
                ) DO UPDATE SET
                    nuke_cooldown = ?
                    WHERE guild_id = ?
            ''',
            (
                interaction.guild.id,
                round(future_time.timestamp()),
                'delete',
                'inactive',
                round(future_time.timestamp()),
                interaction.guild.id,
            )
        ).connection.commit()
        before_time = datetime.datetime.now()
        await interaction.response.edit_message(content=f"{config.WARN_EMOJI} NUKE STARTED", embed=None, view=None)
        roles = []
        for channel in interaction.guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(1)
            except:
                pass
        for category in interaction.guild.categories:
            try:
                await category.delete()
                await asyncio.sleep(1)
            except:
                pass
        for role in interaction.guild.roles:
            try:
                await role.delete()
                await asyncio.sleep(1)
            except:
                if role.name == "@everyone":
                    pass
                else:
                    roles.append(role.mention)
                    pass
        
        after_time = datetime.datetime.now()
        time_diff = after_time - before_time
        time_diff_seconds = time_diff.seconds
        if time_diff_seconds > 3600:
            hours = time_diff_seconds//3600
            minutes = time_diff_seconds%3600//60
            seconds = time_diff_seconds%3600%60%60
            time_taken = f"{hours} hours, {minutes} minutes and {seconds} seconds"

        if 3600 > time_diff_seconds > 60:
            minutes = time_diff_seconds%3600//60
            seconds = time_diff_seconds%3600%60%60
            time_taken = f"{minutes} minutes and {seconds} seconds"

        if 60 > time_diff_seconds:
            seconds = time_diff_seconds%3600%60%60
            time_taken = f"{seconds} seconds"

        role_list = ', '.join(roles)
        chnl = await interaction.guild.create_text_channel(name="✅ Nuke Successful")
        await chnl.send(embed=discord.Embed(
            title="Nuke Completed!",
            description=f"**Processing Time:** {time_taken}\n\nThe following roles can't be deleted,\n{role_list}\n\nEither they are managed by some integrations or their position is higher than me in the role hierarchy.",
            color=discord.Color.magenta()
        ))
        return
    
    @button(label="Deny", style=discord.ButtonStyle.red, custom_id="nuke_deny")
    async def nuke_deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", embed=None, view=None)
        return