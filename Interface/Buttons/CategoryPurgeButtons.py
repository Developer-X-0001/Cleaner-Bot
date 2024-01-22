import config
import discord

from discord.ui import View, button, Button
from Interface.Buttons.ErrorReportButton import ErrorReportView

class CategoryPurgeButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="category_purge_yes")
    async def category_purge_yes(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.CLEAN_EMOJI} Cleaning **{interaction.channel.category.name.upper()}**", view=None)
        no_of_channels = len(interaction.channel.category.channels)
        deleted_channels = 0
        for channel in interaction.channel.category.channels:
            try:
                await channel.delete()
                deleted_channels += 1
                await channel.clone()

            except Exception as e:
                await interaction.edit_original_response(embed=discord.Embed(title="Unexpected Error Occured",description=f"I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{e}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge category", error_msg=e))
                return

            if deleted_channels == no_of_channels:
                try:
                    old_category = await interaction.channel.category
                    old_category_name = old_category.name()
                    new_category = await interaction.guild.create_category(name=old_category_name)
                    for channel in interaction.channel.category.channels:
                        await channel.move(category=new_category, beginning=True)
                    
                    await old_category.delete()
                
                except Exception as e:
                    await interaction.edit_original_response(embed=discord.Embed(title="Unexpected Error Occured",description=f"I am unable to proceed due to the following error:\n\n__**Error Message:**__\n```cpp\n{e}\n```", color=discord.Color.red()), view=ErrorReportView(cmd="/purge category", error_msg=e))
                    return
    
    @button(label="No", style=discord.ButtonStyle.red, custom_id="category_purge_no")
    async def category_purge_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"{config.ERROR_EMOJI} Request Denied", view=None)
        return
    