import json
import datetime as dt
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
    ["На сегодня", "На послезавтра", "По дням"],
    ["Четность недели", "Полностью"],
    ["Разное", "Преподаватели"],
    ["Обратная связь", "Донат", "Профиль"]
]

main_keyboard_teacher = [
    ["На завтра"],
    ["На сегодня", "На послезавтра"],
    ["Четность недели", "Полностью"],
    ["Обратная связь", 'Сбросить регистрацию']

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
    [['Моя группа', 'groupchange']],
    # [['Мои задания', 'my_task']],
    [['Поддержать проект', 'donate']],
    [['Ссылки на одногруппников', 'classmates_links']],
    [['Студенты группы', 'classmates_list']],
    [['Изменения в расписании ', 'notifier_change_menu']],
    [['Мой институт', 'my_faculty']]  # , ['Подписки', 'subscriptions']],
    # [['{}', 'starosta']]
]

feedback_create = [[['Продолжить', 'feedback_create']]]

exit = [['Выход']]
exit_inline = [[['Выход', 'main_menu']]]


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

other_functions = [
    [['Экспорт в календарь', 'export_ics']],
    [['Word документ', 'export_word']],
    [['График посещения занятий (для старосты)', 'export_control']],
    [['Баллы БРС', 'score_raiting']],
    [['Сбросить регистрацию', 'reset_role']]
]

reset_role_commit = [
    [['Продолжить', 'reset_role_commit']]
]

coworking_main = [
    [['Моя бронь', 'coworking_rent_my']],
    [['Бронировать', 'coworking_rent']],
    [['Провести мероприятие', 'coworking_rent_event']],
    [['Выход', 'coworking_main']]
]

coworking_staff = [
    [['Одобрить заявки', 'coworking_accept']],
    [['бронь СЕГОДНЯ', 'coworking_today']],
    [['бронь ЗАВТРА', 'coworking_tomorrow']],
    [['бронь НЕДЕЛЯ', 'coworking_week']],
    [['Выход', 'coworking_staff']]
]

coworking_rent_accept = [
    [['Одобрить', 'rent_accept']],
    [['Отклонить', 'rent_decline']],
    [['Выход', 'coworking_staff']]
]
week_shedule = [
    [['Понедельник', 'shed_week', 1], ['Вторник', 'shed_week', 2], ['Среда', 'shed_week', 3]],
    [['Четверг', 'shed_week', 4], ['Пятница', 'shed_week', 5], ['Суббота', 'shed_week', 6]],

]

notifyer_change = [
    [['Изменить', 'notifier_change']]
]

notifyer_change_UPDATER_SCRIPT = [
    [['Оповещения', 'notifier_change_menu']]
]


def get_near_dates(days=7) -> [[[]]]:
    result = []
    datetime = dt.datetime.now()
    datetime += dt.timedelta(days=1)

    for day in range(days):
        while datetime.weekday() in [5,6]:
            datetime += dt.timedelta(days=1)

        result.append([[datetime.strftime("%a:%d-%m-%Y"), 'coworking_setdate', str(datetime.strftime("%Y-%m-%d"))]])
        datetime += dt.timedelta(days=1)
    result.append([['Выход', 'main_menu']])
    return result

def get_near_time(start=9, stop=16) -> [[[]]]:
    result = []
    datetime = dt.datetime.now()
    datetime += dt.timedelta(days=1)

    for day in range(start, stop+1):
        day = str(day)
        if len(day) == 1:
            day = "0"+day
        result.append([[day, 'coworking_settime', day]])
    result.append([['Выход', 'main_menu']])
    return result

def get_near_time_minute() -> [[[]]]:
    result = []
    datetime = dt.datetime.now()
    datetime += dt.timedelta(days=1)

    for day in range(0, 6):
        day *=10
        day = str(day)
        if len(day) == 1:
            day = "0"+day
        result.append([[day, 'coworking_rent_time_minute', day]])
    result.append([['Выход', 'main_menu']])
    return result

class keyboard:
    def __init__(self, type_name: str, user: User, buttons: list = None, payload=None):
        self.type_name = type_name
        self.buttons = []
        self.user = user
        if self.type_name == 'main_keyboard':
            if self.user.role == 2:  # препод
                self.buttons = main_keyboard_teacher
            else:  # студент
                self.buttons = main_keyboard

        elif self.type_name == 'exit':
            self.buttons = exit
        elif self.type_name == 'exit_inline':
            self.buttons = exit_inline
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
        elif self.type_name == 'other_functions':
            self.buttons = other_functions
        elif self.type_name == 'reset_role_commit':
            self.buttons = reset_role_commit
        elif self.type_name == 'coworking_main':
            self.buttons = coworking_main
        elif self.type_name == 'coworking_rent_date':
            self.buttons = get_near_dates()
        elif self.type_name == 'coworking_rent_time':
            self.buttons = get_near_time()
        elif self.type_name == 'coworking_rent_time_minute':
            self.buttons = get_near_time_minute()
        elif self.type_name == 'coworking_staff':
            self.buttons = coworking_staff
        elif self.type_name == 'coworking_rent_accept':
            self.buttons = coworking_rent_accept
            self.buttons[0][0].append(payload)
            self.buttons[1][0].append(payload)
        elif self.type_name == 'week_shedule':
            self.buttons = week_shedule
        elif self.type_name == 'notifier_change':
            self.buttons = notifyer_change
        elif self.type_name == 'notifyer_change_UPDATER_SCRIPT':
            self.buttons = notifyer_change

    def get_profile(self):
        self.profile = profile
        # self.profile[0][0][0] = self.profile[0][0][0].format(self.user.group_name)
        return self.profile

    def get_inline_keyboard(self) -> dict:
        button_list = []
        for button_row in self.buttons:
            button_row_list = []
            for button in button_row:
                callback_data = "{" + f'"button":"{button[1]}","data":"{button[-1]}"' + "}"
                button_ = {
                    'text': button[0],
                    'callback_data': callback_data
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
