import asyncio
from highrise import BaseBot
from highrise.models import 
# قائمة الإيموجيات مع الكلمات الدالة والمدة
emote_list: list[tuple[list[str], str, float]] = [
all_emote_list: list[tuple[str, str]] = [
    ("1. Rest", "sit-idle-cute"),
    ("2. Zombie", "idle_zombie"),
    ("3. Relaxed", "idle_layingdown2"),
    ("4. Attentive", "idle_layingdown"),
    ("5. Sleepy", "idle-sleep"),
    ("6. Pouty Face", "idle-sad"),
    ("7. Posh", "idle-posh"),
    ("8. Sleepy", "idle-loop-tired"),
    ("9. Tap Loop", "idle-loop-tapdance"),
    ("10. Sit", "idle-loop-sitfloor"),
    ("11. Shy", "idle-loop-shy"),
    ("12. Bummed", "idle-loop-sad"),
    ("13. Chillin'", "idle-loop-happy"),
    ("14. Annoyed", "idle-loop-annoyed"),
    ("15. Aerobics", "idle-loop-aerobics"),
    ("16. Ponder", "idle-lookup"),
    ("17. Hero Pose", "idle-hero"),
    ("18. Relaxing", "idle-floorsleeping2"),
    ("19. Cozy Nap", "idle-floorsleeping"),
    ("20. Enthused", "idle-enthusiastic"),
    ("21. Boogie Swing", "idle-dance-swinging"),
    ("22. Feel The Beat", "idle-dance-headbobbing"),
    ("23. Irritated", "idle-angry"),
    ("24. Yes", "emote-yes"),
    ("25. I Believe I Can Fly", "emote-wings"),
    ("26. The Wave", "emote-wave"),
    ("27. Tired", "emote-tired"),
    ("28. Think", "emote-think"),
    ("29. Theatrical", "emote-theatrical"),
    ("30. Tap Dance", "emote-tapdance"),
    ("31. Super Run", "emote-superrun"),
    ("32. Super Punch", "emote-superpunch"),
    ("33. Sumo Fight", "emote-sumo"),
    ("34. Thumb Suck", "emote-suckthumb"),
    ("35. Splits Drop", "emote-splitsdrop"),
    ("36. Snowball Fight!", "emote-snowball"),
    ("37. Snow Angel", "emote-snowangel"),
    ("38. Shy", "emote-shy"),
    ("39. Secret Handshake", "emote-secrethandshake"),
    ("40. Sad", "emote-sad"),
    ("41. Rope Pull", "emote-ropepull"),
    ("42. Roll", "emote-roll"),
    ("43. ROFL!", "emote-rofl"),
    ("44. Robot", "emote-robot"),
    ("45. Rainbow", "emote-rainbow"),
    ("46. Proposing", "emote-proposing"),
    ("47. Peekaboo!", "emote-peekaboo"),
    ("48. Peace", "emote-peace"),
    ("49. Panic", "emote-panic"),
    ("50. No", "emote-no"),
    ("51. Ninja Run", "emote-ninjarun"),
    ("52. Night Fever", "emote-nightfever"),
    ("53. Monster Fail", "emote-monster_fail"),
    ("54. Model", "emote-model"),
    ("55. Flirty Wave", "emote-lust"),
    ("56. Level Up!", "emote-levelup"),
    ("57. Amused", "emote-laughing2"),
    ("58. Laugh", "emote-laughing"),
    ("59. Kiss", "emote-kiss"),
    ("60. Super Kick", "emote-kicking"),
    ("61. Jump", "emote-jumpb"),
    ("62. Judo Chop", "emote-judochop"),
    ("63. Imaginary Jetpack", "emote-jetpack"),
    ("64. Hug Yourself", "emote-hugyourself"),
    ("65. Sweating", "emote-hot"),
    ("66. Hero Entrance", "emote-hero"),
    ("67. Hello", "emote-hello"),
    ("68. Headball", "emote-headball"),
    ("69. Harlem Shake", "emote-harlemshake"),
    ("70. Happy", "emote-happy"),
    ("71. Handstand", "emote-handstand"),
    ("72. Greedy Emote", "emote-greedy"),
    ("73. Graceful", "emote-graceful"),
    ("74. Moonwalk", "emote-gordonshuffle"),
    ("75. Ghost Float", "emote-ghost-idle"),
    ("76. Gangnam Style", "emote-gangnam"),
    ("77. Frolic", "emote-frollicking"),
    ("78. Faint", "emote-fainting"),
    ("79. Clumsy", "emote-fail2"),
    ("80. Fall", "emote-fail1"),
    ("81. Face Palm", "emote-exasperatedb"),
    ("82. Exasperated", "emote-exasperated"),
    ("83. Elbow Bump", "emote-elbowbump"),
    ("84. Disco", "emote-disco"),
    ("85. Blast Off", "emote-disappear"),
    ("86. Faint Drop", "emote-deathdrop"),
    ("87. Collapse", "emote-death2"),
    ("88. Revival", "emote-death"),
    ("89. Dab", "emote-dab"),
    ("90. Curtsy", "emote-curtsy"),
    ("91. Confusion", "emote-confused"),
    ("92. Cold", "emote-cold"),
    ("93. Charging", "emote-charging"),
    ("94. Bunny Hop", "emote-bunnyhop"),
    ("95. Bow", "emote-bow"),
    ("96. Boo", "emote-boo"),
    ("97. Home Run!", "emote-baseball"),
    ("98. Falling Apart", "emote-apart"),
    ("99. Thumbs Up", "emoji-thumbsup"),
    ("100. Point", "emoji-there"),
    ("101. Love", "emoji-love"),
    ("102. Laughing", "emoji-laugh"),
    ("103. Go", "emoji-go"),
    ("104. Stop", "emoji-stop"),
    ("105. Smile", "emoji-smile"),
    ("106. Sad", "emoji-sad"),
    ("107. Shocked", "emoji-oops"),
    ("108. No", "emoji-no"),
    ("109. Yes", "emoji-yes"),
    ("110. Angry", "emoji-angry"),
    ("111. Clapping", "emoji-clapping"),
    ("112. Crying", "emoji-crying"),
    ("113. Dancing", "emoji-dancing"),
    ("114. Excited", "emoji-excited"),
    ("115. Fear", "emoji-fear"),
    ("116. Thinking", "emoji-thinking"),
    ("117. Waving", "emoji-waving"),
    ("118. Wink", "emoji-wink"),
    ("119. Cool", "emoji-cool"),
    ("120. Confused", "emoji-confused"),
    ("121. Proud", "emoji-proud"),
    ("122. Embarrassed", "emoji-embarrassed"),
    ("123. Party", "emoji-party"),
    ("124. Ninja", "emoji-ninja"),
    ("125. Pirate", "emoji-pirate"),
    ("126. Robot", "emoji-robot"),
    ("127. Zombie", "emoji-zombie"),
    ("128. Sleep", "emoji-sleep"),
    ("129. Working", "emoji-working"),
    ("130. Studying", "emoji-studying"),
    ("131. Typing", "emoji-typing"),
    ("132. Reading", "emoji-reading"),
    ("133. Watching", "emoji-watching"),
    ("134. Listening", "emoji-listening"),
    ("135. Cooking", "emoji-cooking"),
    ("136. Eating", "emoji-eating"),
    ("137. Drinking", "emoji-drinking"),
    ("138. Cleaning", "emoji-cleaning"),
    ("139. Shopping", "emoji-shopping"),
    ("140. Exercising", "emoji-exercising"),
    ("141. Running", "emoji-running"),
    ("142. Swimming", "emoji-swimming"),
    ("143. Dancing", "emoji-dancing2"),
    ("144. Singing", "emoji-singing"),
    ("145. Playing", "emoji-playing"),
    ("146. Gaming", "emoji-gaming"),
    ("147. Drawing", "emoji-drawing"),
    ("148. Painting", "emoji-painting"),
    ("149. Building", "emoji-building"),
    ("150. Fixing", "emoji-fixing"),
    ("151. Traveling", "emoji-traveling"),
    ("152. Flying", "emoji-flying"),
    ("153. Riding", "emoji-riding"),
    ("154. Driving", "emoji-driving"),
    ("155. Boating", "emoji-boating"),
    ("156. Camping", "emoji-camping"),
    ("157. Fishing", "emoji-fishing"),
    ("158. Hunting", "emoji-hunting"),
    ("159. Exploring", "emoji-exploring"),
    ("160. Celebrating", "emoji-celebrating"),
    ("161. Hugging", "emoji-hugging"),
    ("162. Kissing", "emoji-kissing"),
    ("163. Flirting", "emoji-flirting"),
    ("164. Arguing", "emoji-arguing"),
    ("165. Fighting", "emoji-fighting"),
    ("166. Apologizing", "emoji-apologizing"),
    ("167. Forgiving", "emoji-forgiving"),
    ("168. Thanking", "emoji-thanking"),
    ("169. Praying", "emoji-praying"),
    ("170. Meditating", "emoji-meditating"),
    ("171. Sleeping", "emoji-sleeping"),
    ("172. Dreaming", "emoji-dreaming"),
    ("173. Snoring", "emoji-snoring"),
    ("174. Yawning", "emoji-yawning"),
    ("175. Sneezing", "emoji-sneezing"),
    ("176. Coughing", "emoji-coughing"),
    ("177. Laughing Hard", "emoji-lol"),
    ("178. Facepalm", "emoji-facepalm"),
    ("179. Headbang", "emoji-headbang"),
    ("180. Twerking", "emoji-twerk"),
    ("181. Splits", "emoji-splits"),
    ("182. Magic", "emoji-magic"),
    ("183. Teleport", "emoji-teleport"),
    ("184. Invisible", "emoji-invisible"),
    ("185. Fireworks", "emoji-fireworks"),
    ("186. Celebration", "emoji-celebration")
]
    ...
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
