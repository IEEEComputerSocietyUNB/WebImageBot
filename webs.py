# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def searchImage(key):
    keep_url, first_image, second_image = ([], [], [])
    key = key.replace(' ','%20')
    pages = requests.get("http://www.bing.com/images/search?q="+key+"&first=1&cw=1309&ch=915")

    soup = BeautifulSoup(pages.content, 'html.parser')
    a_link = soup.find_all('a')

    for a in a_link:
        if '.gif' in a['href'] or '.jpg' in a['href'] or '.png' in a['href'] or '.jpeg' in a['href'] or '.bmp' in a['href']:
            first_image.append(a['href'])
            print('GOOD LINK = ' + str(a['href']))
        else:
            try:
                find_image_url = requests.get(a['href'])
            except:
                continue
            else:
                if find_image_url.status_code == 200:
                    keep_url.append(find_image_url)

    for url in keep_url:
        second_soup = BeautifulSoup(url.content, 'html.parser')
        links = second_soup.find_all('a')

        for s in links:
            try:
                if ('.gif' in s['href'] or '.jpg' in s['href'] or '.png' in s['href'] or '.jpeg' in s['href'] or '.bmp' in s['href']) and 'https' in s['href']:
                    print('GOOD SECOND LINK = ' + str(s['href']))
            except:
                continue

searchImage('Temple of the Golden Pavilion')
