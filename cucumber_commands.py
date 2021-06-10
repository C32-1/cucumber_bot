import datetime
import json
import random
from multiprocessing import Pool
import requests
import bs4
from timeit import default_timer as timer

command_list = 'кликуха погода привет помощь стих'.split()

const_api_key = '65de895f37ea08ee2a9c4d856de58897'

req = requests.get('http://www.gr-oborona.ru/pub/rock/egor_letov_stihi.html')
bsoup = bs4.BeautifulSoup(req.content, 'html.parser')

class commands(object):


    @staticmethod
    def command_punkname():
        with open('nicks.txt', 'r', encoding='utf-8') as k:
            nicks = k.readlines()
        with open('names.txt', 'r', encoding='utf-8') as n:
            names = n.readlines()
        return '{0} {1}'.format(random.choice(names).replace('\n', ''), random.choice(nicks).replace('\n', ''))

    @staticmethod
    def command_weather(city):

        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={const_api_key}'

            data = requests.get(url).json()

            temp = data['main']['temp']

            r_name = data['name']

            region = data['sys']['country']

            speed = data['wind']['speed']

            condition = data['weather'][0]['main']

            message_string = f'Погода в {r_name} {datetime.datetime.utcnow()} ' \
                             f'\n Страна: {region} ' \
                             f'\n Температура: {round(int(temp))} C ' \
                             f'\n Состояние: {condition} ' \
                             f'\n Скорость ветра: {speed} км/ч'
            return message_string
        except Exception:
            return 'Город не найден!'

    @staticmethod
    def command_help():
        output = ''
        for j in range(0, len(command_list)):
            output += '\n' + command_list[j]
        return 'Список комманд: {0}'.format(output)

    @staticmethod
    def command_p():
        elements_pre = bsoup.find_all('pre')
        return random.choice(elements_pre[1:])

class need(object):

    def __init__(self, user_name):
        self.user_name = user_name

    async def get_name(self):
        return
