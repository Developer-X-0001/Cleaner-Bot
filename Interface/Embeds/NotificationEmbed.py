import config
import discord

notification_embed = discord.Embed(
    title="Latest Message | January 23, 2023",
    description="Dear members of our amazing community,\
        \n\nWe're thrilled to announce that after addressing the recent disruptions, the Cleaner bot is now back online and fully operational! We appreciate your patience and understanding during this period.",
    color=discord.Color.magenta()
).add_field(
    name="What Happened?",
    value="During the recent disruption, our development team encountered various bugs and broken commands affecting Cleaner's functionality. However, thanks to the collective efforts of our dedicated community and developers, we've successfully resolved these issues, ensuring a smoother and more reliable experience for everyone.",
    inline=False
).add_field(
    name="Your Help Made a Difference!",
    value="A special shoutout to everyone who participated in the beta testing of the Cleaner Update Test bot. Your invaluable feedback and assistance were instrumental in identifying and fixing the issues efficiently. We couldn't have done it without your dedication and support.",
    inline=False
).add_field(
    name="What's Next?",
    value="With the bot now back in action, feel free to use Cleaner's commands as usual. If you encounter any lingering issues or have further suggestions, please don't hesitate to let us know in the #feedback channel.\
        \n\nWe're excited to continue providing you with a seamless and enjoyable experience in our Discord community. Thank you for your understanding, patience, and ongoing support!\
        \n\nBest regards,\
        \n***Developer X***",
    inline=False
).set_footer(
    text="You can view this message again by using /news"
).set_thumbnail(
    url=config.CLEANER_ICON
)