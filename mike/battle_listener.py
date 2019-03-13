import json
import logging
import os
from urllib.parse import urlparse

import aioredis
import aiomysql

from .constants import MEESEEKER_SELECTOR_FOR_CUSTOM_JSON
from .embeds import battle_alert

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()


class TxListener:

    def __init__(self, db, bot):
        self.db = db
        self.bot = bot
        self.battle_log_channel = os.getenv("MIKE_BATTLE_LOG_CHANNEL_ID")

    async def get_connection(self):
        p = urlparse(os.getenv("MIKE_DB"))
        path = p.path[1:]
        connection = await aiomysql.connect(
            host=p.hostname,
            port=p.port,
            user=p.username,
            password=p.password,
            db=path,
        )
        return connection

    async def get_subscriptions(self, player_account):
        conn = await self.get_connection()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM subscriptions where player_account = %s",
                player_account)
            r = await cur.fetchall()
            return r

    async def listen_ops(self):

        # aioredis doesn't support both subscribing and getting the data
        # in a one redis instance. so we create two instances.
        subscriber_redis = await aioredis.create_redis(
            (os.getenv("MIKE_REDIS_HOST"), os.getenv("MIKE_REDIS_PORT")))
        reader_redis = await aioredis.create_redis(
            (os.getenv("MIKE_REDIS_HOST"), os.getenv("MIKE_REDIS_PORT")))

        res = await subscriber_redis.subscribe(
            MEESEEKER_SELECTOR_FOR_CUSTOM_JSON)
        channel = res[0]
        while await channel.wait_message():
            msg = await channel.get_json()
            data = await reader_redis.get(msg["key"])
            try:
                op = json.loads(data)
            except Exception as error:
                # malformed json, skip
                return

            await self.handle_operation(
                op["type"], op["value"], op["timestamp"])

    async def handle_operation(self, op_type, op_value, timestamp):
        # we're only interested in custom jsons
        if op_type != "custom_json_operation":
            return

        # handle malformed json data
        try:
            metadata = json.loads(op_value["json"])
        except Exception as error:
            return

        # we're only interested in fights.
        if metadata.get("type") != "fight":
            return

        # if battle_log is enabled,
        # bot puts all battle stream into a specific channel.
        if self.battle_log_channel:
            channel = self.bot.running_on.get_channel(
                self.battle_log_channel)
            await self.bot.send_message(channel, embed=battle_alert(
                    metadata,
                    timestamp,
                ))

        subscriptions = await self.get_subscriptions(
            metadata["payload"]["target"])

        if len(subscriptions) == 0:
            return

        for subscription in subscriptions:
            if subscription["player_account"] != metadata["payload"]["target"]:
                continue
            member = self.bot.running_on.get_member(
                subscription["discord_backend_id"])
            if not member:
                continue
            print("Sending notification to", subscription["discord_account"])
            await self.bot.send_message(member, embed=battle_alert(
                metadata,
                timestamp,
            ))