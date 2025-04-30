from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# دمج قائمتَي الإيموجي في قائمة واحدة
emote_list: list[tuple[str, str]] = [
    # قائمة 1
    ('1','dance-wrong'), ('2','emote-fashionista'), ('3','emote-gravity'), ('4','dance-icecream'),
    # ... (اختصرنا هنا لعرض مثال) ...
    ('106','idle_layingdown'), ('107','emote-ghost-idle'), ('97','emote-looping'),

    # قائمة 2
    ('Rest', 'sit-idle-cute'), ('Zombie', 'idle_zombie'), ('Relaxed', 'idle_layingdown2'),
    ('Attentive', 'idle_layingdown'), ('Sleepy', 'idle-sleep'), ('Pouty Face', 'idle-sad'),
    ('Yes', 'emote-yes'), ('Hello', 'emote-hello'), ('Laugh', 'emote-laughing'),
    # ... (باقي الإيموجيات من القائمة 2) ...
]

async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower() or emote[1].lower() == emote_name.lower():
                emote_id = emote[1]
                break
        if emote_id == "":
            await self.highrise.chat("Invalid emote")
            return

        user_position = None
        room_users = (await self.highrise.get_room_users()).content
        for room_user, position in room_users:
            if room_user.id == user.id:
                user_position = position
                start_position = position
                break

        if user_position is None:
            await self.highrise.chat("User not found")
            return

        await self.highrise.chat(f"@{user.username} is looping {emote_name}")
        while start_position == user_position:
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.chat(f"Sorry, @{user.username}, this emote isn't free or you don't own it.")
                return
            await asyncio.sleep(10)
            room_users = (await self.highrise.get_room_users()).content
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    break
            else:
                break

    try:
        splited_message = message.split(" ")
        emote_name = " ".join(splited_message[1:])
    except:
        await self.highrise.chat("Invalid command format. Please use '/loop <emote name>'.")
        return

    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()

    room_users = (await self.highrise.get_room_users()).content
    user_list = [room_user.username for room_user, _ in room_users]

    taskgroup.create_task(coro=loop_emote(self, user, emote_name))
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_coro().__name__ == "loop_emote" and not (task.get_name() in user_list):
            task.set_name(user.username)

async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.chat(f"Stopping your emote loop, {user.username}!")
            return
    await self.highrise.chat(f"You're not looping any emotes, {user.username}")
