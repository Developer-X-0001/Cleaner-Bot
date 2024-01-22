import config
import random
import sqlite3
import asyncio
import discord

from discord import app_commands
from discord.ext import commands
from Interface.Buttons.ErrorReportButton import ErrorReportView

class Clean(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/Data.sqlite")

    clean_group = app_commands.Group(name="clean", description="Message cleaning related commands")

    @clean_group.command(name="messages", description="Clean 0-50 number of messages from the current channel")
    @app_commands.describe(pins="Choose either you want to keep the pins or not.", amount="Amount of messages you want to delete, default 5", contains="Delete those messages which contain certain phrases or keywords.")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, pins: app_commands.Choice[str]=None, amount: int=None, contains: str=None):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT default_amount, default_pins FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        if amount is None:
            if data is None:
                amount = 5
            else:
                amount = data[0]

        elif amount > 50:
            await interaction.followup.send(f"{config.WARN_EMOJI} You can't delete more than 50 messages at once!")
            return

        elif amount == 0:
            await interaction.followup.send(f"{config.WARN_EMOJI} No message will be deleted if amount is 0!")
            return
        
        if pins is None:
            if data is None:
                save_pins = False
            else:
                if data[1] == "delete":
                    save_pins = False

                if data[1] == "keep":
                    save_pins = True

        elif pins.value == "keep":
            save_pins = True

        elif pins.value == "delete":
            save_pins = False

        if save_pins == False and contains == None:
            msgs_deleted = len(await interaction.channel.purge(limit=amount, bulk=True))
            await interaction.followup.send(f"{config.CLEAN_EMOJI} Deleted `{msgs_deleted}/{amount}` messages.")
            return

        messages = [message async for message in interaction.channel.history(limit=100)]
        msgs_deleted = 0
        for msg in messages:
            if msgs_deleted >= amount:
                break
            
            if msg.pinned:
                if save_pins == True:
                    await msg.delete()
                    msgs_deleted += 1
            
            if contains is not None:
                if contains in msg.content:                        
                    await msg.delete()
                    msgs_deleted += 1

            if amount >= 10:
                asyncio.sleep(random.uniform(0.5, 1.5))
            
            if amount >= 25:
                asyncio.sleep(random.uniform(1, 2))
                
        await interaction.followup.send(f"{config.CLEAN_EMOJI} Deleted `{msgs_deleted}/{amount}` messages.")
        return

    @clear.error
    async def clean_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/clean messages", error_msg=error), ephemeral=True)
            return
    
    @clean_group.command(name="mass-delete", description="Deletes someone's message all across the server, regardless of other parameters.")
    @app_commands.describe(user="The member who's messages you want to delete.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def mass_delete(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=True)
        
        def user_check(message: discord.Message):
            return message.author == user
        
        counter = 0
        for channel in interaction.guild.text_channels:
            try:
                deleted = await channel.purge(check=user_check)
            except:
                pass
            counter += len(deleted)
        
        await interaction.followup.send(f"{config.CLEAN_EMOJI} All messages sent my {user.mention} are deleted.", ephemeral=True)
        return
    
    @mass_delete.error
    async def mass_delete_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/clean mass-delete", error_msg=error), ephemeral=True)
            return
    
    @clean_group.command(name="user", description="Delete 0-100 messages sent by a specific user from the current channel")
    @app_commands.describe(user="The member who's messages you want to delete.", pins="Choose either you want to keep the pins or not.", amount="Amount of messages you want to delete, default 5", contains="Delete those messages which contain certain phrases or keywords.")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def uc(self, interaction: discord.Interaction, user: discord.Member, pins: app_commands.Choice[str]=None, amount: int=None, contains: str=None):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT default_amount, default_pins FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        
        if user.bot:
            await interaction.followup.send(f"{config.WARN_EMOJI} Please use `/clean bot` for **Bots**!")
            return
        
        if amount is None:
            if data is None:
                amount = 5
            else:
                amount = data[0]

        elif amount > 50:
            await interaction.followup.send(f"{config.WARN_EMOJI} You can't delete more than 50 messages at once!")
            return

        elif amount == 0:
            await interaction.followup.send(f"{config.WARN_EMOJI} No message will be deleted if amount is 0!")
            return
        
        if pins is None:
            if data is None:
                save_pins = False
            else:
                if data[1] == "delete":
                    save_pins = False

                if data[1] == "keep":
                    save_pins = True

        elif pins.value == "keep":
            save_pins = True

        elif pins.value == "delete":
            save_pins = False
        
        messages = [message async for message in interaction.channel.history(limit=100)]
        msgs_deleted = 0
        for msg in messages:
            if msg.author == user:
                if msg.pinned:
                    if save_pins == True:
                        await msg.delete()
                        msgs_deleted += 1
                
                elif contains is not None:
                    if contains in msg.content:
                        await msg.delete()
                        msgs_deleted += 1
                
                else:
                    await msg.delete()
                    msgs_deleted += 1
        
        await interaction.followup.send(f"{config.CLEAN_EMOJI} Deleted `{msgs_deleted}/{amount}` messages send by {user.mention}.")
        return
    
    @uc.error
    async def uc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/clean user", error_msg=error), ephemeral=True)

    @clean_group.command(name="bot", description="Delete 0-100 messages sent by bots from the current channel")
    @app_commands.describe(bot="The bot who's messages you want to delete.", amount="Amount of messages you want to delete, default 5")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def bc(self, interaction: discord.Interaction, bot: discord.Member=None, amount:int=None):
        await interaction.response.defer(ephemeral=True)
        data = self.database.execute("SELECT default_amount FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        
        if bot is not None:
            if not bot.bot:
                await interaction.followup.send(f"{config.WARN_EMOJI} This command is only supported for bots!")
                return
    
        if amount is None:
            if data is None:
                amount = 5
            else:
                amount = data[0]

        elif amount > 50:
            await interaction.followup.send(f"{config.WARN_EMOJI} You can't delete more than 50 messages at once!")
            return

        elif amount == 0:
            await interaction.followup.send(f"{config.WARN_EMOJI} No message will be deleted if amount is 0!")
            return
               
        messages = [message async for message in interaction.channel.history(limit=100)]
        msgs_deleted = 0
        if bot is None:
            for msg in messages:
                if msgs_deleted >= amount:
                    break

                if msg.author.bot:
                    await msg.delete()
                    msgs_deleted += 1
            
            await interaction.followup.send(f"{config.CLEAN_EMOJI} Deleted `{msgs_deleted}/{amount}` bot messages.")
            return

        else:        
            for msg in messages:
                if msgs_deleted >= amount:
                    break
                
                if msg.author == bot:
                    await msg.delete()
                    msgs_deleted += 1
            
            await interaction.followup.send(f"{config.CLEAN_EMOJI} Deleted `{msgs_deleted}/{amount}` bot messages.")
            return

    @bc.error
    async def bc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/clean bot", error_msg=error), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Clean(bot))