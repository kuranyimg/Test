import asyncio
from highrise import BaseBot, User, __main__, Position
from highrise.models import (
    SessionMetadata,
    EmoteEvent,
    ChatEvent,
    UserJoinEvent,
    UserMoveEvent,
    UserLeaveEvent,
)
from functions.emote_loop import emote_list, emote_durations

# تخزين حالات التكرار لكل مستخدم
looping_users = {}  # user_id -> asyncio.Task
paused_users = {}   # user_id -> {"emote_data": ..., "position": ...}

class Bot(BaseBot):
    def __init__(self):
        self.metadata: SessionMetadata | None = None

    async def on_start(self, metadata: SessionMetadata) -> None:
        self.metadata = metadata

    async def on_chat(self, event: ChatEvent) -> None:
        msg = event.message.strip()
        user_id = event.user.id

        # إيقاف التكرار عند كتابة stop
        if msg.lower() == "stop":
            await self.stop_emote_loop(user_id)
            return

        # تشغيل إيموت مرة واحدة
        if msg.lower() in emote_list:
            await self.send_emote_once(msg.lower(), user_id)
            return

        # بدء التكرار
        if msg.lower().startswith(("loop ", "!loop ", "-loop ", "/loop ")):
            parts = msg.split()
            if len(parts) > 1:
                emote_name = parts[1].lower()
                await self.start_emote_loop(emote_name, user_id)
            return

        # تشغيل بالإيموت رقم
        if msg.isdigit():
            emote_index = int(msg)
            if 0 <= emote_index < len(emote_list):
                emote_name = list(emote_list.keys())[emote_index]
                await self.send_emote_once(emote_name, user_id)

    async def send_emote_once(self, emote_name, user_id):
        emote_id = emote_list.get(emote_name)
        if emote_id:
            await self.highrise.send_emote(emote_id, user_id=user_id)

    async def start_emote_loop(self, emote_name, user_id):
        emote_id = emote_list.get(emote_name)
        duration = emote_durations.get(emote_name, 4000)

        if not emote_id:
            return

        await self.stop_emote_loop(user_id)

        async def loop_emote():
            while True:
                if user_id in paused_users:
                    await asyncio.sleep(1)
                    continue
                await self.highrise.send_emote(emote_id, user_id=user_id)
                await asyncio.sleep(duration / 1000)

        task = asyncio.create_task(loop_emote())
        looping_users[user_id] = task

    async def stop_emote_loop(self, user_id):
        if user_id in looping_users:
            looping_users[user_id].cancel()
            del looping_users[user_id]
        if user_id in paused_users:
            del paused_users[user_id]

    async def on_user_move(self, event: UserMoveEvent) -> None:
        user_id = event.user.id
        position = event.position

        # إذا كان يتحرك وأصلاً لديه تكرار، أوقفه مؤقتاً
        if user_id in looping_users:
            paused_users[user_id] = {"position": position}
        # إذا توقف، استأنف التكرار
        elif user_id in paused_users:
            last_pos = paused_users[user_id]["position"]
            if (position.x, position.y, position.z) == (last_pos.x, last_pos.y, last_pos.z):
                del paused_users[user_id]

    async def on_user_leave(self, event: UserLeaveEvent) -> None:
        await self.stop_emote_loop(event.user.id)

    async def on_user_join(self, event: UserJoinEvent) -> None:
        await self.stop_emote_loop(event.user.id)

if __name__ == "__main__":
    __main__.main(Bot())
