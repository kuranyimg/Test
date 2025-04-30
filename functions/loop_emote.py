import asyncio
from highrise import BaseBot
from highrise.models import User

# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
    (['1', 'wrong', 'dance-wrong'], 'dance-wrong', 10),
    (['2', 'fashion', 'fashionista'], 'emote-fashionista', 15),
    (['3', 'gravity'], 'emote-gravity', 10),
    (['4', 'icecream', 'dance-icecream'], 'dance-icecream', 20),
    (['106', 'layingdown', 'rest'], 'idle_layingdown', 30),
    (['107', 'ghost'], 'emote-ghost-idle', 25),
    (['97', 'looping'], 'emote-looping', 30),
    (['sit', 'rest', 'cute'], 'sit-idle-cute', 17.06),
    (['zombie'], 'idle_zombie', 28.75),
    (['relaxed', 'layingdown2'], 'idle_layingdown2', 15.55),
    (['attentive'], 'idle_layingdown', 15.58),
    (['sleepy'], 'idle-sleep', 22.62),
    (['pouty', 'sadface'], 'idle-sad', 24.38),
    (['posh'], 'idle-posh', 21.85),
    (['sleepy loop'], 'idle-loop-tired', 21.95),
    (['tap loop'], 'idle-loop-tapdance', 6.26),
    (['floor sit'], 'idle-loop-sitfloor', 22.32),
    (['shy'], 'idle-loop-shy', 16.47),
    (['bummed'], 'idle-loop-sad', 6.05),
    (['chillin'], 'idle-loop-happy', 18.79),
    (['annoyed'], 'idle-loop-annoyed', 17.06),
    (['aerobics'], 'idle-loop-aerobics', 8.51),
    (['ponder'], 'idle-lookup', 22.34),
    (['hero pose'], 'idle-hero', 21.87),
    (['relaxing'], 'idle-floorsleeping2', 17.25),
    (['cozy'], 'idle-floorsleeping', 10.00),
    (['enthused'], 'idle-enthusiastic', 15.94),
    (['boogie'], 'idle-dance-swinging', 13.20),
    (['feel the beat'], 'idle-dance-headbobbing', 25.37),
    (['irritated'], 'idle-angry', 25.43),
    (['yes'], 'emote-yes', 2.57),
    (['fly', 'wings'], 'emote-wings', 13.13),
    (['wave'], 'emote-wave', 2.69),
    (['tired'], 'emote-tired', 4.61),
    (['think'], 'emote-think', 3.69),
    (['theatrical'], 'emote-theatrical', 8.59),
    (['tap dance'], 'emote-tapdance', 11.06),
    (['super run'], 'emote-superrun', 6.27),
    (['super punch'], 'emote-superpunch', 3.75),
    (['sumo'], 'emote-sumo', 10.87),
    (['thumb suck'], 'emote-suckthumb', 4.19),
    (['splits'], 'emote-splitsdrop', 4.47),
    (['snowball'], 'emote-snowball', 5.23),
    (['snow angel'], 'emote-snowangel', 6.22),
    (['secret handshake'], 'emote-secrethandshake', 3.88),
    (['sad'], 'emote-sad', 5.41),
    (['rope pull'], 'emote-ropepull', 8.77),
    (['roll'], 'emote-roll', 3.56),
    (['rofl'], 'emote-rofl', 6.31),
    (['robot'], 'emote-robot', 7.61),
    (['rainbow'], 'emote-rainbow', 2.81),
    (['proposing'], 'emote-proposing', 4.28),
    (['peekaboo'], 'emote-peekaboo', 3.63),
    (['peace'], 'emote-peace', 5.76),
    (['panic'], 'emote-panic', 2.85),
    (['no'], 'emote-no', 2.70),
    (['ninja run'], 'emote-ninjarun', 4.75),
    (['night fever'], 'emote-nightfever', 5.49),
    (['fail'], 'emote-monster_fail', 4.63),
    (['model'], 'emote-model', 6.49),
    (['flirty'], 'emote-lust', 4.66),
    (['level up'], 'emote-levelup', 6.05),
    (['laugh'], 'emote-laughing', 2.69),
    (['kiss'], 'emote-kiss', 2.39),
    (['kick'], 'emote-kicking', 4.87),
    (['jump'], 'emote-jumpb', 3.58),
    (['judo'], 'emote-judochop', 2.43),
    (['jetpack'], 'emote-jetpack', 16.76),
    (['hug'], 'emote-hugyourself', 4.99),
    (['hot'], 'emote-hot', 4.35),
    (['hero'], 'emote-hero', 5.00),
    (['hello'], 'emote-hello', 2.73),
    (['headball'], 'emote-headball', 10.07),
    (['harlem'], 'emote-harlemshake', 13.56),
    (['happy'], 'emote-happy', 3.48),
    (['handstand'], 'emote-handstand', 4.02),
    (['greedy'], 'emote-greedy', 4.64),
    (['graceful'], 'emote-graceful', 3.75),
    (['moonwalk'], 'emote-gordonshuffle', 8.05),
    (['ghost float'], 'emote-ghost-idle', 19.57),
    (['gangnam'], 'emote-gangnam', 7.28),
]

# قائمة الإيموجيات الثابتة التي لا تحتاج تكرار
non_looping_emotes = {
    'idle_layingdown', 'idle-layingdown', 'idle-layingdown2',
    'idle-sleep', 'idle-sad', 'idle-posh', 'idle-loop-tired',
    'idle-loop-sitfloor', 'idle-loop-shy', 'idle-loop-sad',
    'idle-loop-happy', 'idle-loop-annoyed', 'idle-loop-aerobics',
    'idle-lookup', 'idle-hero', 'idle-floorsleeping', 'idle-floorsleeping2',
    'idle-enthusiastic', 'idle-dance-swinging', 'idle-dance-headbobbing',
    'idle-angry', 'sit-idle-cute', 'idle_zombie'
}

# المهام النشطة لكل مستخدم
user_loops: dict[str, asyncio.Task] = {}

# تفعيل التكرار أو التشغيل مرة واحدة حسب نوع الإيموجي
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

    # أوقف أي تكرار سابق
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]

    # إذا الإيموجي لا تحتاج تكرار
    if emote_id in non_looping_emotes:
        await self.highrise.send_emote(emote_id, user.id)
        await self.highrise.chat(f"@{user.username} is now doing '{emote_id}' (static emote).")
        return

    # الإيموجي المتكررة
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

# إيقاف التكرار
async def stop_loop(self: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await self.highrise.chat(f"@{user.username}, your emote loop has been stopped.")
    else:
        await self.highrise.chat(f"@{user.username}, you have no active loop to stop.")

# تفعيل الإيموجي عند كتابة اسمه مباشرة
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    message = message.strip().lower()
    found = next((emote for emote in emote_list if message in [k.lower() for k in emote[0]]), None)
    if found:
        await loop(self, user, f"loop {message}")
