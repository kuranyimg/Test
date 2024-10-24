class Leaderboard:
    def __init__(self, highrise):
        self.highrise = highrise  # Store the highrise instance
        self.activity_tracker = {}
        self.booster_tracker = {}
        self.duration_tracker = {}  # Track duration in the room
        self.level_threshold = 10  # Points needed for a level up

    # Existing methods...

    def get_active_leaderboard(self):
        # Sort users based on activity count (most active)
        sorted_leaderboard = sorted(self.activity_tracker.items(), key=lambda item: item[1], reverse=True)
        return sorted_leaderboard

    def get_booster_leaderboard(self):
        # Sort users based on their boost status (most boosts)
        sorted_boosters = sorted(self.booster_tracker.items(), key=lambda item: item[1], reverse=True)
        return sorted_boosters

    async def handle_leaderboard_command(self, user: User, option: str, get_user_func):
        if option == "active":
            data = self.get_active_leaderboard()
            leaderboard_str = self.format_leaderboard(data, get_user_func)
            await user.send_whisper(leaderboard_str)
        elif option == "boost":
            data = self.get_booster_leaderboard()
            leaderboard_str = self.format_leaderboard(data, get_user_func)
            await user.send_whisper(leaderboard_str)
