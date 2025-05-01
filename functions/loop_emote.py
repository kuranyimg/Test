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

# Store active loops per user
user_loops: dict[str, asyncio.Task] = {}

async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    cleaned_msg = message.strip().lower()

    # STOP commands
    if any(cleaned_msg == prefix for prefix in ("stop", "Stop", "/stop", "!stop", "-stop")):
        if user.id in user_loops:
            user_loops[user.id].cancel()
            del user_loops[user.id]
            await self.highrise.send_whisper(user.id, "Your emote loop has been stopped.")
        else:
            await self.highrise.send_whisper(user.id, "You have no active emote loop.")
        return

    # LOOP commands
    loop_prefixes = ("loop ", "Loop ", "/loop ", "!loop ", "-loop ")
    if any(cleaned_msg.startswith(prefix.lower()) for prefix in loop_prefixes):
        emote_name = cleaned_msg.split(" ", 1)[1].strip()
        selected = next((e for e in emote_list if emote_name in [alias.lower() for alias in e[0]]), None)
        if not selected:
            await self.highrise.send_whisper(user.id, "Invalid emote name.")
            return

        # Cancel previous loop
        if user.id in user_loops:
            user_loops[user.id].cancel()

        aliases, emote_id, duration = selected
        display_name = aliases[0].capitalize()

        async def emote_loop():
            try:
                while True:
                    await self.highrise.send_emote(emote_id, user.id)
                    await asyncio.sleep(duration)
            except asyncio.CancelledError:
                pass

        task = asyncio.create_task(emote_loop())
        user_loops[user.id] = task

        await self.highrise.send_whisper(user.id, f"You are now looping the emote: **{display_name}**.\nType `stop` to stop.")
        return

    # One-time emote by direct name
    selected = next((e for e in emote_list if cleaned_msg in [alias.lower() for alias in e[0]]), None)
    if selected:
        _, emote_id, _ = selected
        await self.highrise.send_emote(emote_id, user.id)
