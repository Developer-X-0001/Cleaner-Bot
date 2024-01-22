import config
import sqlite3
import discord

from discord.ui import Modal
from Interface.Buttons.ErrorReportButton import ErrorReportView

class SuggestionReplyModal(Modal, title="Report/Suggestion Reply"):
    def __init__(self):
        self.database = sqlite3.connect("./Databases/ReportsAndSuggestionsData.sqlite")
        super().__init__(timeout=None)
    
    reply = discord.ui.TextInput(
        label="Your reply",
        style=discord.TextStyle.long,
        placeholder="Type your reply here...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        data = self.database.execute("SELECT user_id, title, content FROM ReportsAndSuggestions WHERE message_id = ?", (interaction.message.id,)).fetchone()
        if data is None:
            await interaction.response.send_message(f"{config.ERROR_EMOJI} Oops! Something went wrong...", ephemeral=True)
            return
        else:
            user = await interaction.client.fetch_user(data[0])
            try:
                await user.send(content=f"{config.NOTIFICATION_EMOJI} **You have a new reply on your report/suggestion post!**\n\n**{interaction.user.name}** has replied to your following post:\n\n> **{data[1]}**\n> {data[2]}\n\n**Reply:** {self.reply}")
                await interaction.response.send_message(f"{config.MAIL_SENT_EMOJI} Your message has been delivered.", ephemeral=True)
                return
            
            except discord.errors.Forbidden:
                await interaction.response.send_message(f"{config.ERROR_EMOJI} I'm unable to DM {user.name}, instead I've sent the message to their mailbox.", ephemeral=True)
                return
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(embed=discord.Embed(title="Unexpected Error Occured", description=f"{config.ERROR_EMOJI} I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{error}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/suggestion", error_msg=error), ephemeral=True)
        return