command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.description = ''
        self.payload = []
        self.admlevel = 0
        self.role = []
        self.status_list = []
        self.premium = False
        command_list.append(self)

    def keys(self):
        return self.__keys

    def keys(self, array):
        for k in array:
            self.__keys.append(k.lower())

    def process(self):
        pass
