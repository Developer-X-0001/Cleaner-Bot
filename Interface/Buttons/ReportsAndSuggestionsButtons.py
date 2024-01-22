import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import View, button, Button
from Interface.Modals.ReportReplyModal import ReplyModal
from Interface.Modals.SuggestionReplyModal import SuggestionReplyModal

class ReportsAndSuggestionsView(View):
    def __init__(self):
        self.database = sqlite3.connect("./Databases/ReportsAndSuggestionsData.sqlite")
        super().__init__(timeout=None)
    
    @button(label="Reply", style=ButtonStyle.green, custom_id="reply_button")
    async def reply_func(self, interaction: discord.Interaction, button: Button):
        role = interaction.guild.get_role(config.SUPPORTTEAM_ROLE_ID)
        if role in interaction.user.roles or interaction.user == interaction.client.application.owner:
            if interaction.channel.id == config.REPORTS_CHANNEL_ID:
                await interaction.response.send_modal(ReplyModal())
            if interaction.channel.id == config.SUGGESTIONS_CHANNEL_ID:
                await interaction.response.send_modal(SuggestionReplyModal())
        else:
            await interaction.followup.send(content=f"{config.ERROR_EMOJI} MissingPermissions, You aren't authorized to do that!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji=config.UPVOTE_EMOJI, custom_id="upvote_button")
    async def upvote_button(self, interaction: discord.Interaction, button: Button):
        self.database.execute(f"CREATE TABLE IF NOT EXISTS {interaction.message.id} (user_id INTEGER, vote TEXT)")
        self.database.execute(f"INSERT INTO {interaction.message.id} VALUES (?, ?) ON CONFLICT (user_id) DO UPDATE SET vote = ? WHERE user_id = ?", (interaction.user.id, 'upvote', 'upvote', interaction.user.id,)).connection.commit()
        await interaction.followup.send(content=f"{config.DONE_EMOJI} Success!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji=config.DOWNVOTE_EMOJI, custom_id="downvote_button")
    async def downvote_button(self, interaction: discord.Interaction, button: Button):
        self.database.execute(f"CREATE TABLE IF NOT EXISTS {interaction.message.id} (user_id INTEGER, vote TEXT)")
        self.database.execute(f"INSERT INTO {interaction.message.id} VALUES (?, ?) ON CONFLICT (user_id) DO UPDATE SET vote = ? WHERE user_id = ?", (interaction.user.id, 'downvote', 'downvote', interaction.user.id,)).connection.commit()
        await interaction.followup.send(content=f"{config.DONE_EMOJI} Success!", ephemeral=True)
    
    @button(style=ButtonStyle.red, emoji="✖", custom_id="delete_report")
    async def report_delete(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        mod_role = interaction.guild.get_role(config.MODERATOR_ROLE_ID)
        if mod_role in interaction.user.roles or interaction.user == interaction.client.application.owner:
            self.database.execute("DELETE FROM ReportsAndSuggestions WHERE message_id = ?", (interaction.message.id,)).connection.commit()
            self.database.execute(f"DROP TABLE {interaction.message.id}").connection.commit()
            await interaction.message.delete()
            return
        else:
            await interaction.followup.send(content=f"{config.ERROR_EMOJI} MissingPermissions, You aren't authorized to do that!", ephemeral=True)
            return