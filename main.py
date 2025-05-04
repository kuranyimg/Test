import asyncio
from functions.loop_emote import handle_loop_command, stop_emote_loop, handle_user_movement, handle_user_stopped
from functions.vip_manager import add_vip, remove_vip, is_vip, is_owner
from functions.state import bot_state

# تعريف الوظائف هنا
class HighriseBot:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id
        self.is_active = True
        self.vips = []

    async def on_chat(self, user, message):
        """
        التعامل مع رسائل الدردشة، تنفيذ أوامر الإيموتات أو إيقاف التكرار
        """
        if message.lower() in ['stop', 'Stop']:
            stop_emote_loop(user.id)
            return

        await handle_loop_command(self, user, message)

    async def on_user_move(self, user):
        """
        التعامل مع حركة المستخدم
        """
        handle_user_movement(user.id)

    async def on_user_stop(self, user):
        """
        التعامل مع توقف المستخدم
        """
        handle_user_stopped(user.id)

    async def on_whisper(self, sender, receiver, message):
        """
        التعامل مع الرسائل الخاصة بين المستخدمين
        """
        if message.startswith("vip@"):
            username = message.split('@')[1]
            if sender.username == "raybm":  # التأكد من أن المرسل هو المالك
                add_vip(username)
                return "تم إضافة المستخدم إلى قائمة الـ VIP"
            else:
                return "ليس لديك صلاحية لإضافة VIP"
        
        # إضافة أوامر أخرى إذا لزم الأمر

    async def run(self):
        """
        تشغيل البوت
        """
        while self.is_active:
            await asyncio.sleep(1)
            # عمليات أخرى للبوت مثل التحقق من حالة الاتصال أو الاستماع لرسائل جديدة

# استخدام البوت
bot = HighriseBot(username="raybm", user_id=1234)

# تعريف دالة لبدء البوت وتشغيله
async def start_bot():
    await bot.run()

# تشغيل البوت
asyncio.run(start_bot())
