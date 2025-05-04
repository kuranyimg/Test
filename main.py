import asyncio
from highrise import BaseBot, Position
from highrise.models import User

class Bot(BaseBot):
    emote_dict = {
        "dance": {
            "emote": "dance-macarena",
            "delay": 12.5
        },
        "relaxed": {
            "emote": "sit-relaxed",
            "delay": 29.889858,
            "loop": False
        },
        "attentive": {
            "emote": "idle_layingdown",
            "delay": 24.585168,
            "loop": False
        }
    }

    user_loops = {}

    async def send_emote_continuously(self, emote_data: dict, user_id: int) -> None:
        try:
            while user_id in self.user_loops:
                await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"An error occurred in send_emote_continuously: {e}")
            self.user_loops.pop(user_id, None)

    async def start_loop_for_user(self, user: User, emote_name: str):
        command = self.emote_dict.get(emote_name)
        if command:
            loop_task = asyncio.create_task(self.send_emote_continuously(command, user.user_id))
            self.user_loops[user.user_id] = {'command': command, 'loop': loop_task}
            await self.highrise.chat(f"Started emote loop for {user.username}: {emote_name}")
        else:
            await self.highrise.chat(f"Emote '{emote_name}' not found.")

    async def stop_loop_for_user(self, user: User):
        loop_data = self.user_loops.get(user.user_id)
        if loop_data:
            loop_data['loop'].cancel()
            self.user_loops.pop(user.user_id, None)
            await self.highrise.chat(f"Stopped emote loop for {user.username}.")

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        message = message.strip().lower()

        if message in ["stop", "Stop"]:
            await self.stop_loop_for_user(user)

        elif any(message.startswith(prefix) for prefix in ["loop ", "Loop ", "!loop ", "-loop "]):
            parts = message.split()
            if len(parts) > 1:
                emote_name = parts[1].lower()
                if emote_name in self.emote_dict:
                    await self.start_loop_for_user(user, emote_name)
            else:
                await self.start_loop_for_user(user, "dance")

        elif message in self.emote_dict:
            await self.start_loop_for_user(user, message)

    async def on_chat(self, user: User, message: str) -> None:
        message = message.strip().lower()

        if message in ["stop", "Stop"]:
            await self.stop_loop_for_user(user)

        elif any(message.startswith(prefix) for prefix in ["loop ", "Loop ", "!loop ", "-loop "]):
            parts = message.split()
            if len(parts) > 1:
                emote_name = parts[1].lower()
                if emote_name in self.emote_dict:
                    await self.start_loop_for_user(user, emote_name)
            else:
                await self.start_loop_for_user(user, "dance")

        elif message in self.emote_dict:
            await self.start_loop_for_user(user, message)

    async def on_position_update(self, user: User, position: Position) -> None:
        if user.user_id in self.user_loops and not position.is_moving:
            loop_data = self.user_loops[user.user_id]
            loop_task = asyncio.create_task(self.send_emote_continuously(loop_data['command'], user.user_id))
            self.user_loops[user.user_id]['loop'] = loop_task
