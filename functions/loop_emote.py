import asyncio
from highrise import BaseBot
from highrise.models import User

# قائمة الإيموجيات مع مدتها بالثواني
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

# تخزين التكرار الجاري لكل مستخدم
user_loops: dict[str, asyncio.Task] = {}

# الدالة الرئيسية للتكرار المستمر للإيموجي
async def loop(self: BaseBot, user: User, message: str):
    parts = message.strip().split(" ", 1)
    if len(parts) < 2:
        await self.highrise.chat("Please provide an emote name after 'loop'.")
        return
    emote_name = parts[1].strip().lower()

    # إيجاد الإيموجي المناسب من القائمة
    selected = next((emote for emote in emote_list
                     if emote_name == emote[0].lower() or emote_name == emote[1].lower()), None)
    if not selected:
        await self.highrise.chat("Invalid emote name.")
        return

    _, emote_id, duration = selected

    # إيقاف التكرار السابق إن وجد
    if user.id in user_loops:
        user_loops[user.id].cancel()

    async def emote_loop():
        try:
            await self.highrise.chat(f"@{user.username} started looping '{emote_id}' every {duration} seconds.")
            while True:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(emote_loop())
    user_loops[user.id] = task

# دالة لإيقاف التكرار
async def stop_loop(self: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await self.highrise.chat(f"@{user.username}, your emote loop has been stopped.")
    else:
        await self.highrise.chat(f"@{user.username}, you have no active loop to stop.")

# دالة لفحص الرسائل بشكل مباشر بدون أمر loop
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    message = message.strip().lower()

    # هل كتب اسم إيموجي مباشرة؟
    found = next((emote for emote in emote_list
                  if message == emote[0].lower() or message == emote[1].lower()), None)
    if found:
        await loop(self, user, f"loop {message}")
