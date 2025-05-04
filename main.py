import asyncio
from highrise import BaseBot
from highrise.models import User

class Bot(BaseBot):

    emote_dict = {
        "blow": {
            "emote": "emote-headblowup",
            "delay": 11.667537
        },
        "skate": {
            "emote": "emote-iceskating",
            "delay": 7.299156
        },
        "boxer": {
            "emote": "emote-boxer",
            "delay": 5.555702
        },
        "dance": {
            "emote": "dance-macarena",
            "delay": 12.5
        },
        # أضف باقي الإيموتات هنا إذا احتجت
    }

    user_loops = {}

    async def send_emote_continuously(self, emote_data: dict, user_id: str) -> None:
        try:
            while user_id in self.user_loops:
                await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in emote loop for {user_id}: {e}")
            self.user_loops.pop(user_id, None)

    async def start_emote_loop(self, user: User, emote_name: str) -> None:
        command = self.emote_dict[emote_name]
        user_id = user.id
        if user_id not in self.user_loops:
            loop_task = asyncio.create_task(
                self.send_emote_continuously(command, user_id))
            self.user_loops[user_id] = {
                'command': command,
                'loop': loop_task
            }
            await self.highrise.chat(f"Loop started for {user.username} using '{emote_name}' emote.")
        else:
            await self.highrise.chat(f"{user.username}, you're already in a loop.")

    async def stop_user_loop(self, user: User) -> None:
        user_id = user.id
        if user_id in self.user_loops:
            self.user_loops[user_id]['loop'].cancel()
            del self.user_loops[user_id]
            await self.highrise.chat(f"{user.username}, your emote loop has been stopped.")

    def _is_loop_command(self, msg: str) -> bool:
        return msg in ["loop", "Loop", "-loop", "!loop"]

    async def handle_emote_message(self, user: User, message: str) -> None:
        message = message.strip()
        words = message.split()

        if not words:
            return

        command = words[0].lower()

        if command in self.emote_dict:
            if len(words) > 1 and self._is_loop_command(words[1]):
                await self.start_emote_loop(user, command)
            elif len(words) == 1:
                await self.highrise.send_emote(self.emote_dict[command]["emote"], user.id)
        elif command in ["stop", "Stop"]:
            await self.stop_user_loop(user)

    async def on_chat(self, user: User, message: str) -> None:
        await self.handle_emote_message(user, message)

    async def on_whisper(self, user: User, message: str) -> None:
        await self.handle_emote_message(user, message)
