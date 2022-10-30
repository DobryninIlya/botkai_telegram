import json
import random

from ..BotClasses import Command as command_class, traceback
from ..BotClasses import User, Message
from ..BotClasses.Keyboards import keyboard
from ..BotClasses.Stage_handler import Stage
from ..BotClasses.DB_values import Value
from clients.tg.api import TgClient


async def processor(user: User, message: Message, tg_client: TgClient, callback_query=False, stage=None):
    group = user.group_name
    fdigit = group // 1000
    ldigit = group % 100
    mesg = ""
    header = ""
    adress = "\nАдрес: "
    phone = "\nТелефон/факс: "
    mail = "\nE-mail: "
    hours = "\nЧасы работы дирекции: "
    vkid = "\nhttps://vk.com/"
    comm = "\n Беседа: "
    if fdigit == 9:
        header += "ИНСТИТУТ ИНЖЕНЕРНОЙ ЭКОНОМИКИ И ПРЕДПРИНИМАТЕЛЬСТВА"
        adress += "г. Казань, ул. Четаева, 18 (2-е учебное здание КНИТУ-КАИ), к. 423, 439, 442"
        phone += "+7 (843) 231-02-36"
        mail += "ieust@kai.ru"
        hours += "с 9:00 до 17:00"
        vkid += "ieustru" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1dxGifxaEPMPygQVm9qLX"
    elif fdigit == 4:
        if ldigit < 30:
            header += "ИНСТИТУТ КОМПЬЮТЕРНЫХ ТЕХНОЛОГИЙ И ЗАЩИТЫ ИНФОРМАЦИИ"
            adress += " _г. Казань, ул. Б. Красная, 55 (7-е учебное здание КНИТУ-КАИ)_"
            phone += "`+7 (843) 231 16 51`, `+7 (843) 231 00 85`"
            mail += "itki@kai.ru"
            hours += "с 9:00 до 17:00"
            vkid += "dean4" + " (Дирекция)"
            comm += "https://vk.me/join/neDMT9OfwdHc9EpkpWUuRpYvElJT0zffQEU="
        elif ldigit > 30 and ldigit < 50:
            header += "КОЛЛЕДЖ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ"
            adress += " _г. Казань, ул. Большая Красная 55, каб. 116 - 116а,  1 этаж_"
            phone += "`+7 (843) 231-00-00`, `231-00-05`"
            mail += "kit@kai.ru"
            hours += "с 9:00 до 17:00"
            vkid += "kai_kit" + " (Дирекция)"
            comm += "https://vk.me/join/ZvuJKb4XUUv5pKmRQPLZpO25GjR5W9lOSyw="
    elif fdigit == 5:
        header += "ИНСТИТУТ РАДИОЭЛЕКТРОНИКИ И ТЕЛЕКОММУНИКАЦИЙ"
        adress += "_г. Казань, ул. Карла Маркса, 31/7 (5-е учебное здание КНИТУ-КАИ)_"
        phone += """Дневное отделение `+7 (843) 231 59 12`
    Заочное отделение `+7 (843) 231 59 13`"""
        mail += "-"
        hours += "с 9:00 до 17:00"
        vkid += "kai_iret" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d6P6hxYB8ieBeomCDGEL"
    elif fdigit == 3:
        header += "ИНСТИТУТ АВТОМАТИКИ И ЭЛЕКТРОННОГО ПРИБОРОСТРОЕНИЯ"
        adress += "г. Казань, ул. Толстого, 15 (3-е учебное здание КНИТУ-КАИ)"
        phone += """+7 (843) 231 03 94"""
        mail += "dekanat3@mail.ru"
        hours += "с 9:00 до 17:00"
        vkid += "public42139288" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d6qdihb54WBjpLS0foQ9"
    elif fdigit == 2:
        header += "ФИЗИКО-МАТЕМАТИЧЕСКИЙ ФАКУЛЬТЕТ"
        adress += "_г. Казань, ул. Четаева, 18 ​(2-е учебное здание КНИТУ-КАИ)_"
        phone += """декан: `+7 (843) 231 02 04`, `231 16 44`;
    диспетчер: `+7 (843) 231 02 08`;
    факс: `+7 (843) 231 02 08`."""
        mail += "fmf@kai.ru"
        hours += "с 9:00 до 17:00"
        vkid += "kaifmf" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d_DGbRaDtOaV3kNl2GA7"
    elif fdigit == 1:
        header += "ИНСТИТУТ АВИАЦИИ, НАЗЕМНОГО ТРАНСПОРТА И ЭНЕРГЕТИКИ"
        adress += "_г. Казань, ул. Толстого, 15_"
        phone += """`+7 (843) 231 03 98`, `+7 (843) 231 03 20` (веч. отд.)"""
        mail += "iante@kai.ru"
        hours += """с 9:00 до 17:00 (дневное отделение)
    с 15:00 до 19:00 (вечернее и заочное отделение)"""
        vkid += "iante_knrtu_kai" + " Дирекция"
        comm += "https://vk.me/join/AJQ1d/k1ehYuyfxfunfVwa8o"
    elif '569' in str(group):
        mesg = "Информация будет дополнена."

    if header:
        mesg = header + "\n" + adress + phone + mail + hours + vkid + comm
    else:
        mesg = "К сожалению, информация по вашему институту не дополнена. " \
               "Вы можете отправить разработчику сообщение с указанием групп, которые относятся к вашему факультету" \
               "Желательно так же прикрепить информацию об адресе дирекции, контакном телефоне, электронной почте, часы работы" \
               "и ссылку на группу вконтакте"

    await tg_client.send_message(user.id, mesg, parse_mode='Markdown')
    return


command = command_class()

command.keys = ["мой факультет", 'мой институт', 'faculty']
command.process = processor
command.role = [1, 2]
command.payload = ['my_faculty']
