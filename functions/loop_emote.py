import asyncio
import traceback
import json
import os
import random
from highrise import BaseBot
from highrise.models import User

# ملف لحفظ حالة loop البوت
BOT_LOOP_FILE = "bot_emote_loop.json"

emote_list: list[tuple[list[str], str, float]] = [
    (['rest', 'REST', 'Rest'], 'sit-idle-cute', 16.50),
    (['Kawaii Go Go', 'kawaii go go', '1'], 'dance-kawai', 10.85),
    (['Hyped', 'hyped', '2'], 'emote-hyped', 7.62),
    (['Levitate', 'levitate', '3'], 'emoji-halo', 6.52),
    (['Rest', 'rest', '4'], 'sit-idle-cute', 17.73),
    (['Hero Pose', 'hero pose', '5'], 'idle-hero', 22.33),
    (['Uhmmm', 'uhmmm', '6'], 'emote-thought', 27.43),
    (['Crouch', 'crouch', '7'], 'idle-crouched', 28.27),
    (['Zero Gravity', 'zero gravity', '8'], 'emote-astronaut', 13.93),
    (['Zombie Run', 'zombie run', '9'], 'emote-zombierun', 10.05),
    (['Wait', 'wait', '10'], 'dance-wait', 9.92),
    (['Dab', 'dab', '11'], 'emote-dab', 3.75),
    (['Ignition Boost', 'ignition boost', '12'], 'hcc-jetpack', 27.45),
    (['Do The Worm', 'do the worm', '13'], 'emote-snake', 6.63),
    (['Bummed', 'bummed', '14'], 'idle-loop-sad', 21.80),
    (['Chillin\'', 'chillin\'', '15'], 'idle-loop-happy', 19.80),
    (['Sweet Smooch', 'sweet smooch', '16'], 'emote-kissing', 6.69),
    (['Emoji Shush', 'emoji shush', '17'], 'emoji-shush', 3.40),
    (['Idle Tough', 'idle tough', '18'], 'idle_tough', 28.64),
    (['Emote Fail3', 'emote fail3', '19'], 'emote-fail3', 7.06),
    (['Emote Shocked', 'emote shocked', '20'], 'emote-shocked', 5.59),
    (['Emote Theatrical Test', 'emote theatrical test', '21'], 'emote-theatrical-test', 10.86),
    (['Emote Fireworks', 'emote fireworks', '22'], 'emote-fireworks', 13.15),
    (['Emote Electrified', 'emote electrified', '23'], 'emote-electrified', 5.29),
    (['Idle Headless', 'idle headless', '24'], 'idle-headless', 41.80),
    (['Emote Armcannon', 'emote armcannon', '25'], 'emote-armcannon', 8.67),
    (['Dance Tiktok4', 'dance tiktok4', '26'], 'dance-tiktok4', 15.00),
    (['Dance Tiktok7', 'dance tiktok7', '27'], 'dance-tiktok7', 13.89),
    (['Don\'t Touch Dance', 'don\'t touch dance', '28'], 'dance-tiktok13', 9.24),
    (['Hip Hop Dance', 'hip hop dance', '29'], 'dance-hiphop', 27.59),
    (['Emote Hopscotch', 'emote hopscotch', '30'], 'emote-hopscotch', 5.84),
]

user_last_positions = {}
# -----------------------------------------
# USER EMOTE LOOP
# -----------------------------------------
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    try:
        cleaned_msg = message.strip().lower()

        if cleaned_msg in ("stop", "/stop", "!stop", "-stop"):
            if user.id in self.user_loops:
                self.user_loops[user.id]["task"].cancel()
                del self.user_loops[user.id]
                await self.highrise.send_whisper(user.id, "Emote loop stopped. (Type any emote name or number to start again)")
            else:
                await self.highrise.send_whisper(user.id, "You don't have an active emote loop.")
            return

        selected = next((e for e in emote_list if cleaned_msg in [a.lower() for a in e[0]]), None)
        if selected:
            aliases, emote_id, duration = selected

            if user.id in self.user_loops:
                self.user_loops[user.id]["task"].cancel()

            async def emote_loop():
                try:
                    while True:
                        if not self.user_loops[user.id]["paused"]:
                            room_users = await self.highrise.get_room_users()
                            user_ids = [u.id for u, _ in room_users.content]
                            if user.id not in user_ids:
                                self.user_loops[user.id]["task"].cancel()
                                del self.user_loops[user.id]
                                return
                            await self.highrise.send_emote(emote_id, user.id)
                        await asyncio.sleep(duration)
                except asyncio.CancelledError:
                    pass
                except Exception:
                    traceback.print_exc()

            task = asyncio.create_task(emote_loop())
            self.user_loops[user.id] = {
                "paused": False,
                "emote_id": emote_id,
                "duration": duration,
                "task": task,
            }

            await self.highrise.send_whisper(
                user.id,
                f"You are now in a loop for emote number {aliases[0]}. (To stop, type 'stop')",
            )
    except Exception:
        traceback.print_exc()

# -----------------------------------------
# توقف واستئناف المستخدم عند الحركة
# -----------------------------------------
async def handle_user_movement(self: BaseBot, user: User, pos) -> None:
    try:
        if user.id not in self.user_loops:
            return
        old_pos = user_last_positions.get(user.id)
        user_last_positions[user.id] = (pos.x, pos.y, pos.z)

        if old_pos is None:
            return
        if old_pos != (pos.x, pos.y, pos.z):
            self.user_loops[user.id]["paused"] = True
            await asyncio.sleep(2)
            new_pos = user_last_positions.get(user.id)
            if new_pos == (pos.x, pos.y, pos.z):
                self.user_loops[user.id]["paused"] = False
    except Exception:
        traceback.print_exc()

# ================================================
# 👇 BOT EMOTE LOOP
# ================================================

loop_file_path = "functions/bot_emote_loop.json"
bot_loop_data = {
    "emotes": [],
    "mode": "order",  # or "random"
}
bot_loop_task = None

def save_bot_loop():
    with open(loop_file_path, "w") as f:
        json.dump(bot_loop_data, f)

def load_bot_loop():
    global bot_loop_data
    if os.path.exists(loop_file_path):
        try:
            with open(loop_file_path, "r") as f:
                bot_loop_data = json.load(f)
        except Exception:
            pass

async def handle_bot_emote_loop(self: BaseBot, user: User, message: str):
    global bot_loop_task
    msg = message.strip()
    lower = msg.lower()

    if lower in ("rest loop", "reset loop", "stop loop", "stop bot loop"):
        await stop_bot_emote_loop(self, user)
        return

    if lower == "loop list":
        if not bot_loop_data["emotes"]:
            await self.highrise.send_whisper(user.id, "Bot has no emotes saved.")
            return
        txt = "🤖 Bot Emote Loop:\n"
        for idx, emote in enumerate(bot_loop_data["emotes"], 1):
            txt += f"{idx}. {emote['emote_id']} - {emote['duration']:.1f}s\n"
        await self.highrise.send_whisper(user.id, txt)
        return

    if lower.startswith("loopr "):
        target = lower.replace("loopr", "").strip()
        removed = False
        for i, e in enumerate(bot_loop_data["emotes"]):
            if e["emote_id"] == target:
                bot_loop_data["emotes"].pop(i)
                removed = True
                break
        if removed:
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Removed emote: {target}")
        else:
            await self.highrise.send_whisper(user.id, f"❌ Emote not found: {target}")
        return

    if lower.startswith("loop mode "):
        mode = lower.replace("loop mode", "").strip()
        if mode in ("random", "order"):
            bot_loop_data["mode"] = mode
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Bot loop mode set to {mode}.")
        else:
            await self.highrise.send_whisper(user.id, "❌ Mode must be 'order' or 'random'.")
        return

    if lower.startswith("loop "):
        emote_name = lower.replace("loop", "").strip()
        selected = next((e for e in emote_list if emote_name in [a.lower() for a in e[0]]), None)
        if selected:
            _, emote_id, duration = selected
            bot_loop_data["emotes"].append({"emote_id": emote_id, "duration": duration})
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Bot will now loop: {emote_id}")
            if not bot_loop_task or bot_loop_task.done():
                bot_loop_task = asyncio.create_task(start_bot_loop(self))
        else:
            await self.highrise.send_whisper(user.id, f"❌ Emote not recognized: {emote_name}")

async def start_bot_loop(self: BaseBot):
    try:
        while True:
            if not bot_loop_data["emotes"]:
                await asyncio.sleep(5)
                continue

            if bot_loop_data["mode"] == "random":
                chosen = random.choice(bot_loop_data["emotes"])
                await self.highrise.send_emote(chosen["emote_id"])
                await asyncio.sleep(chosen["duration"])
            else:
                for emote in bot_loop_data["emotes"]:
                    await self.highrise.send_emote(emote["emote_id"])
                    await asyncio.sleep(emote["duration"])
    except asyncio.CancelledError:
        pass
    except Exception:
        traceback.print_exc()

async def stop_bot_emote_loop(self: BaseBot, user: User):
    global bot_loop_task
    if bot_loop_task and not bot_loop_task.done():
        bot_loop_task.cancel()
        bot_loop_task = None
        bot_loop_data["emotes"].clear()
        save_bot_loop()
        await self.highrise.send_whisper(user.id, "🛑 Bot emote loop stopped.")
    else:
        await self.highrise.send_whisper(user.id, "❌ No active bot loop to stop.")
