# downloadable imports:
import telebot
import datetime
from telebot import types
import sqlite3
import random
# local imports:
from user_data_handler import *
from user_data_handler import *
from bot_db_manager import *

bot = telebot.TeleBot(token="1319956764:AAH7-bJJyOHG3MkRc7tB1He7FrIJ5XTXTu0")
f = open("last_notified_date.txt", 'r')
last_notification = f.read()
f.close()


def display_user_info(user_id, chat_id, username):
    get_photo_id(user_id)
    bot.send_message(chat_id=chat_id, text="Привет!👋\nТвоя пара на эту неделю:")
    bot.send_photo(chat_id, get_photo_id(user_id))
    bot.send_message(chat_id=chat_id, parse_mode='Markdown',text=f"{get_name(user_id)}, {get_company(user_id)}\nЯ ищу: {get_lfwhat(user_id)}\nМогу быть полезен: {get_skills(user_id)}\nНапиши партнеру в Telegram - [{username}](tg://user?id={user_id})\nНе откладывай, договорись о встрече сразу")


def create_pairs():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE Active = "Yes"''')
    rows = c.fetchall()
    users = list()
    i = 0
    for row in rows:
        users.append((row[0], row[-1], i))
        i += 1
    i = 0
    for user in users:
        pair = random.choice(users[i + 1:])
        if not pair:
            bot.send_message(chat_id=user[0], text="Извини, я не нашел тебе пары на эту неделю")
            conn.close()
            return
        users.pop(pair[-1])
        display_user_info(user_id=user[0], chat_id=pair[0], username=user[1])
        display_user_info(user_id=pair[0], chat_id=user[0], username=pair[1])
    conn.close()


def notify_all():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE Active = "Yes"''')
    rows = c.fetchall()
    for row in rows:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton('Нет')
        markup.row(btn1)
        markup.row(btn2)
        user_id = row[0]
        bot.send_message(chat_id=user_id, text="Привет!👋\nВстречи продолжаются\nУчаствуешь завтра? \nДа / нет\n👨‍💻 Рекомендуем провести встречу по видеосвязи.\nБерегите себя и близких ♥️ И поддерживайте общение с окружающими онлайн!", reply_markup=markup)
        update_state(user_id, 'awaiting_active_bool', "placeholder")
    conn.close()


while True:
    if datetime.datetime.today().weekday() == 4 and datetime.datetime.now().time().hour == 14:
        if int(last_notification.split('-')[0]) != datetime.datetime.today().date().day:
            create_pairs()
            last_notification = datetime.datetime.today().date().strftime("%d-%b-%Y")
            f = open("last_notified_date.txt", 'w')
            f.write(datetime.datetime.today().date().strftime("%d-%b-%Y"))
            f.close()
    elif datetime.datetime.today().weekday() == 3 and datetime.datetime.now().time().hour == 14:
        if int(last_notification.split('-')[0]) != datetime.datetime.today().date().day:
            notify_all()
            last_notification = datetime.datetime.today().date().strftime("%d-%b-%Y")
            f = open("last_notified_date.txt", 'w')
            f.write(datetime.datetime.today().date().strftime("%d-%b-%Y"))
            f.close()
