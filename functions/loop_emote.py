from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task
from highrise import BaseBot

# قائمة الإيموجيات الموحدة مع مدة التكرار
emote_list: list[tuple[str, str, int]] = [
    # (اسم الإيموجي، الاسم الكامل، مدة التكرار بالثواني)
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

# دالة لتكرار الإيموجي
async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
    emote_id = ""
    duration = 10  # القيمة الافتراضية لمدة التكرار 10 ثواني
    for emote in emote_list:
        if emote[0].lower() == emote_name.lower() or emote[1].lower() == emote_name.lower():
            emote_id = emote[1]
            duration = emote[2]  # الحصول على مدة التكرار المحددة للإيموجي
            break

    if emote_id == "":
        await self.highrise.chat("Invalid emote")
        return

    await self.highrise.chat(f"@{user.username} is looping {emote_name} for {duration} seconds.")

    # تكرار الإيموجي لمدة معينة
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        try:
            await self.highrise.send_emote(emote_id, user.id)
        except:
            await self.highrise.chat(f"Sorry, @{user.username}, this emote isn't free or you don't own it.")
            return
        await asyncio.sleep(5)  # إرسال الإيموجي كل 5 ثواني

    await self.highrise.chat(f"@{user.username}'s {emote_name} loop has ended.")

# دالة لفحص الرسائل وبدء التكرار تلقائيًا عند كتابة اسم الإيموجي أو loop
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str) -> None:
    if 'loop' in message.lower():
        # إذا كانت الرسالة تحتوي على "loop" أو "Loop"
        parts = message.split(" ")
        if len(parts) > 1:
            emote_name = " ".join(parts[1:])
        else:
            await self.highrise.chat("Please provide an emote name after the loop command.")
            return
    else:
        # إذا كانت الرسالة تحتوي على اسم إيموجي مباشرة
        emote_name = message.strip()

    await loop_emote(self, user, emote_name)

# دالة للتعامل مع الأوامر الواردة
async def command_handler(self, user: User, message: str):
    parts = message.split(" ")
    command = parts[0].lower()

    if command.startswith("-"):
        command = command[1:]

    functions_folder = "functions"
    for file_name in os.listdir(functions_folder):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            module_path = os.path.join(functions_folder, file_name)

            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the function exists in the module
            if hasattr(module, command) and callable(getattr(module, command)):
                function = getattr(module, command)
                await function(self, user, message)

    # التحقق من وجود الإيموجي في الرسالة بشكل مباشر بدون الحاجة لاستخدام /loop
    from functions.loop_emote import check_and_start_emote_loop
    await check_and_start_emote_loop(self, user, message)

    return
