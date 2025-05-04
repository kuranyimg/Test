import random
from highrise import BaseBot, Position, Highrise
from highrise.models import SessionMetadata, User, AnchorPosition
from functions.loop_emote import check_and_start_emote_loop, handle_loop_command, start_emote_loop, emote_list
from functions.state import user_loops
from functions.vip_data import init_vip_db
from functions.vip_manager import is_vip, handle_vip_command, get_vip_list
from functions.commands import is_teleport_command, handle_teleport_command
import math

def positions_are_close(pos1, pos2, tolerance=0.1):
    return math.isclose(pos1.x, pos2.x, abs_tol=tolerance) and \
           math.isclose(pos1.y, pos2.y, abs_tol=tolerance) and \
           math.isclose(pos1.z, pos2.z, abs_tol=tolerance)

last_positions = {}  # add this near the top of main.py (global dictionary)


# تهيئة قاعدة بيانات الـ VIP
vip_list = init_vip_db()

class Bot(BaseBot):

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        try:
            print("Bot started.")
            await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))
        except Exception as e:
            print(f"Error on bot start: {e}")

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            print(f"{user.username} joined the room.")
            await self.highrise.chat(f"{user.username} joined!")
            await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
            await self.highrise.send_whisper(user.id, "❤️Use: [/help] for more information.")
            await self.highrise.send_whisper(user.id, "❤Type F3 F2 and F1 to teleport between the floor 🤍.")
            await self.highrise.send_emote("dance-hipshake")
            await self.highrise.send_emote("emote-lust", user.id)
            await self.highrise.react("heart", user.id)
        except Exception as e:
            print(f"Error on user join: {e}")

    async def on_user_move(self, user: User, position: Position):
        try:
            if user.username in user_loops:
                last_pos = last_positions.get(user.username)

                if last_pos and positions_are_close(position, last_pos):
                    # المستخدم توقف عن المشي - استئناف التكرار إذا كان متوقف مؤقتًا
                    loop_data = user_loops[user.username]
                    if loop_data.get("paused"):
                        loop_data["paused"] = False
                        emote_name = loop_data["emote_name"]
                        duration = next((d for aliases, e, d in emote_list if e == emote_name), None)
                        if duration:
                            await start_emote_loop(self, user, emote_name, duration)
                else:
                    # المستخدم يتحرك - توقيف التكرار مؤقتًا
                    user_loops[user.username]["paused"] = True

                # تحديث آخر موقع للمستخدم
                last_positions[user.username] = position
        except Exception as e:
            print(f"Error on user move: {e}")
    
    async def on_chat(self, user: User, message: str) -> None:
        try:
            username = user.username.lower()
            is_owner = username == "raybm"

            # VIP management
            if message.lower().startswith(("vip@", "unvip@")):
                if is_owner:
                    response = await handle_vip_command(user, message, vip_list)
                else:
                    response = f"Sorry {user.username}, only the bot owner can manage VIPs."
                await self.highrise.chat(response)
                return

            if is_teleport_command(message) or message.lower().startswith(("tele ", "summon ", "tele@", "summon@")):
                if is_owner or is_vip(username, vip_list):
                    await handle_teleport_command(user, message, self.highrise.send_whisper)
                else:
                    await self.highrise.chat(f"Sorry {user.username}, this command is for VIPs only.")
                return

            if message.lower().lstrip("!/ -").strip() == "viplist":
                await self.highrise.send_whisper(user.id, get_vip_list(vip_list))
                return

            if message.lower().startswith(("loop", "/loop", "!loop", "-loop")):
                class Msg:
                    content = message
                    author = user
                await handle_loop_command(self, Msg())
                return

            for aliases, emote, _ in emote_list:
                if message.lower() in aliases:
                    await self.highrise.send_emote(emote, user.id)
                    return

            await check_and_start_emote_loop(self, user, message)

            floors = {
                "floor1": Position(9.5, 0.0, 16.5),
                "floor2": Position(14.5, 9.0, 6.0),
                "floor3": Position(12.5, 19.25, 6.5),
                "floor4": Position(14.5, 20.0, 1.5),
            }
            for floor, pos in floors.items():
                if message.lower().startswith((f"-{floor}", f"!{floor}", f"/{floor}", floor)):
                    await self.highrise.teleport(user.id, pos)
                    return

            if message.lower().startswith(("!lista", "!emote list", "!list", "/lista", "/emote list", "/list")):
                from functions.commands import emote_list as command_list
                for group in command_list:
                    await self.highrise.send_whisper(user.id, group)
                return

            if message.lower().startswith(("!emoteall", "/emoteall")):
                await self.highrise.send_emote("dance-floss")
                return

            if message.lower().startswith(("-help", "/help", "!help")):
                await self.highrise.chat(f"/lista | /pessoas | /emotes | /marry me? | /play /fish /userinfo @ | !emoteall | !tele @ | !summon @ | !kick @ | !tele z,y,x | !tele @ z,y,x")
                await self.highrise.chat(f"[Emote] All | !emote all [Emote]")
                await self.highrise.chat(f"{user.username}, all commands must start with ! or /")
                await self.highrise.send_emote("dance-floss")
                return

            if message.lower().startswith(("!tp", "/tp", "tele")):
                target_username = message.split("@")[-1].strip()
                await self.teleport_to_user(user, target_username)
                return

            if message.lower().startswith(("summon", "!summon", "/summon")):
                if user.username in ["FallonXOXO", "Its.Melly.Moo.XoXo", "Shaun_Knox", "sh1n1gam1699", "Dreamy._.KY", "hidinurbasement", "@emping", "_irii_", "RayBM"]:
                    target_username = message.split("@")[-1].strip()
                    await self.teleport_user_next_to(target_username, user)
                return

            if message.lower().startswith("!kick"):
                if user.username not in ["FallonXOXO", "RayBM"]:
                    await self.highrise.chat("🤍.")
                    return
                await self.handle_kick_command(message)

        except Exception as e:
            print(f"Error in on_chat: {e}")

    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Teleport error: {e}")

    async def teleport_to_user(self, user: User, target_username: str):
        try:
            users = (await self.highrise.get_room_users()).content
            for target, pos in users:
                if target.username.lower() == target_username.lower():
                    await self.teleport(user, Position(pos.x, pos.y, pos.z - 1, pos.facing))
                    return
        except Exception as e:
            print(f"Teleport to user error: {e}")

    async def teleport_user_next_to(self, target_username: str, requester: User):
        try:
            users = (await self.highrise.get_room_users()).content
            req_pos = next(pos for u, pos in users if u.id == requester.id)
            for u, pos in users:
                if u.username.lower() == target_username.lower():
                    await self.teleport(u, Position(req_pos.x, req_pos.y, req_pos.z + 1, req_pos.facing))
                    return
        except Exception as e:
            print(f"Summon error: {e}")

    async def handle_kick_command(self, message: str):
        try:
            parts = message.split()
            if len(parts) != 2 or "@" not in parts[1]:
                await self.highrise.chat("🤍.")
                return

            username = parts[1][1:]
            users = (await self.highrise.get_room_users()).content
            user_to_kick = next((u for u, _ in users if u.username.lower() == username.lower()), None)

            if not user_to_kick:
                await self.highrise.chat("User not found.")
                return

            await self.highrise.moderate_room(user_to_kick.id, "kick")
            await self.highrise.chat(f"{username} has been banned from the room!")
        except Exception as e:
            await self.highrise.chat(str(e))
