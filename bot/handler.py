import os
import importlib

from bot.BotClasses import command_list, Message, User, Registration, traceback, statistic_updates, statistic_users_active_list, statistic_users_active
from bot.BotClasses.Keyboards import keyboard
from bot.BotClasses.Stage_handler import Stage


def load_modules():
    try:
        files = os.listdir('/home/u_botkai/botraspisanie/botkai_telegram/bot/commands')
    except:
        files = os.listdir("bot/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("bot.commands." + m[0:-3])


load_modules()


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]


async def message_handler(update, tg_client, debug=False):
    ignore_list = ['channel_post', 'edited_channel_post', 'my_chat_member']
    for i in ignore_list:
        if i in update.keys():
            return

    message = Message(update)
    if not message:
        return
    user = User(message)
    global statistic_updates, statistic_users_active_list, statistic_users_active
    statistic_updates += 1
    if not user.id in statistic_users_active_list:
        statistic_users_active += 1
        statistic_users_active_list.append(user.id)
    message.cmd_payload = [statistic_users_active, statistic_updates]

    registration = Registration(user, message, tg_client, debug)
    result, answer, keyboard_answer = await registration.processing()
    if not result:
        await tg_client.send_message(user.id, answer, buttons=keyboard_answer)
        return
    if message.text and message.text[0] == '/':  # Remove slash
        message.text = message.text[1:]
    stage = Stage(user, message)

    if message.text and message.text.lower() == 'выход':
        await tg_client.send_message(user.id, 'Главное меню',
                                     buttons=keyboard('main_keyboard', user).get_keyboard())
        stage._set_status(0)
        return

    distance = len(message.text)
    command = None
    key = ''
    if not len(message.text) and not message.callback_query_id and not stage.status:
        return
    for c in command_list:
        if c.admlevel > user.admLevel:
            continue
        if message.callback_query_id:
            if message.button in c.payload and user.role in c.role:
                await c.process(user, message, tg_client, stage=stage)
                await tg_client.answer_callback_query(message.callback_query_id)
                return
        if stage.status:
            if stage.status in c.status_list:
                await c.process(user, message, tg_client, stage=stage)
                return
        if user.role in c.role and not message.callback_query_id and not stage.status:
            for k in c.keys:
                d = damerau_levenshtein_distance(message.text.lower(), k)
                if d < distance:
                    distance = d
                    command = c
                    key = k
                    if distance == 0 and c.admlevel <= user.admLevel and (user.role in c.role):
                        await c.process(user, message, tg_client, stage=stage)
                        return
    if distance < len(
            message.text.lower()) * 0.4 and command.admlevel <= user.admLevel and user.role in command.role and \
            message.text[1] != '/':
        msg = 'Я понял ваш запрос как "%s"' % key
        await tg_client.send_message(user.id, msg, buttons=keyboard('main_keyboard', user).get_keyboard())
        await command.process(user, message, tg_client, stage=stage)
        return
    if message.callback_query_id:
        return
    await tg_client.send_message(user.id, "Я не понимаю тебя :(", buttons=keyboard('main_keyboard', user).get_keyboard())
    stage._set_status(0)
