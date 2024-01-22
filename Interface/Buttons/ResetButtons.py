import config
import sqlite3
import discord

from discord.ui import View, button, Button

class ResetButtons(View):
    def __init__(self):
        self.database = sqlite3.connect("./Databases/Data.sqlite")
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="reset_yes")
    async def reset_yes(self, interaction: discord.Interaction, button: Button):
        self.database.execute("DELETE FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,)).connection.commit()
        self.database.execute("INSERT INTO GuildSettings VALUES (?, 5, NULL, 0, ?, ?)", (interaction.guild.id, 'delete', 'inactive')).connection.commit()
        await interaction.response.edit_message(content=f"{config.DONE_EMOJI} Success!", embed=None, view=None)
        return

    @button(label="No", style=discord.ButtonStyle.red, custom_id="reset_no")
    async def reset_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", embed=None, view=None)
        return