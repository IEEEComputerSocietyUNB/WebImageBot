# -*- coding: utf-8 -*-
import telepot
import configparser

def onChatMessage(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

bot = telepot.Bot(config['DEFAULT']['token'])
bot.message_loop({'chat': onChatMessage,},
                run_forever='Listening ...')
