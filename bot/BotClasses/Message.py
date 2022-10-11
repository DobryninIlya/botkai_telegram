class Message:
    def __init__(self, update):
        self.message = update['message']
        self.message_id = self.message['message_id']
        self.from_id = self.message['from']['id']
        self.is_bot = self.message['from']['is_bot']
        self.first_name = self.message['from']['first_name']
        self.last_name = self.message['from']['last_name']
        self.username = self.message['from']['username']
        self.language_code = self.message['from']['language_code']
        self.chat = self.message['chat']
        self.text = self.message['text']
        if 'entities' in self.message.keys():
            self.entities = self.message['entities']