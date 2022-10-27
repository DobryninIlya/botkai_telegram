from .User import User
from .Message import Message
from .Database_connection import cursor, connection, cursorR, conn


class Value:
    def __init__(self, user: User, message: Message):
        self.message = message
        self.cursorR = cursorR
        self.conn = conn
        self.user = user

    def _clear_answers_table(self):
        try:
            self.cursorR.execute("DELETE FROM answers WHERE id = {}".format(self.user.id))
            return True
        except:
            return False

    def save_id_to_answer(self, user_anwser_id:int):
        sql = "INSERT INTO answers VALUES ({}, {})".format(self.user.id, user_anwser_id)
        try:
            self.cursorR.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def get_user_to_answer(self):
        sql = "SELECT userId FROM answers WHERE id = {}".format(self.user.id)
        try:
            self.cursorR.execute(sql)
            return self.cursorR.fetchone()[0]
        except:
            return False
        finally:
            self._clear_answers_table()


