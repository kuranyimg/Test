import asyncio
from highrise import BaseBot
from highrise.models import User

# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
    (["kawaii", "Kawaii", "1"], "dance-kawai", 10.851),
    (["hyped", "Hyped", "2"], "emote-hyped", 7.622),
    (["levitate", "Levitate", "3"], "emoji-halo", 6.522),
    (["applause", "Applause", "4"], "emote-applause", 6.0),
    (["stinky", "Stinky", "5"], "emote-smelly", 5.5),
    (["eyeroll", "Eyeroll", "6"], "emote-eyeroll", 5.8),
    (["kissy", "Kissy", "7"], "emoji-kiss", 6.5),
    (["yawn", "Yawn", "8"], "emoji-yawn", 6.3),
    (["giggle", "Giggle", "9"], "emote-giggle", 5.7),
    (["bored", "Bored", "10"], "emote-bored", 6.2),
    # إضافة باقي الإيموجيات هنا بنفس الطريقة
]

# تخزين المهام المتكررة لكل مستخدم
user_loops = {}

# تفعيل التكرار
async def loop(self: BaseBot, user: User, message: str):
    parts = message.strip().split(" ", 1)
    if len(parts) < 2:
        await self.highrise.chat("يرجى كتابة اسم الإيموجي بعد 'loop'.")
        return
    emote_name = parts[1].strip().lower()

    selected = next(
        (emote for emote in emote_list if emote_name in [k.lower() for k in emote[0]]), None)

    if not selected:
        await self.highrise.chat("الإيموجي غير موجود.")
        return

    _, emote_id, duration = selected

    # إيقاف أي تكرار سابق
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]

    # تنفيذ التكرار
    async def emote_loop():
        try:
            await self.highrise.chat(f"بدأ @{user.username} تكرار الإيموجي '{emote_id}' كل {duration:.1f} ثانية.")
            while True:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(emote_loop())
    user_loops[user.id] = task

# إيقاف التكرار
async def stop_loop(self: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await self.highrise.chat(f"@{user.username} تم إيقاف تكرار الإيموجي الخاص بك.")
    else:
        await self.highrise.chat(f"@{user.username} ليس لديك أي تكرار نشط.")

# تفعيل الإيموجي تلقائيًا عند كتابة اسمه مباشرة
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    message = message.strip().lower()
    found = next((emote for emote in emote_list if message in [k.lower() for k in emote[0]]), None)
    if found:
        await loop(self, user, f"loop {message}")
