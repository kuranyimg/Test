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
    ('97', 'emote-looping', 30),emotes = [
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
    ('I Believe I Can Fly', 'emote-wings', 13.134487),
    ('The Wave', 'emote-wave', 2.690873),
    ('Tired', 'emote-tired', 4.61063),
    ('Think', 'emote-think', 3.691104),
    ('Theatrical', 'emote-theatrical', 8.591869),
    ('Tap Dance', 'emote-tapdance', 11.057294),
    ('Super Run', 'emote-superrun', 6.273226),
    ('Super Punch', 'emote-superpunch', 3.751054),
    ('Sumo Fight', 'emote-sumo', 10.868834),
    ('Thumb Suck', 'emote-suckthumb', 4.185944),
    ('Splits Drop', 'emote-splitsdrop', 4.46931),
    ('Snowball Fight!', 'emote-snowball', 5.230467),
    ('Snow Angel', 'emote-snowangel', 6.218627),
    ('Shy', 'emote-shy', 4.477567),
    ('Secret Handshake', 'emote-secrethandshake', 3.879024),
    ('Sad', 'emote-sad', 5.411073),
    ('Rope Pull', 'emote-ropepull', 8.769656),
    ('Roll', 'emote-roll', 3.560517),
    ('ROFL!', 'emote-rofl', 6.314731),
    ('Robot', 'emote-robot', 7.607362),
    ('Rainbow', 'emote-rainbow', 2.813373),
    ('Proposing', 'emote-proposing', 4.27888),
    ('Peekaboo!', 'emote-peekaboo', 3.629867),
    ('Peace', 'emote-peace', 5.755004),
    ('Panic', 'emote-panic', 2.850966),
    ('No', 'emote-no', 2.703034),
    ('Ninja Run', 'emote-ninjarun', 4.754721),
    ('Night Fever', 'emote-nightfever', 5.488424),
    ('Monster Fail', 'emote-monster_fail', 4.632708),
    ('Model', 'emote-model', 6.490173),
    ('Flirty Wave', 'emote-lust', 4.655965),
    ('Level Up!', 'emote-levelup', 6.0545),
    ('Amused', 'emote-laughing2', 5.056641),
    ('Laugh', 'emote-laughing', 2.69161),
    ('Kiss', 'emote-kiss', 2.387175),
    ('Super Kick', 'emote-kicking', 4.867992),
    ('Jump', 'emote-jumpb', 3.584234),
    ('Judo Chop', 'emote-judochop', 2.427442),
    ('Imaginary Jetpack', 'emote-jetpack', 16.759457),
    ('Hug Yourself', 'emote-hugyourself', 4.992751),
    ('Sweating', 'emote-hot', 4.353037),
    ('Hero Entrance', 'emote-hero', 4.996096),
    ('Hello', 'emote-hello', 2.734844),
    ('Headball', 'emote-headball', 10.073119),
    ('Harlem Shake', 'emote-harlemshake', 13.558597),
    ('Happy', 'emote-happy', 3.483462),
    ('Handstand', 'emote-handstand', 4.015678),
    ('Greedy Emote', 'emote-greedy', 4.639828),
    ('Graceful', 'emote-graceful', 3.7498),
    ('Moonwalk', 'emote-gordonshuffle', 8.052307),
    ('Ghost Float', 'emote-ghost-idle', 19.570492),
    ('Gangnam Style', 'emote-gangnam', 7.275486),
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
