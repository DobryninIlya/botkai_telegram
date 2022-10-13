import os
import importlib

from bot.BotClasses import command_list, Message, User, Registration, Keyboards, traceback

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


async def message_handler(update, tg_client):
    message = Message(update)
    if not message == None or not message.message:
        return
    user = User(message)
    registration = Registration(user, message, tg_client)
    result, answer, keyboard = await registration.processing()
    if not result:
        await tg_client.send_message(user.id, answer, buttons=keyboard)
        return
    if message.text[0] == '/':  # Remove slash
        message.text = message.text[1:]
    distance = len(message.text)
    command = None
    key = ''
    for c in command_list:
        if user.role in c.role:
            for k in c.keys:
                d = damerau_levenshtein_distance(message.text.lower(), k)
                if d < distance:
                    distance = d
                    command = c
                    key = k
                    if distance == 0 and c.admlevel <= user.admLevel and (user.role in c.role):
                        await c.process(user, message, tg_client)
                        return
    if distance < len(message.text.lower()) * 0.4 and command.admlevel <= user.admLevel and user.role in command.role and message.text[1]!='/':
        msg = 'Я понял ваш запрос как "%s"' % key
        await tg_client.send_message(user.id, msg, buttons=Keyboards.main_keyboard)
        await command.process(user, message, tg_client)
        return
    await tg_client.send_message(user.id, "Я не понимаю тебя :(")
