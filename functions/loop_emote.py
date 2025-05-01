import asyncio
from highrise import BaseBot
from highrise.models import 
# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
    "1": {
        "id": "idle_zombie",
        "duration": 28.754937
    },
    "2": {
        "id": "idle_layingdown2",
        "duration": 10
    },
    "3": {
        "id": "idle_layingdown",
        "duration": 10
    },
    "4": {
        "id": "idle-sad",
        "duration": 24.377214
    },

        "id": "idle-hero",
        "duration": 7
    },
    "14": {
        "id": "idle-floorsleeping2",
        "duration": 8.1
    },
    "15": {
        "id": "idle-floorsleeping",
        "duration": 10
    },
    "16": {
        "id": "idle-enthusiastic",
        "duration": 15.1
    },
    "17": {
        "id": "idle-dance-headbobbing",
        "duration": 24.8
    },
    "18": {
        "id": "idle-angry",
        "duration": 5
    },
    "19": {
        "id": "emote-yes",
        "duration": 2
    },
    "20": {
        "id": "emote-wings",
        "duration": 12.9
    },
    "21": {
        "id": "emote-wave",
        "duration": 2.690873
    },
    "22": {
        "id": "emote-tired",
        "duration": 4.61063
    },
    "23": {
        "id": "emote-think",
        "duration": 3.691104
    },
    "24": {
        "id": "emote-theatrical",
        "duration": 8.591869
    },
    "25": {
        "id": "emote-tapdance",
        "duration": 10.9
    },
    "26": {
        "id": "emote-superrun",
        "duration": 6.273226
    },
    "27": {
        "id": "emote-superpunch",
        "duration": 3.751054
    },
    "28": {
        "id": "emote-sumo",
        "duration": 10.0
    },
    "29": {
        "id": "emote-kissing",
        "duration": 5.5
    },
    "30": {
        "id": "emote-splitsdrop",
        "duration": 4.2
    },
    "31": {
        "id": "emote-snowball",
        "duration": 5.0
    },
    "32": {
        "id": "emote-snowangel",
        "duration": 6.218627
    },
    "33": {
        "id": "emote-shy",
        "duration": 4.477567
    },
    "34": {
        "id": "emote-secrethandshake",
        "duration": 3.4
    },
    "35": {
        "id": "emote-sad",
        "duration": 5.411073
    },
    "36": {
        "id": "emote-ropepull",
        "duration": 8.5
    },
    "37": {
        "id": "emote-roll",
        "duration": 3
    },
    "38": {
        "id": "emote-rofl",
        "duration": 6.314731
    },
    "39": {
        "id": "emote-robot",
        "duration": 7.607362
    },
    "40": {
        "id": "emote-rainbow",
        "duration": 2.3
    },
    "41": {
        "id": "emote-proposing",
        "duration": 4.27888
    },
    "42": {
        "id": "emote-peekaboo",
        "duration": 3.629867
    },
    "43": {
        "id": "emote-peace",
        "duration": 5.4
    },
    "44": {
        "id": "emote-panic",
        "duration": 2.850966
    },
    "45": {
        "id": "emote-no",
        "duration": 2.6
    },
    "46": {
        "id": "emote-ninjarun",
        "duration": 4.5
    },
    "47": {
        "id": "emote-nightfever",
        "duration": 5.488424
    },
    "48": {
        "id": "emote-monster_fail",
        "duration": 4.5
    },
    "49": {
        "id": "emote-model",
        "duration": 6.2
    },
    "50": {
        "id": "emote-levelup",
        "duration": 6.0545
    },
    "51": {
        "id": "emote-laughing2",
        "duration": 5.056641
    },
    "52": {
        "id": "emote-laughing",
        "duration": 2.69161
    },
    "53": {
        "id": "emote-kiss",
        "duration": 2.387175
    },
    "54": {
        "id": "emote-kicking",
        "duration": 4.6
    },
    "55": {
        "id": "emote-jumpb",
        "duration": 3.584234
    },
    "56": {
        "id": "emote-judochop",
        "duration": 2.3
    },
    "57": {
        "id": "emote-jetpack",
        "duration": 16.759457
    },
    "58": {
        "id": "emote-hugyourself",
        "duration": 4.992751
    },
    "59": {
        "id": "emote-hot",
        "duration": 4.353037
    },
    "60": {
        "id": "emote-hero",
        "duration": 4.996096
    },
    "61": {
        "id": "emote-hello",
        "duration": 2.734844
    },
    "62": {
        "id": "emote-harlemshake",
        "duration": 13.0
    },
    "63": {
        "id": "emote-happy",
        "duration": 3.483462
    },
    "64": {
        "id": "emote-handstand",
        "duration": 4.015678
    },
    "65": {
        "id": "emote-greedy",
        "duration": 4.4
    },
    "66": {
        "id": "emote-launch",
        "duration": 8.5
    },
    "67": {
        "id": "emote-gordonshuffle",
        "duration": 8.052307
    },
    "68": {
        "id": "emote-ghost-idle",
        "duration": 16
    },
    "69": {
        "id": "emote-gangnam",
        "duration": 6
    },
    "70": {
        "id": "emote-fainting",
        "duration": 15
    },
    "71": {
        "id": "emote-fail2",
        "duration": 5.5
    },
    "72": {
        "id": "emote-fail1",
        "duration": 5.617942
    },
    "73": {
        "id": "emote-exasperatedb",
        "duration": 2.5
    },
    "74": {
        "id": "emote-exasperated",
        "duration": 2.1
    },
    "75": {
        "id": "emote-elbowbump",
        "duration": 3.799768
    },
    "76": {
        "id": "emote-disco",
        "duration": 4.9
    },
    "77": {
        "id": "emote-disappear",
        "duration": 6.195985
    },
    "78": {
        "id": "emote-deathdrop",
        "duration": 3.5
    },
    "79": {
        "id": "emote-death2",
        "duration": 4.855549
    },
    "80": {
        "id": "emote-death",
        "duration": 6.2
    },
    "81": {
        "id": "emote-dab",
        "duration": 2.717871
    },
    "82": {
        "id": "emote-curtsy",
        "duration": 2.425714
    },
    "83": {
        "id": "emote-confused",
        "duration": 8.578827
    },
    "84": {
        "id": "emote-cold",
        "duration": 3.4
    },
    "85": {
        "id": "emote-charging",
        "duration": 8.025079
    },
    "86": {
        "id": "emote-bunnyhop",
        "duration": 12.30
    },
    "87": {
        "id": "emote-bow",
        "duration": 3.344036
    },
    "88": {
        "id": "emote-boo",
        "duration": 4.3
    },
    "89": {
        "id": "emote-baseball",
        "duration": 7.1
    },
    "90": {
        "id": "emote-apart",
        "duration": 4.809542
    },
    "91": {
        "id": "emoji-thumbsup",
        "duration": 2.702369
    },
    "92": {
        "id": "emoji-there",
        "duration": 2.059095
    },
    "93": {
        "id": "emoji-sneeze",
        "duration": 2.996694
    },
    "94": {
        "id": "emoji-smirking",
        "duration": 4.823158
    },
    "95": {
        "id": "emoji-sick",
        "duration": 5.070367
    },
    "96": {
        "id": "emoji-scared",
        "duration": 3.008487
    },
    "97": {
        "id": "emoji-punch",
        "duration": 1.755783
    },
    "98": {
        "id": "emoji-pray",
        "duration": 4.503179
    },
    "99": {
        "id": "emoji-poop",
        "duration": 4.5
    },
    "100": {
        "id": "emoji-naughty",
        "duration": 4.277602
    },
    "101": {
        "id": "emoji-mind-blown",
        "duration": 2.397167
    },
    "102": {
        "id": "emoji-lying",
        "duration": 6.0
    },
    "103": {
        "id": "emoji-halo",
        "duration": 5.837754
    },
    "104": {
        "id": "emoji-hadoken",
        "duration": 2.723709
    },
    "105": {
        "id": "emoji-give-up",
        "duration": 5.407888
    },
    "106": {
        "id": "emoji-gagging",
        "duration": 5.500202
    },
    "107": {
        "id": "dance-fruity",
        "duration": 17.05
    },
    "108": {
        "id": "emoji-dizzy",
        "duration": 4.053049
    },
    "109": {
        "id": "idle-space",
        "duration": 27
    },
    "110": {
        "id": "emoji-crying",
        "duration": 3.696499
    },
    "111": {
        "id": "emoji-clapping",
        "duration": 2.161757
    },
    "112": {
        "id": "emoji-celebrate",
        "duration": 3.3
    },
    "113": {
        "id": "emoji-arrogance",
        "duration": 6.869441
    },
    "114": {
        "id": "emoji-angry",
        "duration": 5.760023
    },
    "115": {
        "id": "dance-voguehands",
        "duration": 9.10
    },
    "116": {
        "id": "dance-tiktok8",
        "duration": 10.7
    },
    "117": {
        "id": "dance-tiktok2",
        "duration": 9.8
    },
    "118": {
        "id": "dance-smoothwalk",
        "duration": 5.8
    },
    "119": {
        "id": "dance-singleladies",
        "duration": 19.3
    },
    "120": {
        "id": "dance-shoppingcart",
        "duration": 3.45
    },
    "121": {
        "id": "dance-russian",
        "duration": 9.6
    },
    "122": {
        "id": "dance-pennywise",
        "duration": 0.5
    },
    "123": {
        "id": "dance-orangejustice",
        "duration": 5.5
    },
    "124": {
        "id": "dance-metal",
        "duration": 14.2
    },
    "125": {
        "id": "dance-macarena",
        "duration": 11.5
    },
    "126": {
        "id": "dance-hipshake",
        "duration": 12.2
    },
    "127": {
        "id": "dance-duckwalk",
        "duration": 10
    },
    "128": {
        "id": "dance-blackpink",
        "duration": 5.6
    },
    "129": {
        "id": "dance-aerobics",
        "duration": 8.3
    },
    "130": {
        "id": "emote-hyped",
        "duration": 7.2
    },
    "131": {
        "id": "dance-jinglebell",
        "duration": 10.14
    },
    "132": {
        "id": "idle-nervous",
        "duration": 4
    },
    "133": {
        "id": "emote-attention",
        "duration": 4.0
    },
    "134": {
        "id": "emote-astronaut",
        "duration": 13.45
    },
    "135": {
        "id": "dance-zombie",
        "duration": 12.27
    },
    "136": {
        "id": "emoji-ghost",
        "duration": 2.5
    },
    "137": {
        "id": "emote-hearteyes",
        "duration": 3.8
    },
    "138": {
        "id": "emote-swordfight",
        "duration": 5.7
    },
    "139": {
        "id": "emote-timejump",
        "duration": 3.8
    },
    "140": {
        "id": "emote-snake",
        "duration": 4.8
    },
    "141": {
        "id": "emote-heartfingers",
        "duration": 4.001974
    },
    "142": {
        "id": "emote-heartshape",
        "duration": 6.232394
    },
    "143": {
        "id": "emote-hug",
        "duration": 3.3
    },
    "144": {
        "id": "emoji-eyeroll",
        "duration": 2.8
    },
    "145": {
        "id": "emote-embarrassed",
        "duration": 7.2
    },
    "146": {
        "id": "emote-float",
        "duration": 8.3
    },
    "147": {
        "id": "emote-telekinesis",
        "duration": 9.8
    },
    "148": {
        "id": "dance-sexy",
        "duration": 12.1
    },
    "149": {
        "id": "emote-puppet",
        "duration": 16.325823
    },
    "150": {
        "id": "idle-fighter",
        "duration": 16.5
    },
    "151": {
        "id": "dance-pinguin",
        "duration": 10.7
    },
    "152": {
        "id": "dance-creepypuppet",
        "duration": 6.416121
    },
    "153": {
        "id": "emote-sleigh",
        "duration": 11.2
    },
    "154": {
        "id": "emote-maniac",
        "duration": 4.7
    },
    "155": {
        "id": "emote-energyball",
        "duration": 7.4
    },
    "156": {
        "id": "idle_singing",
        "duration": 9.5
    },
    "157": {
        "id": "emote-frog",
        "duration": 14.2
    },
    "158": {
        "id": "emote-superpose",
        "duration": 4
    },
    "159": {
        "id": "emote-cute",
        "duration": 5.8
    },
    "160": {
        "id": "dance-tiktok9",
        "duration": 11.5
    },
    "161": {
        "id": "dance-weird",
        "duration": 21
    },
    "162": {
        "id": "dance-tiktok10",
        "duration": 7.5
    },
    "163": {
        "id": "emote-pose7",
        "duration": 4.2
    },
    "164": {
        "id": "emote-pose8",
        "duration": 4.2
    },
    "165": {
        "id": "idle-dance-casual",
        "duration": 8.3
    },
    "166": {
        "id": "emote-pose1",
        "duration": 2
    },
    "167": {
        "id": "emote-pose3",
        "duration": 4.5
    },
    "168": {
        "id": "emote-pose5",
        "duration": 4.4
    },
    "169": {
        "id": "emote-cutey",
        "duration": 3.1
    },
    "170": {
        "id": "emote-punkguitar",
        "duration": 8.5
    },
    "171": {
        "id": "emote-zombierun",
        "duration": 8.9
    },
    "172": {
        "id": "emote-fashionista",
        "duration": 5.2
    },
    "173": {
        "id": "emote-gravity",
        "duration": 8.955966
    },
    "174": {
        "id": "dance-icecream",
        "duration": 13.85
    },
    "175": {
        "id": "dance-wrong",
        "duration": 11.83
    },
    "176": {
        "id": "idle-uwu",
        "duration": 5
    },
    "177": {
        "id": "idle-dance-tiktok4",
        "duration": 14.75
    },
    "178": {
        "id": "emote-shy2",
        "duration": 4.7
    },
    "179": {
        "id": "dance-anime",
        "duration": 7.93
    },
    "180": {
        "id": "dance-kawai",
        "duration": 9.77
    },
    "181": {
        "id": "idle-wild",
        "duration": 24
    },
    "182": {
        "id": "emote-iceskating",
        "duration": 7.20
    },
    "183": {
        "id": "emote-pose6",
        "duration": 5.1
    },
    "184": {
        "id": "emote-celebrationstep",
        "duration": 3.1
    },
    "185": {
        "id": "emote-creepycute",
        "duration": 7.6
    },
    "186": {
        "id": "emote-frustrated",
        "duration": 5.2
    },
    "187": {
        "id": "emote-pose10",
        "duration": 3.7
    },
    "188": {
        "id": "sit-relaxed",
        "duration": 5
    },
    "189": {
        "id": "sit-open",
        "duration": 5
    },
    "190": {
        "id": "emote-slap",
        "duration": 2.1
    },
    "191": {
        "id": "emote-boxer",
        "duration": 5.3
    },
    "192": {
        "id": "emote-headblowup",
        "duration": 11.667537
    },
    "193": {
        "id": "emote-kawaiigogo",
        "duration": 10
    },
    "194": {
        "id": "idle-dance-tiktok7",
        "duration": 12.5
    },
    "195": {
        "id": "emote-shrink",
        "duration": 8.25
    },
    "196": {
        "id": "emote-pose9",
        "duration": 4.27
    },
    "197": {
        "id": "emote-teleporting",
        "duration": 11.744
    },
    "198": {
        "id": "dance-touch",
        "duration": 11.60
    },
    "199": {
        "id": "idle-guitar",
        "duration": 12.3
    },
    "200": {
        "id": "emote-gift",
        "duration": 6.9
    },
    "201": {
        "id": "dance-employee",
        "duration": 6.43
    },
    "202": {
        "id": "emote-outfit",
        "duration": 11
    },
    "203": {
        "id": "emote-pose12",
        "duration": 4.1
    },
    "204": {
        "id": "dance-tiktok5",
        "duration": 11.05
    },
    "205": {
        "id": "emote-fading",
        "duration": 12.2
    },
    "206": {
        "id": "emote-dinner",
        "duration": 13
    },
    "207": {
        "id": "emote-opera",
        "duration": 4.2
    },
    "208": {
        "id": "dance-hiphop",
        "duration": 25
    },
    "209": {
        "id": "dance-tiktok15",
        "duration": 13
    },
    "210": {
        "id": "dance-tiktok6",
        "duration": 10
    },
    "211": {
        "id": "emote-juggling",
        "duration": 4.2
    },
    "212": {
        "id": "emote-thief",
        "duration": 4.7
    },
    "213": {
        "id": "emote-shocked",
        "duration": 4.6
    },
    "214": {
        "id": "emote-flirt",
        "duration": 6.5
    },
    "215": {
        "id": "emote-outfit2",
        "duration": 8
    },
    "216": {
        "id": "emote-fireworks",
        "duration": 12
    },
    "217": {
        "id": "emote-dropped",
        "duration": 5
    },
    "218": {
        "id": "emote-oops",
        "duration": 6.7
    },
    "219": {
        "id": "emote-wavey",
        "duration": 11
    },
    "220": {
        "id": "emote-twitched",
        "duration": 7
    },
    "221": {
        "id": "emote-surf",
        "duration": 17
    },
    "222": {
        "id": "emote-pose11",
        "duration": 3.8
    },
    "223": {
        "id": "dance-tiktok16",
        "duration": 9.3
    },
    "224": {
        "id": "dance-shuffle",
        "duration": 7.7
    },
    "225": {
        "id": "dance-tiktok3",
        "duration": 9
    },
    "226": {
        "id": "dance-tiktok1",
        "duration": 11
    },
    "227": {
        "id": "emote-cartwheel",
        "duration": 5
    },
    "228": {
        "id": "emote-electrified",
        "duration": 4.7
    },
    "229": {
        "id": "emote-dramatic",
        "duration": 8
    },
    "230": {
        "id": "dance-anime",
        "duration": 7.5
    },
    "231": {
        "id": "emote-armcannon",
        "duration": 7.6
    },
    "232": {
        "id": "dance-cheerleader",
        "duration": 16.3
    },
    "233": {
        "id": "emote-trampoline",
        "duration": 5
    },
    "234": {
        "id": "emote-suckthumb",
        "duration": 4.185944
    },
    "235": {
        "id": "emote-stargazer",
        "duration": 7.320773
    },
    "236": {
        "id": "idle-toilet",
        "duration": 32.174447
    },
    "237": {
        "id": "emote-cutesalute",
        "duration": 2.1
    },
    "238": {
        "id": "emote-salute",
        "duration": 2.1
    },
    "239": {
        "id": "dance-tiktok11",
        "duration": 8.8
    },
    "240": {
        "id": "emote-kissing-bound",
        "duration": 4.5
    },
    "241": {
        "id": "idle-floating",
        "duration": 8
    },
    "242": {
        "id": "emote-thought",
        "duration": 22.339865
    },
    "243": {
        "id": "idle-crouched",
        "duration": 22.339865
    },
    "244": {
        "id": "emoji-shush",
        "duration": 2
    },
    "245": {
        "id": "idle_tough",
        "duration": 10
    },
    "246": {
        "id": "emote-fail3",
        "duration": 6
    },
    "247": {
        "id": "idle-headless",
        "duration": 41
    },
    "248": {
        "id": "dance-tiktok7",
        "duration": 12.5
    },
    "249": {
        "id": "dance-tiktok13",
        "duration": 8
    },
    "250": {
        "id": "emote-hopscotch",
        "duration": 4.5
    },
    "251": {
        "id": "emote-pose13",
        "duration": 5
    },
    "252": {
        "id": "profile-breakscreen",
        "duration": 10
    },
    "253": {
        "id": "emote-kissing-passionate",
        "duration": 8.7
    },
    "254": {
        "id": "run-vertical",
        "duration": 1.005
    },
    "255": {
        "id": "emote-receive-disappointed",
        "duration": 5.7
    },
    "256": {
        "id": "emote-gooey",
        "duration": 4.2
    },
    "257": {
        "id": "emote-sheephop",
        "duration": 3.5
    },
    "258": {
        "id": "emote-receive-happy",
        "duration": 4.2
    },
    "259": {
        "id": "emote-confused2",
        "duration": 7
    },
    "260": {
        "id": "emote-pose4",
        "duration": 5
    },
    "261": {
        "id": "emote-pose2",
        "duration": 4.5
    },
    "262": {
        "id": "idle-dance-tiktok6",
        "duration": 8
    },
    "263": {
        "id": "dance-kid",
        "duration": 8.7
    },
    "264": {
        "id": "dance-anime3",
        "duration": 11
    },
    "265": {
        "id": "dance-tiktok12",
        "duration": 13
    },
    "266": {
        "id": "idle-cold",
        "duration": 10
    },
    "267": {
        "id": "emote-handwalk",
        "duration": 6
    },
    "268": {
        "id": "sit-chair",
        "duration": 1
    },
    "269": {
        "id": "mining-mine",
        "duration": 3.7
    },
    "270": {
        "id": "mining-success",
        "duration": 2.5
    },
    "271": {
        "id": "mining-fail",
        "duration": 2.5
    },
    "272": {
        "id": "fishing-pull",
        "duration": 1
    },
    "273": {
        "id": "fishing-idle",
        "duration": 1
    },
    "274": {
        "id": "fishing-cast",
        "duration": 1
    },
    "275": {
        "id": "fishing-pull-small",
        "duration": 1
    },
    "276": {
        "id": "dance-tiktok14",
        "duration": 10
    },
    "277": {
        "id": "emote-looping",
        "duration": 8.2
    },
    "278": {
        "id": "dance-wild",
        "duration": 10
    },
    "279": {
        "id": "emote-howl",
        "duration": 5
    },
    "280": {
        "id": "idle-howl",
        "duration": 10
    },
    "281": {
        "id": "hcc-jetpack",
        "duration": 22.339865
    },
    "282": {
        "id": "dance-handsup",
        "duration": 22.2
    },
    "283": {
        "id": "dance-woah",
        "duration": 9
    }
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
