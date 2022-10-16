import json
import traceback
from datetime import datetime

import aiohttp

from .User import User
from .Message import Message
from .Keyboards import registration_role, main_keyboard
from .Database_connection import cursor, connection, cursorR, conn


class Stage:
    def __init__(self, user: User, message: Message, tg_client):
        self.user_id = 0
        self.message = message
        self.cursor = cursor
        self.connection = connection
        self.cursorR = cursorR
        self.conn = conn
        self.user = user
        self.user_group_id = None
        self.user_group_name = None
        self.tg_client = tg_client

    def _execute(self, sql_query):
        self.cursor.execute(sql_query)
        self.connection.commit()
        return

    def _get_status_code(self):
        sql = "SELECT Status FROM Status WHERE ID = {}".format(self.user_id)
        self.cursorR.execute(sql)
        result = self.cursorR.fetchone()
        if not result:
            return False
        result = result[0]
        return result

    def _set_status(self, code):
        if not code:
            self.cursorR.execute("DELETE FROM Status WHERE ID={}".format(self.user_id))
            self.conn.commit()
            return
        try:
            self.cursorR.execute("INSERT INTO Status VALUES ({},{})".format(self.user_id, code))
        except:
            self.cursorR.execute("UPDATE Status SET Status = {}".format(code))
        finally:
            self.conn.commit()

    def handler(self):
        pass
