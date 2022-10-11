import json
import traceback
from typing import Optional

import aiohttp


class TgClient:
    def __init__(self, token: str = ''):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    async def get_me(self) -> dict:
        url = self.get_url("getMe")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def get_updates_in_objects(self, offset: Optional[int] = None, timeout: int = 0):
        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        return res_dict

    async def send_message(self, chat_id: int, text: str, buttons=None):
        try:
            url = self.get_url("sendMessage")
            payload = {
                'chat_id': chat_id,
                'text': text
            }
            if buttons or type(buttons) == type([]):
                payload['reply_markup'] = self.get_keyboard(buttons)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    # {"keyboard": [[{"text": "тест1"}]], "resize_keyboard": true}
    def get_keyboard(self, buttons: list) -> list:
        if not len(buttons):
            keyboard = {
                'remove_keyboard': True
            }
            keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
            keyboard = str(keyboard.decode('utf-8'))
            return keyboard
        buttons_massive = []
        for layer in buttons:
            layer_massive = []
            for button in layer:
                layer_massive.append(self.get_button(button))
            buttons_massive.append(layer_massive)

        keyboard = {
            'resize_keyboard': False,
            'keyboard': buttons

        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def get_button(self, text):
        return {'text': text}

    async def get_chat_member(self, user_id: int) -> dict:
        url = self.get_url("getChatMember")
        payload = {
            'user_id': user_id,
            'chat_id': '@botkainews'
        }
        print(user_id)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                return res_dict