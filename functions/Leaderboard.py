import sqlite3
import re
from datetime import datetime

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
    ''')  # To track join time for session duration
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
        elif category in {"most_active", "most_talkative", "most_daily_streak", "most_stayed"}:
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
        "5. 👑 Room Champions\n"
        "Use `leaderboard <number>` or `leaderboard <name>` to view a leaderboard."
    )

def _format_leaderboard_lines(data_unused, choice):
    emoji_titles = {
        "most_active": "⏳ Time Spent in Room",
        "most_talkative": "💬 Total Messages Sent",
        "most_daily_streak": "📅 Daily Visit Streak",
        "most_stayed": "🛋️ Longest Single Stay",
        "room_champion": "👑 Room Champions",
    }
    title = emoji_titles.get(choice, choice)

    if choice == "room_champion":
        # Compute top users based on how many categories they rank in top 1000 (for example)
        categories = ["most_active", "most_talkative", "most_daily_streak", "most_stayed"]
        # Build a dict: user -> count of categories they rank in top 1000
        user_counts = {}
        for cat in categories:
            cat_data = get_category_scores(cat)
            # Filter out removed users
            filtered = {u: v for u, v in cat_data.items() if not is_user_removed(None, u)}
            sorted_users = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
            for rank, (user, _) in enumerate(sorted_users, 1):
                if rank > 1000:
                    break
                user_counts[user] = user_counts.get(user, 0) + 1
        # Sort by count desc, then alphabetically
        sorted_champs = sorted(user_counts.items(), key=lambda x: (-x[1], x[0]))[:10]
        if not sorted_champs:
            return [f"📉 No data yet for {title}."]
        lines = [f"🏆 {title} Leaderboard:"]
        for i, (user, count) in enumerate(sorted_champs, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            lines.append(f"{medal} @{user} – {count} categories")
        return lines

    # Default for other categories
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
        "5": "room_champion",
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
            return i, value, cat_data.get(username, 0)
    return None, None, 0

def get_user_full_rank_summary(data_unused, username):
    username = username.lower()
    categories = ["most_active", "most_talkative", "most_daily_streak", "most_stayed"]
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    lines = [f"🧑 @{username}'s Top Ranks:"]
    champion_count = 0

    for cat in categories:
        rank, val, raw_val = get_user_rank_text(None, username, cat)
        if rank is None:
            lines.append(f"❌ {cat.replace('_',' ').title()} – No rank")
            continue
        if rank <= 1000:
            champion_count += 1
        medal = medals.get(rank, f"{rank}.")
        if cat in ["most_active", "most_stayed"]:
            val_str = format_duration(raw_val)
        else:
            val_str = format_number(raw_val)
        # Emoji titles for display
        titles = {
            "most_active": "⏳ Time Spent in Room",
            "most_talkative": "💬 Total Messages Sent",
            "most_daily_streak": "📅 Daily Visit Streak",
            "most_stayed": "🛋️ Longest Single Stay",
        }
        lines.append(f"{medal} {titles[cat]} – {val_str}")

    lines.append(f"👑 Room Champion in {champion_count} categories")
    return "\n".join(lines)

# --- Update functions called from main.py ---

def update_leaderboard_on_join(data_unused, username: str):
    # No immediate update needed on join for leaderboard, but track join time for session duration
    now = int(datetime.utcnow().timestamp())
    set_user_join_time(username, now)

def update_leaderboard_on_leave(username: str):
    if is_user_removed(None, username):
        return
    username = username.lower()
    join_time = get_user_join_time(username)
    if join_time is None:
        # No join time recorded, cannot update time spent
        return
    now = int(datetime.utcnow().timestamp())
    session_duration = max(0, now - join_time)

    # Update most_active: add session_duration to existing total
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM leaderboard WHERE username = ? AND category = ?", (username, "most_active"))
    row = cur.fetchone()
    total_time = row[0] if row else 0
    total_time += session_duration
    cur.execute(
        "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
        (username, "most_active", total_time),
    )

    # Update most_stayed if session_duration > existing record
    cur.execute("SELECT value FROM leaderboard WHERE username = ? AND category = ?", (username, "most_stayed"))
    row = cur.fetchone()
    longest_stay = row[0] if row else 0
    if session_duration > longest_stay:
        cur.execute(
            "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
            (username, "most_stayed", session_duration),
        )

    conn.commit()
    conn.close()

    # Clear join time
    remove_user_session(username)

def update_leaderboard_on_message(data_unused, username: str):
    if is_user_removed(None, username):
        return
    username = username.lower()
    # Increment total messages sent
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM leaderboard WHERE username = ? AND category = ?", (username, "most_talkative"))
    row = cur.fetchone()
    total_msgs = row[0] if row else 0
    total_msgs += 1
    cur.execute(
        "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
        (username, "most_talkative", total_msgs),
    )
    conn.commit()
    conn.close()

def update_leaderboard_on_chat(data_unused, username: str):
    # Currently same as on_message for now or could be used for other passive metrics
    update_leaderboard_on_message(data_unused, username)

def update_daily_streak(username: str):
    if is_user_removed(None, username):
        return
    username = username.lower()
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    last_date = get_last_visit_date(username)
    streak = 0
    if last_date:
        from datetime import timedelta
        last_dt = datetime.strptime(last_date, "%Y-%m-%d")
        today_dt = datetime.strptime(today_str, "%Y-%m-%d")
        diff = (today_dt - last_dt).days
        if diff == 1:
            # Continue streak
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute("SELECT value FROM leaderboard WHERE username = ? AND category = ?", (username, "most_daily_streak"))
            row = cur.fetchone()
            streak = row[0] if row else 0
            streak += 1
            cur.execute(
                "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
                (username, "most_daily_streak", streak),
            )
            conn.commit()
            conn.close()
        elif diff > 1:
            # Reset streak
            conn = _get_conn()
            cur = conn.cursor()
            streak = 1
            cur.execute(
                "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
                (username, "most_daily_streak", streak),
            )
            conn.commit()
            conn.close()
    else:
        # First visit recorded, start streak at 1
        streak = 1
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO leaderboard(username, category, value) VALUES (?, ?, ?)",
            (username, "most_daily_streak", streak),
        )
        conn.commit()
        conn.close()
    # Update last_visit date
    set_last_visit_date(username, today_str)

def handle_leaderboard_command(bot, user, message: str) -> str | None:
    # Parses leaderboard commands and returns text or None
    msg = message.strip().lower()
    if not (msg.startswith("leaderboard") or msg == "!rank"):
        return None

    if msg == "!rank":
        # Show user ranks summary
        return get_user_full_rank_summary(None, user.username)

    parts = msg.split()
    if len(parts) == 1:
        # Just "leaderboard" -> show menu
        return get_leaderboard_menu_text()
    elif len(parts) == 2:
        choice = parts[1]
        return get_leaderboard_text_by_choice(None, choice, public=False)

    return None

def handle_leaderboard_admin_commands(bot, user, message: str) -> bool:
    msg = message.strip().lower()
    if not (msg.startswith("!removelb") or msg.startswith("!unremovelb")):
        return False
    # Only owners can do this
    if not hasattr(bot, "bot_owners") or user.username.lower() not in [o.lower() for o in bot.bot_owners]:
        return False

    if msg.startswith("!removelb"):
        parts = msg.split()
        if len(parts) == 2:
            username = parts[1].lstrip("@")
            if remove_user(username):
                bot.leaderboard_data = load_leaderboard_data()
                bot.highrise.chat(f"✅ Removed @{username} from leaderboard tracking.")
            else:
                bot.highrise.chat(f"⚠️ User @{username} was already removed.")
            return True

    if msg.startswith("!unremovelb"):
        parts = msg.split()
        if len(parts) == 2:
            username = parts[1].lstrip("@")
            if unremove_user(username):
                bot.leaderboard_data = load_leaderboard_data()
                bot.highrise.chat(f"✅ Restored @{username} to leaderboard tracking.")
            else:
                bot.highrise.chat(f"⚠️ User @{username} was not removed.")
            return True

    return False
