import os
import os.path

from mike.client import CustomClient
from .embeds import get_help


def main():
    # init the modified Discord client
    bot = CustomClient(
        command_prefix="$",
        config=dict())

    # remove the default help command, we're overriding a better one.
    bot.remove_command("help")

    # register the commands
    @bot.command(pass_context=True)
    async def subscribe(ctx, player):

        # check if the username is valid
        if not bot.steem_username_is_valid(player):
            await bot.say_error(f"Error: {player} is not a valid username.")
            return

        # get the discord handle with ID. (Example: foo#N)
        discord_account = f"{ctx.message.author.id}#{ctx.message.author.name}"

        # Check active subscriptions
        active_subscription_count = bot.db.active_subscription_count(
            discord_account)

        if active_subscription_count > 4:
            await bot.say_error(f" You can only subscribe to 5 accounts, "
                                f"{ctx.message.author.mention}.")
            return

        # Check if subscription is already exists
        if bot.db.subscription_exists(player, discord_account):
            await bot.say_error(f"Error. You have"
                                f" already subscribed to {player}, "
                                f"{ctx.message.author.mention}.")
            return

        # Finally, subscribe
        bot.db.subscribe(player, discord_account)
        await bot.asay_success(f"Subscription is successful. "
                               f"(From {ctx.message.author.mention}"
                               f" to {player}.)")

    @bot.command(pass_context=True)
    async def help(ctx):
        await bot.send_message(
            ctx.message.channel, "Available commands", embed=get_help())

    # shoot!
    bot.run(os.getenv("MIKE_BOT_TOKEN"))


if __name__ == "__main__":
    main()
