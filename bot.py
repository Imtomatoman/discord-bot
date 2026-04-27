import discord
import os
from discord.ext import commands

TOKEN = os.environ.get(MTQ5ODExNzk1NDY2MTc4MTU5NQ.Gpf98x.sY8jxSQTzufdCj6yjkF5msGP0Ot5QL1aVzeKyI)
ACTIVE_STOCK = "active_stock.txt"
MASTER_SUPPLY = "master_supply.txt"
REFILL_AMOUNT = 5

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


def read_lines(filepath: str) -> list[str]:
    """Read non-empty lines from a file, or return [] if file doesn't exist."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def write_lines(filepath: str, lines: list[str]) -> None:
    """Write lines back to a file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


def refill_active_stock() -> bool:
    """
    Pull up to REFILL_AMOUNT entries from master_supply into active_stock.
    Returns True if at least one entry was moved, False if master is also empty.
    """
    master = read_lines(MASTER_SUPPLY)
    if not master:
        return False

    to_move = master[:REFILL_AMOUNT]
    remaining = master[REFILL_AMOUNT:]

    active = read_lines(ACTIVE_STOCK)
    write_lines(ACTIVE_STOCK, active + to_move)
    write_lines(MASTER_SUPPLY, remaining)
    return True


def pop_entry() -> str | None:
    """
    Get and remove the first entry from active_stock.
    Refills from master_supply if active_stock is empty.
    Returns None if both files are empty.
    """
    active = read_lines(ACTIVE_STOCK)

    if not active:
        if not refill_active_stock():
            return None  # Both files empty
        active = read_lines(ACTIVE_STOCK)

    entry = active[0]
    write_lines(ACTIVE_STOCK, active[1:])
    return entry


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.command(name="gen")
async def gen(ctx: commands.Context):
    entry = pop_entry()

    if entry is None:
        await ctx.send("❌ **Out of stock.** Please check back later.")
        return

    try:
        await ctx.author.send(f"✅ Here is your code/account:\n```\n{entry}\n```")
        # Confirm in channel without revealing the entry
        await ctx.send(f"✅ {ctx.author.mention}, check your DMs!")
    except discord.Forbidden:
        # DMs are closed — put the entry back at the top so it isn't lost
        active = read_lines(ACTIVE_STOCK)
        write_lines(ACTIVE_STOCK, [entry] + active)
        await ctx.send(
            f"❌ {ctx.author.mention}, I couldn't send you a DM. "
            "Please enable DMs from server members and try again."
        )
    except discord.HTTPException as e:
        # Unexpected Discord error — also return entry to stock
        active = read_lines(ACTIVE_STOCK)
        write_lines(ACTIVE_STOCK, [entry] + active)
        await ctx.send(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")
    bot.run(TOKEN)
