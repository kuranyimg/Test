import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition
from functions import json  # json يحتوي على bot_location و save_data
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

        # أمر حفظ موقع البوت
        if message.lower() == "!sbot" and user.username == "RayBM":
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        json.bot_location["x"] = pos.x
                        json.bot_location["y"] = pos.y
                        json.bot_location["z"] = pos.z
                        json.bot_location["facing"] = pos.facing
                        await self.highrise.send_whisper(user.id, f"تم حفظ موقع البوت: {json.bot_location}")
                        break
            except Exception as e:
                print("Set bot error:", e)
                await self.highrise.send_whisper(user.id, "حدث خطأ أثناء حفظ موقع البوت.")

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
