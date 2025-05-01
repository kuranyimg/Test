import asyncio
from highrise import BaseBot
from highrise.models import 
# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
    "1", "kawaii": {"name": "Kawaii Go Go", "id": "dance-kawai", "duration": 10.851},
    "2", "hyped": {"name": "Hyped", "id": "emote-hyped", "duration": 7.622},
    "3", "levitate": {"name": "Levitate", "id": "emoji-halo", "duration": 6.522},
    "4", "applause": {"name": "Applause", "id": "emote-applause", "duration": 6.0},
    "5", "stinky": {"name": "Stinky", "id": "emote-smelly", "duration": 5.5},
    "6", "eyeroll": {"name": "Eyeroll", "id": "emote-eyeroll", "duration": 5.8},
    "7", "kissy": {"name": "Kissy Face", "id": "emoji-kiss", "duration": 6.5},
    "8", "yawn": {"name": "Yawn", "id": "emoji-yawn", "duration": 6.3},
    "9", "giggle": {"name": "Giggle", "id": "emote-giggle", "duration": 5.7},
    "10", "bored": {"name": "Bored", "id": "emote-bored", "duration": 6.2},
    "11", "flirty": {"name": "Flirty", "id": "emote-flirty", "duration": 6.4},
    "12", "surprised": {"name": "Surprised", "id": "emote-surprised", "duration": 6.1},
    "13", "sad": {"name": "Sad", "id": "emote-sad", "duration": 6.8},
    "14", "angry": {"name": "Angry", "id": "emote-angry", "duration": 6.0},
    "15", "laughing": {"name": "Laughing", "id": "emoji-laugh", "duration": 7.3},
    "16", "dance": {"name": "Dance", "id": "emoji-dance", "duration": 8.2},
    "17", "wave": {"name": "Wave", "id": "emoji-wave", "duration": 5.5},
    "18", "heart": {"name": "Heart", "id": "emoji-heart", "duration": 4.9},
    "19", "clap": {"name": "Clap", "id": "emoji-clap", "duration": 6.0},
    "20", "cheer": {"name": "Cheer", "id": "emoji-cheer", "duration": 7.0},
    "21", "silly": {"name": "Silly", "id": "emoji-silly", "duration": 5.6},
    "22", "cool": {"name": "Cool", "id": "emoji-cool", "duration": 6.2},
    "23", "confused": {"name": "Confused", "id": "emoji-confused", "duration": 6.0},
    "24", "angry": {"name": "Angry", "id": "emoji-angry", "duration": 6.7},
    "25", "sleepy": {"name": "Sleepy", "id": "emoji-sleepy", "duration": 6.3},
    "26", "crying": {"name": "Crying", "id": "emoji-crying", "duration": 7.5},
    "27", "shy": {"name": "Shy", "id": "emoji-shy", "duration": 5.8},
    "28", "wink": {"name": "Wink", "id": "emoji-wink", "duration": 6.1},
    "29", "thumbsup": {"name": "Thumbsup", "id": "emoji-thumbsup", "duration": 5.9},
    "30", "thumbsdown": {"name": "Thumbsdown", "id": "emoji-thumbsdown", "duration": 6.4},
    "31", "hug": {"name": "Hug", "id": "emoji-hug", "duration": 7.1},
    "32", "smile": {"name": "Smile", "id": "emoji-smile", "duration": 5.4},
    "33", "dance2": {"name": "Dance 2", "id": "emoji-dance2", "duration": 8.3},
    "34", "thinking": {"name": "Thinking", "id": "emoji-thinking", "duration": 6.6},
    "35", "facepalm": {"name": "Facepalm", "id": "emoji-facepalm", "duration": 5.3},
    "36", "praise": {"name": "Praise", "id": "emoji-praise", "duration": 7.2},
    "37", "excited": {"name": "Excited", "id": "emoji-excited", "duration": 6.7},
    "38", "victory": {"name": "Victory", "id": "emoji-victory", "duration": 7.0},
    "39", "cheeky": {"name": "Cheeky", "id": "emoji-cheeky", "duration": 5.9},
    "40", "magic": {"name": "Magic", "id": "emoji-magic", "duration": 6.1},
    "41", "peek": {"name": "Peek", "id": "emoji-peek", "duration": 5.2},
    "42", "sad2": {"name": "Sad 2", "id": "emoji-sad2", "duration": 6.0},
    "43", "peace": {"name": "Peace", "id": "emoji-peace", "duration": 6.5},
    "44", "surprise2": {"name": "Surprise 2", "id": "emoji-surprise2", "duration": 6.3},
    "45", "yay": {"name": "Yay", "id": "emoji-yay", "duration": 7.4},
    "46", "love": {"name": "Love", "id": "emoji-love", "duration": 7.1},
    "47", "hype": {"name": "Hype", "id": "emoji-hype", "duration": 7.0},
    "48", "heartbroken": {"name": "Heartbroken", "id": "emoji-heartbroken", "duration": 6.9},
    "49", "woot": {"name": "Woot", "id": "emoji-woot", "duration": 7.6},
    "50", "joy": {"name": "Joy", "id": "emoji-joy", "duration": 6.8},
}

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
