import asyncio
import random
import os
import importlib.util
from highrise import BaseBot, Position, Highrise  # ← أضف Highrise هنا
from highrise.models import SessionMetadata, Position, User, AnchorPosition
from functions.vip_manager import is_vip, handle_vip_command, get_vip_list
from functions.commands import is_teleport_command, handle_teleport_command
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement
import logging

# إعدادات اللوق
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}  # user.id -> {paused, emote_id, duration, task}
        print("Bot is initializing...")

    async def on_start(self, highrise):
        self.highrise = highrise
        print("Bot is ready.")
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))
        logger.info("Bot moved to starting position.")

    async def on_chat(self, user: User, message: str):
        try:
            await check_and_start_emote_loop(self, user, message)
        except Exception as e:
            logger.error(f"Chat error: {e}")

    async def on_whisper(self, user: User, message: str):
        try:
            await check_and_start_emote_loop(self, user, message)
        except Exception as e:
            logger.error(f"Whisper error: {e}")

    async def on_user_move(self, user: User, pos: Position):
        try:
            await handle_user_movement(self, user, pos)
        except Exception as e:
            logger.error(f"Move error: {e}")
