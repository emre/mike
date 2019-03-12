import json
import logging
import os

import aioredis

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

    async def listen_ops(self):
        sub = await aioredis.create_redis(
            ('localhost', 6379))
        reader_redis = await aioredis.create_redis(
            ('localhost', 6379))

        res = await sub.subscribe(MEESEEKER_SELECTOR_FOR_CUSTOM_JSON)
        ch1 = res[0]
        while await ch1.wait_message():
            msg = await ch1.get_json()
            data = await reader_redis.get(msg["key"])
            op = json.loads(data)
            await self.handle_operation(
                op["type"], op["value"], op["timestamp"])

    async def handle_operation(self, op_type, op_value, timestamp):
        if op_type != "custom_json_operation":
            return

        metadata = json.loads(op_value["json"])
        if metadata.get("type") != "fight":
            return

        if self.battle_log_channel:
            channel = self.bot.running_on.get_channel(
                self.battle_log_channel)
            await self.bot.send_message(channel, embed=battle_alert(
                    metadata,
                    timestamp,
                ))

        subscriptions = self.db.all_subscriptions()
        for subscription in subscriptions:
            if subscription["player_account"] == metadata["payload"]["target"]:
                member = self.bot.running_on.get_member(
                    subscription["discord_backend_id"])
                await self.bot.send_message(member, embed=battle_alert(
                    metadata,
                    timestamp,
                ))
