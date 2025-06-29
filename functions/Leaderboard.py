import sqlite3
import re
from datetime import datetime, timedelta

DB_PATH = None  # Set this dynamically

def set_db_path(path: str):
    global DB_PATH
    DB_PATH = path
    _init_db()

def _get_conn():
    if not DB_PATH:
        raise RuntimeError("DB_PATH is not set!")
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    cur = conn.cursor()
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
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            username TEXT PRIMARY KEY,
            join_timestamp INTEGER NOT NULL
        )
    ''')  # To track join time for longest stay and session time
    conn.commit()
    conn.close()

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
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(value)

def format_xp(value: int) -> str:
    return f"{format_number(value)} XP"

# -- Removal system --
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

# -- DB loading and saving --
def load_leaderboard_data():
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
        username = username.lower()
        if category in data:
            data[category][username] = value

    cur.execute("SELECT username, last_date FROM last_visit")
    for username, last_date in cur.fetchall():
        data["last_visit"][username.lower()] = last_date

    conn.close()
    return data

def save_leaderboard_data(data):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM leaderboard")
    cur.execute("DELETE FROM last_visit")
    for category, users in data.items():
        if category == "last_visit":
            for username, last_date in users.items():
                cur.execute(
                    "INSERT OR REPLACE INTO last_visit(username, last_date) VALUES (?, ?)",
                    (username.lower(), last_date),
                )
        elif category in {"most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"}:
            for username, value in users.items():
                cur.execute(
                    "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
                    (username.lower(), category, value),
                )
    conn.commit()
    conn.close()

# -- Individual Helpers --
def get_category_scores(category: str) -> dict:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, value FROM leaderboard WHERE category = ?", (category,))
    res = {username.lower(): value for username, value in cur.fetchall()}
    conn.close()
    return res

def set_category_score(username: str, category: str, value: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
        (username.lower(), category, value),
    )
    conn.commit()
    conn.close()

def get_last_visit_date(username: str) -> str | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT last_date FROM last_visit WHERE username = ?", (username.lower(),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def set_last_visit_date(username: str, last_date: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO last_visit(username, last_date) VALUES (?, ?)",
        (username.lower(), last_date),
    )
    conn.commit()
    conn.close()

def set_user_join_time(username: str, timestamp: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO user_sessions(username, join_timestamp) VALUES (?, ?)",
        (username.lower(), timestamp),
    )
    conn.commit()
    conn.close()

def get_user_join_time(username: str) -> int | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT join_timestamp FROM user_sessions WHERE username = ?", (username.lower(),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def remove_user_session(username: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_sessions WHERE username = ?", (username.lower(),))
    conn.commit()
    conn.close()

# -- Leaderboard Logic --
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

def _format_leaderboard_lines(data_unused, choice):
    emoji_titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "all_time": "🏅 All-Time Room Legends",
    }
    title = emoji_titles.get(choice, choice)
    category_data = get_category_scores(choice)
    filtered = {u: v for u, v in category_data.items() if not is_user_removed(None, u)}
    sorted_users = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:10]

    if not sorted_users:
        return [f"📉 No data yet for {title}."]

    lines = [f"🏆 {title} Leaderboard:"]
    for i, (user, value) in enumerate(sorted_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        val = (
            format_duration(value) if choice in ["most_active", "most_stayed"]
            else format_number(value) if choice in ["most_talkative", "most_daily_streak"]
            else format_xp(value) if choice == "all_time"
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
    return (lines[0], "\n".join(lines[:6]), "\n".join([lines[0]] + lines[6:]))

def get_user_rank_text(data_unused, username, category):
    cat_data = get_category_scores(category)
    username = username.lower()
    filtered = {u: v for u, v in cat_data.items() if not is_user_removed(None, u)}
    sorted_users = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    for i, (user, value) in enumerate(sorted_users, 1):
        if user == username:
            val = (
                format_duration(value) if category in ["most_active", "most_stayed"]
                else format_number(value) if category in ["most_talkative", "most_daily_streak"]
                else format_xp(value) if category == "all_time"
                else str(value)
            )
            return i, user, val
    return None, username, "0"

def get_user_full_rank_summary(data_unused, username):
    summary = [f"🧑 @{username}'s Top Ranks:"]
    keys = ["most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"]
    titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "all_time": "🏅 All-Time Room Legends",
    }
    for key in keys:
        rank, _, value = get_user_rank_text(None, username, key)
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}" if rank else "-"
        summary.append(f"{medal} {titles[key]} – {value}")
    return "\n".join(summary)

# -- Update leaderboard on chat or activity --
def update_leaderboard_on_chat(data_unused, username, duration=60):
    """Update active time and longest stay on chat or activity event.
    duration = seconds to add (default 60 seconds).
    """
    if is_user_removed(None, username):
        return
    username = username.lower()
    current_active = get_category_scores("most_active").get(username, 0)
    current_stayed = get_category_scores("most_stayed").get(username, 0)

    # Add time to active (in seconds)
    new_active = current_active + duration
    set_category_score(username, "most_active", new_active)

    # Update longest single stay if current duration > previous
    if duration > current_stayed:
        set_category_score(username, "most_stayed", duration)

    # Update all time with slow XP gain
    update_all_time(username, duration)

def update_leaderboard_on_message(data_unused, username):
    if is_user_removed(None, username):
        return
    username = username.lower()
    current_talkative = get_category_scores("most_talkative").get(username, 0)
    set_category_score(username, "most_talkative", current_talkative + 1)
    update_all_time(username)

def update_leaderboard_on_join(data_unused, username):
    if is_user_removed(None, username):
        return
    username = username.lower()
    now = datetime.utcnow()
    today = now.date()
    last_seen_str = get_last_visit_date(username)
    streak = get_category_scores("most_daily_streak").get(username, 0)
    stayed_time = get_category_scores("most_stayed").get(username, 0)
    if last_seen_str:
        try:
            last_seen = datetime.strptime(last_seen_str, "%Y-%m-%d")
            if today == last_seen.date():
                return
            if (today - last_seen.date()).days == 1:
                if stayed_time >= 1800:  # 30 minutes minimum for streak
                    streak += 1
                else:
                    streak = 1
            else:
                streak = 1
        except Exception:
            streak = 1
    else:
        streak = 1
    set_last_visit_date(username, today.isoformat())
    set_category_score(username, "most_daily_streak", streak)
    update_all_time(username)

def update_all_time(username=None, add_duration=None):
    """
    Calculate all-time XP.

    If add_duration is provided, add XP slowly based on this session duration.
    Otherwise, recalc all users from current base categories.
    """
    if username is None:
        users = set()
        for cat in ["most_active", "most_talkative", "most_daily_streak"]:
            users.update(get_category_scores(cat).keys())
        for u in users:
            update_all_time(u)
        return
    username = username.lower()
    active = get_category_scores("most_active").get(username, 0)
    talk = get_category_scores("most_talkative").get(username, 0)
    streak = get_category_scores("most_daily_streak").get(username, 0)

    # Slow XP gain: instead of adding full active seconds, scale down with factor
    # Example: 1 XP per 10 seconds active instead of 1:1
    slow_factor = 10

    if add_duration is not None:
        xp_gain = add_duration // slow_factor
        # Add existing all_time XP + new xp_gain
        current_all_time = get_category_scores("all_time").get(username, 0)
        value = current_all_time + xp_gain
    else:
        multiplier = 3 ** (streak - 1) if streak else 0
        value = active // slow_factor + talk * 5 + streak * multiplier

    set_category_score(username, "all_time", value)

# -- Handle user leaving the room --
def update_leaderboard_on_leave(username: str):
    """
    Call when user leaves room.

    Calculate total session time from join timestamp until now.
    Update most_active, most_stayed (if longest), and all_time accordingly.
    Remove session record.
    """
    if is_user_removed(None, username):
        return
    username = username.lower()
    join_time = get_user_join_time(username)
    if join_time is None:
        # No session info, can't update session duration
        return

    now_ts = int(datetime.utcnow().timestamp())
    session_duration = now_ts - join_time
    if session_duration < 0:
        session_duration = 0  # Safety check

    # Update most_active
    current_active = get_category_scores("most_active").get(username, 0)
    new_active = current_active + session_duration
    set_category_score(username, "most_active", new_active)

    # Update most_stayed (longest single stay)
    current_stayed = get_category_scores("most_stayed").get(username, 0)
    if session_duration > current_stayed:
        set_category_score(username, "most_stayed", session_duration)

    # Update all_time with slow XP gain
    update_all_time(username, session_duration)

    # Remove session record
    remove_user_session(username)

# -- Commands --
import asyncio

async def handle_leaderboard_command(bot, user, message):
    msg = message.lower().strip()
    if msg == "leaderboard":
        return get_leaderboard_menu_text()
    m = re.match(r"leaderboard\s*(\S+)?", msg)
    if m:
        choice = m.group(1)
        if not choice:
            return get_leaderboard_menu_text()
        txt = get_leaderboard_text_by_choice(None, choice, public=True)
        if isinstance(txt, tuple):
            return "\n\n".join(txt[1:])
        return txt
    if msg == "!rank":
        return get_user_full_rank_summary(None, user.username)
    return None

async def handle_leaderboard_admin_commands(bot, user, message):
    if user.username.lower() not in [u.lower() for u in getattr(bot, "bot_owners", [])]:
        return None
    msg = message.strip().lower()
    if msg == "!resetlb all":
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM leaderboard")
        cur.execute("DELETE FROM last_visit")
        cur.execute("DELETE FROM user_sessions")
        conn.commit()
        conn.close()
        return "✅ All leaderboard data has been reset."

    m = re.match(r"!resetlb\s+(\w+)", msg)
    if m:
        cat = m.group(1).lower()
        map_num = {"1": "most_active", "2": "most_talkative", "3": "most_daily_streak", "4": "most_stayed", "5": "all_time"}
        cat = map_num.get(cat, cat)
        if cat in {"most_active", "most_talkative", "most_daily_streak", "most_stayed", "all_time"}:
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM leaderboard WHERE category = ?", (cat,))
            conn.commit()
            conn.close()
            return f"✅ `{cat}` leaderboard reset."
        return f"❌ Invalid category `{cat}`."

    m = re.match(r"!removelb\s+@?(\w+)", message, re.IGNORECASE)
    if m:
        username = m.group(1)
        if remove_user(username):
            return f"✅ @{username} removed from leaderboard."
        return f"⚠️ @{username} is already removed."

    m = re.match(r"!unremovelb\s+@?(\w+)", message, re.IGNORECASE)
    if m:
        username = m.group(1)
        if unremove_user(username):
            return f"✅ @{username} is back in the leaderboard."
        return f"⚠️ @{username} was not removed."

    return None
