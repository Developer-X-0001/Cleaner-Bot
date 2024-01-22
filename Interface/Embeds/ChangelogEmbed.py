import config
import discord

changelog_embed = discord.Embed(
    colour=discord.Color.magenta()
).add_field(
    name="Fixed and updated Clean commands.",
    value="1. Removed **pins** and **contains** argument from `/clean bot` and `/clean user` commands.\
        \n2. Decreased maximum message deletion amount to **50**.",
    inline=False
).add_field(
    name="Improved Badwords system.",
    value="1. Ability to add multiple badwords at once.\
        \n2. Added autocomplete function in `/badwords remove` when removing badwords.",
    inline=False
).add_field(
    name="Rewamped the Database system.",
    value="Basically we re-created the database structure.",
    inline=False
).add_field(
    name="Cooldown for `/nuke` command reduced to **15 days**.",
    value="- Previously it was set to 30 days, we are also planning to release a Premium version of Cleaner.",
    inline=False
).set_author(
    name='Last Updated on October 5, 2022',
    icon_url=config.CLEANER_ICON
).set_thumbnail(
    url=config.CLEANER_ICON
).set_footer(
    text=f'v{config.BOT_VERSION} | type /report to send bug reports to us'
)