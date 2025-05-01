import asyncio
from highrise import BaseBot
from highrise.models import User

# Emote list: (aliases, emote_id, duration)
emote_list: list[tuple[list[str], str, float]] = [
    (['rest', 'resting', 'sit', 'sitdown', 'relax', 'lay'], 'sit-idle-cute', 17.0),
    (['zombie', 'undead', 'walkdead', 'zombiemode', 'creep'], 'idle_zombie', 28.7),
    (['relaxed', 'laying', 'chill', 'sleep', 'relaxing', 'calm'], 'idle_layingdown2', 21.5),
    (['attentive', 'alert', 'focused', 'ready', 'watching', 'observe'], 'idle_layingdown', 24.5),
    (['sleepy', 'tired', 'dozing', 'nap', 'snore', 'zzz'], 'idle-sleep', 22.6),
    (['sad', 'pout', 'cry', 'tears', 'blue', 'unhappy'], 'idle-sad', 24.3),
    (['posh', 'classy', 'elegant', 'graceful', 'chic', 'fancy'], 'idle-posh', 21.8),
    (['looping', 'spin', 'repeat', 'cycle', 'replay', 'again'], 'emote-looping', 30.0),
    (['yes', 'yeah', 'sure', 'ok', 'affirmative', 'yep'], 'emote-yes', 2.5),
    (['hello', 'hi', 'hey', 'greet', 'wave', 'salute'], 'emote-hello', 2.7),
    (['laugh', 'lol', 'haha', 'giggle', 'chuckle', 'lmao'], 'emote-laughing', 2.6),
]

# Store active loops
user_loops: dict[str, asyncio.Task] = {}

# Start emote loop
async def loop(bot: BaseBot, user: User, message: str):
    parts = message.strip().split(" ", 1)
    if len(parts) < 2:
        await bot.highrise.chat("Please provide an emote name after 'loop'.")
        return

    emote_name = parts[1].strip().lower()

    selected = None
    for aliases, emote_id, duration in emote_list:
        if emote_name in [alias.lower() for alias in aliases]:
            selected = (aliases, emote_id, duration)
            break

    if not selected:
        await bot.highrise.chat("Invalid emote name.")
        return

    aliases, emote_id, duration = selected

    # Cancel previous loop if exists
    if user.id in user_loops:
        user_loops[user.id].cancel()

    async def emote_loop():
        try:
            await bot.highrise.chat(f"@{user.username} started looping '{emote_id}' every {duration} seconds.")
            while True:
                await bot.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(emote_loop())
    user_loops[user.id] = task

# Stop emote loop
async def stop_loop(bot: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await bot.highrise.chat(f"@{user.username}, your emote loop has been stopped.")
    else:
        await bot.highrise.chat(f"@{user.username}, you have no active loop to stop.")

# Auto-start emote if message matches a direct emote alias
async def check_and_start_emote_loop(bot: BaseBot, user: User, message: str):
    message = message.strip().lower()
    found = None
    for aliases, emote_id, duration in emote_list:
        if message in [alias.lower() for alias in aliases]:
            found = (aliases, emote_id, duration)
            break

    if found:
        await loop(bot, user, f"loop {message}")
