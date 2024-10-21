from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

# Complete emote list
emote_list : list[tuple[str, str]] = [
    ('1', 'dance-wrong'), ('2', 'emote-fashionista'), ('3', 'emote-gravity'), ('4', 'dance-icecream'),
    ('5', 'idle-dance-casual'), ('6', 'emote-kiss'), ('7', 'emote-no'), ('8', 'emote-sad'),
    ('9', 'emote-yes'), ('10', 'emote-laughing'), ('11', 'emote-hello'), ('12', 'emote-wave'),
    ('13', 'emote-shy'), ('14', 'emote-tired'), ('15', 'emote-lust'), ('16', 'emote-greedy'),
    ('17', 'emote-model'), ('18', 'emote-bow'), ('19', 'emote-curtsy'), ('20', 'emote-snowball'),
    ('21', 'emote-hot'), ('22', 'emote-snowangel'), ('23', 'emote-charging'), ('24', 'emote-confused'),
    ('25', 'emote-telekinesis'), ('26', 'emote-float'), ('27', 'emote-teleporting'), ('28', 'emote-maniac'),
    ('29', 'emote-energyball'), ('30', 'emote-snake'), ('31', 'emote-frog'), ('32', 'emote-superpose'),
    ('33', 'emote-cute'), ('34', 'emote-pose7'), ('35', 'emote-pose8'), ('36', 'emote-pose1'),
    ('37', 'emote-pose5'), ('38', 'emote-pose3'), ('39', 'emote-cutey'), ('40', 'dance-tiktok10'),
    ('41', 'idle_singing'), ('42', 'idle-enthusiastic'), ('43', 'dance-shoppingcart'), ('44', 'dance-russian'),
    ('45', 'dance-pennywise'), ('46', 'dance-tiktok2'), ('47', 'dance-blackpink'), ('48', 'emoji-celebrate'),
    ('49', 'emoji-gagging'), ('50', 'emoji-flex'), ('51', 'emoji-cursing'), ('52', 'emoji-thumbsup'),
    ('53', 'emoji-angry'), ('54', 'emote-punkguitar'), ('55', 'emote-zombierun'), ('56', 'idle-loop-sitfloor'),
    ('57', 'emote-swordfight'), ('58', 'dance-macarena'), ('59', 'dance-weird'), ('60', 'dance-tiktok8'),
    ('61', 'dance-tiktok9'), ('62', 'idle-uwu'), ('63', 'idle-dance-tiktok4'), ('64', 'emote-stargazer'),
    ('65', 'emote-pose9'), ('66', 'emote-boxer'), ('67', 'idle-guitar'), ('68', 'dance-pinguin'),
    ('69', 'emote-astronaut'), ('70', 'dance-anime'), ('71', 'dance-creepypuppet'), ('72', 'emote-creepycute'),
    ('73', 'emote-headblowup'), ('74', 'emote-shy2'), ('75', 'emote-pose10'), ('76', 'emote-celebrate'),
    ('77', 'emote-iceskating'), ('78', 'idle-wild'), ('79', 'idle-nervous'), ('80', 'emote-timejump'),
    ('81', 'idle-toilet'), ('82', 'dance-jinglebell'), ('83', 'emote-hyped'), ('84', 'emote-sleigh'),
    ('85', 'emote-pose6'), ('86', 'sit-relaxed'), ('87', 'dance-kawai'), ('88', 'dance-touch'),
    ('89', 'emote-gift'), ('90', 'dance-employee'), ('91', 'emote-cutesalute'), ('92', 'emote-salute'),
    ('93', 'dance-tiktok11'), ('94', 'emote-kissing-bound'), ('95', 'emote-launch'), ('96', 'idle-floating'),
    ('97', 'emote-looping')
]

# Complete emote duration list (in seconds)
emote_durations = {
    'dance-wrong': 5, 'emote-fashionista': 6, 'emote-gravity': 7, 'dance-icecream': 8,
    'idle-dance-casual': 6, 'emote-kiss': 4, 'emote-no': 5, 'emote-sad': 5,
    'emote-yes': 4, 'emote-laughing': 5, 'emote-hello': 4, 'emote-wave': 3,
    'emote-shy': 4, 'emote-tired': 6, 'emote-lust': 5, 'emote-greedy': 5,
    'emote-model': 7, 'emote-bow': 4, 'emote-curtsy': 4, 'emote-snowball': 5,
    'emote-hot': 6, 'emote-snowangel': 7, 'emote-charging': 8, 'emote-confused': 5,
    'emote-telekinesis': 7, 'emote-float': 6, 'emote-teleporting': 8, 'emote-maniac': 6,
    'emote-energyball': 5, 'emote-snake': 5, 'emote-frog': 4, 'emote-superpose': 5,
    'emote-cute': 4, 'emote-pose7': 5, 'emote-pose8': 5, 'emote-pose1': 4,
    'emote-pose5': 5, 'emote-pose3': 5, 'emote-cutey': 4, 'dance-tiktok10': 7,
    'idle_singing': 6, 'idle-enthusiastic': 6, 'dance-shoppingcart': 8, 'dance-russian': 7,
    'dance-pennywise': 7, 'dance-tiktok2': 7, 'dance-blackpink': 7, 'emoji-celebrate': 3,
    'emoji-gagging': 3, 'emoji-flex': 3, 'emoji-cursing': 3, 'emoji-thumbsup': 3,
    'emoji-angry': 3, 'emote-punkguitar': 6, 'emote-zombierun': 7, 'idle-loop-sitfloor': 6,
    'emote-swordfight': 6, 'dance-macarena': 7, 'dance-weird': 7, 'dance-tiktok8': 7,
    'dance-tiktok9': 7, 'idle-uwu': 5, 'idle-dance-tiktok4': 6, 'emote-stargazer': 6,
    'emote-pose9': 5, 'emote-boxer': 6, 'idle-guitar': 5, 'dance-pinguin': 7,
    'emote-astronaut': 7, 'dance-anime': 6, 'dance-creepypuppet': 7, 'emote-creepycute': 5,
    'emote-headblowup': 6, 'emote-shy2': 4, 'emote-pose10': 5, 'emote-celebrate': 5,
    'emote-iceskating': 7, 'idle-wild': 6, 'idle-nervous': 5, 'emote-timejump': 6,
    'idle-toilet': 5, 'dance-jinglebell': 7, 'emote-hyped': 6, 'emote-sleigh': 7,
    'emote-pose6': 5, 'sit-relaxed': 6, 'dance-kawai': 7, 'dance-touch': 6,
    'emote-gift': 5, 'dance-employee': 7, 'emote-cutesalute': 4, 'emote-salute': 4,
    'dance-tiktok11': 7, 'emote-kissing-bound': 6, 'emote-launch': 7, 'idle-floating': 23,
    'emote-looping': 6
}


async def loop(self: BaseBot, user: User, message: str) -> None:
    async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
        emote_id = ""
        for emote in emote_list:
            if emote[0].lower() == emote_name.lower():
                emote_id = emote[1]
                break

        if emote_id == "":
            await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} To Stop the Loop Just Walk🔄🚫")
            return

        # Get emote duration
        emote_duration = emote_durations.get(emote_id, 10)  # Default to 10 if not found

        user_position = None
        user_in_room = False
        room_users = (await self.highrise.get_room_users()).content
        for room_user, position in room_users:
            if room_user.id == user.id:
                user_position = position
                start_position = position
                user_in_room = True
                break

        if user_position is None:
            await self.highrise.send_whisper(user.id, f"✅️ @{user.username} Siga <RayMG> 🤍 Hastag : #RayMG ✅️")
            return

        await self.highrise.send_whisper(user.id, f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name} 👯🏻‍♂️🔄")

        while start_position == user_position:
            print(f"Loop {emote_name} - {user.username}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"🚫🔄{user.username} loop 🤍 🔄🚫")
                return
            
            await asyncio.sleep(emote_duration - 1)  # Wait for the emote duration minus 1 second

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
        print(emote_name)
    except:
        await self.highrise.send_whisper(user.id, f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
        return
    else:   
        taskgroup = self.highrise.tg
        task_list: list[Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user.username:
                task.cancel()
                
        taskgroup.create_task(coro=loop_emote(self, user, emote_name))

async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list: list[Task] = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.send_whisper(user.id, f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
            return
    await self.highrise.send_whisper(user.id, f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
    return
