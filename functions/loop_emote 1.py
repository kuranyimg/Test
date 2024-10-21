from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task
# Import necessary libraries
from your_library import BaseBot, User  # adjust imports as necessary

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

            # Stop any existing loop for this user
            await self.stop_loop(user)

            # Start the new loop
            await self.highrise.send_whisper(user.id,f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name} 👯🏻‍♂️🔄")
            while True:
                print(f"Loop {emote_name} - {user.username}")
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                except Exception as e:
                    await self.highrise.send_whisper(user.id,f"🚫🔄{user.username} loop 🤍 🔄🚫")
                    print(f"Error in loop: {e}")
                    return

                # Check if the user has left the room
                room_users = (await self.highrise.get_room_users()).content
                user_in_room = False
                for room_user, position in room_users:
                    if room_user.id == user.id:
                        user_in_room = True
                        break

                if not user_in_room:
                    await self.highrise.send_whisper(user.id,f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
                    return

                # Use a short delay instead of a fixed sleep
                await asyncio.sleep(1)  # Adjust the delay as needed

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

            taskgroup.create_task(coro=loop_emote(self, user, emote_name), name=user.username)

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

    # ... (Rest of your Bot class code)

# Define emote_list here
emote_list : list[tuple[str, str]] = [('1','dance-wrong'),('2','emote-fashionista'),('3','emote-gravity'),('4','dance-icecream'),('5','idle-dance-casual'),('6','emote-kiss'),('7','emote-no'),('8','emote-sad'),('9','emote-yes'),('10','emote-laughing'),('11','emote-hello'),('12','emote-wave'),('13','emote-shy'),('14','emote-tired'),('15','emote-lust'),('16','emote-greedy'),('17','emote-model'),('18','emote-bow'),('19','emote-curtsy'),('20','emote-snowball'),('21','emote-hot'),('22','emote-snowangel'),('23','emote-charging'),('24','emote-confused'),('25','emote-telekinesis'),('26','emote-float'),('27','emote-teleporting'),('28','emote-maniac'),('29','emote-energyball'),('30','emote-snake'),('31','emote-frog'),('32','emote-superpose'),('33','emote-cute'),('34','emote-pose7'),('35','emote-pose8'),('36','emote-pose1'),('37','emote-pose5'),('38','emote-pose3'),('39','emote-cutey'),('40','dance-tiktok10'),('41','idle_singing'),('42','idle-enthusiastic'),('43','dance-shoppingcart'),('44','dance-russian'),('45','dance-pennywise'),('46','dance-tiktok2'),('47','dance-blackpink'),('48','emoji-celebrate'),('49','emoji-gagging'),('50','emoji-flex'),('51','emoji-cursing'),('52','emoji-thumbsup'),('53','emoji-angry'),('54','emote-punkguitar'),('55','emote-zombierun'),('56','idle-loop-sitfloor'),('57','emote-swordfight'),('58','dance-macarena'),('59','dance-weird'),('60','dance-tiktok8'),('61','dance-tiktok9'),('62','idle-uwu'),('63','idle-dance-tiktok4'),('64','emote-stargazer'),('65','emote-pose9'),('66','emote-boxer'),('67','idle-guitar'),('68','dance-pinguin'),('69','emote-astronaut'),('70','dance-anime'),('71','dance-creepypuppet'),('72','emote-creepycute'),('73','emote-headblowup'),('74','emote-shy2'),('75','emote-pose10'),('76','emote-celebrate'),('77','emote-iceskating'),('78','idle-wild'),('79','idle-nervous'),('80','emote-timejump'),('81','idle-toilet'),('82','dance-jinglebell'),('83','emote-hyped'),('84','emote-sleigh'),('85','emote-pose6'),('86','sit-relaxed'),('87','dance-kawai'),('88','dance-touch'),('89','emote-gift'),('90','dance-employee'),('91','emote-cutesalute'),('92','emote-salute'),('93','dance-tiktok11'),('94','emote-kissing-bound'),('95','emote-launch'),('96','idle-floating'),('97','emote-looping')]
