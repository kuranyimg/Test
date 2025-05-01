def is_vip(username: str, vip_list: set) -> bool:
    return username.lower() in vip_list

async def handle_vip_command(user, message: str, vip_list: set) -> str:
    if not user.username.lower() in vip_list:
        return "Only VIPs can add other VIPs."

    parts = message.split("@", 1)
    if len(parts) != 2:
        return "Invalid VIP command format. Use vip@username."

    new_vip = parts[1].strip().lower()
    if new_vip in vip_list:
        return f"{new_vip} is already a VIP."

    vip_list.add(new_vip)
    return f"{new_vip} has been added to the VIP list."
