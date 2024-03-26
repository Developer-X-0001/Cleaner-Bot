import config
import sqlite3
import discord

from discord import app_commands
from discord.ext import commands
from Functions.SplitAndClean import split_and_clean
from Interface.Buttons.ErrorReportButton import ErrorReportView

class Audit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.database = sqlite3.connect("./Databases/BadwordsFilter.sqlite")

    bad_words = app_commands.Group(name="badwords", description="Add or remove bad words for the current words")

    @bad_words.command(name="add", description="blacklist a word, to prevent users from saying it")
    @app_commands.describe(words="The words you want to blacklist. (Multiple words are supported separated by commas or spaces)")
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, words:str):
        await interaction.response.defer(ephemeral=True)
        word_list = split_and_clean(words)
        self.database.execute(f"CREATE TABLE IF NOT EXISTS '{interaction.guild.id}' (word TEXT, patterns TEXT)")

        words_existing = []
        words_added = []

        for word in word_list:
            data = self.database.execute(f"SELECT word FROM '{interaction.guild.id}' WHERE word = ?", (word,)).fetchone()
            if data is None:
                self.database.execute(f"INSERT INTO '{interaction.guild.id}' VALUES (?)", (word,)).connection.commit()
                words_added.append(word)
            else:
                words_existing.append(word)

        formatted_existing_words = ""
        counter = 0
        for i in words_existing:
            counter += 1
            formatted_existing_words += f"{counter}. {i}\n"
        
        formatted_added_words = ""
        counter = 0
        for j in words_added:
            counter += 1
            formatted_added_words += f"{counter}. {j}\n"
        
        embed = discord.Embed(
            title=f"Updated Blacklisted Words for {interaction.guild.name}",
            description=f"From a total of `{len(word_list)}` word(s), I've added `{len(words_added)}` while the other `{len(words_existing)}` words are already blacklisted.",
            color=discord.Color.magenta()
        ).add_field(
            name=f"Words Added ({len(words_added)}):",
            value=f"```\n{formatted_added_words}\n```" if formatted_added_words != "" else "```\n \n```",
            inline=False
        ).add_field(
            name=f"Words Ignored ({len(words_existing)}):",
            value=f"```\n{formatted_existing_words}\n```" if formatted_existing_words != "" else "```\n \n```",
            inline=False
        )

        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        await interaction.followup.send(embed=embed)
        return
    
    @add.error
    async def add_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/badwords add", error_msg=error), ephemeral=True)
            return
        
    @bad_words.command(name="remove", description="remove a blacklisted word")
    @app_commands.describe(word="The word you want to remove from blacklist.")
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove(self, interaction: discord.Interaction, word:str):
        await interaction.response.defer(ephemeral=True)
        self.database.execute(f"CREATE TABLE IF NOT EXISTS '{interaction.guild.id}' (word TEXT, patterns TEXT)")
        data = self.database.execute(f"SELECT word FROM '{interaction.guild.id}' WHERE word = ?", (word,)).fetchone()
        if data[0] is None:
            await interaction.followup.send(f"{config.WARN_EMOJI} The provided word can't be found in blacklisted words")
            return
        
        else:
            self.database.execute(f"DELETE FROM '{interaction.guild.id}' WHERE word = ?", (word,)).connection.commit()
            await interaction.followup.send(f"{config.DONE_EMOJI} Removed `{word}` from blacklisted words.")
            return
    
    @remove.autocomplete('word')
    async def badword_remove_autocomplete_callback(self, interaction: discord.Interaction, current: str):
        self.database.execute(f"CREATE TABLE IF NOT EXISTS '{interaction.guild.id}' (word TEXT, patterns TEXT)")
        data = self.database.execute(f"SELECT word FROM '{interaction.guild.id}'").fetchall()
        badwords = []
        for i in data:
            badwords.append(i[0])
            
        return [
            app_commands.Choice(name=word, value=word) for word in badwords if current in word
        ]

    @remove.error
    async def remove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/badwords remove", error_msg=error), ephemeral=True)
            return
    
    @bad_words.command(name="list", description="List the blacklisted words for your server")
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def word_list(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.database.execute(f"CREATE TABLE IF NOT EXISTS '{interaction.guild.id}' (word TEXT, patterns TEXT)")
        data = self.database.execute(f"SELECT word FROM '{interaction.guild.id}'").fetchall()
        if data == []:
            await interaction.followup.send(f"{config.WARN_EMOJI} There aren't any blacklisted words for this server.")
            return
        else:
            count = 0
            word_list = ""

            for word in data:
                count += 1
                word_list += f"{count}. {word[0]}\n"
            
            embed = discord.Embed(
                title=f"Blacklisted Words for {interaction.guild.name}",
                color=discord.Color.magenta()
            )
            embed.description = f"```\n{word_list}```\nTotal Blacklisted Words `{count}`"
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)

            embed.set_footer(text="Add or Remove badwords by /badwords add, /badwords remove")
            
            await interaction.followup.send(embed=embed)
            return
    
    @word_list.error
    async def word_list_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
            return
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
            return
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/badwords list", error_msg=error), ephemeral=True)
            return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Audit(bot))