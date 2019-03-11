import unittest

from mike.db import Database

db_conn_uri = "sqlite:///:memory:"

class DatabaseTests(unittest.TestCase):

    def testInsertSubscription(self):
        db = Database(connection_uri=db_conn_uri)
        db.subscribe("emrebeyler", "emrebeyler#9263")
        player = list(db.subscriptions.find(
                player_account="emrebeyler",
                discord_account="emrebeyler#9263"))
        self.assertEqual(
            len(player),
            1
        )

    def testDuplicateInsert(self):
        db = Database(connection_uri=db_conn_uri)
        db.subscribe("emrebeyler", "emrebeyler#9263")
        db.subscribe("emrebeyler", "emrebeyler#9263")
        player = list(db.subscriptions.find(
                player_account="emrebeyler",
                discord_account="emrebeyler#9263"))
        self.assertEqual(
            len(player),
            1
        )
