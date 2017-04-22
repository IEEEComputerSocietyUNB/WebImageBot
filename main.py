# -*- coding: utf-8 -*-
import telepot
import configparser
import requests
from bs4 import BeautifulSoup

COUNT_IMAGE_SEARCH_KEY = {}

def searchImage(key):
    key = key.replace(' ','%20')
    all_good_images, other_good_images, keep_url = ([], [], [])
    pages = requests.get("http://www.bing.com/images/search?q="+key+"&first=1&cw=1309&ch=915")

    soup = BeautifulSoup(pages.content, 'html.parser')
    a_link = soup.find_all('a')

    for a in a_link:
        if '.gif' in a['href'] or '.jpg' in a['href'] or '.png' in a['href'] or '.jpeg' in a['href'] or '.bmp' in a['href']:
            all_good_images.append(a['href'])
        # else:
        #     try:
        #         find_image_url = requests.get(a['href'])
        #     except:
        #         continue
        #     else:
        #         if find_image_url.status_code == 200:
        #             keep_url.append(find_image_url)

    # for url in keep_url:
    #     second_soup = BeautifulSoup(url.content, 'html.parser')
    #     links = second_soup.find_all('a')
    #
    #     for s in links:
    #         try:
    #             if ('.gif' in s['href'] or '.jpg' in s['href'] or '.png' in s['href'] or '.jpeg' in s['href'] or '.bmp' in s['href']) and 'https' in s['href']:
    #                 other_good_images.append(s['href'])
    #                 print('other good image')
    #         except:
    #             continue

    if key in COUNT_IMAGE_SEARCH_KEY.keys():
        if COUNT_IMAGE_SEARCH_KEY[key] >= len(all_good_images):
            COUNT_IMAGE_SEARCH_KEY[key] = 0
        else:
            COUNT_IMAGE_SEARCH_KEY[key] += 1
    else:
        COUNT_IMAGE_SEARCH_KEY[key] = 0

    if len(all_good_images) == 0:
        return []

    print(all_good_images[COUNT_IMAGE_SEARCH_KEY[key]%len(all_good_images)])
    return all_good_images[COUNT_IMAGE_SEARCH_KEY[key]%len(all_good_images)]

def onChatMessage(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        image_url = searchImage(msg['text'])
        if image_url:
            bot.sendPhoto(chat_id=chat_id, photo=image_url)
        else:
            bot.sendMessage(chat_id=chat_id, text="I'm sorry, there is no image to this key.")

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

bot = telepot.Bot(config['DEFAULT']['token'])
bot.message_loop({'chat': onChatMessage,},
                run_forever='Listening ...')
