import asyncio

from discord.ext import commands
from steem import Steem

from .db import Database


class CustomClient(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs.get("config")
        self.steem = Steem(nodes=["https://api.steemit.com"])
        self.db = Database()

    @asyncio.coroutine
    def on_ready(self):
        for server in self.servers:
            print(f'Running on {server.name}')

    def say_error(self, error):
        return self.say(f":exclamation: {error}")

    def say_success(self, message):
        return self.say(f":thumbsup: {message}")

    def steem_username_is_valid(self, username):
        resp = self.steem.get_accounts([username])
        return bool(len(resp))

    @property
    def running_on(self):
        return list(self.servers)[0]