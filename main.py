import random
import os
from highrise import BaseBot, Position, Highrise  # Be more specific in imports from highrise
from highrise.models import SessionMetadata
from highrise import GetMessagesRequest  # If you are using this later
from functions.loop_emote import check_and_start_emote_loop
from functions.state import user_loops, last_emote_name
from functions.vip_manager import is_vip, handle_vip_command, get_vip_list
from functions.commands import is_teleport_command, handle_teleport_command
from functions.vip_data import init_vip_db
init_vip_db()

class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("working")
        await self.highrise.walk_to(Position(17.5 , 0.0 , 12.5, "FrontRight"))
             
    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        # Only the bot prints the message in the console
        print(f"{user.username} (ID: {user.id})")

        # Announce the user has joined the room publicly
        await self.highrise.chat(f"{user.username} joined!")

        # Send welcome whispers to the user
        await self.highrise.send_whisper(user.id, f"❤️Welcome [{user.username}]! Use: [!emote list] or [1-97] for dances & emotes.")
        await self.highrise.send_whisper(user.id, f"❤️Use: [/help] for more information.")
        await self.highrise.send_whisper(user.id, f"❤Type F3 F2 and F1 to teleport between the floor 🤍.")

        # Send emotes
        await self.highrise.send_emote("dance-hipshake")
        await self.highrise.send_emote("emote-lust", user.id)

       # React with a heart emoji
        await self.highrise.react("heart", user.id)
        
    async def on_chat(self, user: User, message: str) -> None:
        print(f"{user.username}: {message}")    
        username = user.username.lower()
        is_owner = username == "raybm"

        # Handle VIP command
        if message.lower().startswith("vip@") or message.lower().startswith("unvip@"):
            if is_owner:
                response = await handle_vip_command(user, message, vip_list)
            else:
                response = f"Sorry {user.username}, only the bot owner can manage VIPs."
            await self.highrise.chat(response)
            return

        # Handle VIP-only commands
        if (
            is_teleport_command(message)
            or message.lower().startswith("tele ")
            or message.lower().startswith("tele@")
            or message.lower().startswith("summon ")
            or message.lower().startswith("summon@")
            or message.strip() == "-4"
        ):
            if is_owner or is_vip(username, vip_list):
                await handle_teleport_command(user, message, self.highrise.send_whisper)
            else:
                await self.highrise.chat(f"Sorry {user.username}, this command is for VIPs only.")
            return

        # Handle VIP list command
        normalized_msg = message.lower().lstrip("!/ -").strip()
        if normalized_msg == "viplist":
            vip_message = get_vip_list(vip_list)
            await self.highrise.send_whisper(user.id, vip_message)
            return
            
        await check_and_start_emote_loop(self, user, message)
        # Check for direct emote names
                      
            
        if        message.startswith("/tele") or              message.startswith("/tp") or              message.startswith("/fly") or     message.startswith("!tele") or      message.startswith("!tp") or     message.startswith("!fly"):
          if user.username == "iced_yu" or user.username == "FallonXOXO" or user.username == "RayMG":            await self.teleporter(message)

        if        message.startswith("-floor1") or message.startswith("!floor1") or message.startswith("-floor 1") or message.startswith("Floor 1") or message.startswith("Floor1") or message.startswith("/floor1") or    message.startswith("floor1") or message.startswith("-1") or    message.startswith("floor1") or message.startswith("f1") or message.startswith("f 1") or message.startswith("floor1") or message.startswith("F1")  or   message.startswith("floor 1") or message.startswith("!floor 1"):
          await self.highrise.teleport(user.id, Position(9.5 , 0.0 , 16.5))
                 
        if        message.startswith("-floor3") or message.startswith("!floor3") or message.startswith("-floor 3") or message.startswith("Floor 3") or message.startswith("Floor3") or message.startswith("/floor3") or    message.startswith("floor3") or message.startswith("-3") or    message.startswith("floor3") or message.startswith("f3") or message.startswith("f 3") or message.startswith("floor3") or message.startswith("F3")  or   message.startswith("floor 3") or message.startswith("!floor 3"):
          await self.highrise.teleport(user.id, Position(12.5 , 19.25 , 6.5))

        if        message.startswith("-floor4") or message.startswith("!floor4") or message.startswith("-floor 4") or message.startswith("Floor 4") or message.startswith("Floor4") or message.startswith("/floor4") or    message.startswith("floor4") or message.startswith("-4") or    message.startswith("floor4") or message.startswith("f4") or message.startswith("f 4") or message.startswith("floor4") or message.startswith("F4")  or   message.startswith("floor 4") or message.startswith("!floor 4"):
          await self.highrise.teleport(user.id, Position(14.5 , 20.0 , 1.5))
            
        if        message.startswith("-floor2") or message.startswith("!floor2") or message.startswith("-floor 2") or message.startswith("Floor 2") or message.startswith("Floor2") or message.startswith("/floor2") or    message.startswith("floor2") or message.startswith("-2") or    message.startswith("floor2") or message.startswith("f2") or message.startswith("f 2") or message.startswith("floor2") or message.startswith("F2")  or   message.startswith("floor 2") or message.startswith("!floor 2"):
          await self.highrise.teleport(user.id, Position(14.5 , 9.0 , 6.0))
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!angry ,!thumbsup , !cursing , !flex , !gagging , !celebrate , !blackpink , !tiktok2 , !tiktok9 , !pennywise , !russian , !shop , !enthused , !singing ,!wrong , !guitar , !pinguin , !astronaut , !saunter , !flirt , !creepy , !watch , !revelation")
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!tiktok10 ,!tiktok8 , !cutey , !pose3 , !pose5 , !pose1 , !pose8 , !pose7  !pose9 , !cute , !superpose , !frog , !snake , !energyball , !maniac , !teleport , !float , !telekinesi , !fight , !wei , !fashion , !boxer , !bashful , !arabesque , !party")
          
        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
            await self.highrise.send_whisper(user.id,"!confused , !charging , !snowangel , !hot , !snowball , !curtsy , !bow ,!model , !greedy , !tired , !shy , !wave , !hello , !lau ,!yes , !sad , !no , !kiss , !casual , !ren , !sit , !punk , !zombie , !gravity , !icecream ,!uwu , !sayso , !star")

        if        message.startswith("!lista") or    message.startswith("!emote list") or                                 message.startswith("!emote list") or message.startswith("!list"):
          await self.highrise.send_whisper(user.id,"!skating , !bitnervous , !scritchy , !timejump , !gottago , !jingle , !hyped , !sleigh , !surprise , !repose , !kawaii , !touch , !gift , !pushit , !tiktok , !salute , !attention , !smooch , !launch")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/angry ,/thumbsup , /cursing , /flex , /gagging , /celebrate , /blackpink , /tiktok2 , /tiktok9 , /pennywise , /russian , /shop , /enthused , /singing , /wrong , /guitar , /pinguin , /astronaut , /saunter , /flirt , /creepy , /watch , /revelation")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/tiktok10 , /tiktok8 , /cutey , /pose3 , /pose5 , /pose1 , /pose8 , /pose7  /pose9 , /cute , /superpose , /frog , /snake , /energyball , /maniac , /teleport , /float , /telekinesi , /fight , /wei , /fashion , /boxer , /bashful , /arabesque , /party")
          
        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
            await self.highrise.send_whisper(user.id,"/confused , /charging , /snowangel , /hot , /snowball , /curtsy , /bow ,/model , /greedy , /lust , /tired , /shy , /wave , /hello , /lau , /yes , /sad , /no , /kiss , /casual , /ren ,   /sit , /punk , /zombie , /gravity , /icecream ,/uwu , /sayso , /star")

        if        message.startswith("/lista") or    message.startswith("/emote list") or                                 message.startswith("/emote list") or message.startswith("/list"):
          await self.highrise.send_whisper(user.id,"/skating , /bitnervous , /scritchy , /timejump , /gottago , /jingle , /hyped , /sleigh , /surprise , /repose , /kawaii /touch , /pushit , /gift , /tiktok , /salute , /attention , /smooch , /launch")
        
        if        message.startswith("/lista") or         message.startswith("/emote list") or message.startswith("!emoteall") or message.startswith("!emote list") or message.startswith("!lista"):
            await self.highrise.send_emote("dance-floss")
                     
        if             message.startswith("!emotes") or message.startswith("/emotes"):
            await self.highrise.send_emote("emote-robot")
            await self.highrise.send_whisper(user.id,f"emotes available from number 1 to 97")

        if        message.startswith("-Help") or      message.startswith("/help") or      message.startswith("!help") or message.startswith("-help"):
            await self.highrise.chat(f"/lista | /pessoas | /emotes | | /marry me? | /play /fish /userinfo @ | !emoteall | !tele @ | !summon @ | !kick @ | !tele z,y,x | !tele @ z,y,x | ")
            await self.highrise.chat(f"[Emote] All | !emote all [Emote]")        
            await self.highrise.chat(f"{user.username} all activation codes must be used >> ! or/")
            await self.highrise.send_emote("dance-floss")
          
   
        if        message.startswith("/tp") or      message.startswith("!tp") or      message.startswith("tele") or          message.startswith("Tp") or          message.startswith("Tele") or  message.startswith("!tele"):
          target_username =         message.split("@")[-1].strip()
          await                     self.teleport_to_user(user, target_username)

        if                            message.startswith("Summon") or         message.startswith("Summom") or         message.startswith("!summom") or        message.startswith("/summom") or        message.startswith("/summon") or  message.startswith("!summon"):
          if user.username == "FallonXOXO" or user.username == "Its.Melly.Moo.XoXo" or user.username == "Shaun_Knox" or user.username == "sh1n1gam1699" or user.username == "Dreamy._.KY" or user.username == "hidinurbasement" or user.username == "@emping" or user.username == "_irii_" or user.username == "RayBM":
           target_username = message.split("@")[-1].strip()
           await self.teleport_user_next_to(target_username, user)
              
        if message.startswith("!kick"):
          if user.username == "FallonXOXO" or user.username == "RayBM":
              pass
          else:
              await self.highrise.chat("🤍.")
              return
          #separete message into parts
          parts = message.split()
          #check if message is valid "kick @username"
          if len(parts) != 2:
              await self.highrise.chat("🤍.")
              return
          #checks if there's a @ in the message
          if "@" not in parts[1]:
              username = parts[1]
          else:
              username = parts[1][1:]
          #check if user is in room
          room_users = (await self.highrise.get_room_users()).content
          for room_user, pos in room_users:
              if room_user.username.lower() == username.lower():
                  user_id = room_user.id
                  break
          if "user_id" not in locals():
              await self.highrise.chat("user not found, please fix the code coordinate ")
              return
          #kick user
          try:
              await self.highrise.moderate_room(user_id, "kick")
          except Exception as e:
              await self.highrise.chat(f"{e}")
              return
          #send message to chat
          await self.highrise.chat(f"{username} He was banned from the room!!")

    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Caught Teleport Error: {e}")

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
            print(f"An error occurred while teleporting to {target_username}: {e}")

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
                    new_z = z + 1  # Example: Move +1 on the z-axis (upwards)
                    await self.teleport(user, Position(requester_position.x, requester_position.y, new_z, requester_position.facing))
                    break
        except Exception as e:
            print(f"An error occurred while teleporting {target_username} next to {requester_user.username}: {e}")
          
    async def teleporter(self, message: str)-> None:
        """
            Teleports the user to the specified user or coordinate
            Usage: /teleport <username> <x,y,z>
                                                                """
        try:
            command, username, coordinate = message.split(" ")
        except:
            
            return
        
        #checks if the user is in the room
        room_users = (await self.highrise.get_room_users()).content
        for user in room_users:
            if user[0].username.lower() == username.lower():
                user_id = user[0].id
                break
        #if the user_id isn't defined, the user isn't in the room
        if "user_id" not in locals():
            
            return
            
        #checks if the coordinate is in the correct format (x,y,z)
        try:
            x, y, z = coordinate.split(",")
        except:
          
            return
        
        #teleports the user to the specified coordinate
        await self.highrise.teleport(user_id = user_id, dest = Position(float(x), float(y), float(z)))

# Handle when user starts moving
async def on_user_move(self, user: User, position: Position, *args, **kwargs):
    if user.id in user_loops:
        task = user_loops[user.id]
        if not task.cancelled():
            task.cancel()
        del user_loops[user.id]
        await self.highrise.send_whisper(user.id, "تم إيقاف التكرار مؤقتًا لأنك بدأت تتحرك.")

# Handle when user stops moving
async def on_user_stop_moving(self, user: User):
    if user.id not in user_loops:
        last_emote = last_emote_name.get(user.id, '')
        if last_emote:
            await self.highrise.send_whisper(user.id, "جارٍ استئناف التكرار...")
            await check_and_start_emote_loop(self, user, f"loop {last_emote}")

# Command handler for loop and stop
async def command_handler(self, user: User, message: str):
    parts = message.strip().split(" ")
    command = parts[0].lower()

    if command.startswith("-"):
        command = command[1:]

    if command == "loop":
        await check_and_start_emote_loop(self, user, message)
        return

    if command == "stop":
        if user.id in user_loops:
            task = user_loops[user.id]
            if not task.cancelled():
                task.cancel()
            del user_loops[user.id]
            await self.highrise.send_whisper(user.id, "تم إيقاف التكرار.")
        else:
            await self.highrise.send_whisper(user.id, "لا يوجد تكرار قيد التشغيل.")
        return

# Whisper handler to print incoming whispers for debugging
async def on_whisper(self, user: User, message: str) -> None:
    print(f"{user.username} whispered: {message}")

    # Broadcast messages from RayBM or botmes
    if user.username.lower() == "raybm" or user.username.lower() == "botmes":
        await self.highrise.chat(message)
        print(f"Broadcasted private message to the room: {message}")

    # Handle teleport-related commands
    if message.startswith(("tele", "/tp", "/fly", "!tele", "!tp", "!fly")):
        if user.username in [
            "FallonXOXO", "Its.Melly.Moo.XoXo", "sh1n1gam1699", "Abbie_38", 
            "hidinurbasement", "@emping", "BabygirlFae", "RayBM"
        ]:
            await self.teleporter(message)

    # Handle general commands
    if message.startswith(("/", "-", ".", "!")):
        await self.command_handler(user, message)

    # Handle summon commands
    if message.startswith(("Summon", "Summom", "!summom", "/summom", "/summon", "!summon")):
        if user.username in [
            "FallonXOXO", "Shaun_Knox", "@Its.Melly.Moo.XoXo", "@RayBM", "Dreamy._.KY"
        ]:
            target_username = message.split("@")[-1].strip()
            await self.teleport_user_next_to(target_username, user)

    # Handle wallet info
    if message.startswith(("Carteira", "Wallet", "wallet", "carteira")):
        if user.username in ["FallonXOXO", "sh1n1gam1699", "RayBM"]:
            wallet = (await self.highrise.get_wallet()).content
            await self.highrise.send_whisper(user.id, f"AMOUNT : {wallet[0].amount} {wallet[0].type}")
            await self.highrise.send_emote("emote-blowkisses")

# Optional debug movement logging
async def on_user_move(self, user: User, pos: Position) -> None:
    print(f"{user.username} moved to {pos}")

# Optional debug emote logging
async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
    print(f"{user.username} emoted: {emote_id}")
