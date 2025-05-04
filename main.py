import asyncio
from highrise import BaseBot, Position
from highrise.models import User

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.emote_dict = {
            "1": {"emote": "dance-macarena", "delay": 12.5},
            "2": {"emote": "sit-relaxed", "delay": 29.9},
            "3": {"emote": "idle_layingdown", "delay": 24.6},
            "dance": {"emote": "dance-macarena", "delay": 12.5},
            "relaxed": {"emote": "sit-relaxed", "delay": 29.9},
            "attentive": {"emote": "idle_layingdown", "delay": 24.6}
        }
        self.user_loops = {}

    async def send_emote_loop(self, emote_data, user_id):
        try:
            while user_id in self.user_loops:
                await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[ERROR] send_emote_loop: {e}")

    async def stop_loop(self, user: User):
        if user.user_id in self.user_loops:
            loop_task = self.user_loops[user.user_id]["loop"]
            loop_task.cancel()
            del self.user_loops[user.user_id]
            await self.highrise.chat(f"{user.username}, loop stopped.")

    async def start_loop(self, user: User, emote_key: str):
        emote_data = self.emote_dict.get(emote_key.lower())
        if emote_data:
            await self.stop_loop(user)
            task = asyncio.create_task(self.send_emote_loop(emote_data, user.user_id))
            self.user_loops[user.user_id] = {
                "command": emote_data,
                "loop": task,
                "moving": False
            }
            await self.highrise.chat(f"{user.username}, looping: {emote_key}")
        else:
            await self.highrise.chat(f"Unknown emote: {emote_key}")

    async def do_emote_once(self, user: User, emote_key: str):
        emote_data = self.emote_dict.get(emote_key.lower())
        if emote_data:
            await self.highrise.send_emote(emote_data["emote"], user.user_id)
        else:
            await self.highrise.chat(f"Unknown emote: {emote_key}")

    async def handle_message(self, user: User, message: str):
        msg = message.strip()
        msg_lower = msg.lower()

        if msg_lower == "stop":
            await self.stop_loop(user)
            return

        for prefix in ["loop ", "!loop ", "-loop ", "Loop "]:
            if msg_lower.startswith(prefix):
                emote_key = msg[len(prefix):].strip()
                await self.start_loop(user, emote_key)
                return

        # If just emote name or number
        await self.do_emote_once(user, msg)

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        await self.handle_message(user, message)

    async def on_chat(self, user: User, message: str) -> None:
        print(f"[CHAT] {user.username}: {message}")
        await self.handle_message(user, message)

    async def on_position_update(self, user: User, position: Position) -> None:
        if user.user_id in self.user_loops:
            moving = position.is_moving
            loop_info = self.user_loops[user.user_id]
            was_moving = loop_info.get("moving", False)

            if moving and not was_moving:
                # User started moving -> pause
                loop_info["loop"].cancel()
                loop_info["moving"] = True

            elif not moving and was_moving:
                # User stopped moving -> resume
                task = asyncio.create_task(self.send_emote_loop(loop_info["command"], user.user_id))
                loop_info["loop"] = task
                loop_info["moving"] = False
