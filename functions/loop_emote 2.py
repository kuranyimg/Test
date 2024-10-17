from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# Add emote duration in seconds
emote_list : list[tuple[str, str, float]] = [
    ('smooch','emote-kissing-bound', 8), ('fairyfloat','idle-floating', 12), ('fairytwirl','emote-looping', 9), 
    ('kissing','emote-kissing-bound', 8), ('tiktok11','dance-tiktok11', 10),
    # Continue adding duration for each emote
    ...
]

async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        emote_duration = 10  # Default duration

        # Fetch emote ID and duration from emote_list
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower():
                emote_id = emote[1]
                emote_duration = emote[2]  # Get the duration
                break

        if emote_id == "":
            return

        user_position = None
        user_in_room = False
        room_users = (await self.highrise.get_room_users()).content
        for room_user, position in room_users:
            if room_user.id == user.id:
                user_position = position
                start_position = position
                user_in_room = True
                break

        if user_position == None:
            await self.highrise.send_whisper(user.id,f"🚫🔄 @{user.username} To Stop the Loop Just Walk 🔄🚫")
            return

        await self.highrise.send_whisper(user.id,f"👯🏻‍♂️🔄 @{user.username} You are in a loop : {emote_name} 👯🏻‍♂️🔄")
        while start_position == user_position:
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.send_whisper(user.id,f"🚫🔄{user.username} loop 🤍 🔄🚫")
                return

            await asyncio.sleep(emote_duration)  # Use the duration for each emote

            room_users = (await self.highrise.get_room_users()).content
            user_in_room = False
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    user_in_room = True
                    break

            if not user_in_room:
                break

    try:
        splited_message = message.split(" ")
        emote_name = " ".join(splited_message[1:])
    except:
        await self.highrise.send_whisper(user.id,f"✅️ @{user.username} Siga <RayMG> 🤍 Hastag : #RayMG ✅️")
        return
    else:
        taskgroup = self.highrise.tg
        task_list : list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()

        taskgroup.create_task(coro=loop_emote(self, user, emote_name))
