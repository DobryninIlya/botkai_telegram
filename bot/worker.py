import asyncio
import datetime
import traceback
from typing import List

from clients.tg.api import TgClient
from bot.handler import message_handler


# from clients.tg.dcs import UpdateObj


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []
        self.debug = True if token[1] == '5' else False

    async def handle_update(self, upd):
        await message_handler(upd, self.tg_client, self.debug)

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            except:
                print('Ошибка:\n', traceback.format_exc())
                await self.tg_client.send_message(393867797, str(traceback.format_exc()))
                await self.tg_client.send_message(393867797, upd)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]
        # await self.tg_client.send_message(393867797, 'стартуем....')

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
