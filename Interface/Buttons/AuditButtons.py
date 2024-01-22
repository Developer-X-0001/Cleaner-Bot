import config
import sqlite3
import discord

from discord.ui import View, button, Button

class AuditButtons(View):
    def __init__(self, previous_channel: discord.TextChannel, new_channel: discord.TextChannel):
        self.database = sqlite3.connect("./Databases/Data.sqlite")
        self.previous_channel = previous_channel
        self.new_channel = new_channel
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="audit_yes")
    async def audit_yes(self, interaction: discord.Interaction, button: Button):
        self.database.execute("UPDATE GuildSettings SET audit_channel = ? WHERE guild_id = ?", (self.new_channel.id, interaction.guild.id,)).connection.commit()
        await interaction.response.edit_message(content=f"{config.DONE_EMOJI} Audit channel {self.previous_channel.mention} replaced with {self.new_channel.mention}.", embed=None, view=None)
        return

    @button(label="No", style=discord.ButtonStyle.red, custom_id="audit_no")
    async def audit_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", embed=None, view=None)
        return
