#https://delaney.gitbook.io/create-telegram-bot/

import telebot
import requests
import time
from dictionary import dictionary, future_db, full_db, cities
from bs4 import BeautifulSoup
from threading import Thread

TOKEN = '1618872853:AAGlohngJ9dmX5jHjbR7xbpjimG16B-m8EM'
bot = telebot.TeleBot(TOKEN)

def delete(messagecall):
    bot.edit_message_reply_markup(messagecall.message.chat.id, messagecall.message.message_id)
    bot.delete_message(messagecall.message.chat.id, messagecall.message.id)

def send(messagecall, text, reply_markup):
    bot.send_message(messagecall.chat.id, text, None, None, reply_markup)

def numstrip(num):
    listed = list(num)
    for i in listed:
        if i in ' ,.':
            listed.remove(i)
    return(''.join(listed))

def translit(text):
    x = list(text)
    y = []
    for i in x:
        y.append(dictionary[i])
    return(''.join(y))


back1 = telebot.types.InlineKeyboardMarkup()
back1.add (telebot.types.InlineKeyboardButton(text='Назад', callback_data=1))

back2 = telebot.types.InlineKeyboardMarkup()
back2.add (telebot.types.InlineKeyboardButton(text='Назад', callback_data=3))

keyboard1 = telebot.types.InlineKeyboardMarkup()
keyboard1.add(telebot.types.InlineKeyboardButton(text='Добавить новое объявление', callback_data=2))
keyboard1.add(telebot.types.InlineKeyboardButton(text='Мои объявления', callback_data=3))

keyboard2 = telebot.types.InlineKeyboardMarkup()
keyboard2.add(telebot.types.InlineKeyboardButton(text='Циан', callback_data=4))
keyboard2.add(telebot.types.InlineKeyboardButton(text='Авито', callback_data=5))
keyboard2.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=1))

keyboard3 = telebot.types.InlineKeyboardMarkup()
keyboard3.add(telebot.types.InlineKeyboardButton(text='Да', callback_data=6))
keyboard3.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data=5))


#разобраться с markup и remove
savehandler = 0
urls = []
#добавить конструкторы для клавиатур

#board = types.InlineKeyboardMarkup()
#cancel = types.InlineKeyboardButton(text="Отмена", callback_data="Отмена")
#board.add(cancel)


@bot.message_handler(commands=['start'])
def start_message(message):

    send(message,
                    'Привет, я - тестовый парсер объявлений с ЦИАН и Авито. '
                    'Я очень быстрый и вместе с тем бесплатный. \n\n'
                    'Но это до тех пор, пока Саше не нужно держать сервер. '
                    'Парсер будет работать пока работает его камплюктер. \n\n'
                    'Не бойся, все твои данные сохранятся. '
                    'Как только я вновь запущусь, тебе придут новые объявления. \n\n', None)

    send(message, 'Напиши кодовое слово', None)

#подумать как можно завернуть это в ооп, мб абстрактный класс? idk надо приводить код в норм вид

#полезные ссылки по хэндлеру:
#https://stackoverflow.com/questions/45405369/pytelegrambotapi-how-to-save-state-in-next-step-handler-solution
#https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py - ОЧЕНЬ ПОЛЕЗНО


@bot.message_handler(content_types=['text'])
def check_code(message):
    global savehandler
    if message.text.lower() == 'истфак':
        send(message, 'Добро пожаловать!', keyboard1)
        if not message.chat.id in full_db:
            full_db[str(message.chat.id)] = {}
    elif message.text.lower() in cities and savehandler == 1:
        savehandler -= 1
        future_db['город'] = save_city(message)
    elif savehandler == 2:
        savehandler -= 2
        future_db['поиск'] = save_search(message)
    elif savehandler == 3:
        savehandler -= 3
        future_db['мин'] = min_search(message)
    elif savehandler == 4:
        savehandler -= 4
        future_db['макс'] = max_search(message)
        global urls
        urls.append(linkget(message))
    elif savehandler == 5:
        savehandler -= 5
        full_db[str(message.chat.id)][message.text] = future_db
        print(full_db)
        send(message, 'Добро пожаловать!', keyboard1)
    else:
        send(message, 'Не понимаю', None)

@bot.callback_query_handler(func=lambda call: True)
def main_menu(call):

    delete(call)
    if call.data == '1':
        send(call.message, 'Добро пожаловать!', keyboard1)
    elif call.data == '2':
        send(call.message, 'Выбери площадку', keyboard2)
    elif call.data == '3':
        send(call.message, 'Выбери объявление среди списка:', keyboard2)
    elif call.data == '4':
        send(call.message, 'Циан', back2)
    elif call.data == '5':
        send(call.message, 'Авито', back2)
        send(call.message, 'город', None)
        global savehandler
        savehandler += 1
    elif call.data == '6':
        send(call.message, 'название объявления', None)
        savehandler += 5
    else:
        send(call.message, 'ну и что', None)


def save_city(message):
    print(message.text)
    send(message, 'что ищем?', None)
    global savehandler
    savehandler += 2
    return (translit(message.text.lower()))

def save_search(message):
    print(message.text)
    send(message, 'укажи минималку', None)
    global savehandler
    savehandler += 3
    return ('+'.join(message.text.lower().split(' ')))

def min_search(message):
    print(message.text)
    send(message, 'укажи максималку', None)
    global savehandler
    savehandler += 4
    return(numstrip(message.text))

def max_search(message):
    print(message.text)
    return(numstrip(message.text))

def linkget(message):
    global link
    link = f'https://www.avito.ru/{future_db["город"]}?pmax={future_db["макс"]}&pmin={future_db["мин"]}&q={future_db["поиск"]}&s=104'
    send(message, f'Все ок?\n{link}', keyboard3)
    return(link)

def url(page_url):
    print(requests.get(page_url).text)
    return requests.get(page_url).text

##parsed = 'avito.ru'
#def parsing(url = url(urls[0])):
 #   while True:
  #      for i in range(10):
   #         print('jopa')
    #        soup = BeautifulSoup(url, 'lxml')
     #       linkss = soup.find('div', attrs={'class': 'iva-item-titleStep-2bjuh'})
       #     linksss = linkss.find('a')
      #      x = f'avito.ru{linksss.get("href")}'
     #       global parsed
    #        if not parsed == x:
   #             parsed = x
  #          print (parsed)
 #       time.sleep(1)


#def bots():
#    bot.polling()

#p1 = Thread(target=bots)
#p2 = Thread(target=parsing)
#if __name__ == '__main__':
#    p1.start(), p2.start()
#    p1.join(), p2.join()
bot.polling()
#https://pocketadmin.tech/ru/telegram-bot-%D0%BD%D0%B0-python/

#regexp походу позволяет разграничить!

#@bot.message_handler(content_types=['text'], func=lambda message: message.text.lower() == "получить ключ")