import time
from privat import get_currency_value
from messages import *
from threading import Timer


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def job(message, bot):
    bot.send_message(message.chat.id, get_currency_value(USD))
    time.sleep(0.3)
    bot.send_message(message.chat.id, get_currency_value(EUR), disable_notification=True)
    time.sleep(0.3)
    bot.send_message(message.chat.id, get_currency_value(RUR), disable_notification=True)
    time.sleep(0.3)
    bot.send_message(message.chat.id, get_currency_value(BTC), disable_notification=True)
    time.sleep(0.1)


def start_scheduler(message, bot):
    global th
    th = RepeatTimer(1000, job, args=(message, bot, ))
    th.start()


def stop_scheduler():
    global th
    th.cancel()
