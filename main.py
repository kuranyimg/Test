import asyncio
import time
import traceback
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition
from functions.loop_emote import (
    check_and_start_emote_loop,
    handle_user_movement,
    handle_bot_emote_loop,
    emote_list,
    load_bot_loop
)
from functions.data_store import load_bot_location, save_bot_location
from functions.floors import floor_locations, set_floor
from functions import leaderboard as lb

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}
        self.loop_emote_list = emote_list
        self.join_timestamps = {}
        self.ignored_bots = ["MonsterBeat", "MonsterBud"]
        self.bot_location = load_bot_location() or {}
        self.user_enter_time = {}
        # Start with you as the initial bot owner
        self.bot_owners = ["RayBM"]
        self.leaderboard_data = lb.load_leaderboard_data()

        self.leaderboard_cycle = [
            "most_active",
            "most_talkative",
            "most_daily_streak",
            "most_stayed",
            "all_time"
        ]
        self.current_cycle_index = 0

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        try:
            if self.bot_location:
                await self.highrise.walk_to(Position(**self.bot_location))
            load_bot_loop()
            asyncio.create_task(self.periodic_leaderboard_display())
        except Exception:
            traceback.print_exc()
        print("Bot ready ✅")

    async def periodic_leaderboard_display(self):
        await asyncio.sleep(15)
        while True:
            try:
                key = self.leaderboard_cycle[self.current_cycle_index]
                self.current_cycle_index = (self.current_cycle_index + 1) % len(self.leaderboard_cycle)
                leaderboard_text = lb.get_leaderboard_text_by_choice(self.leaderboard_data, key)
                if leaderboard_text:
                    chunks = []
                    chunk = ""
                    for line in leaderboard_text.split("\n"):
                        if len(chunk) + len(line) + 1 > 450:
                            chunks.append(chunk.strip())
                            chunk = ""
                        chunk += line + "\n"
                    if chunk:
                        chunks.append(chunk.strip())

                    for msg in chunks:
                        await self.highrise.chat(msg)
                        await asyncio.sleep(1.5)

                await asyncio.sleep(300)  # every 5 minutes
            except Exception:
                traceback.print_exc()
                await asyncio.sleep(300)

    async def on_stop(self):
        lb.save_leaderboard_data(self.leaderboard_data)
        print("Bot stopped.")

    async def on_user_join(self, user: User, pos=None) -> None:
        try:
            if pos is not None:
                from functions.loop_emote import user_last_positions
                user_last_positions[user.id] = (pos.x, pos.y, pos.z)

            if user.username in self.ignored_bots or lb.is_user_removed(self.leaderboard_data, user.username):
                return

            self.user_enter_time[user.id] = time.time()
            lb.update_leaderboard_on_join(self.leaderboard_data, user.username)

            # Get the user's all_time rank
            lb.update_all_time(self.leaderboard_data)
            rank, _ = lb.get_user_rank_text(self.leaderboard_data, user.username, "all_time")

            # Compose the join message based on rank
            if rank == 1:
                join_msg = f"👑 @{user.username} The Ultimate #1 Legend! joined the room!"
            elif rank and 2 <= rank <= 10:
                join_msg = f"🔥 @{user.username} A Top 10 Legend! Rank #{rank} joined the room!"
            elif rank and 11 <= rank <= 100:
                join_msg = f"✨ @{user.username} A Top 100 Legend! Rank #{rank} joined the room!"
            elif rank and 101 <= rank <= 1000:
                join_msg = f"📊 @{user.username} joined the room! All-Time Legend Rank #{rank}"
            else:
                join_msg = f"👋 @{user.username} joined the room! Welcome!"

            await self.highrise.chat(join_msg)

            await self.highrise.send_whisper(
                user.id,
                "👋 Welcome! Type `leaderboard` to see top visitors.\n📌 Type `!rank` to see your top ranks."
            )
        except Exception:
            traceback.print_exc()

    async def on_user_move(self, user: User, pos: Position | AnchorPosition):
        try:
            await handle_user_movement(self, user, pos)
        except Exception:
            traceback.print_exc()

    async def on_chat(self, user: User, message: str):
        try:
            trigger = message.lower().replace(" ", "")

            if user.id in self.user_enter_time:
                entered = self.user_enter_time.pop(user.id)
                duration = time.time() - entered
                self.user_enter_time[user.id] = time.time()
                lb.update_leaderboard_on_chat(self.leaderboard_data, user.username, duration)

            lb.update_leaderboard_on_message(self.leaderboard_data, user.username)

            if message.startswith("/play ") and user.username not in self.ignored_bots:
                lb.update_leaderboard_on_play(self.leaderboard_data, user.username)

            if trigger in ("leaderboard", "!leaderboard"):
                lines = lb.get_leaderboard_menu_text().split("\n")
                chunk = ""
                for line in lines:
                    if len(chunk) + len(line) + 1 > 450:
                        await self.highrise.send_whisper(user.id, chunk.strip())
                        chunk = ""
                        await asyncio.sleep(0.3)
                    chunk += line + "\n"
                if chunk:
                    await self.highrise.send_whisper(user.id, chunk.strip())
                return

            if trigger.startswith("showleaderboard") or trigger.startswith("leaderboard"):
                choice = message.lower().replace("show leaderboard", "").replace("leaderboard", "").strip()
                if choice:
                    text = lb.get_leaderboard_text_by_choice(self.leaderboard_data, choice)
                    if text:
                        for chunk in chunked(text.split("\n"), 10):
                            await self.highrise.send_whisper(user.id, "\n".join(chunk))
                            await asyncio.sleep(0.3)
                    else:
                        await self.highrise.send_whisper(user.id, "❌ Invalid leaderboard type.")
                return

            if trigger.startswith("!rank"):
                text = lb.get_user_full_rank_summary(self.leaderboard_data, user.username)
                for chunk in chunked(text.split("\n"), 10):
                    await self.highrise.send_whisper(user.id, "\n".join(chunk))
                    await asyncio.sleep(0.3)
                return

            # Bot owner only commands check
            if user.username in self.bot_owners:

                if trigger.startswith("!resetlb"):
                    lb.reset_leaderboard(self.leaderboard_data)
                    await self.highrise.send_whisper(user.id, "✅ Leaderboard reset.")
                    return

                if trigger.startswith("!removelb"):
                    try:
                        _, username = message.split()
                        username = username.lstrip("@")
                        lb.remove_user_from_leaderboard(self.leaderboard_data, username)
                        await self.highrise.send_whisper(user.id, f"✅ Removed {username} from leaderboard.")
                    except:
                        await self.highrise.send_whisper(user.id, "❌ Usage: !removelb @username")
                    return

                if trigger.startswith("!unremovelb"):
                    try:
                        _, username = message.split()
                        username = username.lstrip("@")
                        lb.unremove_user_from_leaderboard(self.leaderboard_data, username)
                        await self.highrise.send_whisper(user.id, f"✅ {username} can now participate in leaderboard.")
                    except:
                        await self.highrise.send_whisper(user.id, "❌ Usage: !unremovelb @username")
                    return

                if trigger == "!removelist":
                    text = lb.get_removed_users_text(self.leaderboard_data)
                    await self.highrise.send_whisper(user.id, text)
                    return

                if trigger.startswith("!addo") or trigger.startswith("/addo"):
                    try:
                        _, new_owner = message.split()
                        new_owner = new_owner.lstrip("@")
                        if new_owner not in self.bot_owners:
                            self.bot_owners.append(new_owner)
                            await self.highrise.send_whisper(user.id, f"✅ {new_owner} added as owner.")
                    except:
                        await self.highrise.send_whisper(user.id, "❌ Usage: !addo @username")
                    return

                if trigger == "!listo":
                    msg = "🤖 Bot Owners:\n" + "\n".join(f"- {o}" for o in self.bot_owners)
                    await self.highrise.send_whisper(user.id, msg)
                    return

                if trigger.startswith("!remo"):
                    try:
                        _, target_owner = message.split()
                        target_owner = target_owner.lstrip("@")
                        if target_owner == "RayBM":
                            await self.highrise.send_whisper(user.id, "❌ You can't remove RayBM.")
                        elif target_owner in self.bot_owners:
                            self.bot_owners.remove(target_owner)
                            await self.highrise.send_whisper(user.id, f"✅ {target_owner} removed from owners.")
                    except:
                        await self.highrise.send_whisper(user.id, "❌ Usage: !remo @username")
                    return

                if trigger.startswith("!setf"):
                    floor_key = trigger.replace("!set", "")
                    room_users = await self.highrise.get_room_users()
                    for room_user, pos in room_users.content:
                        if room_user.username == user.username:
                            set_floor(floor_key, pos)
                            await self.highrise.send_whisper(user.id, f"✅ Saved floor {floor_key}")
                    return

                if message == "!sbot":
                    room_users = await self.highrise.get_room_users()
                    for room_user, pos in room_users.content:
                        if room_user.username == user.username:
                            self.bot_location.update(x=pos.x, y=pos.y, z=pos.z, facing=pos.facing)
                            save_bot_location(self.bot_location)
                            await self.highrise.send_whisper(user.id, f"📍 Bot location saved.")
                    return

            # General teleport commands
            if message == "!base" and self.bot_location:
                await self.highrise.walk_to(Position(**self.bot_location))

            if trigger in ("f1", "!floor1", "-1") and "f1" in floor_locations:
                await self.highrise.teleport(user.id, Position(**floor_locations["f1"]))
            elif trigger in ("f2", "!floor2", "-2") and "f2" in floor_locations:
                await self.highrise.teleport(user.id, Position(**floor_locations["f2"]))
            elif trigger in ("f3", "!floor3", "-3") and "f3" in floor_locations:
                await self.highrise.teleport(user.id, Position(**floor_locations["f3"]))

            if trigger == "!command" and user.username in self.bot_owners:
                commands = [
                    "📚 Available Bot Commands (For Owners Only):",
                    "🔹 !addo @username — Add new owner",
                    "🔹 !listo — List all bot owners",
                    "🔹 !remo @username — Remove owner (not RayBM)",
                    "🔹 !setf1/2/3 — Save floor positions",
                    "🔹 !sbot — Save bot location",
                    "🔹 !base — Move to base",
                    "🔹 f1 / f2 / f3 — Teleport to floor",
                    "🔹 leaderboard — Show leaderboard types",
                    "🔹 !rank — Show your multi-category rank summary",
                    "🔹 !resetlb — Reset leaderboard",
                    "🔹 !removelb @user — Block from leaderboard",
                    "🔹 !unremovelb @user — Unblock",
                    "🔹 !removelist — Show blocked users",
                    "🔹 Emote loops, !emotes, etc."
                ]
                for chunk in chunked(commands, 5):
                    await self.highrise.send_whisper(user.id, "\n".join(chunk))
                    await asyncio.sleep(0.5)
                return

            await check_and_start_emote_loop(self, user, message)

        except Exception:
            traceback.print_exc()

    async def on_whisper(self, user: User, message: str):
        try:
            trigger = message.lower().replace(" ", "")

            if user.username in self.bot_owners:
                await handle_bot_emote_loop(self, user, message)

            if user.username in self.bot_owners or user.username.lower() == "raybm":
                await check_and_start_emote_loop(self, user, message)

            if user.username in self.bot_owners:
                await self.highrise.chat(message)

            if trigger in (
                "emotelist", "emoteslist", "!emotes", "/emotes",
                "!emote", "/emote", "emotes", "emote", "emote list", "emotes list"
            ):
                names = [aliases[0] for aliases, _, _ in self.loop_emote_list]
                for idx, chunk in enumerate(chunked(names, 10), start=1):
                    txt = f"🎭 Emotes ({idx}/{(len(names)+9)//10}):\n" + "\n".join(f"- {n}" for n in chunk)
                    await self.highrise.send_whisper(user.id, txt)

        except Exception:
            traceback.print_exc()
