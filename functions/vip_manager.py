from functions.vip_data import add_vip, remove_vip, get_all_vips, is_vip as db_is_vip

OWNER_USERNAME = "raybm"

def is_vip(username: str) -> bool:
    return db_is_vip(username)

def get_vip_list() -> str:
    vip_list = get_all_vips()
    if not vip_list:
        return "VIP list is empty."
    return "VIPs:\n" + "\n".join(f"- {vip}" for vip in sorted(vip_list))

async def handle_vip_command(user, message: str) -> str:
    username = user.username.lower()

    if username != OWNER_USERNAME:
        return f"Sorry {user.username}, only the bot owner can manage VIPs."

    if message.lower().startswith("vip@"):
        target_username = message.split("@", 1)[1].strip().lower()
        if not target_username:
            return "Please specify a username to add as VIP."
        if db_is_vip(target_username):
            return f"{target_username} is already a VIP."
        add_vip(target_username)
        return f"✅ {target_username} has been added to the VIP list."

    if message.lower().startswith("unvip@"):
        target_username = message.split("@", 1)[1].strip().lower()
        if not target_username:
            return "Please specify a username to remove from VIP."
        if not db_is_vip(target_username):
            return f"{target_username} is not in the VIP list."
        remove_vip(target_username)
        return f"❌ {target_username} has been removed from the VIP list."

    return "Invalid VIP command format. Use vip@username or unvip@username."
