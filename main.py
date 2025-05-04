import asyncio
from highrise import BaseBot, Position
from highrise.models import User

vip = [
    "iced_yu","Damn_snake","love_cant_relate","RayMg","FallonXOXO"
]

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
        # ... other emotes here ...
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

    def _get_emote_commands_list(self):
        emotes_list = list(self.emote_dict.keys())
        unique_emotes = set(emotes_list)
        formatted_list = ', '.join(unique_emotes)
        return f"You can use the following emotes: {formatted_list}. Just type the emote you want to use in the chat!"

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        if user.username in vip:
            message = message.strip().lower()
            if message == "stop":
                for _user_id, loop_data in list(self.user_loops.items()):
                    loop_data['loop'].cancel()
                self.user_loops = {}
            else:
                words = message.split()
                if words and words[0] in self.emote_dict:
                    command = self.emote_dict[words[0]]
                    if len(words) > 1 and words[1] == "loop":
                        room_users_res = await self.highrise.get_room_users()
                        for item in room_users_res.content:
                            room_user = item[0]
                            if room_user.id not in self.user_loops:
                                loop_task = asyncio.create_task(
                                    self.send_emote_continuously(command, room_user.id))
                                self.user_loops[room_user.id] = {
                                    'command': command,
                                    'loop': loop_task
                                }
                        await self.highrise.chat(
                            f"Emote loop for '{words[0]}' started by {user.username}.")
                    elif not words[1:]:
                        room_users_res = await self.highrise.get_room_users()
                        for item in room_users_res.content:
                            room_user = item[0]
                            await self.highrise.send_emote(command["emote"], room_user.id)
