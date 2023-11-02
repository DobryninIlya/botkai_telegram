import asyncio
import datetime
import os
import traceback

from bot.base import Bot


def run():
    loop = asyncio.get_event_loop()
    token = os.getenv("TG_TOKEN")
    try:
        if os.getenv("OS") == 'Windows_NT':  # test key
            token = '5510894762:AAH40UTqeEDFlvzKyx7TpRO4_w_qlQYu04o'
    except:
        token = os.getenv("TG_TOKEN")
    bot = Bot(token, 15)
    try:
        print('bot has been started', flush=True)
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now(), flush=True)
        loop.run_until_complete(bot.stop())
        print('bot has been stopped', datetime.datetime.now(), flush=True)
    except:
        print('Ошибка (глобальная):\n', traceback.format_exc(), flush=True)


if __name__ == '__main__':
    run()
