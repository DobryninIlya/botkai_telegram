import json


class Message:
    def __init__(self, update):
        if 'message' in update.keys():
            self.message = update['message']
            self.language_code = self.message['from']['language_code']
            self.callback_query_id = None
            self.from_id = self.message['from']['id']
        elif 'callback_query' in update.keys():
            self.message = update['callback_query']['message']
            self.callback_query_id = update['callback_query']['id']
            self.data = update['callback_query']['data']
            self.from_id = self.message['chat']['id']
            try:
                self.button = json.loads(self.data)['button']
            except:
                self.button = self.data
        else:
            self.message = None
            return None
        self.message_id = self.message['message_id']
        self.is_bot = self.message['from']['is_bot']
        self.first_name = self.message['from']['first_name']

        if 'lastname' in self.message['from'].keys():
            self.last_name = self.message['from']['last_name']
        else:
            self.last_name = ''
        if 'username' in self.message['from'].keys():
            self.username = self.message['from']['username']
        else:
            self.username = ''
        self.chat = self.message['chat']
        self.text = self.message['text']
        if 'entities' in self.message.keys():
            self.entities = self.message['entities']
