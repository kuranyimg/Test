from highrise import BaseBot
from highrise.models import User

async def emote(self: BaseBot, user: User, message: str) -> None:
    try:
        emote_name, target = message.split(" @")
    except ValueError:
        await self.highrise.chat("Invalid command format. Please use '<emote_name> @<target>'.")
        return

    user_list = await self.webapi.get_users(username=target)
    if user_list.total == 0:
        await self.highrise.chat("Invalid target.")
        return

    user_id = user_list.users[0].user_id
    try:
        await self.highrise.send_emote(emote_name, user_id)
    except Exception as e:
        await self.highrise.chat(f"Failed to send emote: {e}")
        return
