#!/usr/bin/env python3
# downloadable imports:
import pymongo
from pymongo import MongoClient
import telebot
from telebot.types import Message
from telebot import types
# local imports:
import constants
from user_db_updates import *
from user_data_handler import *
from bot_db_manager import *

client = MongoClient("mongodb+srv://mongouser:O6TYkZnXi39z@cluster0.fapa8.mongodb.net/client.test?retryWrites=true&w=majority")
db = client['test']
posts = db.posts
bot = telebot.TeleBot(token="1319956764:AAH7-bJJyOHG3MkRc7tB1He7FrIJ5XTXTu0")


# telegram_id : string
# photo_id : string
# name : string
# company : string
# lfwhat : string
# skills : string
# active : string
# nickname : string
# bot_state : string


def add_new_user(message: Message):
	user_id = message.from_user.id

	if posts.find_one({"telegram_id": user_id}):
		return 1
	post = {
		"telegram_id": user_id,
		"photo_id": 'none',
		"name": 'none',
		"company": 'none',
		"lfwhat": 'none',
		"skills": 'none',
		"active": 'none',
		"nickname": 'none',
		"bot_state": 'awaiting_photo_full' 
	}
	posts.insert_one(post)
	return 0


def main_menu():
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Изменить анкету")
    btn2 = types.KeyboardButton('Перестать участвовать')
    btn3 = types.KeyboardButton('Возобновить участие')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    return markup


def display_user_info(user_id, chat_id):
    get_photo_id(user_id)
    bot.send_photo(chat_id, get_photo_id(user_id))
    bot.send_message(chat_id=chat_id, text=f"{get_name(user_id)}, {get_company(user_id)}\nЯ ищу: {get_lfwhat(user_id)}\nМогу быть полезен: {get_skills(user_id)}")


def change_info_menu():
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Изменить Фото")
    btn2 = types.KeyboardButton('Изменить Имя и Фамилию')
    btn3 = types.KeyboardButton('Изменить компанию и позицию')
    btn4 = types.KeyboardButton('Изменить то, что я ищу')
    btn5 = types.KeyboardButton('Изменить мои навыки')
    btn6 = types.KeyboardButton('Назад')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)
    markup.row(btn5)
    markup.row(btn6)
    return markup


@bot.message_handler(commands=['start'])
def start_reply(message: Message):
    user_existed = add_new_user(message)
    if user_existed:
        bot.send_message(chat_id=message.chat.id, text="user already exists")
    else:
        bot.send_message(chat_id=message.chat.id, text=constants.start_text)
        bot.send_message(chat_id=message.chat.id, text=constants.add_photo_text)


@bot.message_handler(commands=['menu'])
def start_reply(message: Message):
        bot.send_message(chat_id=message.chat.id, text="Держи меню", reply_markup=main_menu())


@bot.message_handler(commands=['reset'])
def start_reply(message: Message):
    markup = types.ReplyKeyboardRemove()
    user_id = message.from_user.id
    update_state(user_id, 'awaiting_photo_full')
    bot.send_message(chat_id=message.chat.id, text=constants.start_text, reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text=constants.add_photo_text)


@bot.message_handler(content_types=['photo'])
def get_photo(message: Message):
    bot_state = get_state(message.from_user.id)
    if bot_state.state_text != 'awaiting_photo_full' and bot_state.state_text != 'awaiting_photo':
        return
    update_status = update_photo(message.from_user.id, message.photo[0].file_id)
    if update_status == 1 and bot_state.state_text == 'awaiting_photo_full':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Использовать имя из профиля")
        markup.row(btn1)
        bot.send_message(chat_id=message.chat.id, text=f"Как тебя представлять другим участникам? В твоем профиле указано, что твоё имя - {message.from_user.username}. " \
                           "Я могу использовать его. Или пришли мне своё имя текстом.", reply_markup=markup)
        update_state(message.from_user.id, 'awaiting_name_full')
    elif update_status == 1 and bot_state.state_text == 'awaiting_photo':
        markup = main_menu()
        update_state(message.from_user.id, 'idle')
        bot.send_message(chat_id=message.chat.id, text="Фотография обновлена", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message: Message):
	bot_state = get_state(message.from_user.id)
	if not bot_state:
		bot.send_message(chat_id=message.chat.id, text="Что - то пошло не так, попробуйте команду /reset")
	elif bot_state.state_text == 'awaiting_name_full':
		if message.text == "Использовать имя из профиля":
			update_name_and_surname(message.from_user.id, message.from_user.username)
		else:
			update_name_and_surname(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text=constants.add_company_text, reply_markup=types.ReplyKeyboardRemove())
		update_state(message.from_user.id, 'awaiting_company_full')
	elif bot_state.state_text == 'awaiting_company_full':
		update_company(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text=constants.lfwhat_text)
		update_state(message.from_user.id, 'awaiting_lfwhat_full')
	elif bot_state.state_text == 'awaiting_lfwhat_full':
		update_lfwhat(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text=constants.skills_text)
		update_state(message.from_user.id, 'awaiting_skills_full')
	elif bot_state.state_text == 'awaiting_skills_full':
		update_skills(message.from_user.id, message.text)
		markup = types.ReplyKeyboardMarkup()
		btn1 = types.KeyboardButton('Участвовать в нетворкинге')
		markup.row(btn1)
		bot.send_message(chat_id=message.chat.id, text=constants.active_text, reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_active')
	elif (bot_state.state_text == 'awaiting_active' and message.text == "Участвовать в нетворкинге") or \
			(bot_state.state_text == 'idle' and message.text == "Возобновить участие"):
		markup = main_menu()
		update_active(message.from_user.id, 'Yes')
		bot.send_message(chat_id=message.chat.id, text="Супер, теперь ты участвуешь в нетворкинге!", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'idle' and message.text == 'Перестать участвовать':
		markup = main_menu()
		update_active(message.from_user.id, 'No')
		bot.send_message(chat_id=message.chat.id, text="Теперь ты не участвуешь в нетворкинге", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'idle' and message.text == "Изменить анкету":
		markup = change_info_menu()
		user_id = message.from_user.id
		bot.send_message(chat_id=message.chat.id, text="Вот твоя анкета:")
		display_user_info(user_id, message.chat.id)
		bot.send_message(chat_id=message.chat.id, text="Выбери, что изменить", reply_markup=markup)
	elif bot_state.state_text == 'idle' and message.text == "Изменить Фото":
		markup = types.ReplyKeyboardRemove()
		bot.send_message(chat_id=message.chat.id, text="Загрузи фото", reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_photo')
	elif bot_state.state_text == 'idle' and message.text == "Изменить Имя и Фамилию":
		markup = types.ReplyKeyboardRemove()
		bot.send_message(chat_id=message.chat.id, text="Введи имя и фамилию:", reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_name')
	elif bot_state.state_text == 'idle' and message.text == "Изменить компанию и позицию":
		markup = types.ReplyKeyboardRemove()
		bot.send_message(chat_id=message.chat.id, text="Введи компанию и позицию:", reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_company')
	elif bot_state.state_text == 'idle' and message.text == "Изменить то, что я ищу":
		markup = types.ReplyKeyboardRemove()
		bot.send_message(chat_id=message.chat.id, text="Введи то, что ты ищешь:", reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_lfwhat')
	elif bot_state.state_text == 'idle' and message.text == "Изменить мои навыки":
		markup = types.ReplyKeyboardRemove()
		bot.send_message(chat_id=message.chat.id, text="Введи свои навыки:", reply_markup=markup)
		update_state(message.from_user.id, 'awaiting_skills')
	elif bot_state.state_text == 'awaiting_active_bool' and (message.text == 'Да' or message.text == 'Нет'):
		markup = main_menu()
		update_active(message.from_user.id, "Yes" if message.text == 'Да' else "No")
		bot.send_message(chat_id=message.chat.id, text="Принято", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'awaiting_name':
		markup = change_info_menu()
		update_name_and_surname(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text="Описание обновлено", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'awaiting_company':
		markup = change_info_menu()
		update_company(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text="Описание обновлено", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'awaiting_lfwhat':
		markup = change_info_menu()
		update_lfwhat(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text="Описание обновлено", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif bot_state.state_text == 'awaiting_skills':
		markup = change_info_menu()
		update_skills(message.from_user.id, message.text)
		bot.send_message(chat_id=message.chat.id, text="Описание обновлено", reply_markup=markup)
		update_state(message.from_user.id, 'idle')
	elif message.text == 'Назад':
		markup = main_menu()
		bot.send_message(chat_id=message.chat.id, text="Выбери, что хочешь сделать:", reply_markup=markup)
		update_state(message.from_user.id, 'idle')


bot.polling(timeout=60)
