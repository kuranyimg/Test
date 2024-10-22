from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# Emote list with corresponding numbers
emote_list : list[tuple[str, str]] = [('1','dance-wrong'),('2','emote-fashionista'),('3','emote-gravity'),('4','dance-icecream'),('5','idle-dance-casual'),('6','emote-kiss'),('7','emote-no'),('8','emote-sad'),('9','emote-yes'),('10','emote-laughing'),('11','emote-hello'),('12','emote-wave'),('13','emote-shy'),('14','emote-tired'),('15','emote-lust'),('16','emote-greedy'),('17','emote-model'),('18','emote-bow'),('19','emote-curtsy'),('20','emote-snowball'),('21','emote-hot'),('22','emote-snowangel'),('23','emote-charging'),('24','emote-confused'),('25','emote-telekinesis'),('26','emote-float'),('27','emote-teleporting'),('28','emote-maniac'),('29','emote-energyball'),('30','emote-snake'),('31','emote-frog'),('32','emote-superpose'),('33','emote-cute'),('34','emote-pose7'),('35','emote-pose8'),('36','emote-pose1'),('37','emote-pose5'),('38','emote-pose3'),('39','emote-cutey'),('40','dance-tiktok10'),('41','idle_singing'),('42','idle-enthusiastic'),('43','dance-shoppingcart'),('44','dance-russian'),('45','dance-pennywise'),('46','dance-tiktok2'),('47','dance-blackpink'),('48','emoji-celebrate'),('49','emoji-gagging'),('50','emoji-flex'),('51','emoji-cursing'),('52','emoji-thumbsup'),('53','emoji-angry'),('54','emote-punkguitar'),('55','emote-zombierun'),('56','idle-loop-sitfloor'),('57','emote-swordfight'),('58','dance-macarena'),('59','dance-weird'),('60','dance-tiktok8'),('61','dance-tiktok9'),('62','idle-uwu'),('63','idle-dance-tiktok4'),('64','emote-stargazer'),('65','emote-pose9'),('66','emote-boxer'),('67','idle-guitar'),('68','dance-pinguin'),('69','emote-astronaut'),('70','dance-anime'),('71','dance-creepypuppet'),('72','emote-creepycute'),('73','emote-headblowup'),('74','emote-shy2'),('75','emote-pose10'),('76','emote-celebrate'),('77','emote-iceskating'),('78','idle-wild'),('79','idle-nervous'),('80','emote-timejump'),('81','idle-toilet'),('82','dance-jinglebell'),('83','emote-hyped'),('84','emote-sleigh'),('85','emote-pose6'),('86','sit-relaxed'),('87','dance-kawai'),('88','dance-touch'),('89','emote-gift'),('90','dance-employee'),('91','emote-cutesalute'),('92','emote-salute'),('93','dance-tiktok11'),('94','emote-kissing-bound'),('95','emote-launch'),('96','idle-floating'),('97','emote-looping')]

# Dictionary to store emote durations (in seconds)
emote_durations = {
    'dance-wrong': 5,
    'emote-fashionista': 4,
    'emote-gravity': 5,
    'dance-icecream': 5,
    'idle-dance-casual': 5,
    'emote-kiss': 3,
    'emote-no': 2,
    'emote-sad': 3,
    'emote-yes': 2,
    'emote-laughing': 5,
    'emote-hello': 2,
    'emote-wave': 2,
    'emote-shy': 3,
    'emote-tired': 3,
    'emote-lust': 4,
    'emote-greedy': 4,
    'emote-model': 4,
    'emote-bow': 2,
    'emote-curtsy': 3,
    'emote-snowball': 3,
    'emote-hot': 4,
    'emote-snowangel': 6,
    'emote-charging': 5,
    'emote-confused': 3,
    'emote-telekinesis': 6,
    'emote-float': 4,
    'emote-teleporting': 5,
    'emote-maniac': 4,
    'emote-energyball': 3,
    'emote-snake': 5,
    'emote-frog': 4,
    'emote-superpose': 5,
    'emote-cute': 3,
    'emote-pose7': 4,
    'emote-pose8': 4,
    'emote-pose1': 4,
    'emote-pose5': 4,
    'emote-pose3': 4,
    'emote-cutey': 5,
    'dance-tiktok10': 5,
    'idle_singing': 6,
    'idle-enthusiastic': 4,
    'dance-shoppingcart': 5,
    'dance-russian': 5,
    'dance-pennywise': 4,
    'dance-tiktok2': 5,
    'dance-blackpink': 6,
    'emoji-celebrate': 3,
    'emoji-gagging': 2,
    'emoji-flex': 3,
    'emoji-cursing': 3,
    'emoji-thumbsup': 2,
    'emoji-angry': 3,
    'emote-punkguitar': 5,
    'emote-zombierun': 5,
    'idle-loop-sitfloor': 7,
    'emote-swordfight': 6,
    'dance-macarena': 4,
    'dance-weird': 5,
    'dance-tiktok8': 4,
    'dance-tiktok9': 5,
    'idle-uwu': 3,
    'idle-dance-tiktok4': 5,
    'emote-stargazer': 4,
    'emote-pose9': 4,
    'emote-boxer': 5,
    'idle-guitar': 5,
    'dance-pinguin': 5,
    'emote-astronaut': 6,
    'dance-anime': 5,
    'dance-creepypuppet': 4,
    'emote-creepycute': 5,
    'emote-headblowup': 6,
    'emote-shy2': 3,
    'emote-pose10': 4,
    'emote-celebrate': 5,
    'emote-iceskating': 4,
    'idle-wild': 6,
    'idle-nervous': 5,
    'emote-timejump': 4,
    'idle-toilet': 5,
    'dance-jinglebell': 5,
    'emote-hyped': 4,
    'emote-sleigh': 5,
    'emote-pose6': 4,
    'sit-relaxed': 4,
    'dance-kawai': 5,
    'dance-touch': 4,
    'emote-gift': 4,
    'dance-employee': 5,
    'emote-cutesalute': 4,
    'emote-kissing-bound': 5,
    'idle-floating': 7,
    'emote-looping': 6,
    'dance-tiktok11': 4,
    'emote-launch': 5,
}

# Function to start a loop for a specific emote
async def loop(self: BaseBot, user: User, message: str) -> None:
    # Defining the loop_emote method locally so it can't be accessed from the command handler.
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[1].lower() == emote_name.lower():
                emote_id = emote[1]
                break
        if emote_id == "":
            await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} Invalid emote or 'Stop' to end loop 🔄🚫")
            return

        # Stop any existing loop for this user
        await stop_loop(self, user)

        # Start the new loop
        await self.highrise.send_whisper(user.id, f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name} 👯🏻‍♂️🔄")
        while True:
            print(f"Loop {emote_name} - {user.username}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} loop stopped 🚫🔄")
                return

            # Use the emote duration for the delay
            emote_duration = emote_durations.get(emote_id, 10)  # Default to 10 seconds if not found
            await asyncio.sleep(emote_duration)

            # Check if the user has left the room
            room_users = (await self.highrise.get_room_users()).content
            user_in_room = False
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_in_room = True
                    break

            if not user_in_room:
                await self.highrise.send_whisper(user.id, f"✅️ @{user.username} has left the room, loop stopped ✅️")
                return

    try:
        splited_message = message.split(" ")
        # Get the emote name from the message or check if it's a stop command
        command = " ".join(splited_message).strip().lower()

        if command == "stop":
            await stop_loop(self, user)
            await self.highrise.send_whisper(user.id, f"✅️ @{user.username} loop stopped ✅️")
            return

        # Start a new emote loop
        await start_new_loop(self, user, command)
    except:
        await self.highrise.send_whisper(user.id, f"❌ @{user.username} Unable to process the command ❌")

# Function to start a new loop for an emote
async def start_new_loop(self: BaseBot, user: User, emote_name: str) -> None:
    # Cancel any existing loop and start a new one
    await stop_loop(self, user)

    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()

    taskgroup.create_task(coro=loop_emote(self, user, emote_name), name=user.username)

# Function to stop the loop for a user
async def stop_loop(self: BaseBot, user: User) -> None:
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅️ @{user.username} Loop stopped ✅️")
            return
    await self.highrise.send_whisper(user.id, f"❌ @{user.username} No active loop found ❌")
