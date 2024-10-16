import asyncio

async def on_chat(self, user: User, message: str) -> None:
    print(f"{user.username}: {message}")  # This line just prints the message to the console

    # Now, handle the tip command:
    await handle_tip_command(self, message, user) 

async def handle_tip_command(self, message, user):
    """Handles both -tipall and -tipme commands, announcing tips in the same room."""
    if message.lower().startswith("-tipall ") or message.lower().startswith("-tipme "):
        if user.username != "RayBM":
            return  # Only allow "RayBM" to use these commands

        parts = message.split(" ")
        if len(parts) != 2:
            await self.highrise.send_message(user.id, "Invalid command")
            return

        try:
            tip_amount = int(parts[1])
        except ValueError:
            await self.highrise.chat("Invalid amount")  # Announce in the same room
            return

        bot_wallet = await self.highrise.get_wallet()
        bot_amount = bot_wallet.content[0].amount

        if bot_amount < tip_amount:
            await self.highrise.chat("Not enough funds")  # Announce in the same room
            return

        bars_dictionary = {
            10000: "gold_bar_10k",
            5000: "gold_bar_5000",
            1000: "gold_bar_1k",
            500: "gold_bar_500",
            100: "gold_bar_100",
            50: "gold_bar_50",
            10: "gold_bar_10",
            5: "gold_bar_5",
            1: "gold_bar_1"
        }
        fees_dictionary = {
            10000: 1000,
            5000: 500,
            1000: 100,
            500: 50,
            100: 10,
            50: 5,
            10: 1,
            5: 1,
            1: 1
        }

        tip = []
        remaining_amount = tip_amount
        total_tip_amount = 0

        for bar in sorted(bars_dictionary.keys(), reverse=True):
            if remaining_amount >= bar:
                bar_amount = remaining_amount // bar
                remaining_amount %= bar
                tip.extend([bars_dictionary[bar]] * bar_amount)
                total_tip_amount += bar_amount * bar + fees_dictionary[bar]

        if total_tip_amount > bot_amount:
            await self.highrise.chat("Not enough funds to tip the specified amount.")  # Announce in the same room
            return

        if message.lower().startswith("-tipall "):
            room_users = await self.highrise.get_room_users()
            if bot_amount < total_tip_amount * len(room_users.content):
                await self.highrise.chat("Not enough funds to tip everyone.")  # Announce in the same room
                return

            # Announce tips one by one
            for room_user, pos in room_users.content:
                for bar in tip:
                    await self.highrise.tip_user(room_user.id, bar)
                    await self.highrise.chat(f"User ID: {room_user.id} has been tipped {tip_amount}!")  # Announce in the same room
                    await asyncio.sleep(1)  # Pause for 1 second

        elif message.lower().startswith("-tipme "):
            for bar in tip:
                await self.highrise.tip_user(user.id, bar)
            await self.highrise.chat(f"You have been tipped {tip_amount}.")  # Announce in the same room
