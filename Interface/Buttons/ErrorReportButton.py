import config
import discord

from discord import ButtonStyle
from discord.ui import View, Button, button

class ErrorReportView(View):
    def __init__(self, cmd: str, error_msg: str):
        self.cmd = cmd
        self.error_msg = error_msg
        super().__init__(timeout=None)
    
    @button(label="Submit Report!", style=ButtonStyle.red)
    async def error_submit_btn(self, interaction: discord.Interaction, button: Button):
        reports_channel = interaction.client.get_channel(config.ERRORREPORTS_CHANNEL_ID)
        embed = discord.Embed(
            title="Error Reported",
            description=f"**Reported By:** {interaction.user.name if not interaction.user.global_name else interaction.user.global_name}\
                \n**Server:** {interaction.guild.name}\
                \n**Command:** `{self.cmd}`\
                \n**Error Message:**\n```cpp\n{self.error_msg}\n```\n",
            color=discord.Color.magenta()
        )

        await reports_channel.send(embed=embed)
        await interaction.response.edit_message(embed=discord.Embed(description=f"{config.SENT_EMOJI} Your report has been forwared to [Cleaner Support Server](https://discord.gg/C9TN63q7xn)", color=discord.Color.magenta()), view=None)
        return