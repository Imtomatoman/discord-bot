import discord
import os
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
ACTIVE_STOCK = "active_stock.txt"
MASTER_SUPPLY = "master_supply.txt"
REFILL_AMOUNT = 5

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

def read_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]

def write_lines(filepath, lines):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

def refill_active_stock():
    master = re
