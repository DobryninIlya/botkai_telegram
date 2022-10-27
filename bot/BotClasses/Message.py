import json


class Message:
    def __init__(self, update):
        self.button = None
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
        if 'text' in self.message.keys():
            self.text = self.message['text']
        else:
            self.text = ""
        if 'entities' in self.message.keys():
            self.entities = self.message['entities']
        if 'caption' in self.message.keys():
            self.text = self.message['caption']
        self.attachments = None
        self.media_group_id = None
        if 'media_group_id' in self.message.keys():
            self.media_group_id = self.message['media_group_id']
        if 'photo' in self.message.keys():
            files = []
            for file in self.message['photo']:
                files.append({
                    'type': 'photo',
                    'media': file['file_id']
                })
            self.attachments = files
