from math import *
import sys
import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import app_commands
import time
import os
import json
import base64
from openai import OpenAI
import requests
import re
from collections import deque
import sqlite3
import datetime
from dotenv import load_dotenv
from pathlib import Path
import aiomysql
from modules.config_parser import config

CHANNEL_ID = 1266861880350212126
USER_ID = 1062000524662161440
INVITE_CODE_TO_TRACK = 'EzX5MuCpHd'
PRAXY_LOGS_CHANNEL_ID = 1265212193687867494
invites = {}
GUILD_ID = 960057732260560926 

DEFAULT_COLOR = config.get("default_color", 0x30B521)
SYSTEM_COLOR = config.get("system_color", 0x8C8B8B)
RED_COLOR = config.get("red_color", 0xFF0000)
YELLOW_COLOR = config.get("yellow_color", 0xEAFF00)
BLUE_COLOR = config.get("blue_color", 0x0066FF)

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
bot_token = os.getenv('BOT_TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', 3306))


openai_key = os.getenv('OPENAIKEY')
def aigen(message):
    global openai_key
    clientai = OpenAI(api_key = openai_key)
    completion = clientai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Your name is Praxy Nivora. You are core member in the HC Union, a minecraft online guild that played Decimation before it closed, and now chills on Hypixel, Manacube and LeoneMC. It is lead by HellSan_HC and has 'Crystal_HC, Bonnie_HC, Astolfo_HC, rbull_HC, Aflex_HC, Robin_HC' as other core members. Use chat expressions like 'u', 'lol', 'lmao', 'alr', 'sup', 'ye', 'nah', 'ngl', 'y', ':)', 'bruh'., and use chat language. Your responses have to be brief."},
        {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message.content

try:
    with sqlite3.connect('hc.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT VALUE, LAST_ID FROM count WHERE id = 1")
        dat = cur.fetchone()
        counting, last_id = dat
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

def get_last_id():
    global last_id
    return last_id
def set_last_id(new):
    global last_id
    last_id = new
    try:
        with sqlite3.connect('hc.db') as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE count SET last_id = {new} WHERE id = 1")
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def get_counting():
    global counting
    return counting
def set_counting(new):
    global counting
    counting = new
    try:
        with sqlite3.connect('hc.db') as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE count SET value = {new} WHERE id = 1")
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

class PraxyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.invites = {}
        self.db_pool = None 

    async def setup_hook(self) -> None:

        try:
            self.db_pool = await aiomysql.create_pool(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                db=DB_NAME,
                port=DB_PORT,
                autocommit=True, 
                charset='utf8mb4'
            )
            print("Main bot created database connection pool successfully.")
        except Exception as e:
            print(f"FAILED to connect to database in main bot: {e.__class__.__name__}: {e}")
            self.db_pool = None
            sys.exit(1)

        print("Running setup_hook...")
        await self.load_cogs()
        print("Cogs loaded from setup_hook.")

        guild_id = 960057732260560926
        guild_obj = discord.Object(id=guild_id)

        self.tree.clear_commands(guild=guild_obj)
        for command in self.tree.walk_commands():
            self.tree.add_command(command, guild=guild_obj)

        try:
            synced_commands = await self.tree.sync(guild=discord.Object(id=960057732260560926))
            print(f'Successfully synced {len(synced_commands)} commands to guild from setup_hook.')

            print("Commands synced (for confirmation - from setup_hook):")
            for cmd in synced_commands:
                print(f"- /{cmd.name}: {cmd.description}")
        except Exception as e:
            print(f"FAILED to sync commands from setup_hook: {e.__class__.__name__}: {e}")

    async def load_cogs(self) -> None:

        await self.load_extension("modules.cogs.database") 
        await self.load_extension("modules.cogs.help")
        await self.load_extension("modules.cogs.utility")
        await self.load_extension("modules.cogs.music")
        print("Loaded cogs.")

    async def on_ready(self):
        print(f'We have logged in as {self.user.name} (ID: {self.user.id})')
        for guild in self.guilds:
            self.invites[guild.id] = await guild.invites()
        status = discord.CustomActivity(name=".gg/hcunion")
        await self.change_presence(status=discord.Status.online, activity=status)

    async def on_message(self, message):

        if message.author == self.user:
            return

        if self.user.mentioned_in(message):

            content_without_mention = message.clean_content.replace(f"@{self.user.display_name}", "", 1).strip()

            if content_without_mention:
                aireply = aigen(content_without_mention)
                await message.channel.send(aireply)
            return 

        if message.content == "💀":
            await message.channel.send("<a:RotatingSkull:1145453604086485075>")

        if "💀" in message.content or "☠️" in message.content:
            emoji_skull = '\U0001F480'
            await message.add_reaction(emoji_skull)

        if message.channel.id == 996713647386673182:
            current = get_counting()
            last = get_last_id()
            if last != 0:
                try:
                    msg = await message.channel.fetch_message(last)
                    await msg.delete()
                except discord.errors.NotFound:
                    pass
            sent = await message.channel.send(r"**Counting channel :** When in doubt, just count. Try not making me lose my count \:D Warning : Deleting count messages = ban from counting. Current count : "+str(current + 1))
            set_last_id(sent.id)

        if message.channel.id == 996713647386673182:
            count = get_counting()
            try:
                if int(message.content) == (count + 1):
                    set_counting(count + 1)
                    emoji1 = '\U00002705'
                    emoji2 = '\U0001F4AF'
                    if int(message.content) % 100 == 0 :
                        await message.add_reaction(emoji2)
                    else :
                        await message.add_reaction(emoji1)
                else :
                    await message.delete()
            except ValueError: 
                await message.delete()
            except Exception as e: 
                print(f"Error in counting: {e}")
                await message.delete()
            return 

        await self.process_commands(message)

bot = PraxyBot()
tree = bot.tree

bot.run(bot_token)