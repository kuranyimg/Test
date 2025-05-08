import asyncio
import json
import os
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition

# استيراد وظائف VIP و Loop Emote
from functions.vip_manager import VIPManager
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.vip_manager = VIPManager()
        self.user_loops = {}
        self.bot_position_file = "functions/bot_position.json"
        self.saved_position = self.load_bot_position()

    def load_bot_position(self):
        if os.path.exists(self.bot_position_file):
            with open(self.bot_position_file, "r") as f:
                data = json.load(f)
                return Position(data["x"], data["y"], data["z"], data["facing"])
        return Position(17.5, 0.0, 12.5, "FrontRight")

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await self.highrise.walk_to(self.saved_position)
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str):
        print(f"[CHAT] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

        # أوامر التنقل بين الطوابق
        if message.lower() in ["-floor1", "!floor1", "-floor 1", "floor 1", "floor1", "/floor1", "-1", "f1", "f 1", "f 1", "f1", "!floor 1"]:
            await self.highrise.teleport(user.id, Position(9.5 , 0.0 , 16.5))

        elif message.lower() in ["-floor2", "!floor2", "-floor 2", "floor 2", "floor2", "/floor2", "-2", "f2", "f 2", "f2", "!floor 2"]:
            await self.highrise.teleport(user.id, Position(14.5 , 9.0 , 6.0))

        elif message.lower() in ["-floor3", "!floor3", "-floor 3", "floor 3", "floor3", "/floor3", "-3", "f3", "f 3", "f3", "!floor 3"]:
            await self.highrise.teleport(user.id, Position(12.5 , 19.25 , 6.5))

        elif message.lower() in ["-floor4", "!floor4", "-floor 4", "floor 4", "floor4", "/floor4", "-4", "f4", "f 4", "f4", "!floor 4"]:
            if self.vip_manager.is_vip(user.id):
                await self.highrise.teleport(user.id, Position(14.5 , 20.0 , 1.5))
            else:
                await self.highrise.send_message(user.id, "You must be a VIP to teleport to floor 4.")

        # أمر حفظ موقع البوت
        elif message.lower() == "!sbot" and user.username == "RayBM":
            pos = await self.highrise.get_position(user.id)
            self.saved_position = pos
            with open(self.bot_position_file, "w") as f:
                json.dump({
                    "x": pos.x,
                    "y": pos.y,
                    "z": pos.z,
                    "facing": pos.facing
                }, f)
            await self.highrise.send_message(user.id, "تم حفظ موقع البوت بنجاح!")

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
