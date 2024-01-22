import config
import discord

help_embed = discord.Embed(
    colour=discord.Color.magenta()
).set_author(
    name='Cleaner Bot Commands',
    icon_url=config.CLEANER_ICON
).set_thumbnail(
    url=config.CLEANER_ICON
).add_field(
    name='Help',
    value='Shows this message',
    inline=False
).add_field(
    name="**__Cleaning Commands:__**",
    value="These commands can be found under /clean command group\
        \n**Clean:** Delete a specified number of messages.\
        \n**User:** Delete a specified of messages sent by the mentioned user.\
        \n**Bot:** Delete a specified number of messages sent by bots.\
        \n**Mass-delete:** Delete someone's messages all across the server, not just from the current channel.",
    inline=False
).add_field(
    name="**__Delete Commands:__**",
    value="These commands can be found under /delete command group\
        \n**Channel:** Delete the mentioned channel.\
        \n**Category:** Delete the mentioned category.\
        \n**Role:** Delete the mentioned role.\
        \n**Thread:** Delete the mentioned thread.\
        \n**Emoji:** Delete the specified emoji.\
        \n**Nickname:** Delete the nickname of the mentioned user set in current server.",
    inline=False
).add_field(
    name="**__Purge Commands:__**",
    value="These commands can be found under /purge command group\
        \n**Channel:** Deletes and re-creates the mentioned or current channel, with same permissions.\
        \n**Category:** Deletes and re-creates the current category",
    inline=False
).add_field(
    name="**__Badword Filter Commands:__**",
    value="These commands can be found under /badwords command group\
        \n- **Add:** Adds one or multiple words to the blacklist words.\
        \n- **List:** Shows all the blacklisted words with their total count.\
        \n- **Remove:** Removes a word from the blacklisted words."
).add_field(
    name="**__Settings Commands:__**",
    value="These commands can be found under /settings command group\
        \n**Audit Channel:** Set a channel to get message logs.\
        \n**Default Pin Condition:** Set default pin check condition, it'll be check when using `/clean messages` command.\
        \n**Default Amount:** Set default cleaning amount for clean message command\
        \n**Reset:** Reset all settings for the current server.\
        \n**Show:** View the current settings for the server.",
    inline=False
).add_field(
    name="**__Special Commands:__**",
    value="Following command can be invoked by server owner only.\
        \n**Nuke:** Wipes everything from the server except members, **THIS IS A DANGEROUS COMMAND!**",
    inline=False
).add_field(
    name="**__Help & Support:__**",
    value="**Report:** Facing issues using the bot? submit the report by /report\
        \n**Suggestion:** Want something to get added to bot? Tell us your ideas /suggestion",
    inline=False
).add_field(
    name="**__Other Commands:__**",
    value="**Check Permissions:** Check if the bot has all necessary permisions to work properly\
        \n**Info** Show bot's information\
        \n**Changelog:** Show latest changelog.\
        \n**Ping:** Show bot's current latency.\
        \n**Help:** Shows this message.",
    inline=False
)
help_embed.set_footer(text=f'v{config.BOT_VERSION} | type /changelog for updates')