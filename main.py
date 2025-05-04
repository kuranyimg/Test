import asyncio
import math
from highrise import BaseBot, Position
from highrise.models import SessionMetadata, User, Message
from functions.loop_emote import check_and_start_emote_loop, user_loops, emote_list, last_positions

def positions_are_close(pos1, pos2, tolerance=0.05):
    return math.isclose(pos1.x, pos2.x, abs_tol=tolerance) and \
           math.isclose(pos1.z, pos2.z, abs_tol=tolerance)

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

            if user.id in user_loops:
                loop_data = user_loops[user.id]
                emote_name = loop_data["emote_name"]
                task = loop_data["task"]

                moved = previous and not positions_are_close(pos, previous)

                if moved:
                    if task and not task.done():
                        task.cancel()
                    user_loops[user.id]["task"] = None

                elif not moved:
                    if task is None or task.done():
                        selected = next((e for e in emote_list if e[1] == emote_name), None)
                        if selected:
                            _, emote_id, duration = selected
                            await self.highrise.send_emote(emote_id, user.id)

                            async def emote_loop():
                                try:
                                    while True:
                                        await self.highrise.send_emote(emote_id, user.id)
                                        await asyncio.sleep(duration)
                                except asyncio.CancelledError:
                                    pass

                            new_task = asyncio.create_task(emote_loop())
                            user_loops[user.id]["task"] = new_task
        except Exception as e:
            print(f"Error in on_user_move: {e}")
