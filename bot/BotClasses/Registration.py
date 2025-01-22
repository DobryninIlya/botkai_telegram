import json
import os
import traceback
from cachetools import TTLCache
from datetime import datetime

import aiohttp

from .User import User
from .Message import Message
from .Keyboards import keyboard
from .Database_connection import cursor, connection, cursorR, conn, login_states

status_list = []
BASE_URL_STAFF = "https://kai.ru/for-staff/raspisanie"


async def getGroupsResponse(groupNumber):
    try:
        cursor.execute("SELECT shedule,date_update FROM saved_timetable WHERE groupp = 1")
        result_query = cursor.fetchone()
        result = result_query[0]
        date_update = result_query[1]
        result = json.loads(result)
        for elem in result:
            if int(elem["group"]) == int(groupNumber):
                return elem["id"], date_update
        return False, False
    except:
        return False, False


class Registration:
    def __init__(self, user: User, message: Message, tg_client, debug: bool):

        self.id = user.id
        self.message = message
        self.cursor = cursor
        self.connection = connection
        self.cursorR = cursorR
        self.conn = conn
        self.user = user
        self.user_group_id = None
        self.user_group_name = None
        self.name = ''
        self.login = ''
        self.tg_client = tg_client
        self.debug = debug
        self.subscription_cache = TTLCache(maxsize=1000, ttl=20 * 60)

    def _get_status_code(self):
        sql = "SELECT Status FROM Status WHERE ID = {}".format(self.id)
        self.cursorR.execute(sql)
        result = self.cursorR.fetchone()
        if not result:
            return False
        result = result[0]
        return result

    def _set_status(self, code):
        if not code:
            self.cursorR.execute("DELETE FROM Status WHERE ID={}".format(self.id))
            self.conn.commit()
            return
        try:
            self.cursorR.execute("INSERT INTO Status VALUES ({},{})".format(self.id, code))
        except:
            self.cursorR.execute("UPDATE Status SET Status = {}".format(code))
        finally:
            self.conn.commit()

    async def check_subscription(self):
        if self.debug:
            return True

        # Проверяем, есть ли результат проверки подписки в кэше
        if self.user.id in self.subscription_cache:
            return self.subscription_cache[self.user.id]

        try:
            result = await self.tg_client.get_chat_member(user_id=self.user.id)
            # Обновляем кэш с результатом проверки подписки
            self.subscription_cache[self.user.id] = result['result']['status'] != 'left'
            if result['result']['status'] == 'kicked':
                msg = "Вы были заблокированы за нарушение правил. Если вы считаете, что произошла ошибка, напишите @dobryninilya"
                await self.tg_client.send_message(self.user.id, msg, parse_mode="Markdown")
                return
            return result['result']['status'] != 'left'
        except Exception as e:
            print('Произошла ошибка проверки обязательной подписки:\n', traceback.format_exc(), flush=True)
            return True

    async def processing(self):
        in_base = self._check_in_base()
        if not await self.check_subscription():
            return False, 'Чтобы пользоваться ботом, вам необходимо подписаться на канал! @botkainews', keyboard(
                'registration_role', self.user).get_keyboard()
        if in_base:
            return True, '', keyboard('main_keyboard', self.user).get_keyboard()
        if not in_base:
            status = self._get_status_code()
            if not status or self.message.text.lower() == 'выход':
                self._set_status(1)
                return False, "В моем мире 4 гендера! Выберите вашу роль (Студент, Родитель, Преподаватель, Абитуриент)\n" \
                              "Чтобы узнать больше о ролях введите Справка в чат." \
                              "Помни, неправильное самоопределение может навредить тебе." \
                              "[Недоступно] Также вы можете авторизоваться через личный кабинет (рекомендуется)", keyboard(
                    'registration_role', self.user).get_keyboard()

            if status == 1:
                role = self.message.text.lower()
                if not role in ['студент', 'родитель', 'преподаватель', 'абитуреиент']:
                    return False, "К сожалению, я не понял тебя! Выбери свою роль (Студент, Родитель, Преподаватель, Абитуриент)!", keyboard(
                        'registration_role', self.user).get_keyboard()
                if role == "студент":
                    self._set_status(11)
                    return False, 'Отлично! Теперь введи номер своей группы', keyboard([], self.user).get_keyboard()
                elif role == "преподаватель":
                    self._set_status(21)
                    return False, 'Отлично! Теперь введи свой логин', keyboard([], self.user).get_keyboard()
                else:
                    return False, 'К сожалению, для этой категории регистрация временно закрыта :(. ', keyboard(
                        'registration_role', self.user).get_keyboard()

            if status == 11:
                group = self.message.text
                try:
                    group = int(group)
                    if group < 1000 or group > 100000:
                        raise AssertionError
                    group_id = await self._show_groupId(group)
                    if not group_id:
                        raise TypeError
                except AssertionError:
                    return False, "Ты ввел некорректный номер группы. Повтори ввод номера группы.", keyboard([],
                                                                                                             self.user).get_keyboard()
                except TypeError:
                    return False, "К сожалению, мне не удалось получить параметры твоей группы с сайта...\n" \
                                  "Такое бывает, когда на сайт не добавили твою группу, либо номер группы введен не верно. " \
                                  "Повтори ввод.", keyboard(None, self.user).get_keyboard()
                except:
                    print('Ошибка:\n', traceback.format_exc())
                    return False, "Совсем не могу разобрать что ты ввел! Повтори ввод номера группы.", keyboard('exit',
                                                                                                                self.user).get_keyboard()
                group_id = await self._show_groupId(group)
                self.user_group_id = group_id
                self.user_group_name = group
                return self._save_user(1)

            elif status == 21:
                try:

                    async with aiohttp.ClientSession() as session:
                        async with await session.post(BASE_URL_STAFF, data="prepodLogin=" + self.message.text.lower(),
                                                      headers={'Content-Type': "application/x-www-form-urlencoded"},
                                                      params={
                                                          "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                      timeout=10) as response:
                            response = await response.json(content_type='text/html')
                    if not len(response):
                        return False, 'Расписание для вас отсуствует на сайте. Повторите ввод. Возможно логин введен неверно.', keyboard('exit',
                                                                                                                self.user).get_keyboard()

                    else:
                        self._set_status(22)
                        login_states.append({
                            'id': self.user.id,
                            'login': self.message.text.lower()
                        })
                        return False, 'Введите свою фамилию', keyboard('exit', self.user).get_keyboard()

                except Exception as E:
                    return False, 'Рсаписание для вас отсутствует, либо данные некорректны', keyboard('exit', self.user).get_keyboard()
            elif status == 22:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with await session.post(
                        'https://kai.ru/for-staff/raspisanie?p_p_id=pubLecturerSchedule_WAR_publicLecturerSchedule10&p_p'
                        '_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getLecturersURL&p_p_cacheability='
                        'cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&query='+self.message.text.lower(),
                                headers={'Content-Type': "application/x-www-form-urlencoded"},
                                timeout=15) as response:
                            response = await response.json(content_type='text/html')

                    if not len(response):
                        return False, "Расписание для вас отсутствует на сайте. Повторите ввод фамилии.", keyboard('exit', self.user).get_keyboard()
                    else:
                        login = ''
                        for l in login_states:
                            if l['id'] == self.user.id:
                                login = l['login']
                                login_states.remove(l)
                                break
                        name = ""
                        for row in response:
                            if row["id"].rstrip().lower() == login.rstrip().lower():
                                name = row["lecturer"]
                                self.user.name = name
                                self.login = login
                                self._set_status(None)
                                return self._save_user(2)
                        if not name:
                            self._set_status(21)
                            return False, "Совпадения не найдены. Повторите ввод. \nВведите логин без лишних символов.", keyboard(
                                'exit', self.user).get_keyboard()


                except Exception as E:
                    print('Ошибка:\n', traceback.format_exc(), flush=True)
                    return False

        return False, "[регистрация]: Произошла ошибка :( Отправь скрин разработчику <З", keyboard('registration_role',
                                                                                                   self.user).get_keyboard()

    def _save_user(self, role_id):
        sql = ''
        if role_id == 1:
            sql = "INSERT INTO tg_users VALUES ({id}, '{name}', '{lastname}', '{username}', {role}, {admLevel}, {is_verificated}, {groupname}, {groupid})".format(
                id=self.id,
                name=self.user.name.replace("'", "''"),
                lastname=self.user.lastname.replace("'", "''"),
                username=self.user.username,
                role=role_id,
                admLevel=0,
                is_verificated=False,
                groupname=self.user_group_name,
                groupid=self.user_group_id
            )
        elif role_id == 2:
            sql = "INSERT INTO tg_users VALUES ({id}, '{name}', '{lastname}', '{username}', {role}, {admLevel}, {is_verificated}, {groupname}, {groupid}, '{login}')".format(
                id=self.id,
                name=self.name,
                lastname='',
                username=self.user.username,
                role=role_id,
                admLevel=0,
                is_verificated=False,
                groupname=0,
                groupid=-1,
                login=self.login
            )
            self.user.role = 2
        try:
            self._execute(sql)
            self._set_status(None)
            return False, 'Крутотень! Теперь ты можешь пользоваться ботом!', keyboard('main_keyboard',
                                                                                      self.user).get_keyboard()
        except:
            print('Ошибка:\n', traceback.format_exc())
            return False, "[регистрация]: Произошла ошибка :( Отправь скрин разработчику <З", keyboard(
                'registration_role', self.user).get_keyboard()

    def _execute(self, sql_query):
        self.cursor.execute(sql_query)
        self.connection.commit()
        return cursor

    def _check_in_base(self):
        sql = "SELECT * FROM tg_users WHERE id={}".format(self.id)
        result = self._execute(sql).fetchall()
        if result:
            return True
        else:
            return False

    async def _show_groupId(self, groupNumber):
        BASE_URL = 'https://schedule-bot.kai.ru/api/schedule_public/groups?token=' + os.getenv('SCHEDULE_BOT_TOKEN')
        try:
            async with aiohttp.ClientSession() as session:
                async with await session.get(BASE_URL) as response:
                    response = await response.json(content_type='text/plain')
            for elem in response['result']['groups']:
                if elem["groupNum"] == str(groupNumber):
                    return elem["id"]
            return False
        except aiohttp.ServerConnectionError:
            return False, "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным."
        except (ConnectionError, TimeoutError, aiohttp.ServerTimeoutError, aiohttp.ServerConnectionError):
            group, _ = await getGroupsResponse(groupNumber)
            if group:
                return group
            return False, "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным."
        except:
            group, _ = await getGroupsResponse(groupNumber)
            if group:
                return group
            print('Ошибка:\n', traceback.format_exc())
            return False
