import os
import sqlite3
import discord
from discord.ext import commands
from Interface.Buttons.ReportsAndSuggestionsButtons import ReportsAndSuggestionsView

import config

intents = discord.Intents.default()
intents.message_content = True

class Cleaner(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents= intents,
            status=discord.Status.dnd,
            activity=discord.Game(name=f"/help | v{config.BOT_VERSION}"),
            application_id = config.APPLICATION_ID
        )

    async def setup_hook(self):
        sqlite3.connect("./Databases/Data.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS NukeCooldowns (
                    guild_id INTEGER,
                    timestamp INTEGER,
                    status TEXT,
                    Primary Key (guild_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS GuildSettings (
                    guild_id INTEGER,
                    default_amount INTEGER,
                    audit_channel INTEGER,
                    nuke_cooldown INTEGER,
                    default_pins TEXT,
                    premium_status TEXT,
                    Primary Key (guild_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS NotificationView (
                    user_id INTEGER,
                    status TEXT,
                    Primary Key (user_id)
                )
            '''
        ).close()

        sqlite3.connect("./Databases/ReportsAndSuggestionsData.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (
                    guild_id INTEGER,
                    user_id INTEGER,
                    message_id INTEGER,
                    title TEXT,
                    content TEXT,
                    Primary Key (message_id)
                )
            '''
        ).close()

        sqlite3.connect("./Databases/BadwordsFilter.sqlite").close()

        self.add_view(ReportsAndSuggestionsView())
        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension(f"Commands.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Events"):
            if filename.endswith('.py'):
                await self.load_extension(f"Events.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Tasks"):
            if filename.endswith('.py'):
                await self.load_extension(f"Tasks.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        await bot.tree.sync()

bot = Cleaner()

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord, current latency is {round(bot.latency * 1000)}ms")

@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.reload_extension(f"{folder}.{cog}")
    await ctx.send(f"🔁 {cog} reloaded!")

@bot.command(name="load")
@commands.is_owner()
async def load(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.load_extension(f"{folder}.{cog}")
    await ctx.send(f"🆙 {cog} loaded!")

@bot.command()
async def membercount(ctx):
    count = 0
    for guild in bot.guilds:
        count += guild.member_count
    
    await ctx.send(count)

bot.run(config.BOT_TOKEN)
