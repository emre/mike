import os
import dataset


class Database:
    """The wrapper class for database operations.
    """

    def __init__(self, connection_uri=None):
        self.connection = dataset.connect(
            connection_uri or os.getenv("MIKE_DB"))

    @property
    def subscriptions(self):
        """Returns the dataset table object."""
        return self.connection["subscriptions"]

    def subscribe(self, player_account, discord_account, discord_backend_id):
        """Subscribe to a player account from a discord account.

        :param player_account: Account name in STEEM blockchain
        :param discord_account: Discord ID. (foo#N)
        :return: None
        """
        self.subscriptions.insert(dict(
            player_account=player_account,
            discord_account=discord_account,
            discord_backend_id=discord_backend_id,
        ))

    def unsubscribe(self, player_account, discord_account):
        """Unsubscribe from a discord account to a discord account.

        :param player_account: Account name in STEEM blockchain
        :param discord_account: Discord ID. (foo#N)
        :return: None
        """
        self.subscriptions.delete(
            player_account=player_account,
            discord_account=discord_account,
        )

    def subscription_exists(self, player_account, discord_account):
        """Check if a subscription is already exists.

        :param player_account: Account name in STEEM blockchain
        :param discord_account: Discord ID. (foo#N)
        :return (boolean): True or False based on the existence
        """
        if self.subscriptions.find_one(
                player_account=player_account,
                discord_account=discord_account):
            return True
        return False

    def active_subscription_count(self, discord_account):
        """Return the active subscription count for a discord account.

        :param discord_account: Discord ID. (foo#N)
        :return (boolean): True or False based on the existence
        """
        return len(list(
            self.subscriptions.find(discord_account=discord_account)))

    def all_subscriptions(self):
        """Returns all subscriptions globally."""
        return list(self.subscriptions.find())

    def subscriptions_by_user(self, discord_account):
        """Return all subscriptions of a particular user.
        :param discord_account: Discord ID. (foo#N)
        """
        return list(self.subscriptions.find(discord_account=discord_account))

    def subscriptions_by_player_account(self, player_account):
        """Return all subscriptions of a player account.
        :param player_account: Account name
        """
        return list(self.subscriptions.find(player_account=player_account))

    def registered_targets(self):
        targets = list(self.subscriptions.find())
        return [t["player_account"] for t in targets]