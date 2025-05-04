import asyncio
import math
import logging
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, Message
from functions.loop_emote import check_and_start_emote_loop, stop_emote_loop, user_loops, emote_list, last_positions

logger = logging.getLogger(__name__)

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Bot is running.")
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))

    async def on_chat(self, user: User, message: str) -> None:
        await check_and_start_emote_loop(self, user, message)

    async def on_message(self, user: User, message: Message) -> None:
        await check_and_start_emote_loop(self, user, message.content)

    async def on_user_move(self, user: User, pos: Position) -> None:
        try:
            previous = last_positions.get(user.id)
            last_positions[user.id] = pos

            # Check if user has an active emote loop
            if user.id in user_loops:
                loop_data = user_loops[user.id]
                emote_name = loop_data["emote_name"]
                task = loop_data["task"]

                # Check if user has moved
                moved = previous and not positions_are_close(pos, previous)

                if moved:
                    if task and not task.done():
                        task.cancel()
                    user_loops[user.id]["task"] = None
                elif not moved:
                    # Restart loop if task is None or done
                    if task is None or task.done():
                        selected = next((e for e in emote_list if e[1] == emote_name), None)
                        if selected:
                            _, emote_id, duration = selected
                            await self.start_emote_loop(user.id, emote_id, duration)

        except Exception as e:
            logger.error(f"Error in on_user_move: {e}")


    async def start_emote_loop(self, user_id: str, emote_id: str, duration: float):
        if user_id in user_loops:
            user_loops[user_id]["task"].cancel()
        
        # Start a new emote loop task
        task = asyncio.create_task(self.emote_loop(emote_id, user_id, duration))
        user_loops[user_id] = {"task": task, "emote_name": emote_id}
        
        await self.highrise.send_whisper(user_id, "Emote loop started. Say 'stop' to end it.")

    async def emote_loop(self, emote_id: str, user_id: str, duration: float):
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            logger.debug(f"Emote loop for user {user_id} canceled.")
        except Exception as e:
            logger.error(f"Error in emote loop for emote {emote_id}, by user {user_id}, with message: {e}")

    async def stop_emote_loop(self, user_id: str):
        if user_id in user_loops:
            user_loops[user_id]["task"].cancel()
            del user_loops[user_id]
            await self.highrise.send_whisper(user_id, "Emote loop has been stopped.")
        else:
            await self.highrise.send_whisper(user_id, "You don't have an active emote loop.")

# Helper function for checking if positions are close
def positions_are_close(pos1, pos2, tolerance=0.05):
    return math.isclose(pos1.x, pos2.x, abs_tol=tolerance) and \
           math.isclose(pos1.z, pos2.z, abs_tol=tolerance)
    
