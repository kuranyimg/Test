from highrise import User
import asyncio

class Leaderboard:
    def __init__(self):
        self.activity_tracker = {}
        self.booster_tracker = {}
        self.duration_tracker = {}  # Track duration in the room
        self.level_threshold = 10  # Points needed for a level up

    def add_activity(self, user_id):
        if user_id not in self.activity_tracker:
            self.activity_tracker[user_id] = 0
        self.activity_tracker[user_id] += 1

    def add_boost(self, user_id, username):
        self.booster_tracker[user_id] = username

    def start_duration(self, user_id):
        if user_id not in self.duration_tracker:
            self.duration_tracker[user_id] = {"time": 0, "active": True, "task": None}
            self.duration_tracker[user_id]["task"] = asyncio.create_task(self.track_duration(user_id))

    def stop_duration(self, user_id):
        if user_id in self.duration_tracker and self.duration_tracker[user_id]["active"]:
            self.duration_tracker[user_id]["active"] = False
            if self.duration_tracker[user_id]["task"]:
                self.duration_tracker[user_id]["task"].cancel()
                self.duration_tracker[user_id]["task"] = None

    async def track_duration(self, user_id):
        while True:
            await asyncio.sleep(1)  # Increment every second
            if self.duration_tracker[user_id]["active"]:
                self.duration_tracker[user_id]["time"] += 1  # Increment time spent in seconds

    def get_duration_leaderboard(self):
        sorted_leaderboard = sorted(self.duration_tracker.items(), key=lambda item: item[1]["time"], reverse=True)
        return sorted_leaderboard

    def format_leaderboard(self, leaderboard_data, get_user_func):
        formatted = ""
        for i, (user_id, data) in enumerate(leaderboard_data):
            user = get_user_func(user_id)
            duration = data["time"]
            formatted += f"{i+1}. @{user.username} - {duration // 60} minutes\n"  # Convert seconds to minutes
        return formatted

    async def handle_leaderboard_command(self, user: User, option: str, get_user_func):
        if option == "active":
            data = self.get_duration_leaderboard()
            leaderboard_str = self.format_leaderboard(data, get_user_func)
            await user.send_whisper(leaderboard_str)

    async def get_user(self, user_id):
        return await self.highrise.get_user(user_id)

# Initialize Leaderboard instance
leaderboard_instance = Leaderboard()
