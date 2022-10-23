import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message, StudentShedule
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.game.EscapeGame import EscapeGame
from clients.tg.api import TgClient

game_list = []


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False):
    print('игра', callback_query, message.callback_query_id)
    if not callback_query and not message.callback_query_id:
        game = EscapeGame(user)
        game_list.append(game)
        msg = 'Побег из 5ого здания'
        await tg_client.send_message(user.id, 'Меню', buttons=keyboard('exit', user).get_keyboard())
        await tg_client.send_message(user.id, msg, buttons=game.get_map())
        await tg_client.send_message(user.id, 'УПРАВЛЕНИЕ',
                                     buttons=keyboard('game_controls', user).get_inline_keyboard())
        return
    game = None
    for game_ in game_list:
        if game_.chat_user.id == user.id:
            game = game_
    if message.button == 'game_UP':
        game.move('up')
        await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(), message='Движение: вверх')
    elif message.button == 'game_DOWN':
        game.move('down')
        await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(), message='Движение: вниз')
    elif message.button == 'game_LEFT':
        game.move('left')
        await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(), message='Движение: влево')
    elif message.button == 'game_RIGHT':
        game.move('right')
        await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(), message='Движение: вправо')
    elif message.button == 'game_ATTACK':
        result = game.attack()
        print('result: ', result)
        if not result:
            balance = game.game_over()
            msg = f'Все враги убиты. Вы заработали: {balance}'
            print(msg)
            await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(game_over=True), message=msg)
            game_list.remove(game)
            del game
        else:
            msg = 'Атака: ' + str(game.user.attack)
            await tg_client.edit_message(user.id, message.message_id, buttons=game.get_map(), message=msg)
    await tg_client.answer_callback_query(message.callback_query_id)

command = command_class()

command.keys = ['игра', 'up', 'down', 'left', 'right', 'играть еще']
command.process = processor
command.role = [1]
command.payload = ['game_map', 'game_RIGHT', 'game_LEFT', 'game_UP', 'game_DOWN', 'game_ATTACK']
