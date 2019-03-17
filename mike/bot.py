import os
import os.path

from .client import CustomClient
from .embeds import get_help, subscription_list_embed
from .battle_listener import TxListener
from .db import Database

import asyncio


def main():
    # init the modified Discord client
    bot = CustomClient(
        command_prefix="$",
        config=dict())

    # remove the default help command, we're overriding a better one.
    bot.remove_command("help")

    @bot.command(pass_context=True)
    async def subscribe(ctx, player):

        # check if the username is valid
        if not bot.steem_username_is_valid(player):
            await bot.say_error(f"Error: {player} is not a valid username.")
            return

        # get the discord handle with ID. (Example: foo#N)
        discord_account = str(ctx.message.author)

        # Check active subscriptions
        active_subscription_count = bot.db.active_subscription_count(
            discord_account)

        if active_subscription_count > 9:
            await bot.say_error(f" You can only subscribe to 10 accounts, "
                                f"{ctx.message.author.mention}.")
            return

        # Check if subscription is already exists
        if bot.db.subscription_exists(player, discord_account):
            await bot.say_error(f"Error. You have"
                                f" already subscribed to {player}, "
                                f"{ctx.message.author.mention}.")
            return

        # Finally, subscribe
        bot.db.subscribe(player, discord_account, ctx.message.author.id)
        await bot.say_success(f"Subscription is successful. "
                               f"(From {ctx.message.author.mention}"
                               f" to {player}.)")

    @bot.command(pass_context=True)
    async def unsubscribe(ctx, player):
        # check if the username is valid
        if not bot.steem_username_is_valid(player):
            await bot.say_error(f"Error: {player} is not a valid username.")
            return

        # get the discord handle with ID. (Example: foo#N)
        discord_account = str(ctx.message.author)

        # Check if subscription is already exists
        if not bot.db.subscription_exists(player, discord_account):
            await bot.say_error(f"Error. You are not"
                                f" subscribed to {player}, "
                                f"{ctx.message.author.mention}.")
            return

        # Finally, unsubscribe
        bot.db.unsubscribe(player, discord_account)
        await bot.say_success(f"Subscription is removed. "
                               f"(From {ctx.message.author.mention}"
                               f" to {player}.)")

    @bot.command(pass_context=True)
    async def subscriptions(ctx):
        subscriptions = bot.db.subscriptions_by_user(str(ctx.message.author))
        await bot.send_message(
            ctx.message.channel, embed=subscription_list_embed(
            str(ctx.message.author), subscriptions))

    @bot.command(pass_context=True)
    async def help(ctx):
        await bot.send_message(
            ctx.message.channel, "Available commands", embed=get_help())

    async def listen_battles():
        """This task listens the battles and and notifies the subscribed
        users via Discord if required.
        """
        await bot.wait_until_ready()
        while not bot.is_closed:
            try:
                tx_listener = TxListener(
                    db=Database(),
                    bot=bot,
                )
                await tx_listener.listen_ops()
            except Exception as error:
                print(error)
                asyncio.sleep(1)

    # shoot!
    bot.loop.create_task(listen_battles())
    # shoot!
    bot.run(os.getenv("MIKE_BOT_TOKEN"))


if __name__ == "__main__":
    main()
