import config
import discord

changelog_embed = discord.Embed(
    colour=discord.Color.magenta()
).add_field(
    name="Fixed and updated Clean commands.",
    value="- Removed **pins** and **contains** argument from `/clean bot` and `/clean user` commands.\
        \n- Decreased maximum message deletion amount to **50**.\
        \n- Added 0.5-1.5s and 1.0-2.0s cooldown on `/clean messages` when amount is greater than 10 and 25 respectively.",
    inline=False
).add_field(
    name="Improved Badwords system.",
    value="- Ability to add multiple badwords at once.\
        \n- Added autocomplete function in `/badwords remove` when removing badwords.",
    inline=False
).add_field(
    name="Updated Role delete command.",
    value="- Added a check where the bot will throw error if the mentioned role is higher than the bot or the user's role.",
    inline=False
).add_field(
    name="Added ability to report errors.",
    value="- Whenever a command fails you'll be shown with a button saying **Submit Report!**, pressing it will send it directly to the support server.",
    inline=False
).add_field(
    name="Rewamped the Database system.",
    value="- Basically we re-created the database structure.",
    inline=False
).add_field(
    name="Cooldown for `/nuke` command reduced to **15 days**.",
    value="- Previously it was set to 30 days.",
    inline=False
).set_author(
    name='Last Updated on October 5, 2022',
    icon_url=config.CLEANER_ICON
).set_thumbnail(
    url=config.CLEANER_ICON
).set_footer(
    text=f'v{config.BOT_VERSION} | type /report to send bug reports to us'
)