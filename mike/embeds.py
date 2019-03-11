from discord import Embed


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