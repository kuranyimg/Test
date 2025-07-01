import sqlite3
import time

DB_PATH = "leaderboard.db"
REMOVED_USERS = set()

leaderboard_categories = [
    "most_active",
    "most_talkative",
    "most_afk_time",
    "most_stayed",
    "room_champion"
]

category_names = {
    "most_active": "⏳ Time Spent in Room",
    "most_talkative": "💬 Total Messages Sent",
    "most_afk_time": "😴 Longest AFK Session",
    "most_stayed": "🛋️ Longest Single Stay",
    "room_champion": "👑 Room Champion",
}

title_map = {
    1: "Legend",
    2: "Ruler",
    3: "Master",
    4: "Conqueror",
    5: "Veteran",
    6: "Icon",
    7: "Prodigy",
    8: "Star",
    9: "Hero",
    10: "Pioneer"
}

user_session_starts = {}
user_last_activity = {}

def ensure_leaderboard_table():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                value INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (username, category)
            )
        """)
        conn.commit()

ensure_leaderboard_table()

def set_user_join_time(username):
    uname = username.lower()
    now = int(time.time())
    user_session_starts[uname] = now
    user_last_activity[uname] = now

def update_most_active_live(username):
    uname = username.lower()
    now = int(time.time())

    if uname not in user_session_starts or uname not in user_last_activity:
        return

    last = user_last_activity[uname]
    elapsed = now - last
    if elapsed <= 0:
        return

    data = get_user_data(uname)
    update_leaderboard_value(uname, "most_active", data["most_active"] + elapsed)
    if elapsed > data["most_afk_time"]:
        update_leaderboard_value(uname, "most_afk_time", elapsed)

    session_elapsed = now - user_session_starts[uname]
    if session_elapsed > data["most_stayed"]:
        update_leaderboard_value(uname, "most_stayed", session_elapsed)

    user_last_activity[uname] = now

def track_user_session_end(username):
    uname = username.lower()
    if uname in user_session_starts:
        start = user_session_starts.pop(uname)
        now = int(time.time())
        duration = now - start
        if duration > 0:
            data = get_user_data(uname)
            update_leaderboard_value(uname, "most_active", data["most_active"] + duration)
            if duration > data["most_stayed"]:
                update_leaderboard_value(uname, "most_stayed", duration)
    user_last_activity.pop(uname, None)

def update_message_count(username):
    uname = username.lower()
    update_most_active_live(uname)
    data = get_user_data(uname)
    update_leaderboard_value(uname, "most_talkative", data["most_talkative"] + 1)

def get_user_data(username):
    uname = username.lower()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for cat in leaderboard_categories[:-1]:
            c.execute("INSERT OR IGNORE INTO leaderboard (username, category, value) VALUES (?, ?, 0)", (uname, cat))
        conn.commit()
        c.execute("SELECT category, value FROM leaderboard WHERE username = ?", (uname,))
        rows = c.fetchall()
        return {cat: val for cat, val in rows}

def update_leaderboard_value(username, category, value):
    if category == "room_champion":
        return
    uname = username.lower()
    if uname in REMOVED_USERS:
        return
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO leaderboard (username, category, value)
            VALUES (?, ?, ?)
            ON CONFLICT(username, category) DO UPDATE SET value=excluded.value
        """, (uname, category, value))
        conn.commit()

def get_top_leaderboard(category, limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT username, value FROM leaderboard
            WHERE category = ?
            ORDER BY value DESC
            LIMIT ?
        """, (category, limit))
        return c.fetchall()

def get_room_champion_leaderboard(limit=10):
    user_scores = {}
    for cat in leaderboard_categories[:-1]:
        top = get_top_leaderboard(cat, 100)
        for rank, (user, _) in enumerate(top):
            points = 100 - rank
            user_scores[user] = user_scores.get(user, 0) + points
    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_users[:limit]

def get_room_champion_rank(username):
    uname = username.lower()
    champs = get_room_champion_leaderboard(1000)
    for i, (user, _) in enumerate(champs):
        if user.lower() == uname:
            return i + 1
    return None

def get_user_full_rank_summary(_, username):
    uname = username.lower()
    stats = get_user_data(uname)
    ranks = {}

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for cat in leaderboard_categories[:-1]:
            c.execute("SELECT username FROM leaderboard WHERE category = ? ORDER BY value DESC", (cat,))
            all_users = [row[0].lower() for row in c.fetchall()]
            ranks[cat] = all_users.index(uname) + 1 if uname in all_users else None

    champ_rank = get_room_champion_rank(uname)
    ranks["room_champion"] = champ_rank

    lines = [f"📊 @{username}’s Leaderboard Stats:\n"]

    def rank_line(symbol, label, value, rank, suffix=""):
        return f"{symbol} {label}: {value}{suffix}\n                 (Rank #{rank})" if rank else f"{symbol} {label}: {value}{suffix}\n                 (Unranked)"

    lines.append(rank_line("🥇", "Time", format_seconds(stats["most_active"]), ranks["most_active"]))
    lines.append(rank_line("💬", "Msgs", format_number(stats["most_talkative"]), ranks["most_talkative"]))
    lines.append(rank_line("😴", "AFK", format_seconds(stats["most_afk_time"]), ranks["most_afk_time"]))
    lines.append(rank_line("🛋️", "Stay", format_seconds(stats["most_stayed"]), ranks["most_stayed"]))

    if champ_rank:
        title = title_map.get(champ_rank, "Elite" if champ_rank <= 100 else "Rookie")
        crowns = "👑" * min(5, champ_rank if champ_rank <= 10 else 1)
        lines.append(f"👑 Champ: #{champ_rank} {crowns} {title}")

    return "\n".join(lines)

def get_leaderboard_text_by_choice(_, category, public=True):
    if category not in leaderboard_categories:
        return "❌ Invalid leaderboard category."

    if category == "room_champion":
        rows = get_room_champion_leaderboard(10)
        lines = ["👑 Room Champions – Top 10:\n"]
        for i, (user, _) in enumerate(rows, 1):
            title = title_map.get(i, "Elite")
            crown = "👑" * min(i, 5)
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            lines.append(f"{medal} @{user} — {crown} {title}")
        return "\n".join(lines)

    rows = get_top_leaderboard(category, 10)
    lines = [f"{category_names[category]} Top 10:"]
    for i, (user, val) in enumerate(rows, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        val_txt = format_seconds(val) if category in ["most_active", "most_afk_time", "most_stayed"] else format_number(val)
        lines.append(f"{medal} @{user} — {val_txt}")
    return "\n".join(lines)

def format_seconds(sec):
    d, h = divmod(sec, 86400)
    h, m = divmod(h, 3600)
    m //= 60
    if d > 0:
        return f"{d}d {h}h"
    return f"{h}h {m}m" if h else f"{m}m"

def format_number(n):
    for unit in ["", "k", "M", "B"]:
        if abs(n) < 1000:
            return f"{int(n)}{unit}"
        n /= 1000
    return f"{n:.1f}T"

def get_leaderboard_menu_text():
    lines = ["🏆 Leaderboard Categories:"]
    for i, cat in enumerate(leaderboard_categories, 1):
        lines.append(f"{i}. {category_names[cat]}")
    lines.append("\nType `leaderboard <name or number>` to view top 10.")
    return "\n".join(lines)

# --- Admin ---

def remove_user(username):
    REMOVED_USERS.add(username.lower())

def unremove_user(username):
    REMOVED_USERS.discard(username.lower())

def is_user_removed(_, username):
    return username.lower() in REMOVED_USERS

def reset_leaderboard(category):
    if category not in leaderboard_categories:
        return False
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM leaderboard WHERE category = ?", (category,))
        conn.commit()
    return True

def reset_user_in_category(username, category):
    uname = username.lower()
    if category not in leaderboard_categories or category == "room_champion":
        return False
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM leaderboard WHERE username = ? AND category = ?", (uname, category))
        conn.commit()
    return True

def reset_user_all_categories(username):
    uname = username.lower()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for cat in leaderboard_categories:
            if cat != "room_champion":
                c.execute("DELETE FROM leaderboard WHERE username = ? AND category = ?", (uname, cat))
        conn.commit()

def handle_leaderboard_command(_, user, message):
    msg = message.lower().strip()
    if msg == "leaderboard":
        return get_leaderboard_menu_text()
    if msg.startswith("leaderboard "):
        arg = msg.split(" ", 1)[1]
        if arg.isdigit():
            index = int(arg) - 1
            if 0 <= index < len(leaderboard_categories):
                return get_leaderboard_text_by_choice(None, leaderboard_categories[index])
        for cat in leaderboard_categories:
            if cat.startswith(arg):
                return get_leaderboard_text_by_choice(None, cat)
        return "❌ Unknown category."
    if msg.startswith("rank "):
        name = msg[5:].lstrip("@").strip()
        return get_user_full_rank_summary(None, name)
    if msg == "rank":
        return get_user_full_rank_summary(None, user.username)
    return None

def handle_leaderboard_admin_commands(_, user, msg):
    if not hasattr(user, "username") or user.username.lower() != "raybm":
        return None

    text = msg.lower().strip()

    if text.startswith("remlb @"):
        username = text.split("@")[1].strip()
        remove_user(username)
        return f"❌ Removed @{username} from leaderboard."

    if text.startswith("unremlb @"):
        username = text.split("@")[1].strip()
        unremove_user(username)
        return f"✅ Unremoved @{username} from leaderboard."

    if text.startswith("resetlb "):
        parts = text.split()
        if len(parts) == 3 and parts[2].startswith("@"):
            category = parts[1]
            username = parts[2][1:]
            cat = leaderboard_categories[int(category)-1] if category.isdigit() else category
            if reset_user_in_category(username, cat):
                return f"🔄 Reset @{username}'s score in {category_names[cat]}"
            else:
                return "❌ Invalid category or user."
        elif len(parts) == 2:
            cat = leaderboard_categories[int(parts[1])-1] if parts[1].isdigit() else parts[1]
            if reset_leaderboard(cat):
                return f"🔄 Reset leaderboard: {category_names[cat]}"
            else:
                return "❌ Invalid category."

    if text.startswith("resetlball @"):
        username = text.split("@")[1].strip()
        reset_user_all_categories(username)
        return f"🧹 Reset all scores for @{username}"

    if text == "resetalllb":
        for cat in leaderboard_categories:
            reset_leaderboard(cat)
        return "🧹 All leaderboards reset."

    if text == "commandlb":
        return (
            "👑 Owner Leaderboard Commands:\n"
            "• remlb @username — Remove from leaderboard\n"
            "• unremlb @username — Add back to leaderboard\n"
            "• resetlb <category|number> — Reset full leaderboard\n"
            "• resetlb <category|number> @username — Reset a user's score\n"
            "• resetlball @username — Reset all user's scores\n"
            "• resetalllb — Reset all leaderboards\n"
            "• commandlb
        )

    return None
