from functions.vip_data import add_vip, remove_vip, is_vip, get_all_vips

async def handle_command(bot, user, message):
    username = user.username.lower()

    # إضافة VIP
    if message.startswith("vip@"):
        if username != "raybm":
            return await bot.send_whisper(user.id, "فقط راي يمكنه إضافة VIP.")
        vip_name = message[4:].strip().lower()
        add_vip(vip_name)
        return await bot.send_whisper(user.id, f"تمت إضافة {vip_name} إلى VIP.")

    # حذف VIP
    if message.startswith("unvip@"):
        if username != "raybm":
            return await bot.send_whisper(user.id, "فقط راي يمكنه إزالة VIP.")
        vip_name = message[7:].strip().lower()
        remove_vip(vip_name)
        return await bot.send_whisper(user.id, f"تمت إزالة {vip_name} من VIP.")

    # قائمة VIP
    if message == "vips":
        vip_list = get_all_vips()
        msg = "قائمة VIP:\n" + "\n".join(vip_list) if vip_list else "لا يوجد VIP حالياً."
        return await bot.send_whisper(user.id, msg)

    # أمر teleport كمثال VIP
    if message.startswith("teleport "):
        if not is_vip(username):
            return await bot.send_whisper(user.id, "هذا الأمر مخصص للـ VIP فقط.")
        target = message.split(" ", 1)[1]
        await bot.teleport_user(user.username, target)

    # أمر summon كمثال VIP
    if message.startswith("summon "):
        if not is_vip(username):
            return await bot.send_whisper(user.id, "هذا الأمر مخصص للـ VIP فقط.")
        target = message.split(" ", 1)[1]
        await bot.summon_user(target)


# الدالتين الإضافيتين هنا:
def is_teleport_command(message: str) -> bool:
    return message.startswith("teleport ")

def handle_teleport_command(message: str):
    if message.startswith("teleport "):
        return "teleport", message.split(" ", 1)[1].strip()
    return None, None
