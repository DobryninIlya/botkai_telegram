import psycopg2
import os
import sqlite3

class database_connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user= os.getenv('DB_USER'), password= os.getenv('DB_PASSWORD'), host= os.getenv('DB_HOST'))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.conn = sqlite3.connect("bot\\BotClasses\\bot.db")
        self.cursorR = self.conn.cursor()


connect = database_connections()
cursor = connect.cursor
connection = connect.connection
cursorR = connect.cursorR
conn = connect.conn