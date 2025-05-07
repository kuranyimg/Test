import asyncio
from highrise import Highrise, BaseBot
from highrise.models import User, Position
from functions.loop_emote import check_and_start_emote_loop, handle_user_movement

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.user_loops = {}  # key: user.id, value: { stop_event, pause_event, task }

    async def on_start(self, highrise: Highrise):
        self.highrise = highrise
        print("Bot is ready.")

    async def on_chat(self, user: User, message: str):
        await check_and_start_emote_loop(self, user, message)

    async def on_whisper(self, user: User, message: str):
        await check_and_start_emote_loop(self, user, message)

    async def on_user_move(self, user: User, pos: Position):
        await handle_user_movement(self, user)

if __name__ == "__main__":
    MyBot().run()
