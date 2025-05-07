import asyncio
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, AnchorPosition
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.user_loops = {}
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str) -> None:
        await check_and_start_emote_loop(self, user, message)

    async def on_whisper(self, user: User, message: str) -> None:
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        await handle_user_movement(self, user)
