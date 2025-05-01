import asyncio
from highrise import BaseBot
from highrise.models import 
# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
"Kawaii Go Go": {
"id": "dance-kawai",
"duration": 10.851059913635254,
"is_free": true
},
"Hyped": {
"id": "emote-hyped",
"duration": 7.621847867965698,
"is_free": true
},
"Levitate": {
"id": "emoji-halo",
"duration": 6.522106409072876,
"is_free": true
},
"Rest": {
"id": "sit-idle-cute",
"duration": 17.733200788497925,
"is_free": false
},
"Hero Pose": {
"id": "idle-hero",
"duration": 22.32689070701599,
"is_free": true
},
"Uhmmm": {
"id": "emote-thought",
"duration": 27.43184781074524,
"is_free": false
},
"Crouch": {
"id": "idle-crouched",
"duration": 28.274845600128174,
"is_free": false
},
"Zero Gravity": {
"id": "emote-astronaut",
"duration": 13.933730125427246,
"is_free": true
},
"Zombie Run": {
"id": "emote-zombierun",
"duration": 10.045882940292358,
"is_free": true
},
"Wait": {
"id": "dance-wait",
"duration": 9.92491340637207,
"is_free": false
},
"Dab": {
"id": "emote-dab",
"duration": 3.754014015197754,
"is_free": true
},
"Ignition Boost": {
"id": "hcc-jetpack",
"duration": 27.44775152206421,
"is_free": false
},
"Do The Worm": {
"id": "emote-snake",
"duration": 6.629446268081665,
"is_free": true
},
"Bummed": {
"id": "idle-loop-sad",
"duration": 21.796815395355225,
"is_free": true
},
"Chillin'": {
"id": "idle-loop-happy",
"duration": 19.79949164390564,
"is_free": true
},
"Sweet Smooch": {
"id": "emote-kissing",
"duration": 6.693175315856934,
"is_free": true
},
"emoji-shush": {
"id": "emoji-shush",
"duration": 3.399787425994873,
"is_free": true
},
"idle_tough": {
"id": "idle_tough",
"duration": 28.643417358398438,
"is_free": true
},
"emote-fail3": {
"id": "emote-fail3",
"duration": 7.062429189682007,
"is_free": true
},
"emote-shocked": {
"id": "emote-shocked",
"duration": 5.588654518127441,
"is_free": true
},
"emote-theatrical-test": {
"id": "emote-theatrical-test",
"duration": 10.855672359466553,
"is_free": true
},
"emote-fireworks": {
"id": "emote-fireworks",
"duration": 13.147647380828857,
"is_free": true
},
"emote-electrified": {
"id": "emote-electrified",
"duration": 5.287879943847656,
"is_free": true
},
"idle-headless": {
"id": "idle-headless",
"duration": 41.802306175231934,
"is_free": true
},
"emote-armcannon": {
"id": "emote-armcannon",
"duration": 8.674283266067505,
"is_free": true
},
"dance-tiktok4": {
"id": "dance-tiktok4",
"duration": 15.003275156021118,
"is_free": true
},
"dance-tiktok7": {
"id": "dance-tiktok7",
"duration": 13.892939567565918,
"is_free": true
},
"Don't Touch Dance": {
"id": "dance-tiktok13",
"duration": 9.240415334701538,
"is_free": true
},
"Hip Hop Dance": {
"id": "dance-hiphop",
"duration": 27.58914303779602,
"is_free": true
},
"emote-hopscotch": {
"id": "emote-hopscotch",
"duration": 5.839895963668823,
"is_free": true
},
"emote-outfit2": {
"id": "emote-outfit2",
"duration": 11.94482946395874,
"is_free": true
},
"emote-pose12": {
"id": "emote-pose12",
"duration": 5.8061487674713135,
"is_free": true
},
"emote-fading": {
"id": "emote-fading",
"duration": 14.052651405334473,
"is_free": true
},
"emote-pose13": {
"id": "emote-pose13",
"duration": 6.385457515716553,
"is_free": true
},
"profile-breakscreen": {
"id": "profile-breakscreen",
"duration": 10.700304508209229,
"is_free": true
},
"emote-surf": {
"id": "emote-surf",
"duration": 19.009833097457886,
"is_free": true
},
"emote-cartwheel": {
"id": "emote-cartwheel",
"duration": 7.9355247020721436,
"is_free": true
},
"emote-kissing-passionate": {
"id": "emote-kissing-passionate",
"duration": 10.469552755355835,
"is_free": true
},
"dance-tiktok1": {
"id": "dance-tiktok1",
"duration": 12.415152788162231,
"is_free": true
},
"run-vertical": {
"id": "run-vertical",
"duration": 3.8643360137939453,
"is_free": false
},
"emote-flirt": {
"id": "emote-flirt",
"duration": 7.952305316925049,
"is_free": true
},
"emote-receive-disappointed": {
"id": "emote-receive-disappointed",
"duration": 7.139604330062866,
"is_free": true
},
"emote-gooey": {
"id": "emote-gooey",
"duration": 5.819651126861572,
"is_free": true
},
"emote-oops": {
"id": "emote-oops",
"duration": 8.021011352539062,
"is_free": true
},
"walk-vertical": {
"id": "walk-vertical",
"duration": 4.1798996925354,
"is_free": false
},
"emote-thief": {
"id": "emote-thief",
"duration": 6.885812044143677,
"is_free": true
},
"emote-sheephop": {
"id": "emote-sheephop",
"duration": 3.778883457183838,
"is_free": true
},
"emote-runhop": {
"id": "emote-runhop",
"duration": 8.723231554031372,
"is_free": true
},
"dance-tiktok15": {
"id": "dance-tiktok15",
"duration": 16.10505175590515,
"is_free": true
},
"emote-receive-happy": {
"id": "emote-receive-happy",
"duration": 5.941981315612793,
"is_free": true
},
"dance-tiktok6": {
"id": "dance-tiktok6",
"duration": 11.991088151931763,
"is_free": true
},
"emote-confused2": {
"id": "emote-confused2",
"duration": 10.05685830116272,
"is_free": true
},
"Muscle pose": {
"id": "emote-pose4",
"duration": 6.080044507980347,
"is_free": true
},
"emote-dinner": {
"id": "emote-dinner",
"duration": 14.245902061462402,
"is_free": true
},
"emote-wavey": {
"id": "emote-wavey",
"duration": 12.597289085388184,
"is_free": true
},
"emote-pose2": {
"id": "emote-pose2",
"duration": 7.204309701919556,
"is_free": true
},
"dance-shuffle": {
"id": "dance-shuffle",
"duration": 9.04664158821106,
"is_free": true
},
"emote-twitched": {
"id": "emote-twitched",
"duration": 9.609788417816162,
"is_free": true
},
"emote-juggling": {
"id": "emote-juggling",
"duration": 5.8310463428497314,
"is_free": true
},
"idle-dance-tiktok6": {
"id": "idle-dance-tiktok6",
"duration": 9.730481386184692,
"is_free": true
},
"emote-opera": {
"id": "emote-opera",
"duration": 5.761024713516235,
"is_free": true
},
"dance-tiktok3": {
"id": "dance-tiktok3",
"duration": 10.40366792678833,
"is_free": true
},
"dance-kid": {
"id": "dance-kid",
"duration": 10.302606105804443,
"is_free": true
},
"dance-anime3": {
"id": "dance-anime3",
"duration": 12.374316215515137,
"is_free": true
},
"dance-tiktok16": {
"id": "dance-tiktok16",
"duration": 11.019992351531982,
"is_free": true
},
"Poke dance": {
"id": "dance-tiktok12",
"duration": 14.846371412277222,
"is_free": true
},
"dance-tiktok5": {
"id": "dance-tiktok5",
"duration": 12.202406644821167,
"is_free": true
},
"idle-cold": {
"id": "idle-cold",
"duration": 17.71292233467102,
"is_free": true
},
"emote-pose11": {
"id": "emote-pose11",
"duration": 5.1134703159332275,
"is_free": true
},
"emote-handwalk": {
"id": "emote-handwalk",
"duration": 7.772777318954468,
"is_free": true
},
"emote-dramatic": {
"id": "emote-dramatic",
"duration": 9.103327989578247,
"is_free": true
},
"emote-outfit": {
"id": "emote-outfit",
"duration": 13.197255373001099,
"is_free": true
},
"idle-phone": {
"id": "idle-phone",
"duration": 31.364736795425415,
"is_free": false
},
"sit-chair": {
"id": "sit-chair",
"duration": 3.299018621444702,
"is_free": true
},
"idle-space": {
"id": "idle-space",
"duration": 37.784958362579346,
"is_free": true
},
"mining-mine": {
"id": "mining-mine",
"duration": 5.022986173629761,
"is_free": true
},
"mining-success": {
"id": "mining-success",
"duration": 3.105142116546631,
"is_free": true
},
"mining-fail": {
"id": "mining-fail",
"duration": 3.4111127853393555,
"is_free": true
},
"Landing a Fish!": {
"id": "fishing-pull",
"duration": 2.8099365234375,
"is_free": true
},
"Now We Wait...": {
"id": "fishing-idle",
"duration": 17.87005352973938,
"is_free": true
},
"Casting!": {
"id": "fishing-cast",
"duration": 2.8209285736083984,
"is_free": true
},
"We Have a Strike!": {
"id": "fishing-pull-small",
"duration": 3.6690878868103027,
"is_free": true
},
"Hip Shake": {
"id": "dance-hipshake",
"duration": 13.383699655532837,
"is_free": true
},
"Fruity Dance": {
"id": "dance-fruity",
"duration": 18.252850770950317,
"is_free": true
},
"Cheer": {
"id": "dance-cheerleader",
"duration": 17.928509950637817,
"is_free": true
},
"Magnetic": {
"id": "dance-tiktok14",
"duration": 11.197176218032837,
"is_free": true
},
"Blowing Kisses": {
"id": "emote-blowkisses",
"duration": 5.9789252281188965,
"is_free": false
},
"Fairy Twirl": {
"id": "emote-looping",
"duration": 9.88614821434021,
"is_free": true
},
"Fairy Float": {
"id": "idle-floating",
"duration": 27.596596002578735,
"is_free": true
},
"Karma Dance": {
"id": "dance-wild",
"duration": 16.25053095817566,
"is_free": true
},
"Moonlit Howl": {
"id": "emote-howl",
"duration": 8.101369619369507,
"is_free": true
},
"Nocturnal Howl": {
"id": "idle-howl",
"duration": 48.618348360061646,
"is_free": true
},
"Trampoline": {
"id": "emote-trampoline",
"duration": 6.105925559997559,
"is_free": true
},
"Launch": {
"id": "emote-launch",
"duration": 10.881689548492432,
"is_free": true
},
"Cute Salute": {
"id": "emote-cutesalute",
"duration": 3.7876434326171875,
"is_free": true
},
"At Attention": {
"id": "emote-salute",
"duration": 4.789774417877197,
"is_free": true
},
"Wop Dance": {
"id": "dance-tiktok11",
"duration": 11.368684530258179,
"is_free": true
},
"Push It": {
"id": "dance-employee",
"duration": 8.551076650619507,
"is_free": true
},
"This Is For You!": {
"id": "emote-gift",
"duration": 6.091700553894043,
"is_free": true
},
"Sweet Little Moves": {
"id": "dance-touch",
"duration": 13.148397445678711,
"is_free": true
},
"Repose": {
"id": "sit-relaxed",
"duration": 31.21304678916931,
"is_free": true
},
"Sleigh Ride": {
"id": "emote-sleigh",
"duration": 12.514251470565796,
"is_free": true
},
"Gimme Attention!": {
"id": "emote-attention",
"duration": 5.653335809707642,
"is_free": true
},
"Jingle Hop": {
"id": "dance-jinglebell",
"duration": 12.085973262786865,
"is_free": true
},
"Timejump": {
"id": "emote-timejump",
"duration": 5.513711452484131,
"is_free": true
},
"Gotta Go!": {
"id": "idle-toilet",
"duration": 33.481799602508545,
"is_free": true
},
"Bit Nervous": {
"id": "idle-nervous",
"duration": 22.80543065071106,
"is_free": true
},
"Scritchy": {
"id": "idle-wild",
"duration": 27.349984645843506,
"is_free": true
},
"Ice Skating": {
"id": "emote-iceskating",
"duration": 8.409219026565552,
"is_free": true
},
"Laid Back": {
"id": "sit-open",
"duration": 27.275065183639526,
"is_free": true
},
"Party Time!": {
"id": "emote-celebrate",
"duration": 4.345993518829346,
"is_free": true
},
"Shrink": {
"id": "emote-shrink",
"duration": 9.985114097595215,
"is_free": true
},
"Arabesque": {
"id": "emote-pose10",
"duration": 5.0028111934661865,
"is_free": true
},
"Bashful Blush": {
"id": "emote-shy2",
"duration": 6.3357625007629395,
"is_free": true
},
"Possessed Puppet": {
"id": "emote-puppet",
"duration": 17.886415243148804,
"is_free": true
},
"Revelations": {
"id": "emote-headblowup",
"duration": 13.659945964813232,
"is_free": true
},
"Watch Your Back": {
"id": "emote-creepycute",
"duration": 9.010944843292236,
"is_free": true
},
"Creepy Puppet": {
"id": "dance-creepypuppet",
"duration": 7.789044618606567,
"is_free": true
},
"Saunter Sway": {
"id": "dance-anime",
"duration": 9.595806360244751,
"is_free": true
},
"Groovy Penguin": {
"id": "dance-pinguin",
"duration": 12.809289932250977,
"is_free": true
},
"Air Guitar": {
"id": "idle-guitar",
"duration": 14.151675462722778,
"is_free": true
},
"Ready To Rumble": {
"id": "emote-boxer",
"duration": 6.754365921020508,
"is_free": true
},
"Celebration Step": {
"id": "emote-celebrationstep",
"duration": 5.181864023208618,
"is_free": true
},
"Big Surprise": {
"id": "emote-pose6",
"duration": 6.458929777145386,
"is_free": true
},
"Ditzy pose": {
"id": "emote-pose9",
"duration": 6.004010438919067,
"is_free": true
},
"Stargazing": {
"id": "emote-stargazer",
"duration": 7.928274631500244,
"is_free": true
},
"dance-wrong": {
"id": "dance-wrong",
"duration": 13.59788990020752,
"is_free": true
},
"UWU Mood": {
"id": "idle-uwu",
"duration": 25.496710538864136,
"is_free": true
},
"emote-fashionista": {
"id": "emote-fashionista",
"duration": 6.325819730758667,
"is_free": true
},
"dance-icecream": {
"id": "dance-icecream",
"duration": 16.57703709602356,
"is_free": true
},
"emote-gravity": {
"id": "emote-gravity",
"duration": 9.024450540542603,
"is_free": true
},
"emote-punkguitar": {
"id": "emote-punkguitar",
"duration": 10.592331171035767,
"is_free": true
},
"Say So Dance": {
"id": "idle-dance-tiktok4",
"duration": 16.550219535827637,
"is_free": true
},
"I'm A Cutie!": {
"id": "emote-cutey",
"duration": 4.068171739578247,
"is_free": true
},
"Fashion Pose": {
"id": "emote-pose5",
"duration": 5.489050388336182,
"is_free": true
},
"I Challenge You!": {
"id": "emote-pose3",
"duration": 5.565914154052734,
"is_free": true
},
"Flirty Wink": {
"id": "emote-pose1",
"duration": 4.714804410934448,
"is_free": true
},
"A Casual Dance": {
"id": "idle-dance-casual",
"duration": 9.570026159286499,
"is_free": true
},
"Cheerful": {
"id": "emote-pose8",
"duration": 5.618878126144409,
"is_free": true
},
"Embracing Model": {
"id": "emote-pose7",
"duration": 5.2841644287109375,
"is_free": true
},
"Fighter": {
"id": "idle-fighter",
"duration": 18.63888120651245,
"is_free": true
},
"Shuffle Dance": {
"id": "dance-tiktok10",
"duration": 9.410870790481567,
"is_free": true
},
"Renegade": {
"id": "idle-dance-tiktok7",
"duration": 14.047954082489014,
"is_free": true
},
"Grave Dance": {
"id": "dance-weird",
"duration": 22.866037607192993,
"is_free": true
},
"Viral Groove": {
"id": "dance-tiktok9",
"duration": 13.03692102432251,
"is_free": true
},
"emote-cute": {
"id": "emote-cute",
"duration": 7.200940847396851,
"is_free": true
},
"Lambi's Pose": {
"id": "emote-superpose",
"duration": 5.434790134429932,
"is_free": true
},
"Froggie Hop": {
"id": "emote-frog",
"duration": 16.1352436542511,
"is_free": true
},
"Sing Along": {
"id": "idle_singing",
"duration": 11.307929277420044,
"is_free": true
},
"Energy Ball": {
"id": "emote-energyball",
"duration": 8.284976243972778,
"is_free": true
},
"Maniac": {
"id": "emote-maniac",
"duration": 5.944519519805908,
"is_free": true
},
"Sword Fight": {
"id": "emote-swordfight",
"duration": 7.7122719287872314,
"is_free": true
},
"Teleport": {
"id": "emote-teleporting",
"duration": 12.893966674804688,
"is_free": true
},
"Floating": {
"id": "emote-float",
"duration": 9.257302045822144,
"is_free": true
},
"Telekinesis": {
"id": "emote-telekinesis",
"duration": 11.01258134841919,
"is_free": true
},
"Slap": {
"id": "emote-slap",
"duration": 4.059824228286743,
"is_free": true
},
"Pissed Off": {
"id": "emote-frustrated",
"duration": 6.4050421714782715,
"is_free": true
},
"Embarrassed": {
"id": "emote-embarrassed",
"duration": 9.089924573898315,
"is_free": true
},
"Enthused": {
"id": "idle-enthusiastic",
"duration": 17.52780532836914,
"is_free": true
},
"Confusion": {
"id": "emote-confused",
"duration": 9.584890842437744,
"is_free": true
},
"Let's Go Shopping": {
"id": "dance-shoppingcart",
"duration": 5.558927774429321,
"is_free": true
},
"ROFL!": {
"id": "emote-rofl",
"duration": 7.650259494781494,
"is_free": true
},
"Roll": {
"id": "emote-roll",
"duration": 4.306966066360474,
"is_free": true
},
"Super Run": {
"id": "emote-superrun",
"duration": 7.162847995758057,
"is_free": true
},
"Super Punch": {
"id": "emote-superpunch",
"duration": 5.751260757446289,
"is_free": true
},
"Super Kick": {
"id": "emote-kicking",
"duration": 6.213217496871948,
"is_free": true
},
"Falling Apart": {
"id": "emote-apart",
"duration": 5.977605819702148,
"is_free": true
},
"Partner Hug": {
"id": "emote-hug",
"duration": 4.525649547576904,
"is_free": true
},
"Secret Handshake": {
"id": "emote-secrethandshake",
"duration": 6.280278205871582,
"is_free": true
},
"Peekaboo!": {
"id": "emote-peekaboo",
"duration": 4.521607160568237,
"is_free": true
},
"Monster Fail": {
"id": "emote-monster_fail",
"duration": 5.419337272644043,
"is_free": true
},
"Zombie Dance": {
"id": "dance-zombie",
"duration": 13.830149173736572,
"is_free": true
},
"Rope Pull": {
"id": "emote-ropepull",
"duration": 10.6853609085083,
"is_free": true
},
"Proposing": {
"id": "emote-proposing",
"duration": 5.909177303314209,
"is_free": true
},
"Sumo Fight": {
"id": "emote-sumo",
"duration": 11.644229650497437,
"is_free": true
},
"Charging": {
"id": "emote-charging",
"duration": 9.532383680343628,
"is_free": true
},
"Ninja Run": {
"id": "emote-ninjarun",
"duration": 6.499711513519287,
"is_free": true
},
"Elbow Bump": {
"id": "emote-elbowbump",
"duration": 6.438911199569702,
"is_free": true
},
"Irritated": {
"id": "idle-angry",
"duration": 26.070024013519287,
"is_free": true
},
"Home Run!": {
"id": "emote-baseball",
"duration": 8.472715139389038,
"is_free": true
},
"Cozy Nap": {
"id": "idle-floorsleeping",
"duration": 14.611307382583618,
"is_free": true
},
"Relaxing": {
"id": "idle-floorsleeping2",
"duration": 18.827470779418945,
"is_free": true
},
"Hug Yourself": {
"id": "emote-hugyourself",
"duration": 6.028209686279297,
"is_free": true
},
"Pouty Face": {
"id": "idle-sad",
"duration": 25.23569631576538,
"is_free": true
},
"Collapse": {
"id": "emote-death2",
"duration": 5.543778896331787,
"is_free": true
},
"Level Up!": {
"id": "emote-levelup",
"duration": 7.271570920944214,
"is_free": true
},
"Posh": {
"id": "idle-posh",
"duration": 23.29422426223755,
"is_free": true
},
"Snow Angel": {
"id": "emote-snowangel",
"duration": 7.334203720092773,
"is_free": true
},
"Sweating": {
"id": "emote-hot",
"duration": 5.572302341461182,
"is_free": true
},
"Snowball Fight!": {
"id": "emote-snowball",
"duration": 6.320742130279541,
"is_free": true
},
"Ponder": {
"id": "idle-lookup",
"duration": 8.754379272460938,
"is_free": true
},
"Headball": {
"id": "emote-headball",
"duration": 11.664129972457886,
"is_free": false
},
"Hero Entrance": {
"id": "emote-hero",
"duration": 6.587759494781494,
"is_free": false
},
"Curtsy": {
"id": "emote-curtsy",
"duration": 3.9908952713012695,
"is_free": true
},
"Russian Dance": {
"id": "dance-russian",
"duration": 11.388729810714722,
"is_free": true
},
"Bow": {
"id": "emote-bow",
"duration": 5.102638483047485,
"is_free": true
},
"Boo": {
"id": "emote-boo",
"duration": 5.578845024108887,
"is_free": true
},
"Fall": {
"id": "emote-fail1",
"duration": 6.896064758300781,
"is_free": true
},
"Clumsy": {
"id": "emote-fail2",
"duration": 7.742251634597778,
"is_free": true
},
"Imaginary Jetpack": {
"id": "emote-jetpack",
"duration": 17.774274826049805,
"is_free": true
},
"Revival": {
"id": "emote-death",
"duration": 8.003193378448486,
"is_free": true
},
"Penny's Dance": {
"id": "dance-pennywise",
"duration": 4.157809495925903,
"is_free": true
},
"Sleepy": {
"id": "idle-sleep",
"duration": 3.353527307510376,
"is_free": true
},
"Attentive": {
"id": "idle_layingdown",
"duration": 26.108940839767456,
"is_free": true
},
"Theatrical": {
"id": "emote-theatrical",
"duration": 10.995978116989136,
"is_free": true
},
"Faint": {
"id": "emote-fainting",
"duration": 18.552194118499756,
"is_free": true
},
"Relaxed": {
"id": "idle_layingdown2",
"duration": 22.587023496627808,
"is_free": true
},
"I Believe I Can Fly": {
"id": "emote-wings",
"duration": 14.205503702163696,
"is_free": true
},
"Amused": {
"id": "emote-laughing2",
"duration": 6.60427188873291,
"is_free": true
},
"Floss": {
"id": "dance-floss",
"duration": 23.12726402282715,
"is_free": false
},
"Don't Start Now": {
"id": "dance-tiktok2",
"duration": 11.37182092666626,
"is_free": true
},
"Model": {
"id": "emote-model",
"duration": 7.427884817123413,
"is_free": true
},
"K-Pop Dance": {
"id": "dance-blackpink",
"duration": 7.974578857421875,
"is_free": true
},
"Karate": {
"id": "dance-martial-artist",
"duration": 13.972932577133179,
"is_free": false
},
"Sick": {
"id": "emoji-sick",
"duration": 6.217142343521118,
"is_free": true
},
"Zombie": {
"id": "idle_zombie",
"duration": 31.391045093536377,
"is_free": true
},
"Cold": {
"id": "emote-cold",
"duration": 5.168632745742798,
"is_free": true
},
"Bunny Hop": {
"id": "emote-bunnyhop",
"duration": 13.63294768333435,
"is_free": true
},
"Disco": {
"id": "emote-disco",
"duration": 6.136807441711426,
"is_free": true
},
"Wiggle Dance": {
"id": "dance-sexy",
"duration": 13.704560279846191,
"is_free": true
},
"Heart Hands": {
"id": "emote-heartfingers",
"duration": 5.182276487350464,
"is_free": true
},
"Savage Dance": {
"id": "dance-tiktok8",
"duration": 13.10374116897583,
"is_free": true
},
"Ghost Float": {
"id": "emote-ghost-idle",
"duration": 20.427579641342163,
"is_free": true
},
"Sneeze": {
"id": "emoji-sneeze",
"duration": 4.327379941940308,
"is_free": true
},
"Pray": {
"id": "emoji-pray",
"duration": 6.003554344177246,
"is_free": true
},
"Handstand": {
"id": "emote-handstand",
"duration": 5.886280059814453,
"is_free": true
},
"Smoothwalk": {
"id": "dance-smoothwalk",
"duration": 7.581580400466919,
"is_free": true
},
"Ring on It": {
"id": "dance-singleladies",
"duration": 22.333438873291016,
"is_free": true
},
"Yoga Flow": {
"id": "dance-spiritual",
"duration": 17.70866560935974,
"is_free": false
},
"Partner Heart Arms": {
"id": "emote-heartshape",
"duration": 7.5974767208099365,
"is_free": true
},
"Ghost": {
"id": "emoji-ghost",
"duration": 3.7432401180267334,
"is_free": true
},
"Push Ups": {
"id": "dance-aerobics",
"duration": 9.887983083724976,
"is_free": true
},
"Naughty": {
"id": "emoji-naughty",
"duration": 5.731683254241943,
"is_free": true
},
"Robotic": {
"id": "dance-robotic",
"duration": 12.225102424621582,
"is_free": false
},
"Faint Drop": {
"id": "emote-deathdrop",
"duration": 4.177362442016602,
"is_free": true
},
"Duck Walk": {
"id": "dance-duckwalk",
"duration": 12.48209023475647,
"is_free": true
},
"Splits Drop": {
"id": "emote-splitsdrop",
"duration": 5.310996055603027,
"is_free": true
},
"Vogue Hands": {
"id": "dance-voguehands",
"duration": 10.565007209777832,
"is_free": true
},
"Give Up": {
"id": "emoji-give-up",
"duration": 6.040206670761108,
"is_free": true
},
"Smirk": {
"id": "emoji-smirking",
"duration": 5.7423319816589355,
"is_free": true
},
"Lying": {
"id": "emoji-lying",
"duration": 7.389834403991699,
"is_free": true
},
"Arrogance": {
"id": "emoji-arrogance",
"duration": 8.159849882125854,
"is_free": true
},
"Breakdance": {
"id": "dance-breakdance",
"duration": 17.939950466156006,
"is_free": false
},
"Point": {
"id": "emoji-there",
"duration": 3.0896713733673096,
"is_free": true
},
"Stinky": {
"id": "emoji-poop",
"duration": 5.85624885559082,
"is_free": true
},
"Fireball Lunge": {
"id": "emoji-hadoken",
"duration": 4.290197372436523,
"is_free": true
},
"Punch": {
"id": "emoji-punch",
"duration": 3.361440658569336,
"is_free": true
},
"Hands in the Air": {
"id": "dance-handsup",
"duration": 23.177976608276367,
"is_free": true
},
"Rock Out": {
"id": "dance-metal",
"duration": 15.781339168548584,
"is_free": true
},
"Orange Juice Dance": {
"id": "dance-orangejustice",
"duration": 7.168856620788574,
"is_free": true
},
"Aerobics": {
"id": "idle-loop-aerobics",
"duration": 10.082928657531738,
"is_free": true
},
"Boogie Swing": {
"id": "idle-dance-swinging",
"duration": 14.46821665763855,
"is_free": false
},
"Annoyed": {
"id": "idle-loop-annoyed",
"duration": 18.624611854553223,
"is_free": true
},
"Gasp": {
"id": "emoji-scared",
"duration": 4.064062595367432,
"is_free": true
},
"Think": {
"id": "emote-think",
"duration": 4.805848598480225,
"is_free": true
},
"Fatigued": {
"id": "idle-loop-tired",
"duration": 11.23218560218811,
"is_free": true
},
"Feel The Beat": {
"id": "idle-dance-headbobbing",
"duration": 23.653693914413452,
"is_free": true
},
"Blast Off": {
"id": "emote-disappear",
"duration": 5.531318426132202,
"is_free": true
},
"Sob": {
"id": "emoji-crying",
"duration": 4.9091150760650635,
"is_free": true
},
"Tap Loop": {
"id": "idle-loop-tapdance",
"duration": 7.8087074756622314,
"is_free": true
},
"Raise The Roof": {
"id": "emoji-celebrate",
"duration": 4.7828662395477295,
"is_free": true
},
"Eye Roll": {
"id": "emoji-eyeroll",
"duration": 3.7542595863342285,
"is_free": true
},
"Stunned": {
"id": "emoji-dizzy",
"duration": 5.3762526512146,
"is_free": true
},
"Graceful": {
"id": "emote-graceful",
"duration": 5.270719289779663,
"is_free": false
},
"Frolic ": {
"id": "emote-frollicking",
"duration": 5.087254524230957,
"is_free": false
},
"Tummy Ache": {
"id": "emoji-gagging",
"duration": 6.836994409561157,
"is_free": true
},
"Greedy Emote": {
"id": "emote-greedy",
"duration": 5.720172643661499,
"is_free": true
},
"Flex": {
"id": "emoji-flex",
"duration": 3.3146491050720215,
"is_free": false
},
"Cursing Emote": {
"id": "emoji-cursing",
"duration": 3.8144092559814453,
"is_free": false
},
"Flirty Wave": {
"id": "emote-lust",
"duration": 5.467925310134888,
"is_free": false
},
"Mind Blown": {
"id": "emoji-mind-blown",
"duration": 3.4589083194732666,
"is_free": true
},
"Shy": {
"id": "emote-shy",
"duration": 5.146667718887329,
"is_free": true
},
"Clap": {
"id": "emoji-clapping",
"duration": 2.9828615188598633,
"is_free": true
},
"Love Flutter": {
"id": "emote-hearteyes",
"duration": 5.989662170410156,
"is_free": true
},
"Thumb Suck": {
"id": "emote-suckthumb",
"duration": 5.227030992507935,
"is_free": true
},
"Exasperated": {
"id": "emote-exasperated",
"duration": 4.09885573387146,
"is_free": true
},
"Jump": {
"id": "emote-jumpb",
"duration": 4.87456488609314,
"is_free": true
},
"Face Palm": {
"id": "emote-exasperatedb",
"duration": 3.8919904232025146,
"is_free": true
},
"Peace": {
"id": "emote-peace",
"duration": 7.00889253616333,
"is_free": true
},
"The Wave": {
"id": "emote-wave",
"duration": 4.0621178150177,
"is_free": true
},
"Panic": {
"id": "emote-panic",
"duration": 3.7224788665771484,
"is_free": true
},
"Harlem Shake": {
"id": "emote-harlemshake",
"duration": 14.377963066101074,
"is_free": true
},
"Tap Dance": {
"id": "emote-tapdance",
"duration": 12.435080289840698,
"is_free": true
},
"Gangnam Style": {
"id": "emote-gangnam",
"duration": 8.071059703826904,
"is_free": true
},
"No": {
"id": "emote-no",
"duration": 3.8635921478271484,
"is_free": true
},
"Sad": {
"id": "emote-sad",
"duration": 6.419863224029541,
"is_free": true
},
"Yes": {
"id": "emote-yes",
"duration": 4.118977308273315,
"is_free": true
},
"Kiss": {
"id": "emote-kiss",
"duration": 3.7398743629455566,
"is_free": true
},
"Moonwalk": {
"id": "emote-gordonshuffle",
"duration": 9.52907681465149,
"is_free": true
},
"Night Fever": {
"id": "emote-nightfever",
"duration": 6.344593524932861,
"is_free": true
},
"Laugh": {
"id": "emote-laughing",
"duration": 3.7673463821411133,
"is_free": true
},
"Judo Chop": {
"id": "emote-judochop",
"duration": 3.610184669494629,
"is_free": true
},
"Rainbow": {
"id": "emote-rainbow",
"duration": 3.074357271194458,
"is_free": true
},
"Robot": {
"id": "emote-robot",
"duration": 9.224223613739014,
"is_free": true
},
"Happy": {
"id": "emote-happy",
"duration": 4.755821943283081,
"is_free": true
},
"emote-": {
"id": "emote-",
"duration": 2.981541633605957,
"is_free": false
},
"emote-holding-hot-cocoa": {
"id": "emote-holding-hot-cocoa",
"duration": 3.8734710216522217,
"is_free": false
},
"emote-mittens": {
"id": "emote-mittens",
"duration": 3.169820785522461,
"is_free": false
},
"Angry": {
"id": "emoji-angry",
"duration": 6.322439670562744,
"is_free": true
},
"Macarena": {
"id": "dance-macarena",
"duration": 13.161751747131348,
"is_free": true
},
"Sit": {
"id": "idle-loop-sitfloor",
"duration": 23.04495859146118,
"is_free": true
},
"Thumbs Up": {
"id": "emoji-thumbsup",
"duration": 3.779395580291748,
"is_free": true
},
"Tired": {
"id": "emote-tired",
"duration": 5.9777562618255615,
"is_free": true
},
"Hello": {
"id": "emote-hello",
"duration": 3.7342917919158936,
"is_free": true
}

# تخزين المهام المتكررة لكل مستخدم
user_loops = {}

# تفعيل التكرار
async def loop(self: BaseBot, user: User, message: str):
    parts = message.strip().split(" ", 1)
    if len(parts) < 2:
        await self.highrise.chat("يرجى كتابة اسم الإيموجي بعد 'loop'.")
        return
    emote_name = parts[1].strip().lower()

    selected = next(
        (emote for emote in emote_list if emote_name in [k.lower() for k in emote[0]]), None)

    if not selected:
        await self.highrise.chat("الإيموجي غير موجود.")
        return

    _, emote_id, duration = selected

    # إيقاف أي تكرار سابق
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]

    # تنفيذ التكرار
    async def emote_loop():
        try:
            await self.highrise.chat(f"بدأ @{user.username} تكرار الإيموجي '{emote_id}' كل {duration:.1f} ثانية.")
            while True:
                await self.highrise.send_emote(emote_id, user.id)
                await asyncio.sleep(duration)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(emote_loop())
    user_loops[user.id] = task

# إيقاف التكرار
async def stop_loop(self: BaseBot, user: User, message: str):
    if user.id in user_loops:
        user_loops[user.id].cancel()
        del user_loops[user.id]
        await self.highrise.chat(f"@{user.username} تم إيقاف تكرار الإيموجي الخاص بك.")
    else:
        await self.highrise.chat(f"@{user.username} ليس لديك أي تكرار نشط.")

# تفعيل الإيموجي تلقائيًا عند كتابة اسمه مباشرة
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    message = message.strip().lower()
    found = next((emote for emote in emote_list if message in [k.lower() for k in emote[0]]), None)
    if found:
        await loop(self, user, f"loop {message}")
