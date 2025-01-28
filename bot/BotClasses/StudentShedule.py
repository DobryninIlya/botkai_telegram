import os
import traceback

import aiohttp, asyncio
import datetime
import json
import re
from pprint import pprint
from .User import User
from .Message import Message
from .Database_connection import cursor, connection, cursorR, conn
from clients.tg.api import TgClient

domain = 'https://schedule-bot.kai.ru'
schedule_path = '/api/schedule_public/'

class StudentShedule:
    def __init__(self, user: User, message: Message, tg_client: TgClient):
        self.user = user
        self.tg_client = tg_client
        self.group_id = user.group_id
        self.BASE_URL = 'https://kai.ru/raspisanie'
        self.today = datetime.date.today()
        self.chetn = int(os.getenv("CHETN"))

    async def alert_for_differences(self, groupname: str, diff: str):
        sql = "SELECT id FROM tg_users WHERE groupname={}".format(groupname)
        cursor.execute(sql)
        result = cursor.fetchall()
        diff += "\n*Изменения уже сохранены.*"
        for elem in result:
            try:
                res = await self.tg_client.send_message(elem[0], diff, parse_mode=True)
                print(res)
            except:
                print('Ошибка:\n', traceback.format_exc(), flush=True)

    async def timetable_differences(self, old: list, new: list):
        week_elements = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота',
            '7': 'Воскресенье',
        }
        if old != new:
            result = "*Обратите внимание!* \nИзменения в вашем расписании:\n"
            for day in sorted(new.keys()):
                try:
                    if new[day] != old[day]:
                        for lesson in new[day]:
                            if lesson not in old[day]:
                                result += "*(+)*:: `{dayNum}| [{daytime}] {daydate} {disciplname}`\n".format(
                                    dayNum=week_elements[lesson['dayNum']],
                                    daytime=lesson['daytime'].rstrip(),
                                    daydate=lesson['daydate'].rstrip(),
                                    disciplname=lesson['disciplname'].rstrip()
                                )
                except KeyError:
                    print("Ошибка в триггере обновления расписания. День:", day, flush=True)
                    continue
            await self.alert_for_differences(self.user.group_name, result)
            return

    async def   _get_response(self, group_id):
        try:
            async with aiohttp.ClientSession() as session: # + os.getenv('SCHEDULE_BOT_TOKEN')
                async with await session.get(domain+schedule_path+str(group_id) + "?token=" + os.getenv('SCHEDULE_BOT_TOKEN')) as response:
                    text = await response.text()
                    response_json = json.loads(text)
            return True, response_json
        except ConnectionError as err:
            return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        except aiohttp.ServerTimeoutError as err:
            return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        except:
            print('Ошибка:\n', traceback.format_exc())
            return False, "&#9888;Произошла непредвиденная ошибка :( &#9888;"
        # sql = "SELECT * FROM saved_timetable WHERE groupp={}".format(self.group_id)
        # cursor.execute(sql)
        # result = cursor.fetchone()
        # if result == None or result[2]=='{}':
        #     return False, "Расписание не найдено. Если вы уверены, что оно есть - напишите t.me/dobryninilya"
        # if result == None or result[2]=='{}':
        #
        #     try:
        #         async with aiohttp.ClientSession() as session:
        #             async with await session.post(self.BASE_URL, data="groupId=" + str(self.group_id),
        #                                           headers={'content-Type': "application/x-www-form-urlencoded; charset=UTF-8"},
        #                                           params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
        #                                                   "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}) as response:
        #                 response = await response.json(content_type='text/html')
        #         if not response:
        #             return False, "Расписание не найдено"
        #         try:
        #             sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(self.group_id, datetime.date.today(),
        #                                                                                json.dumps(response))
        #             cursor.execute(sql)
        #             connection.commit()
        #         except:
        #             sql = "UPDATE saved_timetable SET shedule = '{}', date_update='{}' WHERE groupp ={}".format(json.dumps(response),
        #                                                                                datetime.date.today(), self.group_id)
        #             cursor.execute(sql)
        #             connection.commit()
        #         return True, response
        #     except ConnectionError as err:
        #         return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        #     except aiohttp.ServerTimeoutError as err:
        #         return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        #     except:
        #         print('Ошибка:\n', traceback.format_exc())
        #         return False, "&#9888;Произошла непредвиденная ошибка :( &#9888;"
        # else:
        #     date_update = result[1]
        #     timetable = result[2]
            # if date_update + datetime.timedelta(days=2) < self.today: # Если старое, то обновить и вернуть
            #
            #     try:
            #         async with aiohttp.ClientSession() as session:
            #             async with await session.post(self.BASE_URL, data="groupId=" + str(self.group_id),
            #                                           headers={'Content-Type': "application/x-www-form-urlencoded"},
            #                                           params={
            #                                               "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            #                                               "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
            #                                           timeout=3) as response:
            #                 if response.status != 200:
            #                     return True, json.loads(timetable)
            #                 print(await response.text())
            #                 response = await response.json(content_type='text/html')
            #                 print(response)
            #
            #         assert json.dumps(response), "Расписание имеет некорректную форму"
            #         await self.timetable_differences(json.loads(timetable), response)
            #         sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupname = {}".format(
            #             json.dumps(response), datetime.date.today(), self.group_id)
            #         cursor.execute(sql)
            #         connection.commit()
            #         return True, response
            #     except asyncio.exceptions.TimeoutError:
            #         print("Ошибка таймаута в расписании", flush=True)
            #     except:
            #         print('Ошибка (расписание):\n', traceback.format_exc(), flush=True)
            #         return True, json.loads(timetable)
            # else:
            # return True, json.loads(timetable)

    def _get_week_shedule(self, response):
        week_elements = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота',
            '7': 'Воскресенье',
        }
        result = ''
        schedule = response
        try:
            for daynum in sorted(week_elements.keys()):
                print(daynum)
                day_schedule = [entry for entry in schedule if entry.get("daynum", "") == daynum]
                if not day_schedule:
                    continue
                result += "═──────{}{}────═\n".format(week_elements[daynum], '─' * (11 - len(week_elements[daynum])) if len(
                    week_elements[daynum]) < 11 else '')
                for para in day_schedule:
                    if '---' in (para.get("auditory", "")).rstrip():  # Экранирование множественных тире
                        para["auditory"] = "--"
                    if '---' in (para.get("building", "")).rstrip():
                        para["building"] = "--"
                    para_structure = {
                        'daydate': para.get("daydate", "")[:100].rstrip(),
                        'disciplname': (para.get("disciplname", "")).rstrip(),
                        'auditory': para.get("auditory", "").rstrip(),
                        'building': para.get("building", "").rstrip(),
                        'daytime': para.get("daytime", "")[:5].rstrip(),
                        'discipltype': para.get("discipltype", "")[:4].rstrip()
                    }
                    result += "➤ *{daydate} ⌛{daytime} {discipltype}* _{disciplname}_ {auditory} {building}зд. \n".format(
                        daydate=para_structure['daydate'],
                        discipltype=para_structure['discipltype'],
                        disciplname=para_structure['disciplname'],
                        auditory=para_structure['auditory'],
                        building=para_structure['building'],
                        daytime=para_structure['daytime']
                    )
        except:
            print('Ошибка:\n', traceback.format_exc())
        return result

    def _get_teacher_list(self, response):
        prepodList = []
        resultList = []
        prepodElement = {'discipltype': None, 'disciplname': None,
                         'prepodfio': None}
        for elem in response:
            prepodElement = {'discipltype': elem.get("discipltype", "").rstrip(),
                             'disciplname': elem.get("disciplname", "").rstrip(),
                             'prepodfio': elem.get("prepodfio", "").rstrip()}
            if elem.get("prepodfio", "").rstrip() == "":
                prepodElement['prepodfio'] = ":не-задан:"
            prepodList.append(prepodElement)
        prepodList.sort(key=lambda prepodElement: (prepodElement['disciplname'], prepodElement['prepodfio']))
        i = 0
        for prepod in prepodList:
            discipltype = []
            discipltype.append(prepod['discipltype'])
            try:
                while prepod['prepodfio'] == prepodList[i + 1]['prepodfio']:
                    if prepodList[i + 1]['discipltype'] not in discipltype:
                        discipltype.append(prepodList[i + 1]['discipltype'])
                    prepodList.pop(i)
            except:
                pass
            i += 1
            if discipltype:
                st = ""
                for discipl in discipltype:
                    st += str(discipl).rstrip() + ", "
                st = st[:-2]
                prepod['discipltype'] = st
            res = "👨‍🏫 |" + str(prepod['discipltype']) + "| *" + (
                str(prepod['disciplname'])).rstrip() + "* \n`" + str(prepod['prepodfio']).title() + "`"
            if res not in resultList:
                resultList.append(res)
        result = ''
        for row in resultList:
            result += "\n---------------------------------------------------\n" + row
        return result

    async def showTimetable(self, groupId: int, tomorrow=0):
        try:

            isNormal, response = await self._get_response(groupId)
            schedule = response['result']['schedule']
            if not isNormal:
                return response
            if tomorrow == -1:
                return self._get_week_shedule(schedule)  # Расписание по дню недели
            elif tomorrow == -2:
                return self._get_teacher_list(schedule)  # Список преподов
            elif tomorrow == -3:
                print(self.today.isocalendar()[1] + self.chetn % 2)
                return True if (int(self.today.isocalendar()[1] + self.chetn) % 2) == 0 else False  # Четность недели
            now = datetime.date.today() + datetime.timedelta(days=tomorrow)
            response = find_elements_by_daynum(schedule, str(datetime.date(now.year, now.month, now.day).isoweekday()))
            result = ''
            month = now.month
            if month < 10:
                month = "0" + str(month)
            day = str(now.day) + "." + str(month)
            para_list = []
            for elem in response:
                daydate = elem.get("daydate", "").rstrip()

                if '---' in (elem["auditory"]).rstrip():  # Экранирование множественных тире
                    elem["auditory"] = "-нет-"
                if '---' in (elem["building"]).rstrip():
                    elem["building"] = "-нет-"

                para_structure = {
                    'daydate': elem.get("daydate", "")[:100].rstrip(),
                    'disciplname': elem.get("disciplname", "").rstrip(),
                    'auditory': elem.get("auditory", "").rstrip(),
                    'building': elem.get("building", "").rstrip(),
                    'daytime': elem.get("daytime", "")[:5].rstrip(),
                    'discipltype': elem.get("discipltype", "")[:4].rstrip()
                }
                dateinstr = str((elem.get("daydate", "")).rstrip()).find(day)
                # print((self.today.isocalendar()[1] + self.chetn) % 2, self.today.isocalendar()[1])
                if ((now.isocalendar()[1] + self.chetn) % 2) == 0:  # Если неделя четная
                    chetn = True
                else:
                    chetn = False
                if daydate == 'чет' and chetn:
                    para_list.append(para_structure)
                elif daydate == 'неч' and not chetn:
                    para_list.append(para_structure)
                elif daydate == 'чет\неч' and chetn or daydate == 'неч\чет' and not chetn:
                    para_structure['daydate'] = "1️гр. " + para_structure['daydate']
                    para_list.append(para_structure)
                elif daydate == 'неч\чет' and chetn or daydate == 'чет\неч' and not chetn:
                    para_structure['daydate'] = "2️гр. " + para_structure['daydate']
                    para_list.append(para_structure)
                elif dateinstr != -1:
                    para_structure['daydate'] = f"{day} "
                    para_list.append(para_structure)
                else:
                    # Если содержит дату, то переходим к следующему
                    regex = r"\d{2}\.\d{2}"
                    if re.search(regex, daydate):
                        continue
                    # No sorted, but can view
                    if daydate not in ['чет', 'неч', 'чет\неч', 'неч\чет'] and dateinstr == -1:
                        para_list.append(para_structure)
            for para in para_list:
                result += "➤ *{daydate} ⌛{daytime} {discipltype}* _{disciplname}_ {auditory} {building}зд. \n".format(
                # result += "➤ {daydate} ⌛{daytime} {discipltype} {auditory} {building}зд.```\n{disciplname}``` \n".format(
                    daydate=para['daydate'],
                    discipltype=para['discipltype'],
                    disciplname=para['disciplname'],
                    auditory=para['auditory'],
                    building=para['building'],
                    daytime=para['daytime']
                )
            return result
        except ConnectionError:
            return "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        except aiohttp.ServerTimeoutError:
            return "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        except KeyError:
            return False
        except:
            print('Ошибка:\n', traceback.format_exc())
            return ""

def find_elements_by_daynum(response, daynum):
    return [elem for elem in response if elem.get("daynum") == daynum]
