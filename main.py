import logging
from functions.loop_emote import emote_loop
from functions.commands import handle_commands
from functions.state import State  # If needed for state management
from functions.loop_emote import handle_loop_command, stop_emote_loop, handle_user_movement, handle_user_stopped
# Setup logging for easier debugging
logging.basicConfig(level=logging.INFO)

class HighriseBot:
    def __init__(self, username):
        self.username = username
        self.state = State()  # If you need to manage bot state

    def run(self):
        logging.info(f"Bot {self.username} is starting.")
        # Run bot and handle commands
        while True:
            message = self.get_message_from_user()  # Assuming you get messages from users
            if message:
                self.handle_message(message)

    def handle_message(self, message):
        # Parse message for commands (like "loop", "stop", etc.)
        command = self.parse_message(message)
        if command:
            self.process_command(command)

    def parse_message(self, message):
        # You can add more logic for parsing different types of commands here
        if message.startswith('loop') or message.startswith('/loop') or message.startswith('!loop'):
            return 'loop'
        elif message.lower() == 'stop':
            return 'stop'
        return None

    def process_command(self, command):
        if command == 'loop':
            self.start_emote_loop()
        elif command == 'stop':
            self.stop_emote_loop()

    def start_emote_loop(self):
        # Start emote loop for the bot
        emote_loop(self.username)  # Assuming you are using the emote_loop function to start looping emotes

    def stop_emote_loop(self):
        # Stop the emote loop
        logging.info(f"Stopping emote loop for {self.username}.")
        # Add your stop logic here

    def get_message_from_user(self):
        # Logic to get a message from the user (can be replaced with your actual input method)
        return input("Enter a command: ")  # Assuming you're using input for the user's command

# Example to run the bot
if __name__ == "__main__":
    bot_username = "raybm"  # Bot's username
    bot = HighriseBot(bot_username)
    bot.run()
