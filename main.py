import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition

# استيراد وظائف الـ VIP من vip_manager
from functions.vip_manager import VIPManager
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.vip_manager = VIPManager()  # إنشاء مدير الـ VIP
        self.user_loops = {}  # لتخزين حالة التكرار لكل مستخدم

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str):
        print(f"[CHAT] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

        # تحقق من الرسائل المتعلقة بالنقل
        if message.startswith("-floor1") or message.startswith("!floor1") or message.startswith("-floor 1") or message.startswith("Floor 1") or message.startswith("Floor1") or message.startswith("/floor1") or message.startswith("floor1") or message.startswith("-1") or message.startswith("floor1") or message.startswith("f1") or message.startswith("f 1") or message.startswith("floor1") or message.startswith("F1") or message.startswith("floor 1") or message.startswith("!floor 1"):
            await self.highrise.teleport(user.id, Position(9.5 , 0.0 , 16.5))
        
        elif message.startswith("-floor3") or message.startswith("!floor3") or message.startswith("-floor 3") or message.startswith("Floor 3") or message.startswith("Floor3") or message.startswith("/floor3") or message.startswith("floor3") or message.startswith("-3") or message.startswith("floor3") or message.startswith("f3") or message.startswith("f 3") or message.startswith("floor3") or message.startswith("F3") or message.startswith("floor 3") or message.startswith("!floor 3"):
            await self.highrise.teleport(user.id, Position(12.5 , 19.25 , 6.5))

        elif message.startswith("-floor4") or message.startswith("!floor4") or message.startswith("-floor 4") or message.startswith("Floor 4") or message.startswith("Floor4") or message.startswith("/floor4") or message.startswith("floor4") or message.startswith("-4") or message.startswith("floor4") or message.startswith("f4") or message.startswith("f 4") or message.startswith("floor4") or message.startswith("F4") or message.startswith("floor 4") or message.startswith("!floor 4"):
            if self.vip_manager.is_vip(user.id):  # تحقق من إذا كان المستخدم VIP
                await self.highrise.teleport(user.id, Position(14.5 , 20.0 , 1.5))
            else:
                await self.highrise.send_message(user.id, "You must be a VIP to teleport to floor 4.")

        elif message.startswith("-floor2") or message.startswith("!floor2") or message.startswith("-floor 2") or message.startswith("Floor 2") or message.startswith("Floor2") or message.startswith("/floor2") or message.startswith("floor2") or message.startswith("-2") or message.startswith("floor2") or message.startswith("f2") or message.startswith("f 2") or message.startswith("floor2") or message.startswith("F2") or message.startswith("floor 2") or message.startswith("!floor 2"):
            await self.highrise.teleport(user.id, Position(14.5 , 9.0 , 6.0))

    async def on_whisper(self, user: User, message: str):
        print(f"[WHISPER] {user.username}: {message}")
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user, pos)

    async def on_stop(self):
        print("Bot stopped.")
