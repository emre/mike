from discord import Embed
from datetime import datetime
from dateutil.parser import parse

def get_dw_link(player):
    return f"[{player}](https://drugwars.io/@{player})"


def get_help():
    """Returns the embed objects of the $help command."""
    embed = Embed(
        color=0x2ecc71,
    )
    embed.add_field(
        name="$subscribe",
        value="Subscribe to a player's battles."
              "```$subscribe <player_account>```",
        inline=False,
    )

    embed.add_field(
        name="$help",
        value="Shows this message.",
        inline=False,
    )

    return embed


def battle_alert(metadata, timestamp):
    """Returns the embed object of the battle notification"""
    army_text = ""
    for unit in metadata["payload"]["units"]:
        army_text += f"- {unit['key'].capitalize()} ({unit['amount']})\n "

    embed = Embed(
        color=0x2ecc71,
        title="New Battle!"
    )
    embed.add_field(
        name="Attacker",
        value=get_dw_link(metadata["author"]),
        inline=False,
    )
    embed.add_field(
        name="Target",
        value=get_dw_link(metadata["payload"]["target"]),
        inline=False,
    )

    embed.add_field(
        name="Attacker Army",
        value=army_text,
        inline=False,
    )
    embed.timestamp = parse(timestamp)
    embed.set_thumbnail(
        url=f"https://steemitimages.com/u/{metadata['author']}/avatar")

    return embed

def subscription_list_embed(discord_account, subscriptions):
    """Returns a rich embed includes the subscription list of a particular
    discord account."""

    subscription_list = ""
    for subscription in subscriptions:
        subscription_list += f"- {subscription['player_account']}\n"

    embed = Embed(
        color=3447003,
    )
    embed.title = f"Subscriptions of {discord_account}"
    embed.add_field(
        name="Players",
        value=subscription_list,
    )
    embed.timestamp = datetime.utcnow()
    return embed