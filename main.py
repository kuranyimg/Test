import asyncio
from highrise import BaseBot, Position
from highrise.models import User

class Bot(BaseBot):
    emote_dict = {
        "dance": {"emote": "dance-macarena", "delay": 12.5},
        "relaxed": {"emote": "sit-relaxed", "delay": 29.88},
        "attentive": {"emote": "idle_layingdown", "delay": 24.58}
    }

    user_loops = {}
    user_moving = {}

    async def send_emote_continuously(self, emote_data: dict, user_id: str) -> None:
        try:
            while user_id in self.user_loops:
                if not self.user_moving.get(user_id, False):
                    await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Loop error: {e}")
            self.user_loops.pop(user_id, None)

    async def start_loop_for_user(self, user: User, emote_name: str):
        if emote_name not in self.emote_dict:
            await self.highrise.chat(f"Emote '{emote_name}' not found.")
            return

        # Cancel old loop if exists
        await self.stop_loop_for_user(user, silent=True)

        emote_data = self.emote_dict[emote_name]
        loop_task = asyncio.create_task(self.send_emote_continuously(emote_data, user.user_id))
        self.user_loops[user.user_id] = {'command': emote_data, 'loop': loop_task}
        self.user_moving[user.user_id] = False

    async def stop_loop_for_user(self, user: User, silent=False):
        loop_data = self.user_loops.get(user.user_id)
        if loop_data:
            loop_data['loop'].cancel()
            self.user_loops.pop(user.user_id, None)
            self.user_moving.pop(user.user_id, None)
            if not silent:
                await self.highrise.chat(f"Stopped emote loop for {user.username}.")

    async def handle_message(self, user: User, message: str):
        msg = message.strip()

        if msg.lower() in ["stop"]:
            await self.stop_loop_for_user(user)

        elif any(msg.lower().startswith(prefix) for prefix in ["loop ", "!loop ", "-loop "]):
            parts = msg.split()
            if len(parts) > 1:
                await self.start_loop_for_user(user, parts[1].lower())
            else:
                await self.start_loop_for_user(user, "dance")

        elif msg.lower() in self.emote_dict:
            await self.start_loop_for_user(user, msg.lower())

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        await self.handle_message(user, message)

    async def on_chat(self, user: User, message: str) -> None:
        await self.handle_message(user, message)

    async def on_position_update(self, user: User, position: Position) -> None:
        user_id = user.user_id
        moving = position.is_moving

        if user_id in self.user_loops:
            # إذا بدأ يتحرك، نوقف التكرار مؤقتًا
            if moving:
                self.user_moving[user_id] = True
            else:
                # إذا توقف عن الحركة، نعيد تشغيل اللوب إذا لم يكن شغال
                if self.user_moving.get(user_id, False):
                    self.user_moving[user_id] = False
