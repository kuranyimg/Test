import asyncio
import traceback
import json
import os
import random
from highrise import BaseBot
from highrise.models import User

# ملف لحفظ حالة loop البوت
BOT_LOOP_FILE = "bot_emote_loop.json"

emote_list: list[tuple[list[str], str, float]] = [
    (['rest', 'REST', 'Rest', '0'], 'sit-idle-cute', 16.50),
    (['Kawaii Go Go', 'kawaii go go', '1'], 'dance-kawai', 10.85),
    (['Hyped', 'hyped', '2'], 'hyped', 7.62),
    (['Levitate', 'levitate', '3'], 'emoji-halo', 6.52),
    (['Rest', 'rest', '4'], 'sit-idle-cute', 17.73),
    (['Hero Pose', 'hero pose', '5'], 'hero', 22.33),
    (['Uhmmm', 'uhmmm', '6'], 'thought', 27.43),
    (['Crouch', 'crouch', '7'], 'crouched', 28.27),
    (['Zero Gravity', 'zero gravity', '8'], 'astronaut', 13.93),
    (['Zombie Run', 'zombie run', '9'], 'zombierun', 10.05),
    (['Wait', 'wait', '10'], 'dance-wait', 9.92),
    (['Dab', 'dab', '11'], 'dab', 3.75),
    (['Ignition Boost', 'ignition boost', '12'], 'hcc-jetpack', 27.45),
    (['Do The Worm', 'do the worm', '13'], 'snake', 6.63),
    (['Bummed', 'bummed', '14'], 'sad', 21.80),
    (['Chillin\'', 'chillin\'', '15'], 'happy', 19.80),
    (['Sweet Smooch', 'sweet smooch', '16'], 'kissing', 6.69),
    (['Emoji Shush', 'emoji shush', '17'], 'emoji-shush', 3.40),
    (['Idle Tough', 'idle tough', '18'], 'tough', 28.64),
    (['Fail3', 'fail3', '19'], 'fail3', 7.06),
    (['Shocked', 'shocked', '20'], 'shocked', 5.59),
    (['Theatrical Test', 'theatrical test', '21'], 'theatrical-test', 10.86),
    (['Fireworks', 'fireworks', '22'], 'fireworks', 13.15),
    (['Electrified', 'electrified', '23'], 'electrified', 5.29),
    (['Headless', 'headless', '24'], 'headless', 41.80),
    (['Armcannon', 'armcannon', '25'], 'armcannon', 8.67),
    (['Dance Tiktok4', 'dance tiktok4', '26'], 'dance-tiktok4', 15.00),
    (['Dance Tiktok7', 'dance tiktok7', '27'], 'dance-tiktok7', 13.89),
    (['Don\'t Touch Dance', 'don\'t touch dance', '28'], 'dance-tiktok13', 9.24),
    (['Hip Hop Dance', 'hip hop dance', '29'], 'dance-hiphop', 27.59),
    (['Hopscotch', 'hopscotch', '30'], 'hopscotch', 5.84),
    (['Outfit2', 'outfit2', '31'], 'outfit2', 11.94),
    (['Pose12', 'pose12', '32'], 'pose12', 5.81),
    (['Fading', 'fading', '33'], 'fading', 14.05),
    (['Pose13', 'pose13', '34'], 'pose13', 6.39),
    (['Profile Breakscreen', 'profile breakscreen', '35'], 'profile-breakscreen', 10.70),
    (['Surf', 'surf', '36'], 'surf', 19.01),
    (['Cartwheel', 'cartwheel', '37'], 'cartwheel', 7.94),
    (['Kissing Passionate', 'kissing passionate', '38'], 'kissing-passionate', 10.47),
    (['Dance Tiktok1', 'dance tiktok1', '39'], 'dance-tiktok1', 12.42),
    (['Run Vertical', 'run vertical', '40'], 'run-vertical', 3.86),
    (['Flirt', 'flirt', '41'], 'flirt', 7.95),
    (['Receive Disappointed', 'receive disappointed', '42'], 'receive-disappointed', 7.14),
    (['Gooey', 'gooey', '43'], 'gooey', 5.82),
    (['Oops', 'oops', '44'], 'oops', 8.02),
    (['Walk Vertical', 'walk vertical', '45'], 'walk-vertical', 4.18),
    (['Thief', 'thief', '46'], 'thief', 6.89),
    (['Sheephop', 'sheephop', '47'], 'sheephop', 3.78),
    (['Runhop', 'runhop', '48'], 'runhop', 8.72),
    (['Tiktok15', 'dance tiktok15', '49'], 'dance-tiktok15', 16.11),
    (['Receive Happy', 'receive happy', '50'], 'receive-happy', 5.94),
    (['Tiktok6', 'dance tiktok6', '51'], 'dance-tiktok6', 11.99),
    (['Confused2', 'confused2', '52'], 'confused2', 10.06),
    (['Muscle Pose', 'muscle pose', '53'], 'pose4', 6.08),
    (['Dinner', 'dinner', '54'], 'dinner', 14.25),
    (['Wavey', 'wavey', '55'], 'wavey', 12.60),
    (['Pose2', 'pose2', '56'], 'pose2', 7.20),
    (['DShuffle', 'shuffle', '57'], 'dance-shuffle', 9.05),
    (['Twitched', 'twitched', '58'], 'twitched', 9.61),
    (['Juggling', 'juggling', '59'], 'juggling', 5.83),
    (['Dance Tiktok6', 'dance tiktok6', '60'], 'dance-tiktok6', 9.73),
    (['Opera', 'opera', '61'], 'opera', 5.76),
    (['Dance Tiktok3', 'dance tiktok3', '62'], 'dance-tiktok3', 10.40),
    (['Dance Kid', 'dance kid', '63'], 'dance-kid', 10.30),
    (['Dance Anime3', 'dance anime3', '64'], 'dance-anime3', 12.37),
    (['Dance Tiktok16', 'dance tiktok16', '65'], 'dance-tiktok16', 11.02),
    (['Poke Dance', 'poke dance', '66'], 'dance-tiktok12', 14.85),
    (['Dance Tiktok5', 'dance tiktok5', '67'], 'dance-tiktok5', 12.20),
    (['Cold', 'cold', '68'], 'cold', 17.71),
    (['Pose11', 'pose11', '69'], 'pose11', 5.11),
    (['Handwalk', 'handwalk', '70'], 'handwalk', 7.77),
    (['Dramatic', 'dramatic', '71'], 'dramatic', 9.10),
    (['Outfit', 'outfit', '72'], 'outfit', 13.20),
    (['Phone', 'phone', '73'], 'phone', 31.36),
    (['Sit Chair', 'sit chair', '74'], 'sit-chair', 3.30),
    (['Space', 'space', '75'], 'space', 37.78),
    (['Mining Mine', 'mining mine', '76'], 'mining-mine', 5.02),
    (['Mining Success', 'mining success', '77'], 'mining-success', 3.11),
    (['Mining Fail', 'mining fail', '78'], 'mining-fail', 3.41),
    (['Landing a Fish!', 'landing a fish', '79'], 'fishing-pull', 2.81),
    (['Now We Wait...', 'now we wait', '80'], 'fishing-idle', 17.87),
    (['Casting!', 'casting', '81'], 'fishing-cast', 2.82),
    (['We Have a Strike!', 'we have a strike', '82'], 'fishing-pull-small', 3.67),
    (['Hip Shake', 'hip shake', '83'], 'dance-hipshake', 13.38),
    (['Fruity Dance', 'fruity dance', '84'], 'dance-fruity', 18.25),
    (['Cheer', 'cheer', '85'], 'dance-cheerleader', 17.93),
    (['Magnetic', 'magnetic', '86'], 'dance-tiktok14', 11.20),
    (['Blowing Kisses', 'blowing kisses', '87'], 'blowkisses', 5.98),
    (['Fairy Twirl', 'fairy twirl', '88'], 'looping', 9.89),
    (['Fairy Float', 'fairy float', '89'], 'floating', 27.60),
    (['Karma Dance', 'karma dance', '90'], 'dance-wild', 16.25),
    (['Moonlit Howl', 'moonlit howl', '91'], 'howl', 8.10),
    (['Nocturnal Howl', 'nocturnal howl', '92'], 'howl', 48.62),
    (['Trampoline', 'trampoline', '93'], 'trampoline', 6.11),
    (['Launch', 'launch', '94'], 'launch', 10.88),
    (['Cute Salute', 'cute salute', '95'], 'cutesalute', 3.79),
    (['At Attention', 'at attention', '96'], 'salute', 4.
    (['Wop Dance', 'wop dance', '97'], 'dance-tiktok11', 11.37),
    (['Push It', 'push it', '98'], 'dance-employee', 8.55),
    (['This Is For You!', 'this is for you', '99'], 'gift', 6.09),
    (['Sweet Little Moves', 'sweet little moves', '100'], 'dance-touch', 13.15),
    (['Repose', 'repose', '101'], 'sit-relaxed', 31.21),
    (['Sleigh Ride', 'sleigh ride', '102'], 'sleigh', 12.51),
    (['Gimme Attention!', 'gimme attention', '103'], 'attention', 5.65),
    (['Jingle Hop', 'jingle hop', '104'], 'dance-jinglebell', 12.09),
    (['Timejump', 'timejump', '105'], 'timejump', 5.51),
    (['Gotta Go!', 'gotta go', '106'], 'toilet', 33.48),
    (['Bit Nervous', 'bit nervous', '107'], 'nervous', 22.81),
    (['Scritchy', 'scritchy', '108'], 'wild', 27.35),
    (['Ice Skating', 'ice skating', '109'], 'iceskating', 8.41),
    (['Laid Back', 'laid back', '110'], 'sit-open', 27.28),
    (['Party Time!', 'party time', '111'], 'celebrate', 4.35),
    (['Shrink', 'shrink', '112'], 'shrink', 9.99),
    (['Arabesque', 'arabesque', '113'], 'pose10', 5.00),
    (['Bashful Blush', 'bashful blush', '114'], 'shy2', 6.00),
    (['Possessed Puppet', 'possessed puppet', '115'], 'puppet', 17.89),
    (['Revelations', 'revelations', '116'], 'headblowup', 13.66),
    (['Watch Your Back', 'watch your back', '117'], 'creepycute', 9.01),
    (['Creepy Puppet', 'creepy puppet', '118'], 'creepypuppet', 7.79),
    (['Saunter Sway', 'saunter sway', '119'], 'dance-anime', 9.60),
    (['Groovy Penguin', 'groovy penguin', '120'], 'dance-pinguin', 12.81),
    (['Air Guitar', 'air guitar', '121'], 'guitar', 14.15),
    (['Ready To Rumble', 'ready to rumble', '122'], 'boxer', 6.75),
    (['Celebration Step', 'celebration step', '123'], 'celebrationstep', 5.18),
    (['Big Surprise', 'big surprise', '124'], 'pose6', 6.46),
    (['Ditzy Pose', 'ditzy pose', '125'], 'pose9', 6.00),
    (['Stargazing', 'stargazing', '126'], 'stargazer', 7.93),
    (['Dance Wrong', 'dance wrong', '127'], 'dance-wrong', 13.60),
    (['UWU Mood', 'uwu mood', '128'], 'uwu', 25.50),
    (['Fashionista', 'fashionista', '129'], 'fashionista', 6.33),
    (['Dance Icecream', 'dance icecream', '130'], 'dance-icecream', 16.58),
    (['Gravity', 'gravity', '131'], 'gravity', 9.02),
    (['Punkguitar', 'punkguitar', '132'], 'punkguitar', 10.59),
    (['Say So Dance', 'say so dance', '133'], 'dance-tiktok4', 16.55),
    (['Cutie', 'cutie', '134'], 'cutey', 4.07),
    (['Fashion Pose', 'fashion pose', '135'], 'pose5', 5.49),
    (['I Challenge You!', 'i challenge you', '136'], 'pose3', 5.57),
    (['Flirty Wink', 'flirty wink', '137'], 'pose1', 4.71),
    (['A Casual Dance', 'a casual dance', '138'], 'dance-casual', 9.57),
    (['Cheerful', 'cheerful', '139'], 'pose8', 5.62),
    (['Embracing Model', 'embracing model', '140'], 'pose7', 5.28),
    (['Fighter', 'fighter', '141'], 'fighter', 18.64),
    (['Shuffle Dance', 'shuffle dance', '142'], 'dance-tiktok10', 9.41),
    (['Renegade', 'renegade', '143'], 'dance-tiktok7', 14.05),
    (['Grave Dance', 'grave dance', '144'], 'dance-weird', 22.87),
    (['Viral Groove', 'viral groove', '145'], 'dance-tiktok9', 13.04),
    (['Cute', 'cute', '146'], 'cute', 7.20),
    (['Lambi\'s Pose', 'lambi\'s pose', '147'], 'superpose', 5.43),
    (['Froggie Hop', 'froggie hop', '148'], 'frog', 16.14),
    (['Sing Along', 'sing along', '149'], 'singing', 11.31),
    (['Energy Ball', 'energy ball', '150'], 'energyball', 8.28),
    (['Maniac', 'maniac', '151'], 'maniac', 5.94),
    (['Sword Fight', 'sword fight', '152'], 'swordfight', 7.71),
    (['Teleport', 'teleport', '153'], 'teleporting', 12.89),
    (['Floating', 'floating', '154'], 'float', 9.26),
    (['Telekinesis', 'telekinesis', '155'], 'telekinesis', 11.01),
    (['Slap', 'slap', '156'], 'slap', 4.06),
    (['Pissed Off', 'pissed off', '157'], 'frustrated', 6.41),
    (['Embarrassed', 'embarrassed', '158'], 'embarrassed', 9.09),
    (['Enthused', 'enthused', '159'], 'enthusiastic', 17.53),
    (['Confusion', 'confusion', '160'], 'confused', 9.58),
    (['Shopping', 'go shopping', '161'], 'shoppingcart', 5.56),
    (['ROFL!', 'rofl', '162'], 'rofl', 7.65),
    (['Roll', 'roll', '163'], 'roll', 4.31),
    (['Super Run', 'super run', '164'], 'superrun', 7.16),
    (['Super Punch', 'super punch', '165'], 'superpunch', 5.75),
    (['Super Kick', 'super kick', '166'], 'kicking', 6.21),
    (['Falling Apart', 'falling apart', '167'], 'apart', 5.98),
    (['Partner Hug', 'partner hug', '168'], 'hug', 4.53),
    (['Secret Handshake', 'secret handshake', '169'], 'secrethandshake', 6.28),
    (['Peekaboo!', 'peekaboo', '170'], 'peekaboo', 4.52),
    (['Monster Fail', 'monster fail', '171'], 'monster_fail', 5.42),
    (['Zombie Dance', 'zombie dance', '172'], 'dance-zombie', 13.83),
    (['Rope Pull', 'rope pull', '173'], 'ropepull', 10.69),
    (['Proposing', 'proposing', '174'], 'proposing', 5.91),
    (['Sumo Fight', 'sumo fight', '175'], 'sumo', 11.64),
    (['Charging', 'charging', '176'], 'charging', 9.53),
    (['Ninja Run', 'ninja run', '177'], 'ninjarun', 6.50),
    (['Elbow Bump', 'elbow bump', '178'], 'elbowbump', 6.44),
    (['Irritated', 'irritated', '179'], 'angry', 26.07),
    (['Home Run!', 'home run', '180'], 'baseball', 8.47),
    (['Revival', 'revival', '201'], 'death', 8.00),
    (['Penny\'s Dance', 'penny\'s dance', '202'], 'pennywise', 4.16),
    (['Sleepy', 'sleepy', '203'], 'sleep', 3.35),
    (['Attentive', 'attentive', '204'], 'layingdown', 26.11),
    (['Theatrical', 'theatrical', '205'], 'theatrical', 11.00),
    (['Faint', 'faint', '206'], 'fainting', 18.55),
    (['Relaxed', 'relaxed', '207'], 'layingdown2', 22.59),
    (['I Believe I Can Fly', 'i believe i can fly', '208'], 'wings', 14.21),
    (['Amused', 'amused', '209'], 'laughing2', 6.60),
    (['Floss', 'floss', '210'], 'floss', 23.13),
    (['Don\'t Start Now', 'don\'t start now', '211'], 'dance-tiktok2', 11.37),
    (['Model', 'model', '212'], 'model', 7.43),
    (['K-Pop Dance', 'k-pop dance', '213'], 'dance-blackpink', 7.97),
    (['Karate', 'karate', '214'], 'dance-martial-artist', 13.97),
    (['Sick', 'sick', '215'], 'emoji-sick', 6.22),
    (['Zombie', 'zombie', '216'], 'zombie', 31.39),
    (['Cold', 'cold', '217'], 'cold', 5.17),
    (['Bunny Hop', 'bunny hop', '218'], 'bunnyhop', 13.63),
    (['Disco', 'disco', '219'], 'disco', 6.14),
    (['Wiggle Dance', 'wiggle dance', '220'], 'dance-sexy', 13.70),
    (['Heart Hands', 'heart hands', '221'], 'heartfingers', 5.18),
    (['Savage Dance', 'savage dance', '222'], 'dance-tiktok8', 13.10),
    (['Ghost Float', 'ghost float', '223'], 'ghost-idle', 20.43),
    (['Sneeze', 'sneeze', '224'], 'emoji-sneeze', 4.33),
    (['Pray', 'pray', '225'], 'emoji-pray', 6.00),
    (['Handstand', 'handstand', '226'], 'handstand', 5.89),
    (['Smoothwalk', 'smoothwalk', '227'], 'dance-smoothwalk', 7.58),
    (['Ring on It', 'ring on it', '228'], 'dance-singleladies', 22.33),
    (['Yoga Flow', 'yoga flow', '229'], 'dance-spiritual', 17.71),
    (['Partner Heart Arms', 'partner heart arms', '230'], 'heartshape', 7.60),
    (['Ghost', 'ghost', '231'], 'emoji-ghost', 3.74),
    (['Push Ups', 'push ups', '232'], 'dance-aerobics', 9.89),
    (['Naughty', 'naughty', '233'], 'emoji-naughty', 5.73),
    (['Robotic', 'robotic', '234'], 'dance-robotic', 12.23),
    (['Faint Drop', 'faint drop', '235'], 'deathdrop', 4.18),
    (['Duck Walk', 'duck walk', '236'], 'dance-duckwalk', 12.48),
    (['Splits Drop', 'splits drop', '237'], 'splitsdrop', 5.31),
    (['Vogue Hands', 'vogue hands', '238'], 'dance-voguehands', 10.57),
    (['Give Up', 'give up', '239'], 'emoji-give-up', 6.04),
    (['Smirk', 'smirk', '240'], 'smirking', 5.74),
    (['Lying', 'lying', '241'], 'emoji-lying', 7.39),
    (['Arrogance', 'arrogance', '242'], 'emoji-arrogance', 8.16),
    (['Breakdance', 'breakdance', '243'], 'dance-breakdance', 17.94),
    (['Point', 'point', '244'], 'emoji-there', 3.09),
    (['Stinky', 'stinky', '245'], 'emoji-poop', 5.86),
    (['Fireball Lunge', 'fireball lunge', '246'], 'emoji-hadoken', 4.29),
    (['Punch', 'punch', '247'], 'emoji-punch', 3.36),
    (['Hands in the Air', 'hands in the air', '248'], 'dance-handsup', 23.18),
    (['Rock Out', 'rock out', '249'], 'dance-metal', 15.78),
    (['Orange Juice Dance', 'orange juice dance', '250'], 'dance-orangejustice', 7.17),
    (['Aerobics', 'aerobics', '251'], 'idle-loop-aerobics', 10.08),
    (['Boogie Swing', 'boogie swing', '252'], 'idle-dance-swinging', 14.47),
    (['Annoyed', 'annoyed', '253'], 'idle-loop-annoyed', 18.62),
    (['Gasp', 'gasp', '254'], 'emoji-scared', 4.06),
    (['Think', 'think', '255'], 'think', 4.81),
    (['Fatigued', 'fatigued', '256'], 'idle-loop-tired', 11.23),
    (['Feel The Beat', 'feel the beat', '257'], 'idle-dance-headbobbing', 23.65),
    (['Blast Off', 'blast off', '258'], 'disappear', 5.53),
    (['Sob', 'sob', '259'], 'emoji-crying', 4.91),
    (['Tap Loop', 'tap loop', '260'], 'idle-loop-tapdance', 7.81),
]


user_last_positions = {}
# -----------------------------------------
# USER EMOTE LOOP
# -----------------------------------------
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    try:
        cleaned_msg = message.strip().lower()

        if cleaned_msg in ("stop", "/stop", "!stop", "-stop"):
            if user.id in self.user_loops:
                self.user_loops[user.id]["task"].cancel()
                del self.user_loops[user.id]
                await self.highrise.send_whisper(user.id, "Emote loop stopped. (Type any emote name or number to start again)")
            else:
                await self.highrise.send_whisper(user.id, "You don't have an active emote loop.")
            return

        selected = next((e for e in emote_list if cleaned_msg in [a.lower() for a in e[0]]), None)
        if selected:
            aliases, emote_id, duration = selected

            if user.id in self.user_loops:
                self.user_loops[user.id]["task"].cancel()

            async def emote_loop():
                try:
                    while True:
                        if not self.user_loops[user.id]["paused"]:
                            room_users = await self.highrise.get_room_users()
                            user_ids = [u.id for u, _ in room_users.content]
                            if user.id not in user_ids:
                                self.user_loops[user.id]["task"].cancel()
                                del self.user_loops[user.id]
                                return
                            await self.highrise.send_emote(emote_id, user.id)
                        await asyncio.sleep(duration)
                except asyncio.CancelledError:
                    pass
                except Exception:
                    traceback.print_exc()

            task = asyncio.create_task(emote_loop())
            self.user_loops[user.id] = {
                "paused": False,
                "emote_id": emote_id,
                "duration": duration,
                "task": task,
            }

            await self.highrise.send_whisper(
                user.id,
                f"You are now in a loop for emote number {aliases[0]}. (To stop, type 'stop')",
            )
    except Exception:
        traceback.print_exc()

# -----------------------------------------
# توقف واستئناف المستخدم عند الحركة
# -----------------------------------------
async def handle_user_movement(self: BaseBot, user: User, pos) -> None:
    try:
        if user.id not in self.user_loops:
            return
        old_pos = user_last_positions.get(user.id)
        user_last_positions[user.id] = (pos.x, pos.y, pos.z)

        if old_pos is None:
            return
        if old_pos != (pos.x, pos.y, pos.z):
            self.user_loops[user.id]["paused"] = True
            await asyncio.sleep(2)
            new_pos = user_last_positions.get(user.id)
            if new_pos == (pos.x, pos.y, pos.z):
                self.user_loops[user.id]["paused"] = False
    except Exception:
        traceback.print_exc()

# ================================================
# 👇 BOT EMOTE LOOP
# ================================================

loop_file_path = "functions/bot_emote_loop.json"
bot_loop_data = {
    "emotes": [],
    "mode": "order",  # or "random"
}
bot_loop_task = None

def save_bot_loop():
    with open(loop_file_path, "w") as f:
        json.dump(bot_loop_data, f)

def load_bot_loop():
    global bot_loop_data
    if os.path.exists(loop_file_path):
        try:
            with open(loop_file_path, "r") as f:
                bot_loop_data = json.load(f)
        except Exception:
            pass

async def handle_bot_emote_loop(self: BaseBot, user: User, message: str):
    global bot_loop_task
    msg = message.strip()
    lower = msg.lower()

    if lower in ("rest loop", "reset loop", "stop loop", "stop bot loop"):
        await stop_bot_emote_loop(self, user)
        return

    if lower == "loop list":
        if not bot_loop_data["emotes"]:
            await self.highrise.send_whisper(user.id, "Bot has no emotes saved.")
            return
        txt = "🤖 Bot Emote Loop:\n"
        for idx, emote in enumerate(bot_loop_data["emotes"], 1):
            txt += f"{idx}. {emote['emote_id']} - {emote['duration']:.1f}s\n"
        await self.highrise.send_whisper(user.id, txt)
        return

    if lower.startswith("loopr "):
        target = lower.replace("loopr", "").strip()
        removed = False
        for i, e in enumerate(bot_loop_data["emotes"]):
            if e["emote_id"] == target:
                bot_loop_data["emotes"].pop(i)
                removed = True
                break
        if removed:
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Removed emote: {target}")
        else:
            await self.highrise.send_whisper(user.id, f"❌ Emote not found: {target}")
        return

    if lower.startswith("loop mode "):
        mode = lower.replace("loop mode", "").strip()
        if mode in ("random", "order"):
            bot_loop_data["mode"] = mode
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Bot loop mode set to {mode}.")
        else:
            await self.highrise.send_whisper(user.id, "❌ Mode must be 'order' or 'random'.")
        return

    if lower.startswith("loop "):
        emote_name = lower.replace("loop", "").strip()
        selected = next((e for e in emote_list if emote_name in [a.lower() for a in e[0]]), None)
        if selected:
            _, emote_id, duration = selected
            bot_loop_data["emotes"].append({"emote_id": emote_id, "duration": duration})
            save_bot_loop()
            await self.highrise.send_whisper(user.id, f"✅ Bot will now loop: {emote_id}")
            if not bot_loop_task or bot_loop_task.done():
                bot_loop_task = asyncio.create_task(start_bot_loop(self))
        else:
            await self.highrise.send_whisper(user.id, f"❌ Emote not recognized: {emote_name}")

async def start_bot_loop(self: BaseBot):
    try:
        while True:
            if not bot_loop_data["emotes"]:
                await asyncio.sleep(5)
                continue

            if bot_loop_data["mode"] == "random":
                chosen = random.choice(bot_loop_data["emotes"])
                await self.highrise.send_emote(chosen["emote_id"])
                await asyncio.sleep(chosen["duration"])
            else:
                for emote in bot_loop_data["emotes"]:
                    await self.highrise.send_emote(emote["emote_id"])
                    await asyncio.sleep(emote["duration"])
    except asyncio.CancelledError:
        pass
    except Exception:
        traceback.print_exc()

async def stop_bot_emote_loop(self: BaseBot, user: User):
    global bot_loop_task
    if bot_loop_task and not bot_loop_task.done():
        bot_loop_task.cancel()
        bot_loop_task = None
        bot_loop_data["emotes"].clear()
        save_bot_loop()
        await self.highrise.send_whisper(user.id, "🛑 Bot emote loop stopped.")
    else:
        await self.highrise.send_whisper(user.id, "❌ No active bot loop to stop.")
