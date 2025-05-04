import asyncio
from highrise import User, Position
from highrise.bot import BaseBot

class Emote:
    name: str
    id: str
    duration: float
    is_free: bool

    def __init__(self, name: str, id: str, duration: float, is_free: bool):
        self.name = name
        self.id = id
        self.duration = duration
        self.is_free = is_free


# قائمة الإيموتات
emotes: list[Emote] = [
    Emote(name="Rest", id="sit-idle-cute", duration=17.062613, is_free=False),
    Emote(name="Zombie", id="idle_zombie", duration=28.754937, is_free=False),
    Emote(name="Relaxed", id="idle_layingdown2", duration=21.546653, is_free=False),
    Emote(name="Attentive", id="idle_layingdown", duration=24.585168, is_free=False),
    Emote(name="Tap Loop", id="idle-loop-tapdance", duration=6.261593, is_free=False),
    Emote(name="Sit", id="idle-loop-sitfloor", duration=22.321055, is_free=True),
    Emote(name="Shy", id="idle-loop-shy", duration=16.47449, is_free=False),
    Emote(name="Bummed", id="idle-loop-sad", duration=6.052999, is_free=False),
    Emote(name="Chillin'", id="idle-loop-happy", duration=18.798322, is_free=False),
    Emote(name="Annoyed", id="idle-loop-annoyed", duration=17.058522, is_free=False),
    Emote(name="Aerobics", id="idle-loop-aerobics", duration=8.507535, is_free=False),
    Emote(name="Ponder", id="idle-lookup", duration=22.339865, is_free=False),
    Emote(name="Hero Pose", id="idle-hero", duration=21.877099, is_free=False),
    Emote(name="Relaxing", id="idle-floorsleeping2", duration=17.253372, is_free=False),
    Emote(name="Cozy", id="idle-floorsleeping", duration=13.935264, is_free=False),
    Emote(name="Enthused", id="idle-enthusiastic", duration=15.941537, is_free=True),
    Emote(name="Boogie Swing", id="idle-dance-swinging", duration=13.198551, is_free=False),
    Emote(name="Feel The Beat", id="idle-dance-headbobbing", duration=25.367458, is_free=False),
    Emote(name="Irritated", id="idle-angry", duration=25.427848, is_free=False),
    Emote(name="The Wave", id="emote-wave", duration=2.690873, is_free=True),
    Emote(name="Tired", id="emote-tired", duration=4.61063, is_free=True),
    Emote(name="Think", id="emote-think", duration=3.691104, is_free=False),
    Emote(name="Theatrical", id="emote-theatrical", duration=8.591869, is_free=False),
    Emote(name="Tap Dance", id="emote-tapdance", duration=11.057294, is_free=False)
]

class LoopEmoteBot(BaseBot):
    async def on_message(self, message: str, user: User) -> None:
        # إذا كان الرسالة تبدأ بكلمة "loop" أو أي من الأوامر الأخرى لتكرار الإيموت
        if message.lower().startswith("loop") or message.lower().startswith("!loop") or message.lower().startswith("-loop"):
            emote_name = message[5:].strip()  # الحصول على اسم الإيموت بعد كلمة "loop"
            emote = self.get_emote_by_name(emote_name)
            if emote:
                await self.loop_emote(user, emote)
            else:
                await self.send_message(user, "إيموت غير معروف.")
        
        # لتشغيل الإيموت عند كتابته فقط (بدون تكرار)
        else:
            emote = self.get_emote_by_name(message)
            if emote:
                await self.play_emote(user, emote)
            else:
                await self.send_message(user, "إيموت غير معروف.")

    async def loop_emote(self, user: User, emote: Emote) -> None:
        """يشغل الإيموت بشكل مستمر للمستخدم"""
        while True:
            await self.play_emote(user, emote)
            await asyncio.sleep(emote.duration)  # الانتظار مدة الإيموت

    async def play_emote(self, user: User, emote: Emote) -> None:
        """لتشغيل الإيموت مرة واحدة"""
        # هنا تحتاج إلى الكود الخاص بتشغيل الإيموت في اللعبة
        # استبدل هذه الجملة بكود لتشغيل الإيموت بناءً على ID الإيموت
        print(f"{user.username} is doing {emote.name} ({emote.id})")

    def get_emote_by_name(self, name: str) -> Emote:
        """لإيجاد الإيموت بناءً على اسمه"""
        for emote in emotes:
            if emote.name.lower() == name.lower():
                return emote
        return None
