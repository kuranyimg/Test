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

user_loops: dict[str, asyncio.Task] = {}

async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    cleaned_msg = message.strip()
    lower_msg = cleaned_msg.lower()

    # Stop loop command
    if lower_msg == "stop":
        if user.id in user_loops:
            user_loops[user.id].cancel()
            del user_loops[user.id]
            await self.highrise.chat(f"@{user.username}, your emote loop has been stopped.")
        else:
            await self.highrise.chat(f"@{user.username}, you have no active loop.")
        return

    # Check if it's a loop command
    loop_prefixes = ("loop ", "/loop ", "!loop ", "-loop ")
    if any(lower_msg.startswith(prefix) for prefix in loop_prefixes):
        emote_name = cleaned_msg.split(" ", 1)[1].strip().lower()
        selected = next((e for e in emote_list if emote_name in [alias.lower() for alias in e[0]]), None)

        if not selected:
            await self.highrise.chat("Invalid emote name.")
            return

        # Cancel existing loop if present
        if user.id in user_loops:
            user_loops[user.id].cancel()

        _, emote_id, duration = selected

        async def emote_loop():
            try:
                await self.highrise.chat(f"@{user.username} is now looping '{emote_id}'.")
                while True:
                    await self.highrise.send_emote(emote_id, user.id)
                    await asyncio.sleep(duration)
            except asyncio.CancelledError:
                pass

        user_loops[user.id] = asyncio.create_task(emote_loop())
        return

    # One-time emote
    selected = next((e for e in emote_list if lower_msg in [alias.lower() for alias in e[0]]), None)
    if selected:
        _, emote_id, _ = selected
        await self.highrise.send_emote(emote_id, user.id)
