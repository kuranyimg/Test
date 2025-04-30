from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task
from highrise import BaseBot

# قائمة الإيموجيات الموحدة
emote_list: list[tuple[str, str]] = [
    # أمثلة من قائمة 1
    ('1', 'dance-wrong'), ('2', 'emote-fashionista'), ('3', 'emote-gravity'),
    ('4', 'dance-icecream'), ('106', 'idle_layingdown'), ('107', 'emote-ghost-idle'),
    ('97', 'emote-looping'),
    # أمثلة من قائمة 2
    ('Rest', 'sit-idle-cute'), ('Zombie', 'idle_zombie'), ('Relaxed', 'idle_layingdown2'),
    ('Attentive', 'idle_layingdown'), ('Sleepy', 'idle-sleep'), ('Pouty Face', 'idle-sad'),
    ('Yes', 'emote-yes'), ('Hello', 'emote-hello'), ('Laugh', 'emote-laughing'),
]

async def loop(self: BaseBot, user: User, message: str) -> None:
    # استخراج اسم الإيموجي من الرسالة
    try:
        splited_message = message.split(" ")
        emote_name = " ".join(splited_message[1:]).strip()
        if not emote_name:
            raise ValueError
    except:
        await self.highrise.chat("يرجى كتابة الأمر بهذا الشكل: /loop <emote name أو رقم>")
        return

    # البحث عن الإيموجي في القائمة
    emote_id = ""
    for emote in emote_list:
        if emote[0].lower() == emote_name.lower() or emote[1].lower() == emote_name.lower():
            emote_id = emote[1]
            break

    if not emote_id:
        await self.highrise.chat("الإيموجي غير موجود أو غير متوفر.")
        return

    # الحصول على موقع المستخدم
    user_position = None
    room_users = (await self.highrise.get_room_users()).content
    for room_user, position in room_users:
        if room_user.id == user.id:
            user_position = position
            start_position = position
            break

    if user_position is None:
        await self.highrise.chat("لم يتم العثور على المستخدم.")
        return

    # إلغاء أي لوب سابق لهذا المستخدم
    taskgroup = self.highrise.tg
    for task in list(taskgroup._tasks):
        if task.get_name() == user.username:
            task.cancel()

    await self.highrise.chat(f"تشغيل تكرار الإيموجي @{user.username}: {emote_name}")

    # دالة التكرار الداخلي
    async def loop_emote():
        while True:
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except:
                await self.highrise.chat(f"عذرًا، @{user.username} هذا الإيموجي غير مجاني أو لا تملكه.")
                return
            await asyncio.sleep(10)

            # التحقق من موقع المستخدم
            current_users = (await self.highrise.get_room_users()).content
            for u, pos in current_users:
                if u.id == user.id:
                    if pos != start_position:
                        await self.highrise.chat(f"تم إيقاف التكرار لأنك غيّرت موقعك، @{user.username}.")
                        return
                    break
            else:
                await self.highrise.chat(f"تم إيقاف التكرار لأنك غادرت الغرفة، @{user.username}.")
                return

    # بدء التكرار وتسمية التاسك باسم المستخدم
    task = taskgroup.create_task(coro=loop_emote())
    task.set_name(user.username)

async def stop_loop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    for task in list(taskgroup._tasks):
        if task.get_name() == user.username:
            task.cancel()
            await self.highrise.chat(f"تم إيقاف التكرار، @{user.username}.")
            return
    await self.highrise.chat(f"لا يوجد تكرار نشط لك، @{user.username}.")
