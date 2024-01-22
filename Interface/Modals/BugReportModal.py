import config
import sqlite3
import discord

from Interface.Buttons.ReportsAndSuggestionsButtons import ReportsAndSuggestionsView
from Interface.Buttons.ErrorReportButton import ErrorReportView

class BugReport(discord.ui.Modal, title="Report"):
    heading = discord.ui.TextInput(
        label="Title of your report",
        style=discord.TextStyle.short,
        placeholder="Type the title of your report, i.e Commands not working",
        required=True,
        max_length=30
    )

    report = discord.ui.TextInput(
        label="Tell us what you want to report",
        style=discord.TextStyle.long,
        placeholder="Describe your issue in detail",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        database = sqlite3.connect("./Databases/ReportsAndSuggestionsData.sqlite")
        channel = interaction.client.get_channel(config.REPORTS_CHANNEL_ID)
        report_embed = discord.Embed(
            title=self.heading,
            description=self.report,
            color=discord.Color.magenta()
        ).set_author(
            name=interaction.user,
            icon_url=interaction.user.avatar
        ).set_footer(text=f"Sent from, Guild: {interaction.guild.name} | Members: {interaction.guild.member_count}")

        if interaction.guild.icon:
            report_embed.set_thumbnail(url=interaction.guild.icon.url)

        msg = await channel.send(embed=report_embed, view=ReportsAndSuggestionsView())
        database.execute("INSERT INTO ReportsAndSuggestions VALUES (?, ?, ?, ?, ?)", (interaction.guild.id, interaction.user.id, msg.id, self.heading, self.report,)).connection.commit()
        await interaction.response.send_message(f"{config.SENT_EMOJI} Your report has been sent!", ephemeral=True)
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/report", error_msg=error), ephemeral=True)
        return