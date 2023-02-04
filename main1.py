from config.telegram_config.TOKEN_telegram import TOKEN
from parsing_lalafo1 import main
import telebot
import asyncio
import time


bot = telebot.TeleBot(TOKEN, parse_mode=None)
name_channel = '@akkondiokm'  # здесь указывается группа
proverka = {'NEW_URl': None}

while True:
    get_lalafo = asyncio.run(main())
    if proverka.get('NEW_URl') != get_lalafo['URL_INTERNAL']:
        bot.send_message(name_channel, 
        f'''📌Название: {get_lalafo['title']}\n'''
        f'''🔎Адрес: {get_lalafo['adress']}\n'''
        f'''💰Цена: USD {get_lalafo['price']}\n'''
        f'''✍Описание: {get_lalafo['description']}\n'''
        f'''Фото: {get_lalafo['image_urls']}\n'''
        f'''Ссылка на обьявление: {get_lalafo['URL_INTERNAL']}\n'''
        )
        proverka['NEW_URl'] = get_lalafo['URL_INTERNAL']
    time.sleep(10)
