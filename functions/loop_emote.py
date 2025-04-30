from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task
from highrise import BaseBot

# قائمة الإيموجيات مع المدة بالثواني
emote_list: list[tuple[str, str, int]] = [
    ('1', 'dance-wrong', 10),
    ('2', 'emote-fashionista', 15),
    ('3', 'emote-gravity', 10),
    ('4', 'dance-icecream', 20),
    ('106', 'idle_layingdown', 30),
    ('107', 'emote-ghost-idle', 25),
    ('97', 'emote-looping', 30),
    ('Rest', 'sit-idle-cute', 20),
    ('Zombie', 'idle_zombie', 15),
    ('Relaxed', 'idle_layingdown2', 30),
    ('Attentive', 'idle_layingdown', 25),
    ('Sleepy', 'idle-sleep', 30),
    ('Pouty Face', 'idle-sad', 20),
    ('Yes', 'emote-yes', 10),
    ('Hello', 'emote-hello', 15),
    ('Laugh', 'emote-laughing', 20),
]

# تخزين المهام حسب المستخدم
active_loops: dict[str, Task] = {}

# تكرار الإيموجي بناءً على المدة
async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
    emote_id = ""
    duration = 10

    for emote in emote_list:
        if emote[0].lower() == emote_name.lower() or emote[1].lower() == emote_name.lower():
            emote_id = emote[1]
            duration = emote[2]
            break

    if emote_id == "":
        await self.highrise.chat(f"@{user.username} Invalid emote.")
        return

    await self.highrise.chat(f"@{user.username} is now looping {emote_name} every {duration} seconds.")

    try:
        while True:
            await self.highrise.send_emote(emote_id, user.id)
            await asyncio.sleep(duration)
    except asyncio.CancelledError:
        await self.highrise.chat(f"@{user.username} has stopped looping {emote_name}.")

# التحقق من الرسائل وتفعيل أو إيقاف التكرار
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str) -> None:
    lower_msg = message.strip().lower()

    # إيقاف التكرار
    if lower_msg == "stop":
        task = active_loops.get(user.id)
        if task:
            task.cancel()
            del active_loops[user.id]
        else:
            await self.highrise.chat(f"@{user.username} you have no active loop.")
        return

    # استخراج اسم الإيموجي
    parts = message.strip().split(" ")
    if lower_msg.startswith("loop ") or lower_msg.startswith("Loop "):
        emote_name = " ".join(parts[1:])
    else:
        emote_name = message.strip()

    # إيقاف أي تكرار قديم للمستخدم
    old_task = active_loops.get(user.id)
    if old_task:
        old_task.cancel()

    # بدء التكرار الجديد
    task = asyncio.create_task(loop_emote(self, user, emote_name))
    task.set_name(f"loop-{user.username}")
    active_loops[user.id] = task
