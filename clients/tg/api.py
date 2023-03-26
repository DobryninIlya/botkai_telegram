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

    async def send_message(self, chat_id: int, text: str, buttons=None, parse_mode=None):
        try:
            url = self.get_url("sendMessage")
            payload = {
                'chat_id': chat_id,
                'text': text
            }
            if buttons or type(buttons) == type([]):
                payload['reply_markup'] = buttons
            if parse_mode:
                payload['parse_mode'] = 'Markdown'
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    async def edit_message(self, chat_id: int, message_id: str, buttons, message:str, parse_mode=None):
        try:
            url = self.get_url("editMessageText")
            payload = {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': message
            }
            if buttons or type(buttons) == type([]):
                payload['reply_markup'] = buttons
            if parse_mode:
                payload['parse_mode'] = 'Markdown'
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    async def answer_callback_query(self, callback_query_id: str):
        try:
            url = self.get_url("answerCallbackQuery")
            payload = {
                'callback_query_id': callback_query_id
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    async def get_chat_member(self, user_id: int) -> dict:
        url = self.get_url("getChatMember")
        payload = {
            'user_id': user_id,
            'chat_id': '@botkainews'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                return res_dict

    async def forward_message(self, chat_id: int, from_chat_id: str, message_id: str):
        try:
            url = self.get_url("forwardMessage")
            payload = {
                'chat_id': chat_id,
                'message_id': message_id-1,
                'from_chat_id': from_chat_id
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    async def send_media_group(self, chat_id: int, media: list):
        try:
            url = self.get_url("sendMediaGroup")
            payload = {
                'chat_id': chat_id,
                'media': media
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())

    async def send_document(self, chat_id: int, document: str, caption: str = 'Документ', filename='Document'):
        try:
            url = self.get_url("sendDocument")
            data = aiohttp.FormData()
            data.add_field('document', document, content_type='multipart/form-data', filename=filename)
            data.add_field('chat_id', str(chat_id), content_type='text/plain')
            data.add_field('caption', caption, content_type='text/plain')
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as resp:
                    res_dict = await resp.json()
                    return res_dict
        except:
            print('Ошибка:\n', traceback.format_exc())