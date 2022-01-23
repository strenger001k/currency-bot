from bot import bot
from config import ADMIN_CHAT
from messages import *
from db import *
from privat import get_currency_value, sale_ccy, buy_ccy
from threading import Thread
import time
from scheduler import start_scheduler, stop_scheduler

ALREADY_START = False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_CHAT:
        admin_menu(message)
    else:
        bot.send_message(message.chat.id,
                                 HELLO_AGAIN_MESSAGE,
                                 reply_markup=remove_keyboard())
        if check_registration(message.from_user.id):
            if not is_block(message.from_user.id):
                bot.send_message(message.chat.id,
                                 HELLO_AGAIN_MESSAGE,
                                 reply_markup=remove_keyboard())
                if is_scheduler(message.from_user.id):
                    global ALREADY_START
                    if ALREADY_START:
                        stop_scheduler()
                    start_scheduler(message, bot)
                    ALREADY_START = True
                    time.sleep(0.1)
                    bot.send_message(message.chat.id, SUCCESS_SCHEDULER)
            else:
                bot.send_message(message.chat.id, BLOCK_MESSAGE)
        else:
            create_user(user_id=message.from_user.id,
                        username=message.from_user.username,
                        user_name=message.from_user.first_name,
                        user_surname=message.from_user.last_name)
            bot.send_message(message.chat.id,
                             HELLO_MESSAGE,
                             reply_markup=remove_keyboard())
        main_menu(message)


def main_menu(message):
    answer = bot.send_message(message.chat.id,
                              MAIN_MENU,
                              reply_markup=get_user_keyboard(message))
    bot.register_next_step_handler(answer, processing_main_keyboard)


def currency_menu(message):
    bot.send_message(message.chat.id,
                     ENTER_CURRENCY,
                     reply_markup=get_currency_keyboard())


def processing_main_keyboard(message):
    if message.text == GET_CCY:
        bot.send_message(message.chat.id,
                         ENTER_CURRENCY,
                         reply_markup=get_currency_keyboard())
    elif message.text == FEEDBACK_MESSAGE:
        answer = bot.send_message(message.chat.id,
                                  DISCRIBE_PROBLEM,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, send_to_admin)
    elif message.text == TIMER:
        if not is_scheduler(message.from_user.id):
            answer = bot.send_message(message.chat.id,
                                      SCHEDULER_TIME,
                                      parse_mode="HTML",
                                      reply_markup=yes_no_keyboard())

            bot.register_next_step_handler(answer, scheduler_time_user)
        else:
            bot.send_message(message.chat.id, SUCCESS_SCHEDULER)
            main_menu(message)
    elif message.text == OFF_TIMER:
        answer = bot.send_message(message.chat.id,
                                  OFF_SCHEDULER_TIME,
                                  parse_mode="HTML",
                                  reply_markup=yes_no_keyboard())
        bot.register_next_step_handler(answer, scheduler_time_user)
    else:
        bot.send_message(message.chat.id, REGISTRATION)


def scheduler_time_user(message):
    if not is_scheduler(message.from_user.id):
        if message.text == YES:
            global ALREADY_START
            ALREADY_START = True
            start_scheduler(message, bot)
            scheduler_user_on(message.from_user.id)
            bot.send_message(message.chat.id, SUCCESS_SCHEDULER)
        else:
            bot.send_message(message.chat.id, UNSUCCESS_SCHEDULER)
    else:
        if message.text == YES:
            stop_scheduler()
            scheduler_user_off(message.from_user.id)
            bot.send_message(message.chat.id, UNSUCCESS_SCHEDULER)
        else:
            bot.send_message(message.chat.id, CONTINUE_SCHEDULER)
    main_menu(message)


@bot.callback_query_handler(func=lambda call: True)
def info_message(call):
    bot.answer_callback_query(call.id)
    if UAN in call.data:
        answer = bot.send_message(call.message.chat.id,
                                  ENTER_VALUE_CONVERT,
                                  parse_mode="HTML",
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, convert_currency, call.data)
    elif call.data == BACK_CCY:
        currency_menu(call.message)
    elif call.data == BACK:
        main_menu(call.message)
    else:
        bot.send_message(call.message.chat.id,
                         get_currency_value(call.data),
                         reply_markup=convert_from_grn(call.data))


def convert_currency(message, ccy):
    if message.text == BACK:
        bot.send_message(message.chat.id,
                         CANCEL,
                         reply_markup=remove_keyboard())
        currency_menu(message)
    else:
        try:
            if ccy.split('|')[0] == UAN:
                bot.send_message(message.chat.id,
                                 sale_ccy(ccy, float(message.text)),
                                 disable_web_page_preview=True,
                                 parse_mode="HTMl",
                                 reply_markup=remove_keyboard())
            else:
                bot.send_message(message.chat.id,
                                 buy_ccy(ccy, float(message.text)),
                                 disable_web_page_preview=True,
                                 parse_mode="HTMl",
                                 reply_markup=remove_keyboard())
        except:
            bot.send_message(message.chat.id, ERROR_MESSAGE)
        currency_menu(message)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == BACK and message.chat.id != ADMIN_CHAT:
        main_menu(message)
    else:
        if message.chat.id != ADMIN_CHAT:
            bot.send_message(message.chat.id, REGISTRATION)
        else:
            admin_answer(message)


def send_to_admin(message):
    if message.text == BACK:
        main_menu(message)
    else:
        if message.from_user.username:
            bot.send_message(ADMIN_CHAT,
                             MESSAGE_PROBLEM_USERNAME.
                             format(message.from_user.username,
                                    message.from_user.username,
                                    message.text),
                             disable_web_page_preview=True,
                             parse_mode="HTML",
                             reply_markup=answer_keyboard())
            bot.send_message(message.chat.id, PROBLEM_SUCCESS)
            main_menu(message)
        else:
            bot.send_message(ADMIN_CHAT,
                             MESSAGE_PROBLEM.format
                             (message.from_user.first_name,
                              message.text))


def admin_menu(message):
    answer = bot.send_message(message.chat.id,
                              ADMIN_MENU,
                              reply_markup=get_admin_keyboard())
    bot.register_next_step_handler(answer, admin_answer)


# admin`s processing
def admin_answer(message):
    if message.text == GET_ALL_USERS:
        answer = bot.send_message(message.chat.id,
                                  get_all_user(),
                                  parse_mode='html',
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, go_back)
    elif message.text == SENDER:
        answer = bot.send_message(message.chat.id,
                                  GET_SENDER_TEXT,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, sender)
    elif message.text == BLOCK_USER:
        answer = bot.send_message(message.chat.id,
                                  GET_USER_ID_BLOCK,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, block)
    elif message.text == UNBLOCK_USER:
        answer = bot.send_message(message.chat.id,
                                  GET_USER_ID_BLOCK,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, unblock)
    elif message.text == SEARCH_USER:
        answer = bot.send_message(message.chat.id,
                                  GET_USER_ID_SEARCH,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer, search)
    elif message.text == GET_TXT_USER:
        bot.send_message(message.chat.id, SUCCESS_FILE)
        get_file(message)
    elif message.text == ANSWER:
        try:
            username = message.json['reply_to_message']['entities'][0]['url'].\
                                   split('https://t.me/')[1]
        except:
            bot.send_message(message.chat.id,
                             SEND_MESSAGE_YOURSELF)
        answer = bot.send_message(message.chat.id,
                                  FEEDBACK_ANSWER,
                                  reply_markup=back_keyboard())
        bot.register_next_step_handler(answer,
                                       feedback_answer,
                                       search_user_id(username))
    elif message.text == BACK:
        admin_menu(message)


def go_back(message):
    if message.text == BACK:
        admin_menu(message)


def feedback_answer(message, id_user):
    if message.text == BACK:
        admin_menu(message)
    else:
        if id_user:
            bot.send_message(id_user,
                             ADMIN_ANSWER.format(message.text))
        else:
            bot.send_message(message.chat.id,
                             SEND_MESSAGE_YOURSELF)
        admin_menu(message)


def thread_sender(users_id, text):
    for id in users_id:
        bot.send_message(id, text)
        time.sleep(0.1)


def sender(message):
    if message.text == BACK:
        admin_menu(message)
    else:
        th = Thread(target=thread_sender, args=(get_all_id(), message.text, ))
        th.start()
        admin_menu(message)


def block(message):
    if message.text == BACK:
        admin_menu(message)
    else:
        if message.text.isdigit():
            bot.send_message(message.chat.id, block_user(int(message.text)))
        else:
            bot.send_message(message.chat.id, ERROR_MESSAGE)
        admin_menu(message)


def unblock(message):
    if message.text == BACK:
        admin_menu(message)
    else:
        if message.text.isdigit():
            bot.send_message(message.chat.id, unblock_user(int(message.text)))
        else:
            bot.send_message(message.chat.id, ERROR_MESSAGE)
        admin_menu(message)


def search(message):
    if message.text == BACK:
        admin_menu(message)
    else:
        if message.text.isdigit():
            bot.send_message(message.chat.id,
                             search_user(int(message.text)),
                             parse_mode='html')
        else:
            bot.send_message(message.chat.id, ERROR_MESSAGE)
        admin_menu(message)


def get_file(message):
    to_excel()
    with open('database.xlsx', 'rb') as file_send:
        bot.send_document(message.chat.id, file_send)
    admin_menu(message)
