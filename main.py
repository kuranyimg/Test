import logging
from highrise import BaseBot, User, Position

from functions.loop_emote import (
    handle_loop_command,
    stop_emote_loop,
    handle_user_movement,
    handle_user_stopped
)

logging.basicConfig(level=logging.INFO)

class MyHighriseBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.owner = "raybm"

    async def on_start(self, session_metadata):
        logging.info("Bot started in room: %s", session_metadata.room_name)

    async def on_chat(self, user: User, message: str):
        msg = message.strip().lower()

        if msg == "stop":
            stop_emote_loop(user.id)
            return

        if any(msg.startswith(prefix) for prefix in ["loop", "/loop", "!loop", "-loop"]):
            await handle_loop_command(self, user, msg)
            return

        await handle_loop_command(self, user, msg)

    async def on_user_move(self, user: User, position: Position, direction: str):
        handle_user_movement(user.id)

    async def on_user_stop(self, user: User, position: Position):
        handle_user_stopped(user.id)
