from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

emote_list : list[tuple[str, str]] = [('smooch','emote-kissing-bound'),('fairyfloat','idle-floating'),('fairytwirl','emote-looping'),('kissing','emote-kissing-bound'),('tiktok11','dance-tiktok11'),('tiktok','dance-tiktok11'),('tik11','dance-tiktok11'),('gottago','idle-toilet'),('astronaut', 'emote-astronaut'),('wrong','dance-wrong'),('fashion','emote-fashionista'),('gravity','emote-gravity'),('icecream','dance-icecream'),('casual','idle-dance-casual'),('kiss','emote-kiss'),('no','emote-no'),('sad','emote-sad'),('yes','emote-yes'),('lau','emote-laughing'),('hello','emote-hello'),('wave','emote-wave'),('shy','emote-shy'),('tired','emote-tired'),('flirt','emote-lust'),('flirtywave','emote-lust'),('flirty','emote-lust'),('greedy','emote-greedy'),('model','emote-model'),('bow','emote-bow'),('curtsy','emote-curtsy'),('snowball','emote-snowball'),('hot','emote-hot'),('snowangel','emote-snowangel'),('charging','emote-charging'),('confused','emote-confused'),('telekinesis','emote-telekinesis'),('float','emote-float'),('teleport','emote-teleporting'),('maniac','emote-maniac'),('energyball','emote-energyball'),('snake','emote-snake'),('frog','emote-frog'),('superpose','emote-superpose'),('cute','emote-cute'),('pose7','emote-pose7'),('pose8','emote-pose8'),('pose1','emote-pose1'),('pose5','emote-pose5'),('pose3','emote-pose3'),('cutey','emote-cutey'),('tik10','dance-tiktok10'),('sing','idle_singing'),('singing','idle_singing'),('enthused','idle-enthusiastic'),('shop','dance-shoppingcart'),('russian','dance-russian'),('pennywise','dance-pennywise'),('tik2','dance-tiktok2'),('dontstartnow','dance-tiktok2'),('blackpink','dance-blackpink'),('kpop','dance-blackpink'),('celebrate','emoji-celebrate'),('gagging','emoji-gagging'),('flex','emoji-flex'),('cursing','emoji-cursing'),('thumbsup','emoji-thumbsup'),('angry','emoji-angry'),('punk','emote-punkguitar'),('zombie','emote-zombierun'),('sit','idle-loop-sitfloor'),('fight','emote-swordfight'),('ren','dance-macarena'),('wei','dance-weird'),('tik8','dance-tiktok8'),('savage','dance-tiktok8'),('tik9','dance-tiktok9'),('viral','dance-tiktok9'),('uwu','idle-uwu'),('tik4','idle-dance-tiktok4'),('sayso','idle-dance-tiktok4'),('star','emote-stargazer'),('pose9','emote-pose9'),('boxer','emote-boxer'),('guitar','idle-guitar'),('penguin','dance-pinguin'),('pinguin','dance-pinguin'),('zero','emote-astronaut'),('anime','dance-anime'),('saunter','dance-anime'),('creepy','dance-creepypuppet'),('watch','emote-creepycute'),('revelations','emote-headblowup'),('revelation','emote-headblowup'),('bashful','emote-shy2'),('arabesque','emote-pose10'),('pose10','emote-pose10'),('party','emote-celebrate'),('skating','emote-iceskating'),('scritchy','idle-wild'),('bitnervous','idle-nervous'),('nervous','idle-nervous'),('timejump','emote-timejump'),('jump','emote-timejump'),('jingle','dance-jinglebell'),('hyped','emote-hyped'),('sleigh','emote-sleigh'),('surprise','emote-pose6'),('repose','sit-relaxed'),('relaxed','sit-relaxed'),('kawaii','dance-kawai'),('kawai','dance-kawai'),('touch','dance-touch'),('gift','emote-gift'),('pushit','dance-employee'),('salute','emote-cutesalute'),('launch','emote-launch')]


# Sample emote duration dictionary (you can adjust the values as needed)
emote_durations = {
    'emote-kissing-bound': 6, 'idle-floating': 7, 'emote-looping': 6, 'dance-tiktok11': 7, 'idle-toilet': 5,
    'emote-astronaut': 7, 'dance-wrong': 5, 'emote-fashionista': 6, 'emote-gravity': 7, 'dance-icecream': 8,
    'idle-dance-casual': 6, 'emote-kiss': 4, 'emote-no': 5, 'emote-sad': 5, 'emote-yes': 4, 'emote-laughing': 5,
    'emote-hello': 4, 'emote-wave': 3, 'emote-shy': 4, 'emote-tired': 6, 'emote-lust': 5, 'emote-greedy': 5,
    'emote-model': 7, 'emote-bow': 4, 'emote-curtsy': 4, 'emote-snowball': 5, 'emote-hot': 6, 'emote-snowangel': 7,
    'emote-charging': 8, 'emote-confused': 5, 'emote-telekinesis': 7, 'emote-float': 6, 'emote-teleporting': 8,
    'emote-maniac': 6, 'emote-energyball': 5, 'emote-snake': 5, 'emote-frog': 4, 'emote-superpose': 5, 'emote-cute': 4,
    'emote-pose7': 5, 'emote-pose8': 5, 'emote-pose1': 4, 'emote-pose5': 5, 'emote-pose3': 5, 'emote-cutey': 4,
    'dance-tiktok10': 7, 'idle_singing': 6, 'idle-enthusiastic': 6, 'dance-shoppingcart': 8, 'dance-russian': 7,
    'dance-pennywise': 7, 'dance-tiktok2': 7, 'dance-blackpink': 7, 'emoji-celebrate': 3, 'emoji-gagging': 3,
    'emoji-flex': 3, 'emoji-cursing': 3, 'emoji-thumbsup': 3, 'emoji-angry': 3, 'emote-punkguitar': 6,
    'emote-zombierun': 7, 'idle-loop-sitfloor': 6, 'emote-swordfight': 6, 'dance-macarena': 7, 'dance-weird': 7,
    'dance-tiktok8': 7, 'dance-tiktok9': 7, 'idle-uwu': 5, 'idle-dance-tiktok4': 6, 'emote-stargazer': 6,
    'emote-pose9': 5, 'emote-boxer': 6, 'idle-guitar': 5, 'dance-pinguin': 7, 'emote-astronaut': 7, 'dance-anime': 6,
    'dance-creepypuppet': 7, 'emote-creepycute': 6, 'emote-headblowup': 7, 'emote-shy2': 5, 'emote-pose10': 6,
    'emote-celebrate': 5, 'emote-iceskating': 7, 'idle-wild': 5, 'idle-nervous': 4, 'emote-timejump': 7, 'dance-jinglebell': 8,
    'emote-hyped': 6, 'emote-sleigh': 7, 'emote-pose6': 5, 'sit-relaxed': 6, 'dance-kawai': 7, 'dance-touch': 6,
    'emote-gift': 5, 'dance-employee': 7, 'emote-cutesalute': 4, 'emote-launch': 7
}

async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
    emote_id = ""
    emote_duration = 10  # Default duration
    for emote in emote_list:
        if emote[0].lower() == emote_name.lower():
            emote_id = emote[1]
            emote_duration = emote_durations.get(emote_id, 10)  # Use duration from dictionary, default to 10 seconds
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
    if user_position is None:
        await self.highrise.send_whisper(user.id, f"🚫🔄 @{user.username} To Stop the Loop Just Walk 🔄🚫")
        return
    await self.highrise.send_whisper(user.id, f"👯🏻‍♂️🔄 @{user.username} You are in a loop: {emote_name} 👯🏻‍♂️🔄")
    while start_position == user_position:
        print(f"Loop {emote_name} - {user.username}")
        try:
            await self.highrise.send_emote(emote_id, user.id)
        except:
            await self.highrise.send_whisper(user.id, f"✅️ {user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
            return
        await asyncio.sleep(emote_duration)  # Use the emote duration here
        room_users = (await self.highrise.get_room_users()).content
        user_in_room = False
        for room_user, position in room_users:
            if room_user.id == user.id:
                user_position = position
                user_in_room = True
                break
        if not user_in_room:
            break
