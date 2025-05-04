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
        },

        "att": {
            "emote": "idle_layingdown",
            "delay": 24.585168,
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

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        message = message.strip().lower()
        
        if message == "stop":
            # Stop the loop
            loop_data = self.user_loops.get(user.user_id)
            if loop_data:
                loop_data['loop'].cancel()
                self.user_loops.pop(user.user_id, None)
            await self.highrise.chat(f"Stopped emote loop for {user.username}.")
        
        elif message in self.emote_dict:
            command = self.emote_dict[message]
            # Start the loop for the user
            if user.user_id not in self.user_loops:
                loop_task = asyncio.create_task(self.send_emote_continuously(command, user.user_id))
                self.user_loops[user.user_id] = {'command': command, 'loop': loop_task}
                await self.highrise.chat(f"Started emote loop for {user.username}: {message}")

        # Handle the 'loop' command variants in whisper as well
        elif message in ["loop", "Loop", "!loop", "-loop"]:
            # If the loop command is received, start the loop for the user
            if user.user_id not in self.user_loops:
                loop_task = asyncio.create_task(self.send_emote_continuously(self.emote_dict["dance"], user.user_id))
                self.user_loops[user.user_id] = {'command': self.emote_dict["dance"], 'loop': loop_task}
                await self.highrise.chat(f"Started emote loop for {user.username}: dance")
    
    async def on_position_update(self, user: User, position: Position) -> None:
        # Check if the user stopped moving and resume the loop immediately
        if user.user_id in self.user_loops:
            # If the user stops moving, resume the loop immediately
            if position.is_moving is False:
                loop_data = self.user_loops[user.user_id]
                loop_task = asyncio.create_task(self.send_emote_continuously(loop_data['command'], user.user_id))
                self.user_loops[user.user_id]['loop'] = loop_task
