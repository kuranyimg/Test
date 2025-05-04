import asyncio
from highrise import BaseBot, Position
from highrise.models import User
import asyncio
import time
from asyncio import run as arun

from highrise.__main__ import *

from equip import equip
from keep_alive import keep_alive
from remove_outfit import remove

keep_alive()
from highrise import *
from highrise import BaseBot, Position
from highrise.models import *
from highrise.models import (
  AnchorPosition,
  Position,
  SessionMetadata,
  User,
)

#  YOU CAN CHANGR VIP LIST RAY
vip = [
    "iced_yu","Damn_snake","love_cant_relate","RayMg","FallonXOXO"
]

class Bot(BaseBot):

  def __init__(self):

    self.user_teleport_position = Position(x=1.5, y=0.25, z=14.5, facing='FrontRight')
    self.user_teleport_position2 = Position(x=5.5, y=10.0, z=3.5, facing='FrontRight')
    self.user_teleport_position3 = Position(x=10.5, y=14.75, z=4.5, facing='FrontLeft')
    self.bar = Position(x=15.0, y=0.25, z=2.5, facing='FrontLeft')

    self.user_loops = {}

  async def get_users(self, selected_users, default_user):
    target_users = []
    if len(selected_users) == 0:
      return [default_user]

    users = await self.highrise.get_room_users()
    for user in users.content:
      if user[0].username in selected_users:
        target_users.append(user[0])
    return target_users

  async def on_user_join(self, user: User,position: Position | AnchorPosition) -> None:
          await self.highrise.send_whisper(user.id, f"welcome to the room {user.username}!")


  emote_dict = {
      "blow": {
          "emote": "emote-headblowup",
          "delay": 11.667537
      },
      "skate": {
          "emote": "emote-iceskating",
          "delay": 7.299156
      },
      "boxer": {
          "emote": "emote-boxer",
          "delay": 5.555702
      },
      "tired": {
          "emote": "emote-tired",
          "delay": 10
      },
      "dance": {
          "emote": "dance-macarena",
          "delay": 12.5
      },
      "loopsit": {
          "emote": "idle-loop-sitfloor",
          "delay": 10
      },
      "weird": {
          "emote": "dance-weird",
          "delay": 22
      },
      "laugh": {
          "emote": "emote-laughing",
          "delay": 3
      },
      "kiss": {
          "emote": "emote-kiss",
          "delay": 3
      },
      "wave": {
          "emote": "emote-wave",
          "delay": 10
      },
      "teleport": {
          "emote": "emote-teleporting",
          "delay": 12.5
      },
      "hot": {
          "emote": "emote-hot",
          "delay": 4.8
      },
      "shopping": {
          "emote": "dance-shoppingcart",
          "delay": 5
      },
      "greedy": {
          "emote": "emote-greedy",
          "delay": 4.8
      },
      "float": {
          "emote": "emote-float",
          "delay": 9.3
      },
      "celebrate": {
          "emote": "emoji-celebrate",
          "delay": 4
      },
      "wop": {
          "emote": "dance-tiktok11",
          "delay": 11
      },
      "swordfight": {
          "emote": "emote-swordfight",
          "delay": 6
      },
      "sexy": {
            "emote": "dance-sexy",
            "delay": 6
        },

      "shy": {
          "emote": "emote-shy",
          "delay": 10
      },
      "tiktok2": {
          "emote": "dance-tiktok2",
          "delay": 11
      },
      "charging": {
          "emote": "emote-charging",
          "delay": 8.5
      },
      "worm": {
          "emote": "emote-snake",
          "delay": 6
      },
      "russian": {
          "emote": "dance-russian",
          "delay": 10.3
      },
      "sad": {
          "emote": "emote-sad",
          "delay": 10
      },
      "cursing": {
          "emote": "emoji-cursing",
          "delay": 2.5
      },
      "flex": {
          "emote": "emoji-flex",
          "delay": 3
      },
      "gagging": {
          "emote": "emoji-gagging",
          "delay": 6
      },
      "tiktok8": {
          "emote": "dance-tiktok8",
          "delay": 11
      },
      "kpop": {
          "emote": "dance-blackpink",
          "delay": 7
      },
      "pennywise": {
          "emote": "dance-pennywise",
          "delay": 1.5
      },
      "bow": {
          "emote": "emote-bow",
          "delay": 3.3
      },
      "curtsy": {
          "emote": "emote-curtsy",
          "delay": 2.8
      },
      "snowangel": {
          "emote": "emote-snowangel",
          "delay": 6.8
      },
      "energyball": {
          "emote": "emote-energyball",
          "delay": 8.3
      },
      "frog": {
          "emote": "emote-frog",
          "delay": 15
      },
      "cute": {
          "emote": "emote-cute",
          "delay": 7.3
      },
      "tiktok9": {
          "emote": "dance-tiktok9",
          "delay": 13
      },
      "shuffle": {
          "emote": "dance-tiktok10",
          "delay": 9
      },
      "pose7": {
          "emote": "emote-pose7",
          "delay": 5.3
      },
      "pose8": {
          "emote": "emote-pose8",
          "delay": 4.6
      },
      "casual": {
          "emote": "idle-dance-casual",
          "delay": 9.7
      },
      "pose1": {
          "emote": "emote-pose1",
          "delay": 3
      },
      "pose3": {
          "emote": "emote-pose3",
          "delay": 4.7
      },
      "pose5": {
          "emote": "emote-pose5",
          "delay": 5
      },
      "cutey": {
          "emote": "emote-cutey",
          "delay": 3.5
      },
      "model": {
          "emote": "emote-model",
          "delay": 6.3
      },
      "astro": {
          "emote": "emote-astronaut",
          "delay": 0
      },  # No delay specified, set to 0
      "guitar": {
          "emote": "emote-punkguitar",
          "delay": 10
      },
      "fashionista": {
          "emote": "emote-fashionista",
          "delay": 6
      },
      "uwu": {
          "emote": "idle-uwu",
          "delay": 25
      },
      "wrong": {
          "emote": "dance-wrong",
          "delay": 13
      },
      "sayso": {
          "emote": "idle-dance-tiktok4",
          "delay": 16
      },
      "maniac": {
          "emote": "emote-maniac",
          "delay": 5.5
      },
      "enthused": {
          "emote": "idle-enthusiastic",
          "delay": 16.5
      },
      "happy": {
          "emote": "emote-happy",
          "delay": 0
      },  # No delay specified, set to 0
      "timejump": {
          "emote": "emote-timejump",
          "delay": 1.9
      },  # No delay specified, set to 0
      "creepy": {
          "emote": "dance-creepypuppet",
          "delay": 10
      },
      "sleigh": {
          "emote": "emote-sleigh",
          "delay": 9
      },  # No delay specified, set to 0
      "singing": {
          "emote": "idle_singing",
          "delay": 12
      },
      "anime": {
          "emote": "dance-anime",
          "delay": 8.4
      },  # No delay specified, set to 0
      "hyped": {
          "emote": "emote-hyped",
          "delay": 6.7
      },  # No delay specified, set to 0
      "jingle": {
          "emote": "dance-jinglebell",
          "delay": 11.8
      },  # No delay specified, set to 0
      "snowball": {
          "emote": "emote-snowball",
          "delay": 6
      },
      "cutesalute": {
          "emote": "emote-cutesalute",
          "delay": 22.321055
      },
      "enthused": {
          "emote": "idle-enthusiastic",
          "delay": 15.941537
      },
      "salute": {
          "emote":"emote-salute",
          "delay": 3
      },
      "pushit": {
          "emote": "dance-employee",
          "delay": 8
      },
      "gift": {
          "emote": "emote-gift",
          "delay": 5.8
      },
      "touch": {
          "emote": "dance-touch",
          "delay": 10.000
      },
      "creepycute": {
          "emote": "emote-creepycute",
          "delay": 7.902453
      },
      "kawai": {
          "emote": "dance-kawai",
          "delay": 7.9
      },
      "scritchy": {
          "emote":"idle-wild",
          "delay": 26.422824},
      "nervous":
      {"emote":"idle-nervous",
      'delay': 21.714221},
      "toilet":
        {"emote":"idle-toilet",
        'delay': 32.174447},

      "superpose":
        {"emote":"emote-superpose",
        'delay': 4.530791}
  }


    async def send_emote_loop(self, emote_data, user_id):
        try:
            while user_id in self.user_loops:
                await self.highrise.send_emote(emote_data["emote"], user_id)
                await asyncio.sleep(emote_data["delay"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[ERROR] send_emote_loop: {e}")

    async def stop_loop(self, user: User):
        if user.user_id in self.user_loops:
            loop_task = self.user_loops[user.user_id]["loop"]
            loop_task.cancel()
            del self.user_loops[user.user_id]
            await self.highrise.chat(f"{user.username}, loop stopped.")

    async def start_loop(self, user: User, emote_key: str):
        emote_data = self.emote_dict.get(emote_key.lower())
        if emote_data:
            await self.stop_loop(user)
            task = asyncio.create_task(self.send_emote_loop(emote_data, user.user_id))
            self.user_loops[user.user_id] = {
                "command": emote_data,
                "loop": task,
                "moving": False
            }
            await self.highrise.chat(f"{user.username}, looping: {emote_key}")
        else:
            await self.highrise.chat(f"Unknown emote: {emote_key}")

    async def do_emote_once(self, user: User, emote_key: str):
        emote_data = self.emote_dict.get(emote_key.lower())
        if emote_data:
            await self.highrise.send_emote(emote_data["emote"], user.user_id)
        else:
            await self.highrise.chat(f"Unknown emote: {emote_key}")

    async def handle_message(self, user: User, message: str):
        msg = message.strip()
        msg_lower = msg.lower()

        # If stop command
        if msg_lower == "stop":
            await self.stop_loop(user)
            return

        # Check for loop commands
        for prefix in ["loop ", "!loop ", "-loop ", "Loop "]:
            if msg_lower.startswith(prefix):
                emote_key = msg[len(prefix):].strip()
                await self.start_loop(user, emote_key)
                return

        # If just emote name or number
        # First check if it's a valid number in emote_dict, then check the name.
        if msg_lower in self.emote_dict:
            await self.do_emote_once(user, msg_lower)
        elif msg.isdigit() and msg in self.emote_dict:
            await self.do_emote_once(user, msg)
        else:
            await self.highrise.chat(f"Unknown emote: {msg}")

    async def on_whisper(self, user: User, message: str) -> None:
        print(f"[WHISPER] {user.username}: {message}")
        await self.handle_message(user, message)

    async def on_chat(self, user: User, message: str) -> None:
        print(f"[CHAT] {user.username}: {message}")
        await self.handle_message(user, message)

    async def on_position_update(self, user: User, position: Position) -> None:
        if user.user_id in self.user_loops:
            moving = position.is_moving
            loop_info = self.user_loops[user.user_id]
            was_moving = loop_info.get("moving", False)

            if moving and not was_moving:
                # User started moving -> pause
                loop_info["loop"].cancel()
                loop_info["moving"] = True

            elif not moving and was_moving:
                # User stopped moving -> resume
                task = asyncio.create_task(self.send_emote_loop(loop_info["command"], user.user_id))
                loop_info["loop"] = task
                loop_info["moving"] = False
