import json
from .User import User

##### Classic version (old)
# main_keyboard = [
#     ["На завтра"],
#     ["На сегодня", "На послезавтра", "Полностью"],
#     ["Четность недели", "Задания и объявления"],
#     ["Разное", "Преподаватели"],
#     ["Обратная связь", "Донат", "Профиль"]
# ]
main_keyboard = [
    ["На завтра"],
    ["На сегодня", "На послезавтра"],
    ["Четность недели", "Полностью"],
    ["Разное", "Преподаватели"],
    ["Обратная связь", "Донат", "Профиль"]
]
registration_role = [
    ['Студент'],
    ['Преподаватель'],
    ['Родитель'],
    ['Абитуриент'],
    ['Личный кабинет']
]

feedback = [
    ['Отправить сообщение']
]

profile = [
    [['{} группа', 'groupchange']],
    # [['Мои задания', 'my_task']],
    [['Поддержать проект', 'donate']],
    [['Ссылки на одногруппников', 'classmates_links']],
    [['Студенты группы', 'classmates_list']],
    [['Мой институт', 'my_faculty']]  # , ['Подписки', 'subscriptions']],
    # [['{}', 'starosta']]
]

feedback_create = [[['Продолжить', 'feedback_create']]]

exit = [['Выход']]

game_controls = [
    ['.', 'UP', '.'],
    ['LEFT', 'ATTACK', 'RIGHT'],
    ['.', 'DOWN', '.'],
]
game_controls = [
    [['.', 'none'], ['UP', 'game_UP'], ['.', 'none']],
    [['LEFT', 'game_LEFT'], ['ATTACK', 'game_ATTACK'], ['RIGHT', 'game_RIGHT']],
    [['.', 'none'], ['DOWN', 'game_DOWN'], ['exit', 'main_menu']]
]
game_over = [['с']]

group_change = [[['Изменить', 'group_change_commit']]]
answer_feedback = [[['Ответить пользователю', 'answer_feedback']]]
donate_link = [[['Отправить перевод', 'https://www.tinkoff.ru/cf/7EDMYnSmO68']]]


class keyboard:
    def __init__(self, type_name: str, user: User, buttons: list = None, payload=None):
        self.type_name = type_name
        self.buttons = []
        self.user = user
        if self.type_name == 'main_keyboard':
            self.buttons = main_keyboard
        elif self.type_name == 'exit':
            self.buttons = exit
        elif self.type_name == 'registration_role':
            self.buttons = registration_role
        elif self.type_name == 'feedback':
            self.buttons = feedback
        elif self.type_name == 'profile':
            self.buttons = self.get_profile()
        elif self.type_name == 'feedback_create':
            self.buttons = feedback_create
        elif self.type_name == 'game_map':
            self.buttons = buttons
        elif self.type_name == 'game_controls':
            self.buttons = game_controls
        elif self.type_name == 'game_over':
            self.buttons = game_over
        elif self.type_name == 'group_change':
            self.buttons = group_change
        elif self.type_name == 'answer_for_feedback':
            button = answer_feedback[0][0][1]
            answer_feedback[0][0][1] = json.dumps({'button': button, 'user_id': payload})
            self.buttons = answer_feedback
        elif self.type_name == 'donate_link':
            self.buttons = donate_link

    def get_profile(self):
        self.profile = profile
        # self.profile[0][0][0] = self.profile[0][0][0].format(self.user.group_name)
        return self.profile

    def get_inline_keyboard(self) -> dict:
        button_list = []
        for button_row in self.buttons:
            button_row_list = []
            for button in button_row:
                button_ = {
                    'text': button[0],
                    'callback_data': button[1]
                }
                button_row_list.append(button_)
            button_list.append(button_row_list)
        keyboard = {"inline_keyboard": button_list}
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def get_keyboard(self) -> list:
        if not len(self.buttons):
            keyboard = {
                'remove_keyboard': True
            }
            keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
            keyboard = str(keyboard.decode('utf-8'))
            return keyboard
        buttons_massive = []
        for layer in self.buttons:
            layer_massive = []
            for button in layer:
                layer_massive.append(self.get_button(button))
            buttons_massive.append(layer_massive)
        keyboard = {
            'resize_keyboard': True,
            'one_time': True,
            'keyboard': self.buttons

        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def get_link(self) -> list:
        button_list = []
        for button_row in self.buttons:
            button_row_list = []
            for button in button_row:
                button_ = {
                    'text': button[0],
                    'url': button[1]
                }
                button_row_list.append(button_)
            button_list.append(button_row_list)
        keyboard = {"inline_keyboard": button_list}
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def get_button(self, text):
        return {'text': text}
