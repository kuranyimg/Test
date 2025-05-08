import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition

from functions.loop_emote import check_and_start_emote_loop, handle_user_movement
from functions.json import bot_location, floor1_location, floor2_location, floor3_location, save_data


class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        if bot_location:
            try:
                await self.highrise.walk_to(Position(**bot_location))
                print("Bot moved to saved position.")
            except Exception as e:
                print("Error moving to saved position:", e)
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.lower().replace(" ", "")
        print(f"[CHAT] {user.username}: {message}")

        # حفظ موقع البوت
        if message == "!sbot" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        bot_location.update(x=pos.x, y=pos.y, z=pos.z, facing=pos.facing)
                        save_data()
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع البوت: {bot_location}")
                        break
            except Exception as e:
                print("Set bot error:", e)

        # يمشي إلى موقع البوت
        elif message == "!base" and user.username == "RayBM":
            try:
                if bot_location:
                    await self.highrise.walk_to(Position(**bot_location))
            except Exception as e:
                print("Error in !base:", e)

        # حفظ مواقع الطوابق
        elif message == "!sfloor1" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        floor1_location.update(x=pos.x, y=pos.y, z=pos.z, facing=pos.facing)
                        save_data()
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع Floor 1: {floor1_location}")
                        break
            except Exception as e:
                print("sfloor1 error:", e)

        elif message == "!sfloor2" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        floor2_location.update(x=pos.x, y=pos.y, z=pos.z, facing=pos.facing)
                        save_data()
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع Floor 2: {floor2_location}")
                        break
            except Exception as e:
                print("sfloor2 error:", e)

        elif message == "!sfloor3" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        floor3_location.update(x=pos.x, y=pos.y, z=pos.z, facing=pos.facing)
                        save_data()
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع Floor 3: {floor3_location}")
                        break
            except Exception as e:
                print("sfloor3 error:", e)

        # التنقل للطوابق
        elif msg in ("!floor1", "floor1", "f1", "-1") and floor1_location:
            await self.highrise.teleport(user.id, Position(**floor1_location))

        elif msg in ("!floor2", "floor2", "f2", "-2") and floor2_location:
            await self.highrise.teleport(user.id, Position(**floor2_location))

        elif msg in ("!floor3", "floor3", "f3", "-3") and floor3_location:
            await self.highrise.teleport(user.id, Position(**floor3_location))

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
