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

    if message.button == "score_rating":
        if check_user_registration(user.id) != None:
            msg = "Баллы аттестации. Обратите внимание, страница может загружаться до 1 минуты."
            url_for_att = params_att.format(user.id)
            sign = get_sign(url_for_att)
            url = att_app + "tg_id%3D{}___loading%3Dtrue___sign%3D{}".format(user.id, sign)
            button = button_template
            button[0][0][1] = url
            await tg_client.send_message(user.id, msg, buttons=keyboard('attestation', user, buttons=button).get_link())
        else:
            redirect = att_path.format("")
            url_for_sign = params_auth.format(user.id, redirect)
            sign = get_sign(url_for_sign)
            url = auth_path.format(domain, user.id, redirect, sign)
            params = url.split('?')
            params = params[1]
            msg = "Войдите в ваш аккаунт КАИ на портале авторизации КапиПары.\n Для последующего просмотра БРС без ввода пароля - нажмитен на кнопку 'Баллы БРС' в меню 'Разное' еще раз. "
            button = button_template
            params = params.replace("=", "%3D")
            params = params.replace("&", "___")
            params = params.replace("/", "---")
            button[0][0][1] = auth_app + params
            await tg_client.send_message(user.id, msg, buttons=keyboard('attestation', user, buttons=button).get_link())

        return


    return


command = command_class()

command.keys = ["аттестация"]
command.process = processor
command.role = [1]
command.payload = ['attestation_open', 'score_rating', 'attestation_auth']
command.status_list = [110, 111]
