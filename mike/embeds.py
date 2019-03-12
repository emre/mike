from discord import Embed
from datetime import datetime


def get_help():
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


def battle_alert(attacker, units, started_at):
    army_text = ""
    for unit in units:
        army_text += f"x{unit['amount']} {unit['key']}, "
    army_text = army_text[:-2]
    army_text += "."
    embed = Embed(
        color=0x2ecc71,
    )
    embed.add_field(
        name="New Battle!",
        value=f"@{attacker} attacks you with {army_text}."
    )
    embed.add_field(
        name="Started At",
        value=started_at,
        inline=False,
    )

    return embed

def subscription_list_embed(discord_account, subscriptions):
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