import config
import sqlite3
import discord

from Interface.Buttons.ReportsAndSuggestionsButtons import ReportsAndSuggestionsView
from Interface.Buttons.ErrorReportButton import ErrorReportView

class SubSuggestion(discord.ui.Modal, title="Suggestion"):
    heading = discord.ui.TextInput(
        label="Title of your suggestion",
        style=discord.TextStyle.short,
        placeholder="Type something catchy, for more upvotes ;)",
        required=True,
        max_length=30
    )

    suggestion = discord.ui.TextInput(
        label="Tell us what is in your brain",
        style=discord.TextStyle.long,
        placeholder="Suggest something unique ;)",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        database = sqlite3.connect("./Databases/ReportsAndSuggestionsData.sqlite")
        channel = interaction.client.get_channel(config.SUGGESTIONS_CHANNEL_ID)
        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.suggestion,
            color=discord.Color.magenta()
        ).set_author(
            name=interaction.user,
            icon_url=interaction.user.avatar
        ).set_footer(text=f"Sent from, Guild: {interaction.guild.name} | Members: {interaction.guild.member_count}")

        if interaction.guild.icon:
            suggestion_embed.set_thumbnail(url=interaction.guild.icon.url)
        
        msg = await channel.send(embed=suggestion_embed, view=ReportsAndSuggestionsView())
        database.execute("INSERT INTO ReportsAndSuggestions VALUES (?, ?, ?, ?, ?)", (interaction.guild.id, interaction.user.id, msg.id, self.heading, self.suggestion,)).connection.commit()
        await interaction.response.send_message(f"{config.SENT_EMOJI} Your suggestion has been recorded!", ephemeral=True)
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/suggestion", error_msg=error), ephemeral=True)
        return