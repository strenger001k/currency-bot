from http.client import CONTINUE
from telebot import types
from config import ADMIN
import db

ERROR_MESSAGE = 'Ошибка'
REGISTRATION = "Нажмите /start"

HELLO_MESSAGE = 'Добро пожаловать в нашего бота!'
HELLO_AGAIN_MESSAGE = 'Снова привет!)'
BLOCK_MESSAGE = f'Вы заблокированы.\nОбратитесь к администратору {ADMIN}'
BACK = 'Назад'
BACK_CCY = 'Вернуться к выбору валют'
FEEDBACK_MESSAGE = 'Связатся с нами ❤️'
GET_CCY = 'Курс валют 📉'
TIMER = 'Рассылка ⏳'
OFF_TIMER = 'Отключить рассылку ⌛️'
MAIN_MENU = 'Главное меню 🔮'
DISCRIBE_PROBLEM = 'Опишите вашу проблему'
PROBLEM_SUCCESS = 'Сообщение отправлено.\nНаш администратор в ближайшее время свяжется с вами'
ENTER_CURRENCY = 'Выбирите валюту'
MESSAGE_PROBLEM_USERNAME = 'Пользователь: <a href="https://t.me/{}">{}</a>\nСообщение: {}'
MESSAGE_PROBLEM = 'Пользователь: {}\nСообщение: {}'
CONVERT_CCY = 'Конвертировать {} в {} '
CONVERT_CCY_BTC = 'Конвертировать {} в {}'
ENTER_VALUE_CONVERT = 'Введите сумму (если число не целое используйте точку)\nПример: <code>27.52</code>'
ADMIN_ANSWER = "Ответ администратора на вашу проблему:\n{}"
SCHEDULER_TIME = 'Каждые 6 часов будет присылаться курс валют\nВыберите <code>Да</code> или <code>Нет</code>'
OFF_SCHEDULER_TIME = 'Отключить рассылку?\nВыберите <code>Да</code> или <code>Нет</code>'
SUCCESS_SCHEDULER = '❗️❗️❗️ Рассылка включена ❗️❗️❗️'
CONTINUE_SCHEDULER = '❗️❗️❗️ Рассылка работает ❗️❗️❗️'
UNSUCCESS_SCHEDULER = 'Рассылка отключена'
YES = 'Да ✅'
NO = 'Нет ❌'
CANCEL = 'Отмена'


ADMIN_MENU = 'Админ панель'
GET_ALL_USERS = 'Пользователи 📝'
SENDER = 'Рассылка 💌'
SEARCH_USER = 'Найти пользователя 🔍'
BLOCK_USER = 'Заблокировать 🚫'
UNBLOCK_USER = 'Разблокировать ⭕️'
GET_TXT_USER = 'Файл с пользователями 🗂'
ANSWER = 'Ответить'
GET_SENDER_TEXT = 'Ответьте на это сообщение текстом для рассылки'
GET_USER_ID_BLOCK = 'Ответьте на это сообщение id пользователя, которого нужно заблокировать'
GET_USER_ID_SEARCH = 'Ответьте на это сообщение id пользователя, которого надо найти'
FEEDBACK_ANSWER = 'Ответьте на это сообщение и пользователь получит ответ'
BLOCK_SUCCESS = 'Пользователь заблокирован'
UNBLOCK_SUCCESS = 'Пользователь разблокирован'
ERROR_SEARCH = 'Пользователь не найден (('
SUCCESS_FILE = 'Ваш файл 🗂'
SEND_MESSAGE_YOURSELF = 'ID нет, свяжитесь с пользователем сами.\nДанные можно посмотреть в списке пользователей'
ALL_USERS = 'ID: <b>{}</b>\nUsername: {}\nName: {}\nSurname: {}\nBlock: <b>{}</b>\nScheduler: {}\n\n'


USD = 'USD 🇺🇸'
EUR = 'EUR 🇪🇺'
RUR = 'RUR 🇷🇺'
BTC = 'BTC ₿'
UAN = 'UAN 🇺🇦'
CURRENCY_ANSWER = "{}\nПокупка: {} 💵\nПродажа: {} 💵"
CONVERT = '{}  →  {}\n{} {}\n<a href="https://privatbank.ua/">privatbank</a>'


def remove_keyboard():
    return types.ReplyKeyboardRemove()


def get_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = types.InlineKeyboardButton(USD, callback_data=USD)
    inline_btn_2 = types.InlineKeyboardButton(EUR, callback_data=EUR)
    inline_btn_3 = types.InlineKeyboardButton(RUR, callback_data=RUR)
    inline_btn_4 = types.InlineKeyboardButton(BTC, callback_data=BTC)
    inline_btn_5 = types.InlineKeyboardButton(BACK, callback_data=BACK)
    keyboard.add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)
    return keyboard


def get_admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    keyboard.add(GET_ALL_USERS, GET_TXT_USER, SENDER, SEARCH_USER, BLOCK_USER, UNBLOCK_USER)
    return keyboard


def get_user_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    if message.chat.id is not None:
        if not db.is_scheduler(message.chat.id):
            keyboard.add(GET_CCY, FEEDBACK_MESSAGE, TIMER)
        else:
            keyboard.add(GET_CCY, FEEDBACK_MESSAGE, OFF_TIMER)
    else:
        if not db.is_scheduler(message.from_user.id):
            keyboard.add(GET_CCY, FEEDBACK_MESSAGE, TIMER)
        else:
            keyboard.add(GET_CCY, FEEDBACK_MESSAGE, OFF_TIMER)
    return keyboard


def answer_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    keyboard.add(ANSWER, BACK)
    return keyboard


def back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,  resize_keyboard=True)
    keyboard.row(BACK)
    return keyboard


def yes_no_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    keyboard.add(YES, NO)
    return keyboard


def convert_from_grn(ccy):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if ccy != BTC:
        inline_btn_1 = types.InlineKeyboardButton(CONVERT_CCY.format(UAN, ccy), callback_data=f'{UAN}|{ccy}')
        inline_btn_2 = types.InlineKeyboardButton(CONVERT_CCY.format(ccy, UAN), callback_data=f'{ccy}|{UAN}')
    else:
        inline_btn_1 = types.InlineKeyboardButton(CONVERT_CCY_BTC.format(USD, ccy), callback_data=f'{UAN}|{ccy}')
        inline_btn_2 = types.InlineKeyboardButton(CONVERT_CCY_BTC.format(ccy, USD), callback_data=f'{ccy}|{UAN}')
    inline_btn_3 = types.InlineKeyboardButton(BACK_CCY, callback_data=BACK_CCY)
    keyboard.add(inline_btn_1)
    keyboard.add(inline_btn_2)
    keyboard.add(inline_btn_3)
    return keyboard
