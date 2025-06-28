import sqlite3
import re
from datetime import datetime, timedelta

DB_PATH = None  # Set this dynamically or via init function

# To set the DB path externally (e.g. from data_store.py or main.py)
def set_db_path(path: str):
    global DB_PATH
    DB_PATH = path
    _init_db()

def _get_conn():
    if not DB_PATH:
        raise RuntimeError("DB_PATH is not set! Call set_db_path() first.")
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    cur = conn.cursor()
    # Create tables if not exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            value INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (username, category)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS removed_users (
            username TEXT PRIMARY KEY
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS last_visit (
            username TEXT PRIMARY KEY,
            last_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Formatting helpers (same as before) ---

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

# --- Removed users handling ---

def load_removed_users():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username FROM removed_users")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

def save_removed_user(username: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO removed_users(username) VALUES (?)", (username.lower(),))
    conn.commit()
    conn.close()

def remove_removed_user(username: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM removed_users WHERE username = ?", (username.lower(),))
    conn.commit()
    conn.close()

def is_user_removed(data_unused, username: str) -> bool:
    # data_unused param is for compatibility with old interface
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM removed_users WHERE username = ?", (username.lower(),))
    found = cur.fetchone() is not None
    conn.close()
    return found

def remove_user(username: str):
    if not is_user_removed(None, username):
        save_removed_user(username)
        return True
    return False

def unremove_user(username: str):
    if is_user_removed(None, username):
        remove_removed_user(username)
        return True
    return False

# --- Leaderboard data loading and saving ---

def load_leaderboard_data():
    """
    Return dict with all categories as keys mapping username->value dicts.
    This loads all data from DB into memory.
    """
    conn = _get_conn()
    cur = conn.cursor()
    data = {
        "most_active": {},
        "most_talkative": {},
        "most_daily_streak": {},
        "most_stayed": {},
        "all_time": {},
        "last_visit": {},
    }
    cur.execute("SELECT username, category, value FROM leaderboard")
    for username, category, value in cur.fetchall():
        if category in data:
            data[category][username] = value

    cur.execute("SELECT username, last_date FROM last_visit")
    for username, last_date in cur.fetchall():
        data["last_visit"][username] = last_date

    conn.close()
    return data

def save_leaderboard_data(data):
    """
    Save all leaderboard data from dictionary to DB.
    WARNING: This will replace all leaderboard and last_visit data.
    """
    conn = _get_conn()
    cur = conn.cursor()

    # Clear existing leaderboard data
    cur.execute("DELETE FROM leaderboard")
    cur.execute("DELETE FROM last_visit")

    # Insert leaderboard data
    for category, users in data.items():
        if category == "last_visit":
            # Insert last_visit dates
            for username, last_date in users.items():
                cur.execute(
                    "INSERT OR REPLACE INTO last_visit(username, last_date) VALUES (?, ?)",
                    (username, last_date),
                )
        elif category in {"most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"}:
            for username, value in users.items():
                cur.execute(
                    "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
                    (username, category, value),
                )
    conn.commit()
    conn.close()

# --- Helpers to get/set individual leaderboard values ---

def get_category_scores(category: str) -> dict:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, value FROM leaderboard WHERE category = ?", (category,))
    res = dict(cur.fetchall())
    conn.close()
    return res

def set_category_score(username: str, category: str, value: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
        (username, category, value),
    )
    conn.commit()
    conn.close()

def get_last_visit_date(username: str) -> str | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT last_date FROM last_visit WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def set_last_visit_date(username: str, last_date: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO last_visit(username, last_date) VALUES (?, ?)",
        (username, last_date),
    )
    conn.commit()
    conn.close()

# --- Main leaderboard logic ---

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
    category_data = get_category_scores(choice)
    # Remove removed users:
    filtered = {u: v for u, v in category_data.items() if not is_user_removed(None, u)}
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

def get_leaderboard_text_by_choice(data_unused, choice: str, public=False):
    name_map = {
        "1": "most_active",
        "2": "most_talkative",
        "3": "most_daily_streak",
        "4": "most_stayed",
        "5": "all_time",
    }
    choice = name_map.get(choice.lower(), choice.lower())
    lines = _format_leaderboard_lines(None, choice)
    if public or sum(len(line) for line in lines) < 400:
        return "\n".join(lines)
    header = lines[0]
    first_half = lines[1:6]
    second_half = lines[6:]
    return (header, "\n".join([header] + first_half), "\n".join([header] + second_half))

def get_user_rank_text(data_unused, username, category):
    cat_data = get_category_scores(category)
    filtered = {u: v for u, v in cat_data.items() if not is_user_removed(None, u)}
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

def get_user_full_rank_summary(data_unused, username):
    summary = [f"🧑 @{username}'s Top Ranks:"]
    emoji_titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "all_time": "🏅 All-Time Room Legends",
    }
    for key in ["most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"]:
        rank, _, value = get_user_rank_text(None, username, key)
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}" if rank else "-"
        summary.append(f"{medal} {emoji_titles[key]} – {value}")
    return "\n".join(summary)

def update_leaderboard_on_chat(data_unused, username, duration):
    if is_user_removed(None, username):
        return
    duration = int(duration)
    current_active = get_category_scores("most_active").get(username, 0)
    current_stayed = get_category_scores("most_stayed").get(username, 0)
    # Update most_active
    set_category_score(username, "most_active", current_active + duration)
    # Update most_stayed if duration > current
    if duration > current_stayed:
        set_category_score(username, "most_stayed", duration)
    update_all_time(username)

def update_leaderboard_on_message(data_unused, username):
    if is_user_removed(None, username):
        return
    current_talkative = get_category_scores("most_talkative").get(username, 0)
    set_category_score(username, "most_talkative", current_talkative + 1)
    update_all_time(username)

def update_leaderboard_on_join(data_unused, username):
    if is_user_removed(None, username):
        return
    now = datetime.utcnow()
    last_seen_str = get_last_visit_date(username)
    last_seen = None
    if last_seen_str:
        try:
            last_seen = datetime.strptime(last_seen_str, "%Y-%m-%d")
        except Exception:
            pass
    today = now.date()
    if last_seen and today == last_seen.date():
        return
    streak = get_category_scores("most_daily_streak").get(username, 0)
    stayed_time = get_category_scores("most_stayed").get(username, 0)
    if last_seen and (today - last_seen.date()).days == 1:
        if stayed_time >= 1800:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
    set_last_visit_date(username, today.isoformat())
    set_category_score(username, "most_daily_streak", streak)
    update_all_time(username)

def update_all_time(username=None):
    if username is None:
        # Update all users
        users = set()
        for category in ["most_active", "most_talkative", "most_daily_streak"]:
            scores = get_category_scores(category)
            users.update(scores.keys())
        for u in users:
            update_all_time(u)
        return

    active = get_category_scores("most_active").get(username, 0)
    talk = get_category_scores("most_talkative").get(username, 0)
    streak = get_category_scores("most_daily_streak").get(username, 0)
    multiplier = 3 ** (streak - 1) if streak else 0
    value = active + talk * 5 + streak * multiplier
    set_category_score(username, "all_time", value)

# --- Command handlers remain the same, except they receive bot instance and call above functions ---

import asyncio
import re

async def handle_leaderboard_command(bot, user, message):
    msg = message.lower().strip()
    if msg == "leaderboard":
        return get_leaderboard_menu_text()

    m = re.match(r"leaderboard\s*(\S+)?", msg)
    if m:
        choice = m.group(1)
        if not choice:
            return get_leaderboard_menu_text()
        text = get_leaderboard_text_by_choice(None, choice, public=True)
        if isinstance(text, tuple):
            return "\n\n".join(text[1:])
        return text

    if msg == "!rank":
        return get_user_full_rank_summary(None, user.username)

    return None

async def handle_leaderboard_admin_commands(bot, user, message):
    if user.username.lower() not in (u.lower() for u in getattr(bot, "bot_owners", [])):
        return None
    msg = message.lower().strip()
    if msg == "!resetlb":
        # Reset all leaderboard data
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM leaderboard")
        cur.execute("DELETE FROM last_visit")
        conn.commit()
        conn.close()
        return "✅ All leaderboard data has been reset."

    m = re.match(r"!resetlb\s+(\w+)", msg)
    if m:
        cat = m.group(1).lower()
        valid_cats = {"most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"}
        if cat in valid_cats:
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM leaderboard WHERE category = ?", (cat,))
            if cat == "most_daily_streak":
                # Also clear last_visit for all users? Maybe no
                pass
            conn.commit()
            conn.close()
            return f"✅ Leaderboard `{cat}` has been reset."
        else:
            return f"❌ Invalid category `{cat}`."

    m = re.match(r"!removelb\s+@?(\w+)", message, re.IGNORECASE)
    if m:
        username = m.group(1)
        if remove_user(username):
            return f"✅ @{username} removed from leaderboard."
        return f"⚠️ @{username} is already removed."
    return None
