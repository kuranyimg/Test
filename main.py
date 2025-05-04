import asyncio
import logging
from functions.loop_emote import LoopEmoteBot
from highrise.bot import BaseBot
from highrise.models import User, Position

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HighriseBot(BaseBot):
    def __init__(self, username: str):
        super().__init__(username)
        self.loop_emote_bot = LoopEmoteBot()  # Integrate LoopEmoteBot

    async def on_ready(self):
        """Called when the bot is ready and connected."""
        logger.info(f"{self.username} is ready!")
        # You can initialize more actions here when the bot is ready

    async def on_message(self, message: str, user: User):
        """Handles incoming messages."""
        logger.info(f"Message received: {message} from {user.username}")
        # Process the message to trigger emotes or loop emotes
        await self.loop_emote_bot.on_message(message, user)

    async def on_user_move(self, user: User, pos: Position):
        """Handles user movement in the room."""
        logger.info(f"{user.username} moved to {pos}")
        # Here you can add any additional functionality when users move
        # For example, restarting a looped emote when they stop moving

    async def on_user_join(self, user: User):
        """Handles when a user joins the room."""
        logger.info(f"{user.username} has joined the room!")
        # You can handle user join events, like sending a welcome message or initiating loops

    async def on_user_leave(self, user: User):
        """Handles when a user leaves the room."""
        logger.info(f"{user.username} has left the room.")
        # Handle user leaving, e.g., stop loops or clean up resources

    async def on_error(self, error: Exception):
        """Handles any unexpected errors."""
        logger.error(f"An error occurred: {error}")

    async def run(self):
        """Starts the bot."""
        await self.start()

if __name__ == "__main__":
    bot = HighriseBot(username="LPbot")  # Use your bot username here
    asyncio.run(bot.run())  # Run the bot using asyncio
