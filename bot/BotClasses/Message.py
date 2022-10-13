class Message:
    def __init__(self, update):
        if 'message' in update.keys():
            self.message = update['message']
        else:
            self.message = None
            return None
        self.message_id = self.message['message_id']
        self.from_id = self.message['from']['id']
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
        self.language_code = self.message['from']['language_code']
        self.chat = self.message['chat']
        self.text = self.message['text']
        if 'entities' in self.message.keys():
            self.entities = self.message['entities']
