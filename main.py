import asyncio
from highrise import BaseBot, Position
from highrise.models import User

class Bot(BaseBot):
    emote_dict = {
        "1": {"emote": "dance-macarena", "delay": 12.5},
        "2": {"emote": "sit-relaxed", "delay": 29.9},
        "3": {"emote": "idle_layingdown", "delay": 24.6},
        "dance": {"emote": "dance-macarena", "delay": 12.5},
        "relaxed": {"emote": "sit-relaxed", "delay": 29.9},
        "attentive": {"emote": "idle_layingdown", "delay": 24.6}
    }

    user_loops = {}

    async def send_emote_loop(self, emote_data, user_id):
        try:
            while user_id in self.user_loops:
                await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[ERROR] send_emote_loop: {e}")
            self.user_loops.pop(user_id, None)

    async def stop_loop(self, user: User):
        if user.user_id in self.user_loops:
            self.user_loops[user.user_id]['loop'].cancel()
            self.user_loops.pop(user.user_id, None)
            await self.highrise.chat(f"{user.username}, loop stopped.")

    async def start_loop(self, user: User, emote_key: str):
        emote_data = self.emote_dict.get(emote_key.lower())
        if emote_data:
            if user.user_id in self.user_loops:
                await self.stop_loop(user)
            task = asyncio.create_task(self.send_emote_loop(emote_data, user.user_id))
            self.user_loops[user.user_id] = {'command': emote_data, 'loop': task}
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

        if msg_lower in ["stop"]:
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
        if user.user_id in self.user_loops and not position.is_moving:
            current = self.user_loops[user.user_id]
            task = asyncio.create_task(self.send_emote_loop(current['command'], user.user_id))
            self.user_loops[user.user_id]['loop'] = task
