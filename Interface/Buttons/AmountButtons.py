import config
import sqlite3
import discord

from discord.ui import View, button, Button

class AmountButtons(View):
    def __init__(self, new_amount: int):
        self.database = sqlite3.connect("./Databases/Data.sqlite")
        self.new_amount = new_amount
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="amount_yes")
    async def amount_yes(self, interaction: discord.Interaction, button: Button):
        self.database.execute("UPDATE GuildSettings SET default_amount = ? WHERE guild_id = ?", (self.new_amount, interaction.guild.id,)).connection.commit()
        await interaction.response.edit_message(content=f"{config.DONE_EMOJI} Default amount replaced with `{self.new_amount}`.", embed=None, view=None)
        return

    @button(label="No", style=discord.ButtonStyle.red, custom_id="amount_no")
    async def amount_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", embed=None, view=None)
        return