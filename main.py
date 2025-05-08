import asyncio
from highrise import Highrise, BaseBot
from highrise.models import User, Position
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}  # key: user.id, value: { stop_event, pause_event, task }
        self.running_tasks = []  # Keep track of tasks
        print("Bot is initializing...")

    async def on_start(self, highrise: Highrise):
        self.highrise = highrise
        print("Bot is ready.")
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))
        logger.info("Bot is walking to initial position")

    async def on_chat(self, user: User, message: str):
        try:
            await check_and_start_emote_loop(self, user, message)
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")

    async def on_whisper(self, user: User, message: str):
        try:
            await check_and_start_emote_loop(self, user, message)
        except Exception as e:
            logger.error(f"Error processing whisper message: {e}")

    async def on_user_move(self, user: User, pos: Position):
        try:
            await handle_user_movement(self, user)
        except Exception as e:
            logger.error(f"Error processing user move: {e}")

    async def on_stop(self):
        # Properly handle task cancellation and shutdown
        for task in self.running_tasks:
            task.cancel()
        logger.info("All tasks are being canceled")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
