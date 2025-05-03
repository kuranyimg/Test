Here’s the refactored and improved version of the provided main.py code, with some enhancements and fixes for clarity and efficiency:

import random
import os
from highrise import BaseBot, Position, Highrise
from highrise.models import SessionMetadata, User, AnchorPosition
from highrise import GetMessagesRequest

from functions.loop_emote import check_and_start_emote_loop
from functions.state import user_loops, last_emote_name
from functions.vip_manager import is_vip, handle_vip_command, get_vip_list
from functions.commands import is_teleport_command, handle_teleport_command
from functions.vip_data import init_vip_db

init_vip_db()

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Bot is starting...")
        await self.highrise.walk_to(Position(17.5, 0.0, 12.5, "FrontRight"))

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        print(f"{user.username} (ID: {user.id}) joined")
        await self.highrise.chat(f"{user.username} joined!")
        await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
        await self.highrise.send_whisper(user.id, "❤️Use: [/help] for more information.")
        await self.highrise.send_whisper(user.id, "❤Type F3 F2 and F1 to teleport between the floor 🤍.")
        await self.highrise.send_emote("dance-hipshake")
        await self.highrise.send_emote("emote-lust", user.id)
        await self.highrise.react("heart", user.id)

    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username}: {message}")
        username = user.username.lower()
        is_owner = username == "raybm"

        # Handle VIP command
        if message.lower().startswith(("vip@", "unvip@")):
            if is_owner:
                response = await handle_vip_command(user, message, vip_list)
            else:
                response = f"Sorry {user.username}, only the bot owner can manage VIPs."
            await self.highrise.chat(response)
            return

        # Handle VIP-only commands
        if is_teleport_command(message) or message.lower().startswith(("tele ", "summon ", "tele@", "summon@")):
            if is_owner or is_vip(username, vip_list):
                await handle_teleport_command(user, message, self.highrise.send_whisper)
            else:
                await self.highrise.chat(f"Sorry {user.username}, this command is for VIPs only.")
            return

        # VIP list command
        if message.lower().lstrip("!/ -").strip() == "viplist":
            vip_message = get_vip_list(vip_list)
            await self.highrise.send_whisper(user.id, vip_message)
            return

        # Check and start emote loop
        await check_and_start_emote_loop(self, user, message)

        # Handle teleport commands
        if message.lower().startswith(("!tele", "/tele", "tele", "tp", "fly")):
            if user.username in ["iced_yu", "FallonXOXO", "RayMG"]:
                await self.teleporter(message)

        # Handle floor teleportation
        floor_teleports = {
            "floor1": Position(9.5, 0.0, 16.5),
            "floor3": Position(12.5, 19.25, 6.5),
            "floor4": Position(14.5, 20.0, 1.5),
            "floor2": Position(14.5, 9.0, 6.0)
        }

        for floor, position in floor_teleports.items():
            if message.lower().startswith((f"-{floor}", f"!{floor}", f"/{floor}", floor)):
                await self.highrise.teleport(user.id, position)

        # Handle emote list commands
        emote_list = [
            "!angry !thumbsup !cursing !flex !gagging !celebrate !blackpink !tiktok2 !tiktok9 !pennywise !russian !shop !enthused !singing !wrong !guitar !pinguin !astronaut !saunter !flirt !creepy !watch !revelation",
            "!tiktok10 !tiktok8 !cutey !pose3 !pose5 !pose1 !pose8 !pose7 !pose9 !cute !superpose !frog !snake !energyball !maniac !teleport !float !telekinesi !fight !wei !fashion !boxer !bashful !arabesque !party",
            "!confused !charging !snowangel !hot !snowball !curtsy !bow !model !greedy !tired !shy !wave !hello !lau !yes !sad !no !kiss !casual !ren !sit !punk !zombie !gravity !icecream !uwu !sayso !star",
            "!skating !bitnervous !scritchy !timejump !gottago !jingle !hyped !sleigh !surprise !repose !kawaii !touch !gift !pushit !tiktok !salute !attention !smooch !launch",
            "/angry /thumbsup /cursing /flex /gagging /celebrate /blackpink /tiktok2 /tiktok9 /pennywise /russian /shop /enthused /singing /wrong /guitar /pinguin /astronaut /saunter /flirt /creepy /watch /revelation",
            "/tiktok10 /tiktok8 /cutey /pose3 /pose5 /pose1 /pose8 /pose7 /pose9 /cute /superpose /frog /snake /energyball /maniac /teleport /float /telekinesi /fight /wei /fashion /boxer /bashful /arabesque /party",
            "/confused /charging /snowangel /hot /snowball /curtsy /bow /model /greedy /lust /tired /shy /wave /hello /lau /yes /sad /no /kiss /casual /ren /sit /punk /zombie /gravity /icecream /uwu /sayso /star",
            "/skating /bitnervous /scritchy /timejump /gottago /jingle /hyped /sleigh /surprise /repose /kawaii /touch /pushit /gift /tiktok /salute /attention /smooch /launch"
        ]

        # Send emote list to user
        if message.startswith(("!lista", "!emote list", "!list", "/lista", "/emote list", "/list")):
            for emote_batch in emote_list:
                await self.highrise.send_whisper(user.id, emote_batch)

        # Handle specific emote commands
        if message.startswith(("!emoteall", "/emoteall")):
            await self.highrise.send_emote("dance-floss")

        # Help command
        if message.startswith(("-Help", "/help", "!help")):
            await self.highrise.chat(f"/lista | /pessoas | /emotes | /marry me? | /play /fish /userinfo @ | !emoteall | !tele @ | !summon @ | !kick @ | !tele z,y,x | !tele @ z,y,x | ")
            await self.highrise.chat(f"[Emote] All | !emote all [Emote]")        
            await self.highrise.chat(f"{user.username} all activation codes must be used >> ! or/")
            await self.highrise.send_emote("dance-floss")

        # Teleport Command Handling
        if message.lower().startswith(("!tp", "/tp", "tele")):
            target_username = message.split("@")[-1].strip()
            await self.teleport_to_user(user, target_username)

        # Summon Command Handling
        if message.lower().startswith(("summon", "!summon", "/summon")):
            if user.username in ["FallonXOXO", "Its.Melly.Moo.XoXo", "Shaun_Knox", "sh1n1gam1699", "Dreamy._.KY", "hidinurbasement", "@emping", "_irii_", "RayBM"]:
                target_username = message.split("@")[-1].strip()
                await self.teleport_user_next_to(target_username, user)

        # Kick Command Handling
        if message.startswith("!kick"):
            if user.username in ["FallonXOXO", "RayBM"]:
                pass
            else:
                await self.highrise.chat("🤍.")
                return

            # Separate message into parts
            parts = message.split()
            # Check if message is valid "kick @username"
            if len(parts) != 2:
                await self.highrise.chat("🤍.")
                return

            # Check if there's a @ in the message
            if "@" not in parts[1]:
                username = parts[1]
            else:
                username = parts[1][1:]

            # Check if user is in room
            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() == username.lower():
                    user_id = room_user.id
                    break

            if "user_id" not in locals():
                await self.highrise.chat("User not found.")
                return

            # Kick user
            try:
                await self.highrise.moderate_room(user_id, "kick")
            except Exception as e:
                await self.highrise.chat(f"{e}")
                return

            # Send message to chat
            await self.highrise.chat(f"{username} has been banned from the room!")

    # Teleport to User Function
    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Teleport Error: {e}")

    # Teleport User to Another User's Location
    async def teleport_to_user(self, user: User, target_username: str) -> None:
        try:
            room_users = await self.highrise.get_room_users()
            for target, position in room_users.content:
                if target.username.lower() == target_username.lower():
                    z = position.z
                    new_z = z - 1
                    await self.teleport(user, Position(position.x, position.y, new_z, position.facing))
                    break
        except Exception as e:
            print(f"Teleporting error for {target_username}: {e}")

    async def teleport_user_next_to(self, target_username: str, requester_user: User) -> None:
        try:
            # Get the position of the requester_user
            room_users = await self.highrise.get_room_users()
            requester_position = None
            for user, position in room_users.content:
                if user.id == requester_user.id:
                    requester_position = position
                    break

            # Find the target user and their position
            for user, position in room_users.content:
                if user.username.lower() == target_username.lower():
                    z = requester_position.z
                    new_z = z + 1  # Move +1 on the z-axis (upwards)
                    await self.teleport(user, Position(requester_position.x, requester_position.y
