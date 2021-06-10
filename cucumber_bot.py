import json
import random
import time

import requests
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cucumber_commands import commands, command_list
import bs4
from timeit import default_timer as timer

class bot_main(object):

    def __init__(self, chat_id):
        self.chat_id = chat_id

    @staticmethod
    def get_vk_token(flag=True):
        if flag is True:
            with open('config.json', 'r') as f:
                data = json.load(f)
            token = data['token']
            f.close()
            return token
        else:
            return 'none'

    @staticmethod
    def cucumber_auth():
        auth = vk_api.VkApi(token=bot_main.get_vk_token(flag=True))
        return auth

    @staticmethod
    def msg_write(chat_id, msg):
        bot_main.cucumber_auth().method('messages.send', {'chat_id': chat_id, 'message': msg, 'random_id': get_random_id()})

    @staticmethod
    def arg_split(text):
        return text.split()[1:]

    @staticmethod
    def on_msg(message):
        message = message.lower()

        if message == command_list[0]:
            return commands.command_punkname()

        if message == '{0} {1}'.format(command_list[1], ' '.join(bot_main.arg_split(message))):
            city = ' '.join(bot_main.arg_split(message))
            return commands.command_weather(city=city)

        if message == command_list[2]:
            return 'чё приветкаешь?'

        if message == command_list[3]:
            return commands.command_help()

        if message == command_list[4]:
            return commands.command_p()

def main():

    lp = VkBotLongPoll(bot_main.cucumber_auth(), group_id=197949409)
    vk = bot_main.cucumber_auth().get_api()

    try:
        for event in lp.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                try:
                    rm = event.message.get('text')
                    sender = event.chat_id
                    bot_main.msg_write(sender, bot_main.on_msg(rm))
                except vk_api.ApiError:
                    pass
    except requests.exceptions.ReadTimeout:
        print('Connection error!')
        main()


if __name__ == '__main__':
    main()