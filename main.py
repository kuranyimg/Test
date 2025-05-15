import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition

from functions.loop_emote import check_and_start_emote_loop, handle_user_movement, emote_list
from functions.json import bot_location
from functions.data_store import add_mod, is_mod, add_vip, is_vip, save_floor, get_floor
from functions.loop_emote import (
    check_and_start_emote_loop,
    handle_user_movement,
    emote_list,
    start_loop_for_user,
    stop_loop_for_user,
    load_bot_loop,
    save_bot_loop
)
from functions.json import bot_location
from functions.data_store import add_mod, is_mod, add_vip, is_vip, save_floor, get_floor

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}
        self.loop_emote_list = emote_list
        self.bot_loop = load_bot_loop()  # تحميل إيموت البوت المحفوظ

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        if bot_location:
            try:
                await self.highrise.walk_to(Position(**bot_location))
                print("Bot moved to saved position.")
            except Exception as e:
                print("Error moving to saved position:", e)

        # تشغيل إيموت البوت المحفوظ تلقائياً
        if self.bot_loop:
            await start_loop_for_user(self, self.user, self.bot_loop)
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        print(f"[CHAT] {user.username}: {message}")

        # عرض قائمة الإيموتات
        if msg in ("emotelist", "emoteslist", "!emotes", "/emotes", "!emote", "/emote", "emotes", "emote"):
            try:
                emote_names = [aliases[0] for aliases, _, _ in self.loop_emote_list]
                emote_text = "Available Emotes:\n" + "\n".join(f"- {name}" for name in emote_names)
                await self.highrise.send_whisper(user.id, emote_text)
            except Exception as e:
                print("Error sending emote list:", e)
            return

        # بدء إيموت بالهمس أو كتابة الاسم مباشرة
        await check_and_start_emote_loop(self, user, message)

        # أوامر الإدارية (Mod & VIP)
        if message.startswith("!mod ") and user.username == "RayBM":
            target = message[5:].strip().lstrip("@")
            add_mod(target)
            await self.highrise.send_whisper(user.id, f"تمت إضافة {target} كمشرف.")
            return

        if message.startswith("!vip ") and user.username == "RayBM":
            target = message[5:].strip().lstrip("@")
            add_vip(target)
            await self.highrise.send_whisper(user.id, f"تمت إضافة {target} إلى قائمة VIP.")
            return

        # summon@username
        if msg.startswith(("summon@", "summon @")) and is_mod(user.username):
            target = message.split("@")[-1].strip()
            users = await self.highrise.get_room_users()
            for room_user, pos in users.content:
                if room_user.username.lower() == target.lower():
                    await self.highrise.walk_to(pos)
                    await self.highrise.send_whisper(user.id, f"تم نقل البوت إلى {target}.")
                    return

        # tele@username
        if msg.startswith(("tele@", "tele @")) and is_mod(user.username):
            target = message.split("@")[-1].strip()
            users = await self.highrise.get_room_users()
            bot_pos = None
            for room_user, pos in users.content:
                if room_user.username == self.user.username:
                    bot_pos = pos
            for room_user, _ in users.content:
                if room_user.username.lower() == target.lower() and bot_pos:
                    await self.highrise.teleport(room_user.id, bot_pos)
                    await self.highrise.send_whisper(user.id, f"تم نقل {target} إلى موقع البوت.")
                    return

        # حفظ موقع البوت
        if msg == "!sbot" and user.username == "RayBM":
            users = await self.highrise.get_room_users()
            for room_user, pos in users.content:
                if room_user.username == user.username:
                    bot_location["x"] = pos.x
                    bot_location["y"] = pos.y
                    bot_location["z"] = pos.z
                    bot_location["facing"] = pos.facing
                    await self.highrise.send_whisper(user.id, f"تم حفظ موقع البوت.")
                    return

        # العودة لموقع البوت
        if msg == "!base" and is_mod(user.username):
            if bot_location:
                await self.highrise.walk_to(Position(**bot_location))
                return

        # حفظ موقع الطابق
        if msg.startswith("!setfloor") and is_mod(user.username):
            parts = message.lower().split()
            if len(parts) >= 2 and parts[1] in ("1", "2", "3"):
                floor_num = parts[1]
                users = await self.highrise.get_room_users()
                for room_user, pos in users.content:
                    if room_user.username == self.user.username:
                        save_floor(floor_num, pos)
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع الطابق {floor_num}.")
                        return

        # أوامر الطوابق
        msg = msg.replace(" ", "")
        if msg in ("-floor1", "!floor1", "floor1", "/floor1", "f1", "-1"):
            pos = get_floor("1")
            if pos:
                await self.highrise.teleport(user.id, Position(**pos))
        elif msg in ("-floor2", "!floor2", "floor2", "/floor2", "f2", "-2"):
            pos = get_floor("2")
            if pos:
                await self.highrise.teleport(user.id, Position(**pos))
        elif msg in ("-floor3", "!floor3", "floor3", "/floor3", "f3", "-3"):
            pos = get_floor("3")
            if pos:
                await self.highrise.teleport(user.id, Position(**pos))

        # تكرار إيموت لمستخدم آخر
        if msg.startswith("!loop "):
            parts = message.split()
            if len(parts) == 3 and is_mod(user.username):
                target_user = parts[1].lower()
                emote = parts[2].lower()

                if target_user == "bot":
                    await start_loop_for_user(self, self.user, emote)
                    save_bot_loop(emote)
                    await self.highrise.send_whisper(user.id, f"تم تشغيل الإيموت {emote} للبوت.")
                    return

                users = await self.highrise.get_room_users()
                for room_user, _ in users.content:
                    if room_user.username.lower() == target_user:
                        await start_loop_for_user(self, room_user, emote)
                        await self.highrise.send_whisper(user.id, f"تم تشغيل الإيموت {emote} لـ {target_user}.")
                        return
                await self.highrise.send_whisper(user.id, f"المستخدم {target_user} غير موجود.")
                return

        if msg == "stop":
            await stop_loop_for_user(self, user)

    async def on_whisper(self, user: User, message: str):
        msg = message.lower().strip()
        print(f"[WHISPER] {user.username}: {message}")

        if msg in ("emotelist", "emoteslist", "!emotes", "/emotes", "emotes", "emote"):
            try:
                emote_names = [aliases[0] for aliases, _, _ in self.loop_emote_list]
                emote_text = "Available Emotes:\n" + "\n".join(f"- {name}" for name in emote_names)
                await self.highrise.send_whisper(user.id, emote_text)
            except Exception as e:
                print("Error sending emote list whisper:", e)
            return

        # تنفيذ إيموت عبر الهمس
        await check_and_start_emote_loop(self, user, message)

        # إيقاف إيموت البوت بالهمس
        if msg == "stop" and user.username == "RayBM":
            await stop_loop_for_user(self, self.user)
            save_bot_loop("")  # حذف الحفظ
            await self.highrise.send_whisper(user.id, "تم إيقاف إيموت البوت.")

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_user_leave(self, user: User) -> None:
        await stop_loop_for_user(self, user)

    async def on_stop(self):
        print("Bot stopped.")
