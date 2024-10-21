from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

emote_list: list[tuple[str, str]] = [
    # New emotes added as requested
    ('relaxed', 'sit-relaxed'),
    ('cozynap', 'idle-cozynap'),
    ('ghostfloat', 'emote-ghostfloat'),
    ('rest', 'emote-rest'),
    ('jinglehop', 'dance-jinglehop'),
    ('loveflutter', 'emote-loveflutter'),
    ('attentive', 'emote-attentive'),
    ('clumsy', 'emote-clumsy'),
    ('gimmeattention', 'emote-gimmeattention'),
    ('shrink', 'emote-shrink'),
    ('fruitydance', 'dance-fruitydance'),
    ('nocturnalhowl', 'emote-nocturnalhowl'),
    ('laidback', 'emote-laidback'),

    # Previous emotes (maintained)
    ('smooch','emote-kissing-bound'),
    ('fairyfloat','idle-floating'),
    ('fairytwirl','emote-looping'),
    ('kissing','emote-kissing-bound'),
    ('tiktok11','dance-tiktok11'),
    ('tiktok','dance-tiktok11'),
    ('tik11','dance-tiktok11'),
    ('gottago','idle-toilet'),
    ('astronaut', 'emote-astronaut'),
    ('wrong','dance-wrong'),
    ('fashion','emote-fashionista'),
    ('gravity','emote-gravity'),
    ('icecream','dance-icecream'),
    ('casual','idle-dance-casual'),
    ('kiss','emote-kiss'),
    ('no','emote-no'),
    ('sad','emote-sad'),
    ('yes','emote-yes'),
    ('lau','emote-laughing'),
    ('hello','emote-hello'),
    ('wave','emote-wave'),
    ('shy','emote-shy'),
    ('tired','emote-tired'),
    ('flirt','emote-lust'),
    ('flirtywave','emote-lust'),
    ('flirty','emote-lust'),
    ('greedy','emote-greedy'),
    ('model','emote-model'),
    ('bow','emote-bow'),
    ('curtsy','emote-curtsy'),
    ('snowball','emote-snowball'),
    ('hot','emote-hot'),
    ('snowangel','emote-snowangel'),
    ('charging','emote-charging'),
    ('confused','emote-confused'),
    ('telekinesis','emote-telekinesis'),
    ('float','emote-float'),
    ('teleport','emote-teleporting'),
    ('maniac','emote-maniac'),
    ('energyball','emote-energyball'),
    ('snake','emote-snake'),
    ('frog','emote-frog'),
    ('superpose','emote-superpose'),
    ('cute','emote-cute'),
    ('pose7','emote-pose7'),
    ('pose8','emote-pose8'),
    ('pose1','emote-pose1'),
    ('pose5','emote-pose5'),
    ('pose3','emote-pose3'),
    ('cutey','emote-cutey'),
    ('tik10','dance-tiktok10'),
    ('sing','idle_singing'),
    ('singing','idle_singing'),
    ('enthused','idle-enthusiastic'),
    ('shop','dance-shoppingcart'),
    ('russian','dance-russian'),
    ('pennywise','dance-pennywise'),
    ('tik2','dance-tiktok2'),
    ('dontstartnow','dance-tiktok2'),
    ('blackpink','dance-blackpink'),
    ('kpop','dance-blackpink'),
    ('celebrate','emoji-celebrate'),
    ('gagging','emoji-gagging'),
    ('flex','emoji-flex'),
    ('cursing','emoji-cursing'),
    ('thumbsup','emoji-thumbsup'),
    ('angry','emoji-angry'),
    ('punk','emote-punkguitar'),
    ('zombie','emote-zombierun'),
    ('sit','idle-loop-sitfloor'),
    ('fight','emote-swordfight'),
    ('ren','dance-macarena'),
    ('wei','dance-weird'),
    ('tik8','dance-tiktok8'),
    ('savage','dance-tiktok8'),
    ('tik9','dance-tiktok9'),
    ('viral','dance-tiktok9'),
    ('uwu','idle-uwu'),
    ('tik4','idle-dance-tiktok4'),
    ('sayso','idle-dance-tiktok4'),
    ('star','emote-stargazer'),
    ('pose9','emote-pose9'),
    ('boxer','emote-boxer'),
    ('guitar','idle-guitar'),
    ('penguin','dance-pinguin'),
    ('pinguin','dance-pinguin'),
    ('zero','emote-astronaut'),
    ('anime','dance-anime'),
    ('saunter','dance-anime'),
    ('creepy','dance-creepypuppet'),
    ('watch','emote-creepycute'),
    ('revelations','emote-headblowup'),
    ('revelation','emote-headblowup'),
    ('bashful','emote-shy2'),
    ('arabesque','emote-pose10'),
    ('pose10','emote-pose10'),
    ('party','emote-celebrate'),
    ('skating','emote-iceskating'),
    ('scritchy','idle-wild'),
    ('bitnervous','idle-nervous'),
    ('nervous','idle-nervous'),
    ('timejump','emote-timejump'),
    ('jump','emote-timejump'),
    ('jingle','dance-jinglebell'),
    ('hyped','emote-hyped'),
    ('sleigh','emote-sleigh'),
    ('surprise','emote-pose6'),
    ('repose','sit-relaxed'),
    ('relaxed','sit-relaxed'),
    ('kawaii','dance-kawai'),
    ('kawai','dance-kawai'),
    ('touch','dance-touch'),
    ('gift','emote-gift'),
    ('pushit','dance-employee'),
    ('salute','emote-cutesalute'),
    ('launch','emote-launch')
]


emote_list: list[tuple[str, str, float]] = [
    # New emotes added as requested
    ('relaxed', 'sit-relaxed', 5.0),
    ('cozynap', 'idle-cozynap', 7.0),
    ('ghostfloat', 'emote-ghostfloat', 4.5),
    ('rest', 'emote-rest', 6.0),
    ('jinglehop', 'dance-jinglehop', 4.8),
    ('loveflutter', 'emote-loveflutter', 3.5),
    ('attentive', 'emote-attentive', 3.0),
    ('clumsy', 'emote-clumsy', 2.5),
    ('gimmeattention', 'emote-gimmeattention', 3.2),
    ('shrink', 'emote-shrink', 2.8),
    ('fruitydance', 'dance-fruitydance', 4.7),
    ('nocturnalhowl', 'emote-nocturnalhowl', 5.3),
    ('laidback', 'emote-laidback', 6.0),

    # Previous emotes (maintained)
    ('smooch','emote-kissing-bound', 3.0),
    ('fairyfloat','idle-floating', 4.0),
    ('fairytwirl','emote-looping', 4.5),
    ('kissing','emote-kissing-bound', 3.0),
    ('tiktok11','dance-tiktok11', 5.5),
    ('tiktok','dance-tiktok11', 5.5),
    ('tik11','dance-tiktok11', 5.5),
    ('gottago','idle-toilet', 4.2),
    ('astronaut', 'emote-astronaut', 4.8),
    ('wrong','dance-wrong', 3.5),
    ('fashion','emote-fashionista', 4.0),
    ('gravity','emote-gravity', 3.8),
    ('icecream','dance-icecream', 5.0),
    ('casual','idle-dance-casual', 4.2),
    ('kiss','emote-kiss', 2.5),
    ('no','emote-no', 2.2),
    ('sad','emote-sad', 2.8),
    ('yes','emote-yes', 2.0),
    ('lau','emote-laughing', 3.5),
    ('hello','emote-hello', 2.3),
    ('wave','emote-wave', 2.0),
    ('shy','emote-shy', 2.7),
    ('tired','emote-tired', 4.3),
    ('flirt','emote-lust', 3.0),
    ('flirtywave','emote-lust', 3.0),
    ('flirty','emote-lust', 3.0),
    ('greedy','emote-greedy', 3.2),
    ('model','emote-model', 3.8),
    ('bow','emote-bow', 2.5),
    ('curtsy','emote-curtsy', 2.8),
    ('snowball','emote-snowball', 3.5),
    ('hot','emote-hot', 4.0),
    ('snowangel','emote-snowangel', 5.2),
    ('charging','emote-charging', 3.7),
    ('confused','emote-confused', 2.9),
    ('telekinesis','emote-telekinesis', 4.6),
    ('float','emote-float', 4.0),
    ('teleport','emote-teleporting', 5.1),
    ('maniac','emote-maniac', 3.8),
    ('energyball','emote-energyball', 4.3),
    ('snake','emote-snake', 4.0),
    ('frog','emote-frog', 3.7),
    ('superpose','emote-superpose', 4.5),
    ('cute','emote-cute', 2.8),
    ('pose7','emote-pose7', 3.5),
    ('pose8','emote-pose8', 3.5),
    ('pose1','emote-pose1', 3.5),
    ('pose5','emote-pose5', 3.5),
    ('pose3','emote-pose3', 3.5),
    ('cutey','emote-cutey', 3.0),
    ('tik10','dance-tiktok10', 5.2),
    ('sing','idle_singing', 5.8),
    ('singing','idle_singing', 5.8),
    ('enthused','idle-enthusiastic', 4.0),
    ('shop','dance-shoppingcart', 4.5),
    ('russian','dance-russian', 4.7),
    ('pennywise','dance-pennywise', 5.2),
    ('tik2','dance-tiktok2', 4.9),
    ('dontstartnow','dance-tiktok2', 4.9),
    ('blackpink','dance-blackpink', 5.3),
    ('kpop','dance-blackpink', 5.3),
    ('celebrate','emoji-celebrate', 2.5),
    ('gagging','emoji-gagging', 2.3),
    ('flex','emoji-flex', 2.5),
    ('cursing','emoji-cursing', 2.4),
    ('thumbsup','emoji-thumbsup', 2.2),
    ('angry','emoji-angry', 2.0),
    ('punk','emote-punkguitar', 4.2),
    ('zombie','emote-zombierun', 5.0),
    ('sit','idle-loop-sitfloor', 6.0),
    ('fight','emote-swordfight', 5.0),
    ('ren','dance-macarena', 4.8),
    ('wei','dance-weird', 4.3),
    ('tik8','dance-tiktok8', 5.1),
    ('savage','dance-tiktok8', 5.1),
    ('tik9','dance-tiktok9', 5.4),
    ('viral','dance-tiktok9', 5.4),
    ('uwu','idle-uwu', 3.7),
    ('tik4','idle-dance-tiktok4', 4.6),
    ('sayso','idle-dance-tiktok4', 4.6),
    ('star','emote-stargazer', 4.8),
    ('pose9','emote-pose9', 3.5),
    ('boxer','emote-boxer', 4.0),
    ('guitar','idle-guitar', 5.0),
    ('penguin','dance-pinguin', 4.9),
    ('pinguin','dance-pinguin', 4.9),
    ('zero','emote-astronaut', 4.8),
    ('anime','dance-anime', 5.5),
    ('saunter','dance-anime', 5.5),
    ('creepy','dance-creepypuppet', 5.3),
    ('watch','emote-creepycute', 4.2),
    ('revelations','emote-headblowup', 3.5),
    ('revelation','emote-headblowup', 3.5),
    ('bashful','emote-shy2', 3.2),
    ('arabesque','emote-pose10', 3.5),
    ('pose10','emote-pose10', 3.5),
    ('party','emote-celebrate', 2.5),
    ('skating','emote-iceskating', 5.4),
    ('scritchy','idle-wild', 3.7),
    ('bitnervous','idle-nervous', 3.1),
    ('nervous','idle-nervous', 3.1),
    ('timejump','emote-timejump', 4.2),
    ('jump','emote-timejump', 4.2),
    ('jingle','dance-jinglebell', 5.2),
    ('hyped','emote-hyped', 3.0),
    ('sleigh','emote-sleigh', 5.5),
    ('surprise','emote-pose6', 2.5),
    ('repose','sit-relaxed', 5.0),
    ('kawaii','dance-kawai', 5.3),
    ('touch','dance-touch', 4.5),
    ('gift','emote-gift', 3.5),
    ('pushit','dance-employee', 4.7),
    ('salute','emote-cutesalute', 3.0),
    ('launch','emote-launch', 5.0)
]


async def send_emote_and_wait(highrise, emote_id, user_id):
    await highrise.send_emote(emote_id, user_id)
    duration = emote_durations.get(emote_id, 0.5)  # Default duration if not specified
    await asyncio.sleep(duration)  # Wait for the duration of the emote

async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
    emote_id = ""
    
    for emote in emote_list:
        if emote[0].lower() == emote_name.lower():
            emote_id = emote[1]
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
        try:
            # Start the emote and wait for it to finish before sending the next
            await send_emote_and_wait(self.highrise, emote_id, user.id)

            # Check user position again after sending the emote
            room_users = (await self.highrise.get_room_users()).content
            user_in_room = False
            
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    user_in_room = True
                    break
            
            if not user_in_room:
                break  # Exit loop if user is no longer in the room

        except Exception as e:
            await self.highrise.send_whisper(user.id, f"✅️{user.username} Siga <@RayMG> 🤍 Hastag : #RayMG ✅️")
            return
