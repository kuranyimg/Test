import asyncio
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, ChatEvent, Position, User
from functions.loop_emote import emote_list, emote_durations

looping_users = {}
paused_users = {}

class Bot(BaseBot):
    def __init__(self):
        self.metadata: SessionMetadata | None = None

    async def on_start(self, metadata: SessionMetadata) -> None:
        self.metadata = metadata
        print("Bot started.")

    async def on_chat(self, event: ChatEvent) -> None:
        try:
            msg = event.message.strip().lower()
            user_id = event.user.id

            if msg == "emotes":
                emotes = ", ".join(emote_list.keys())
                await self.highrise.send_whisper(user_id, f"Available emotes: {emotes}")
                return

            if msg == "stop":
                await self.stop_emote_loop(user_id)
                await self.highrise.send_whisper(user_id, "Loop stopped.")
                return

            if msg in emote_list:
                await self.send_emote_once(msg, user_id)
                await self.highrise.send_whisper(user_id, f"Sent emote: {msg}")
                return

            if msg.startswith(("loop ", "!loop ", "-loop ", "/loop ")):
                parts = msg.split()
                if len(parts) > 1:
                    emote_name = parts[1].lower()
                    await self.start_emote_loop(emote_name, user_id)
                    await self.highrise.send_whisper(user_id, f"Looping: {emote_name}")
                return

            if msg.isdigit():
                index = int(msg)
                if 0 <= index < len(emote_list):
                    emote_name = list(emote_list.keys())[index]
                    await self.send_emote_once(emote_name, user_id)
                    await self.highrise.send_whisper(user_id, f"Sent emote by number: {emote_name}")
        except Exception as e:
            print("Error in on_chat:", e)

    async def send_emote_once(self, emote_name, user_id):
        try:
            emote_id = emote_list.get(emote_name)
            if emote_id:
                await self.highrise.send_emote(emote_id, user_id=user_id)
        except Exception as e:
            print("Error in send_emote_once:", e)

    async def start_emote_loop(self, emote_name, user_id):
        await self.stop_emote_loop(user_id)
        emote_id = emote_list.get(emote_name)
        duration = emote_durations.get(emote_name, 4000)

        if not emote_id:
            print("Invalid emote name:", emote_name)
            return

        async def loop_task():
            try:
                while True:
                    if user_id in paused_users:
                        await asyncio.sleep(1)
                        continue
                    await self.highrise.send_emote(emote_id, user_id=user_id)
                    await asyncio.sleep(duration / 1000)
            except asyncio.CancelledError:
                print(f"Loop canceled for {user_id}")
                pass
            except Exception as e:
                print("Loop error:", e)

        looping_users[user_id] = asyncio.create_task(loop_task())

    async def stop_emote_loop(self, user_id):
        if user_id in looping_users:
            looping_users[user_id].cancel()
            del looping_users[user_id]
        if user_id in paused_users:
            del paused_users[user_id]

    async def on_user_move(self, user: User, pos: Position) -> None:
        user_id = user.id
        if user_id in looping_users:
            paused_users[user_id] = {"pos": pos}
        elif user_id in paused_users:
            last = paused_users[user_id]["pos"]
            if (last.x, last.y, last.z) == (pos.x, pos.y, pos.z):
                del paused_users[user_id]

if __name__ == "__main__":
    __main__.main(Bot())
