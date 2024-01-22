import config
import discord

from discord import ButtonStyle
from discord.ui import View, button, Button
from Interface.Buttons.ErrorReportButton import ErrorReportView

class CategoryDeleteButtons(View):
    def __init__(self, category: discord.CategoryChannel):
        self.category = category
        super().__init__(timeout=None)
    
    @button(label="Confirm", style=ButtonStyle.green, custom_id="category_delete_confirm_button")
    async def cat_del_confirm(self, interaction: discord.Interaction, button: Button):
        count = 1
        channel_names = ""
        for channel in self.category.channels:
            channel_names += f"{count}. {channel.name}"
            count += 1

        embed = discord.Embed(description=f"**Deleting 📁{self.category.name}:**\nDeleting following channels\n```{channel_names}```\n{config.LOADING_EMOJI} **Processing**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=None)

        for channel in self.category.channels:
            try:
                await channel.delete()
            except Exception as e:
                await interaction.edit_original_response(embed=discord.Embed(title="Unexpected Error Occured",description=f"I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{e}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete category", error_msg=e))
                return

        try:
            await self.category.delete()
        except Exception as e:
            await interaction.edit_original_response(embed=discord.Embed(title="Unexpected Error Occured",description=f"I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{e}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/delete category", error_msg=e))
            return

        await interaction.edit_original_response(embed=discord.Embed(description=f"**Deleted 📁{self.category.name}:**\nDeleted channels\n```{channel_names}```\n{config.DONE_EMOJI} **Process Completed**", color=discord.Color.green()))
        return
    
    @button(label="Deny", style=ButtonStyle.red, custom_id="category_delete_deny_button")
    async def cat_del_deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=discord.Embed(description=f"{config.ERROR_EMOJI} **Process Denied**", color=discord.Color.red()), view=None)
        return