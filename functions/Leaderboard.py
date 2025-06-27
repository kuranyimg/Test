import json
import os
import re
from datetime import datetime, timedelta

def get_data_path(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

LEADERBOARD_FILE = get_data_path("leaderboard.json")
REMOVED_USERS_FILE = get_data_path("removed_users.json")

def format_duration(seconds: int) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days > 0:
        return f"{days}d{hours}h" if hours > 0 else f"{days}d"
    elif hours > 0:
        return f"{hours}h{minutes}m" if minutes > 0 else f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return f"{seconds}s"

def format_number(value: int) -> str:
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}b"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(value)

def format_xp(value: int) -> str:
    return f"{format_number(value)} XP"

def load_leaderboard_data():
    def fix(val):
        if isinstance(val, dict):
            return 0
        return val

    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                raw = json.load(f)
                for key in ["most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"]:
                    if key not in raw:
                        raw[key] = {}
                    else:
                        raw[key] = {k: fix(v) for k, v in raw[key].items()}
                if "last_visit" not in raw:
                    raw["last_visit"] = {}
                return raw
            except Exception:
                pass
    return {
        "most_active": {},
        "most_talkative": {},
        "most_daily_streak": {},
        "most_stayed": {},
        "all_time": {},
        "last_visit": {},
    }

def save_leaderboard_data(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_removed_users():
    if os.path.exists(REMOVED_USERS_FILE):
        with open(REMOVED_USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_removed_users(users):
    with open(REMOVED_USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def is_user_removed(data, username: str) -> bool:
    return username.lower() in load_removed_users()

def remove_user(username: str):
    users = load_removed_users()
    uname = username.lower()
    if uname not in users:
        users.append(uname)
        save_removed_users(users)
        return True
    return False

def unremove_user(username: str):
    users = load_removed_users()
    uname = username.lower()
    if uname in users:
        users.remove(uname)
        save_removed_users(users)
        return True
    return False

def get_leaderboard_menu_text():
    return (
        "📊 Leaderboard Categories:\n"
        "1. ⏳ Time Spent in Room\n"
        "2. 💬 Total Messages Sent\n"
        "3. 📅 Daily Visit Streak\n"
        "4. 🛋️ Longest Single Stay\n"
        "5. 🏅 All-Time Room Legends\n"
        "Use `leaderboard <number>` or `leaderboard <name>` to view a leaderboard."
    )

def _format_leaderboard_lines(data, choice):
    emoji_titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "all_time": "🏅 All-Time Room Legends",
    }
    title = emoji_titles.get(choice, choice)
    category_data = data.get(choice, {})
    filtered = {u: v for u, v in category_data.items() if not is_user_removed(data, u)}
    sorted_users = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:10]

    if not sorted_users:
        return [f"📉 No data yet for {title}."]

    lines = [f"🏆 {title} Leaderboard:"]
    for i, (user, value) in enumerate(sorted_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        val = (
            format_duration(int(value)) if choice in ["most_active", "most_stayed"]
            else format_number(int(value)) if choice in ["most_talkative", "most_daily_streak"]
            else format_xp(int(value)) if choice == "all_time"
            else str(value)
        )
        lines.append(f"{medal} @{user} – {val}")
    return lines

def get_leaderboard_text_by_choice(data, choice: str, public=False):
    name_map = {
        "1": "most_active",
        "2": "most_talkative",
        "3": "most_daily_streak",
        "4": "most_stayed",
        "5": "all_time",
    }
    choice = name_map.get(choice.lower(), choice.lower())
    lines = _format_leaderboard_lines(data, choice)
    if public or sum(len(line) for line in lines) < 400:
        return "\n".join(lines)
    header = lines[0]
    first_half = lines[1:6]
    second_half = lines[6:]
    return (header, "\n".join([header] + first_half), "\n".join([header] + second_half))

def get_user_rank_text(data, username, category):
    cat_data = data.get(category, {})
    filtered = {u: v for u, v in cat_data.items() if not is_user_removed(data, u)}
    sorted_users = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    for i, (user, value) in enumerate(sorted_users, 1):
        if user.lower() == username.lower():
            val = (
                format_duration(int(value)) if category in ["most_active", "most_stayed"]
                else format_number(int(value)) if category in ["most_talkative", "most_daily_streak"]
                else format_xp(int(value)) if category == "all_time"
                else str(value)
            )
            return i, user, val
    return None, username, "0"

def get_user_full_rank_summary(data, username):
    summary = [f"🧑 @{username}'s Top Ranks:"]
    emoji_titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "all_time": "🏅 All-Time Room Legends",
    }
    for key in ["most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"]:
        rank, _, value = get_user_rank_text(data, username, key)
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}" if rank else "-"
        summary.append(f"{medal} {emoji_titles[key]} – {value}")
    return "\n".join(summary)

def update_leaderboard_on_chat(data, username, duration):
    if is_user_removed(data, username):
        return
    duration = int(duration)
    data["most_active"][username] = data["most_active"].get(username, 0) + duration
    if duration > data["most_stayed"].get(username, 0):
        data["most_stayed"][username] = duration
    update_all_time(data, username)

def update_leaderboard_on_message(data, username):
    if is_user_removed(data, username):
        return
    data["most_talkative"][username] = data["most_talkative"].get(username, 0) + 1
    update_all_time(data, username)

def update_leaderboard_on_join(data, username):
    if is_user_removed(data, username):
        return
    now = datetime.utcnow()
    last_seen_str = data.get("last_visit", {}).get(username)
    last_seen = None
    if last_seen_str:
        try:
            last_seen = datetime.strptime(last_seen_str, "%Y-%m-%d")
        except Exception:
            pass
    today = now.date()
    if last_seen and today == last_seen.date():
        return
    streak = data["most_daily_streak"].get(username, 0)
    if last_seen and (today - last_seen.date()).days == 1:
        if data["most_stayed"].get(username, 0) >= 1800:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
    data["last_visit"][username] = today.isoformat()
    data["most_daily_streak"][username] = streak
    update_all_time(data, username)

def update_all_time(data, username=None):
    if username:
        active = data["most_active"].get(username, 0)
        talk = data["most_talkative"].get(username, 0)
        streak = data["most_daily_streak"].get(username, 0)
        multiplier = 3 ** (streak - 1) if streak else 0
        data["all_time"][username] = active + talk * 5 + streak * multiplier
    else:
        users = set(data["most_active"].keys()) | set(data["most_talkative"].keys()) | set(data["most_daily_streak"].keys())
        for u in users:
            update_all_time(data, u)

async def handle_leaderboard_command(bot, user, message):
    msg = message.lower().strip()
    if msg == "leaderboard":
        return get_leaderboard_menu_text()

    m = re.match(r"leaderboard\s*(\S+)?", msg)
    if m:
        choice = m.group(1)
        if not choice:
            return get_leaderboard_menu_text()
        data = bot.leaderboard_data
        text = get_leaderboard_text_by_choice(data, choice, public=True)
        if isinstance(text, tuple):
            return "\n\n".join(text[1:])
        return text

    if msg == "!rank":
        return get_user_full_rank_summary(bot.leaderboard_data, user.username)

    return None

async def handle_leaderboard_admin_commands(bot, user, message):
    if user.username.lower() not in (u.lower() for u in getattr(bot, "bot_owners", [])):
        return None
    msg = message.lower().strip()
    if msg == "!resetlb":
        bot.leaderboard_data = load_leaderboard_data()
        for key in bot.leaderboard_data:
            if isinstance(bot.leaderboard_data[key], dict):
                bot.leaderboard_data[key] = {}
        save_leaderboard_data(bot.leaderboard_data)
        return "✅ All leaderboard data has been reset."

    m = re.match(r"!resetlb\s+(\w+)", msg)
    if m:
        cat = m.group(1).lower()
        name_map = {
            "1": "most_active",
            "2": "most_talkative",
            "3": "most_daily_streak",
            "4": "most_stayed",
            "5": "all_time",
        }
        cat = name_map.get(cat, cat)
        if cat in bot.leaderboard_data:
            bot.leaderboard_data[cat] = {}
            save_leaderboard_data(bot.leaderboard_data)
            return f"✅ Leaderboard `{cat}` has been reset."
        return f"❌ Invalid category `{cat}`."

    m = re.match(r"!removelb\s+@?(\w+)", message, re.IGNORECASE)
    if m:
        username = m.group(1)
        if remove_user(username):
            save_leaderboard_data(bot.leaderboard_data)
            return f"✅ @{username} removed from leaderboard."
        return f"⚠️ @{username} is already removed."

    m = re.match(r"!unremovelb\s+@?(\w+)", message, re.IGNORECASE)
    if m:
        username = m.group(1)
        if unremove_user(username):
            save_leaderboard_data(bot.leaderboard_data)
            return f"✅ @{username} restored to leaderboard."
        return f"⚠️ @{username} was not removed."

    if msg == "!removedlist":
        users = load_removed_users()
        if not users:
            return "✅ No removed users."
        return "🚫 Removed Users:\n" + "\n".join(f"- @{u}" for u in users)

    return None
