import asyncio
from highrise import BaseBot
from highrise.models import User

# قائمة الإيموجيات مع مدتها بالثواني
emote_list: list[tuple[str, str, float]] = [
    ('Rest', 'sit-idle-cute', 17.062613),
    ('Zombie', 'idle_zombie', 28.754937),
    ('Relaxed', 'idle_layingdown2', 21.546653),
    ('Attentive', 'idle_layingdown', 24.585168),
    ('Sleepy', 'idle-sleep', 22.620446),
    ('Pouty Face', 'idle-sad', 24.377214),
    ('Posh', 'idle-posh', 21.851256),
    ('Sleepy', 'idle-loop-tired', 21.959007),
    ('Tap Loop', 'idle-loop-tapdance', 6.261593),
    ('Sit', 'idle-loop-sitfloor', 22.321055),
    ('Shy', 'idle-loop-shy', 16.47449),
    ('Bummed', 'idle-loop-sad', 6.052999),
    ('Chillin\'', 'idle-loop-happy', 18.798322),
    ('Annoyed', 'idle-loop-annoyed', 17.058522),
    ('Aerobics', 'idle-loop-aerobics', 8.507535),
    ('Ponder', 'idle-lookup', 22.339865),
    ('Hero Pose', 'idle-hero', 21.877099),
    ('Relaxing', 'idle-floorsleeping2', 17.253372),
    ('Cozy Nap', 'idle-floorsleeping', 13.935264),
    ('Enthused', 'idle-enthusiastic', 15.941537),
    ('Boogie Swing', 'idle-dance-swinging', 13.198551),
    ('Feel The Beat', 'idle-dance-headbobbing', 25.367458),
    ('Irritated', 'idle-angry', 25.427848),
    ('Yes', 'emote-yes', 2.565001),
    ('Hello', 'emote-hello', 2.734844),
    ('Laugh', 'emote-laughing', 2.69161),
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
