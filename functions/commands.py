from functions.json import data_mappings, save_data, load_data
from highrise import Highrise

# Initialize
highrise = Highrise()

async def on_chat(self, user, message):
    # When the bot owner sets the location
    if message == "/sbot" and user.username in data_mappings["ownerz"]:
        try:
            room_users = await self.highrise.get_room_users()
            for room_user, pos in room_users.content:
                if room_user.username == user.username:
                    # Set the bot's location
                    data_mappings["bot_location"] = {"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}
                    save_data()  # Save updated location to JSON
                    await self.highrise.send_whisper(user.id, f"Bot location set to {data_mappings['bot_location']}")
                    break
        except Exception as e:
            print("Set bot error:", e)

    # Move the bot back to saved location
    if message == "/base" and user.username in data_mappings["ownerz"]:
        try:
            load_data()  # Load saved data
            bot_location = data_mappings["bot_location"]
            await self.highrise.walk_to(Position(**bot_location))
        except Exception as e:
            print("Error in /base:", e)
