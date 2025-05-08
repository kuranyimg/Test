import asyncio
import json
import os
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition

from functions.loop_emote import check_and_start_emote_loop, handle_user_movement

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}  # لتخزين حالة التكرار لكل مستخدم
        self.bot_position_file = "functions/bot_position.json"
        self.saved_position = self.load_bot_position()

    def load_bot_position(self):
        try:
            if os.path.exists(self.bot_position_file):
                with open(self.bot_position_file, "r") as f:
                    data = json.load(f)
                    return Position(data["x"], data["y"], data["z"], data["facing"])
        except Exception as e:
            print("Failed to load bot position:", e)

        # الموقع الافتراضي
        return Position(17.5, 0.0, 12.5, "FrontRight")

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await self.highrise.walk_to(self.saved_position)
        print("Bot is ready and moved to saved position.")

    async def on_chat(self, user: User, message: str):
        print(f"[CHAT] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

        # أمر حفظ مكان البوت
        if message.lower() == "!sbot" and user.username == "RayBM":
            try:
                pos = await self.highrise.get_position(user.id)
                self.saved_position = pos
                with open(self.bot_position_file, "w") as f:
                    json.dump({
                        "x": pos.x,
                        "y": pos.y,
                        "z": pos.z,
                        "facing": pos.facing
                    }, f)
                await self.highrise.send_message(user.id, "تم حفظ موقع البوت بنجاح.")
            except Exception as e:
                print("Error saving bot position:", e)
                await self.highrise.send_message(user.id, "حدث خطأ أثناء حفظ الموقع.")

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
