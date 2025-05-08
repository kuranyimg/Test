import logging
from highrise import BaseBot, Highrise
from highrise.models import Position, User
from loop_emote import check_and_start_emote_loop, handle_user_movement

logging.basicConfig(level=logging.INFO)

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}  # user.id -> {stop_event, pause_event, task}

    async def on_start(self, highrise: Highrise):
        self.highrise = highrise
        logging.info("Bot is ready.")
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))

    async def on_chat(self, user: User, message: str):
        await check_and_start_emote_loop(self, user, message)

    async def on_whisper(self, user: User, message: str):
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position):
        await handle_user_movement(self, user)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
