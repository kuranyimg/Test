from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task
# Import necessary libraries
from your_library import BaseBot, User  # adjust imports as necessary

# Define the emote durations in seconds
emote_durations = {
    'emote-kissing-bound': 5,
    'idle-floating': 7,
    'emote-looping': 6,
    'dance-tiktok11': 4,
    'dance-tiktok11': 4,
    'idle-toilet': 5,
    'emote-astronaut': 6,
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
    'idle_singing': 6,
    'idle-enthusiastic': 4,
    'dance-shoppingcart': 5,
    'dance-russian': 5,
    'dance-pennywise': 4,
    'dance-tiktok2': 5,
    'dance-tiktok2': 5,
    'dance-blackpink': 6,
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
    'dance-tiktok8': 4,
    'dance-tiktok9': 5,
    'dance-tiktok9': 5,
    'idle-uwu': 3,
    'idle-dance-tiktok4': 5,
    'idle-dance-tiktok4': 5,
    'emote-stargazer': 4,
    'emote-pose9': 4,
    'emote-boxer': 5,
    'idle-guitar': 5,
    'dance-pinguin': 5,
    'dance-pinguin': 5,
    'emote-astronaut': 6,
    'dance-anime': 5,
    'dance-anime': 5,
    'dance-creepypuppet': 4,
    'emote-creepycute': 5,
    'emote-headblowup': 6,
    'emote-headblowup': 6,
    'emote-shy2': 3,
    'emote-pose10': 4,
    'emote-pose10': 4,
    'emote-celebrate': 5,
    'emote-iceskating': 4,
    'idle-wild': 6,
    'idle-nervous': 5,
    'idle-nervous': 5,
    'emote-timejump': 4,
    'emote-timejump': 4,
    'dance-jinglebell': 5,
    'emote-hyped': 4,
    'emote-sleigh': 5,
    'emote-pose6': 4,
    'sit-relaxed': 4,
    'sit-relaxed': 4,
    'dance-kawai': 5,
    'dance-kawai': 5,
    'dance-touch': 4,
    'emote-gift': 4,
    'dance-employee': 5,
    'emote-cutesalute': 4,
    'emote-launch': 5,
}
emote_list : list[tuple[str, str]] = [('1','dance-wrong'),('2','emote-fashionista'),('3','emote-gravity'),('4','dance-icecream'),('5','idle-dance-casual'),('6','emote-kiss'),('7','emote-no'),('8','emote-sad'),('9','emote-yes'),('10','emote-laughing'),('11','emote-hello'),('12','emote-wave'),('13','emote-shy'),('14','emote-tired'),('15','emote-lust'),('16','emote-greedy'),('17','emote-model'),('18','emote-bow'),('19','emote-curtsy'),('20','emote-snowball'),('21','emote-hot'),('22','emote-snowangel'),('23','emote-charging'),('24','emote-confused'),('25','emote-telekinesis'),('26','emote-float'),('27','emote-teleporting'),('28','emote-maniac'),('29','emote-energyball'),('30','emote-snake'),('31','emote-frog'),('32','emote-superpose'),('33','emote-cute'),('34','emote-pose7'),('35','emote-pose8'),('36','emote-pose1'),('37','emote-pose5'),('38','emote-pose3'),('39','emote-cutey'),('40','dance-tiktok10'),('41','idle_singing'),('42','idle-enthusiastic'),('43','dance-shoppingcart'),('44','dance-russian'),('45','dance-pennywise'),('46','dance-tiktok2'),('47','dance-blackpink'),('48','emoji-celebrate'),('49','emoji-gagging'),('50','emoji-flex'),('51','emoji-cursing'),('52','emoji-thumbsup'),('53','emoji-angry'),('54','emote-punkguitar'),('55','emote-zombierun'),('56','idle-loop-sitfloor'),('57','emote-swordfight'),('58','dance-macarena'),('59','dance-weird'),('60','dance-tiktok8'),('61','dance-tiktok9'),('62','idle-uwu'),('63','idle-dance-tiktok4'),('64','emote-stargazer'),('65','emote-pose9'),('66','emote-boxer'),('67','idle-guitar'),('68','dance-pinguin'),('69','emote-astronaut'),('70','dance-anime'),('71','dance-creepypuppet'),('72','emote-creepycute'),('73','emote-headblowup'),('74','emote-shy2'),('75','emote-pose10'),('76','emote-celebrate'),('77','emote-iceskating'),('78','idle-wild'),('79','idle-nervous'),('80','emote-timejump'),('81','idle-toilet'),('82','dance-jinglebell'),('83','emote-hyped'),('84','emote-sleigh'),('85','emote-pose6'),('86','sit-relaxed'),('87','dance-kawai'),('88','dance-touch'),('89','emote-gift'),('90','dance-employee'),('91','emote-cutesalute'),('92','emote-salute'),('93','dance-tiktok11'),('94','emote-kissing-bound'),('95','emote-launch'),('96','idle-floating'),('97','emote-looping')]

async def loop(self: BaseBot, user: User, message: str) -> None:
    # Defining the loop_emote method locally so it cann't be accessed from the command handler.
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower():
                emote_id = emote[1]
                break
        if emote_id == "":
            await self.highrise.send_whisper(user.id,f"🚫🔄 @{user.username} To Stop the Loop Just Walk🔄🚫")
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
            await self.highrise.send_whisper(user.id,f"✅️ @{user.username} Siga <RayMG> 🤍 Hastag : #RayMG ✅️")
            return
        await self.highrise.send_whisper(user.id,f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name} 👯🏻‍♂️🔄")
        while start_position == user_position:
            print(f"Loop {emote_name} - {user.username}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.send_whisper(user.id,f"🚫🔄{user.username} loop 🤍 🔄🚫")
                return
            await asyncio.sleep(10)
            room_users = (await self.highrise.get_room_users()).content
            user_in_room = False
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    user_in_room = True
                    break
            if user_in_room == False:
                break
    try:
        splited_message = message.split(" ")
        # The emote name is every string after the first one
        emote_name = " ".join(splited_message[1:])
        print(emote_name)
    except:
        await self.highrise.send_whisper(user.id,f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
        return
    else:   
        taskgroup = self.highrise.tg
        task_list : list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                # Removes the task from the task group
                task.cancel()
                
        taskgroup.create_task(coro=loop_emote(self, user, emote_name))

            
async def stop_loop(self: BaseBot, user: User, message: str) -> None:
        taskgroup = self.highrise.tg
        task_list : list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
                await self.highrise.send_whisper(user.id,f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
                return
        await self.highrise.send_whisper(user.id,f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
        return
