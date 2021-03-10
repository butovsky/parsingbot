
import telebot
import requests
import time
from dictionary import dictionary, future_db, full_db, cities
from bs4 import BeautifulSoup
from threading import Thread
import sqlite3

#мне кажется если привлечь ооп то код станет чище и лучше
#idk надо что то делать - займусь позже, работает и уже замечательно, и всего то на 250 строк

dbconnect = sqlite3.connect('parser.db', check_same_thread=False)
dbcursor = dbconnect.cursor()
dbcursor.execute("""CREATE TABLE IF NOT EXISTS user_id(
        id text NOT NULL PRIMARY KEY,
        UNIQUE(id)); """)
dbconnect.commit()

TOKEN = '1671579913:AAEVSxlFYnWLj9P9YPfQLwzV4vHRaXpTR_U'
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

keyboardmain = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardmain.row('Главное меню')

keyboard1 = telebot.types.InlineKeyboardMarkup()
keyboard1.add(telebot.types.InlineKeyboardButton(text='Добавить новое объявление', callback_data=2))
keyboard1.add(telebot.types.InlineKeyboardButton(text='Мои объявления', callback_data=3))


keyboard3 = telebot.types.InlineKeyboardMarkup()
keyboard3.add(telebot.types.InlineKeyboardButton(text='Да', callback_data=6))
keyboard3.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data=5))

savehandler = 0
#добавить конструкторы для клавиатур


@bot.message_handler(commands=['start'])
def start_message(message):

    send(message,
                    'Привет, я - тестовый парсер объявлений с Авито. '
                    'Я очень быстрый и вместе с тем бесплатный. \n\n'
                    'Но это до тех пор, пока Саше не нужно держать сервер. '
                    'Парсер будет работать, пока работает его компьютер. \n\n'
                    'Не бойся, все твои данные сохранятся. '
                    'Как только я вновь запущусь, тебе придут самые свежие объявления. \n\n', None)

    send(message, 'Напиши кодовое слово', None)


@bot.message_handler(content_types=['text'])
def check_code(message):
#savehandler - это мой путь решения проблемы хендлера по тексту: он всего один, а сценариев должно быть несколько, скорее всего он не совсем удобен если сценариев не 10 а 100, требует доработки - однако для тестового проекта пока сгодится
    global savehandler
#сделал что то вроде кодового слова, вместо него можно все написанное ниже сразу передать в хендлер по команде /start
    if message.text.lower() == 'истфак':
        send(message, 'добро пожаловать!', keyboard1)
        send(message, 'выбери пункт в меню, чтобы продолжить', keyboardmain)
        dbcursor.execute("""CREATE TABLE IF NOT EXISTS """ + f'id{str(message.chat.id)}' + """(
        name text NOT NULL PRIMARY KEY,
        city text NOT NULL,
        search text NOT NULL,
        min integer,
        max integer,
        link text NOT NULL,
        last text NOT NULL); """)
        dbcursor.execute("""REPLACE INTO user_id(id) VALUES(?); """, [str(message.chat.id)])
        dbconnect.commit()

    elif message.text.lower() == 'главное меню':
        send(message, 'добро пожаловать!', keyboard1)

    elif savehandler == 1:
        savehandler += 1
        full_db[message.chat.id] = future_db
        full_db[message.chat.id]['название'] = message.text
        send(message, 'город', None)

    elif message.text.lower() in cities and savehandler == 2:
        savehandler -= 2
        full_db[message.chat.id]['город'] = save_city(message)

    elif savehandler == 3:
        savehandler -= 3
        full_db[message.chat.id]['поиск'] = save_search(message)

    elif savehandler == 4:
        savehandler -= 4
        full_db[message.chat.id]['мин'] = min_search(message)

    elif savehandler == 5:
        savehandler -= 5
        full_db[message.chat.id]['макс'] = max_search(message)
        full_db[message.chat.id]['ссылка'] = linkget(message)

    else:
        send(message, 'Не понимаю', None)

@bot.callback_query_handler(func=lambda call: True)
def main_menu(call):

    delete(call)

    if call.data == '1':
        send(call.message, 'добро пожаловать!', keyboard1)

    elif call.data == '3':
        global keyboard4
        keyboard4 = telebot.types.InlineKeyboardMarkup()
        global finalnames
        finalnames = []
        dbnames = dbcursor.execute("SELECT name FROM " + f'id{str(call.message.chat.id)}' + "")
        for dbname in dbnames:
            finalname = (''.join(list(dbname)))
            finalnames.append(finalname)
            keyboard4.add(telebot.types.InlineKeyboardButton(text=finalname, callback_data=finalname))
        keyboard4.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=1))
        send(call.message, 'Выбери объявление среди списка:', keyboard4)
        global callhandler
        callhandler = 0

    elif call.data == '4':
        send(call.message, 'Циан', back2)

    elif call.data == '2':
        send(call.message, 'под каким названием сохранить запрос?', None)
        global savehandler
        savehandler += 1

    elif call.data == '6':
        dbvalues = tuple(full_db[call.message.chat.id].values())
        print(dbvalues)
        sql = """INSERT INTO """ + f'id{str(call.message.chat.id)}' + """(name, city, search, min, max, link, last) VALUES(?, ?, ?, ?, ?, ?, ?); """
        dbcursor.execute(sql, dbvalues)
        dbconnect.commit()
        dbcursor.execute("SELECT * FROM " + f'id{str(call.message.chat.id)}' + "")
        rows = dbcursor.fetchall()
        for row in rows:
            print (row)
        send(call.message, 'добро пожаловать!', keyboard1)

    elif call.data in finalnames and callhandler == 0:
        keyboard5 = telebot.types.InlineKeyboardMarkup()
        keyboard5.add(telebot.types.InlineKeyboardButton(text='да', callback_data=str(call.data)))
        keyboard5.add(telebot.types.InlineKeyboardButton(text='нет', callback_data=3))
        send(call.message, 'удаляем?', keyboard5)
        callhandler = 1

    elif call.data in finalnames and callhandler == 1:
        callhandler -= 1
        dbcursor.execute("DELETE FROM " + f'id{str(call.message.chat.id)}' +  " WHERE name=?", [call.data])
        keyboard6 = telebot.types.InlineKeyboardMarkup()
        keyboard6.add(telebot.types.InlineKeyboardButton(text='назад', callback_data=3))
        send(call.message, 'успешно удалено', keyboard6)

    else:
        send(call.message, 'ну и что', None)


def save_city(message):
    print(message.text)
    send(message, 'что ищем?', None)
    global savehandler
    savehandler += 3
    return (translit(message.text.lower()))

def save_search(message):
    print(message.text)
    send(message, 'укажи минималку', None)
    global savehandler
    savehandler += 4
    return ('+'.join(message.text.lower().split(' ')))

def min_search(message):
    print(message.text)
    send(message, 'укажи максималку', None)
    global savehandler
    savehandler += 5
    return(int(numstrip(message.text)))

def max_search(message):
    print(message.text)
    return(int(numstrip(message.text)))

def linkget(message):
    global link
    link = f'https://www.avito.ru/{future_db["город"]}?pmax={future_db["макс"]}&pmin={future_db["мин"]}&q={future_db["поиск"]}&s=104'
    send(message, f'все ок?\n{link}', keyboard3)
    return(link)

def url(page_url):
    return requests.get(page_url).text

#не функция а пиздец, СРОЧНО необходимо что то с ней сделать чтобы она работала но выглядела попривлекательнее

def test():
    while True:
        try:
            dbcursor.execute("SELECT * FROM user_id")
            ids = dbcursor.fetchall()
            for id in ids:
                finalid = ''.join(list(id))
                print(finalid)
                linkquery = "SELECT link FROM " + f'id{finalid}' + ""
                dbcursor.execute(linkquery)
                dburls = dbcursor.fetchall()
                for dburl in dburls:
                    finalurl = (''.join(list(dburl)))
                    print(finalurl)
                    soup = BeautifulSoup(url(finalurl), 'lxml')
                    linkss = soup.find('div', attrs={'class': 'iva-item-titleStep-2bjuh'})
                    linksss = linkss.find('a')
                    x = f'avito.ru{linksss.get("href")}'
                    lastquery = "SELECT last FROM " + f'id{finalid}' " WHERE link = ?;"
                    dbcursor.execute(lastquery, [finalurl])
                    dblast = (''.join(list(dbcursor.fetchone())))
                    if not dblast == x:
                        updatequery = "UPDATE " + f'id{finalid}' + " SET last = ? WHERE link = ?;"
                        dbcursor.execute(updatequery, [x, finalurl])
                        dbconnect.commit()
                        bot.send_message(chat_id=int(finalid), text=f'Новое объявление по твоему запросу: {x}')
                    time.sleep(5)
            time.sleep(30)
        except IndexError:
            continue

def bots():
    bot.polling()

p1 = Thread(target=bots)
p2 = Thread(target=test)
if __name__ == '__main__':
    p1.start(), p2.start()
    p1.join(), p2.join()
bot.polling()