import json
import os
import random
import requests

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from clients.tg.api import TgClient
from ..BotClasses.Database_connection import cursor, connection

button_template = [[['Открыть', '']]]
domain = 'https://schedule-bot.kai.ru'
auth_path = '{}/portal/authorization/?tg_id={}&redirect_url={}&sign={}'
att_path = '{}/portal/attestation/'
sign_path = '{}/portal/sign?{}'
params_auth = 'path?tg_id={}&redirect_url={}&secret='+os.getenv('WEB_KAI_SECRET')
params_att = 'path?tg_id={}&secret='+os.getenv('WEB_KAI_SECRET')
auth_app = "https://t.me/knrtukaibot/capy?startapp="
att_app = "https://t.me/knrtukaibot/capy_attestation?startapp="
def check_user_registration(tg_id):
    sql = f"SELECT login FROM public.mobile_user_password WHERE uid='tg{tg_id}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return None
    return result

def get_sign(path: str):
    params = path.split('?')
    params = params[1]
    try:
        response = requests.get(sign_path.format(domain, params))
        sign = response.json()["result"]["sign"]
        return sign
    except:
        return None
async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    msg = "Баллы аттестации. Обратите внимание, страница может загружаться до 1 минуты."
    url_for_att = params_att.format(user.id)
    sign = get_sign(url_for_att)
    url = att_app + "user_id%3D{}___sign%3D{}".format(user.id, sign)
    button = button_template
    button[0][0][1] = url
    await tg_client.send_message(user.id, msg, buttons=keyboard('attestation', user, buttons=button).get_link())

    return


command = command_class()

command.keys = ["импорт в календарь"]
command.process = processor
command.role = [1]
command.payload = []
