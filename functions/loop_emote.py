import asyncio
from highrise import BaseBot
from highrise.models import User

# قائمة الإيموجيات: [أسماء مفتاحية، ID، مدة]
emote_list: list[tuple[list[str], str, float]] = [
    (['cozy nap'], 'idle-floorsleeping', 13.94),
    (['sleepy'], 'idle-sleep', 22.62),
    (['relaxed', 'layingdown2'], 'idle_layingdown2', 21.55),
    (['layingdown', 'rest'], 'idle_layingdown', 30),
    (['hero'], 'emote-hero', 5.00),
    # أضف المزيد من الإيموجيات هنا...
]

# إيموجيات لا تحتاج للتكرار — تُفعّل مرة وتستمر
one_time_emotes = {
    'idle-floorsleeping',
    'idle-sleep',
    'idle_layingdown2',
    'idle_layingdown',
    # أضف المزيد هنا إذا أردت
}

# حفظ المهام النشطة لكل مستخدم
user_loops: dict[str, asyncio.Task] = {}

# تفعيل الإيموجي مع التكرار أو بدونه
async def loop(self: BaseBot, user: User, message: str):
    parts = message.strip().split(" ", 1)
    if len(parts) < 2:
        await self.highrise.chat("Please provide an emote name after 'loop'.")
        return

    emote_name = parts[1].strip().lower()

    selected = next(
        (emote for emote in emote_list if emote_name in [k.lower() for k in emote[0]]), None)

    if not selected:
        await self.highrise.chat("Invalid emote name.")
        return

    _, emote_id, duration = selected

    # إيقاف أي إيموجي مفعّل مسبقًا
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]

    # إذا كانت الإيموجي من النوع الذي لا يحتاج للتكرار
    if emote_id in one_time_emotes:
        await self.highrise.send_emote(emote_id, user.id)
        await self.highrise.chat(f"@{user.username} started '{emote_id}' (one-time emote).")
        return

    # تكرار الإيموجي إذا كان يتطلب ذلك
    async def emote_loop():
        try:
            await self.highrise.chat(f"@{user.username} started looping '{emote_id}' every {duration:.1f} seconds.")
            while True:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(emote_loop())
    user_loops[user.id] = task

# إيقاف الإيموجي
async def stop_loop(self: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await self.highrise.chat(f"@{user.username}, your emote loop has been stopped.")
    else:
        await self.highrise.chat(f"@{user.username}, you have no active loop to stop.")

# تفعيل الإيموجي من خلال الرسالة مباشرة
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    message = message.strip().lower()
    found = next((emote for emote in emote_list if message in [k.lower() for k in emote[0]]), None)
    if found:
        await loop(self, user, f"loop {message}")
