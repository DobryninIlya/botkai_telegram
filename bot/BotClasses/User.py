from .Message import Message
from .Database_connection import cursor, connection, cursorR, conn

class User:
    def __init__(self, update: Message):
        self.id = update.from_id
        self.name = update.first_name
        self.lastname = update.last_name
        try:
            self.username = update.username
        except:
            pass
        self.role = None
        self.admLevel = 0
        self.is_verificated = False

        self._get_user_data()

    def _get_user_data(self):
        sql = "SELECT * FROM tg_users WHERE id={}".format(self.id)
        cursor.execute(sql)
        self.result = cursor.fetchone()
        if not self.result:
            return
        self.admLevel = self.result[5]
        self.is_verificated = self.result[6]
        self.group_name = self.result[7]
        self.group_id = self.result[8]
        self.role = self.result[4]

