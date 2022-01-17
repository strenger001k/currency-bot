import requests
import json
from messages import *
from config import PRIVAT_API

privat24_api = requests.get(PRIVAT_API)
currency = json.loads(privat24_api.text)


def toFixed(number, value=0):
    return f'{number:.{value}f}'


def get_currency_value(ccy):
    currency_ccy = next(x for x in currency if x["ccy"] == ccy.split()[0])
    if ccy != BTC:
        return CURRENCY_ANSWER.format(ccy,
                                      toFixed(float(currency_ccy['buy']), 2),
                                      toFixed(float(currency_ccy['sale']), 2))
    else:
        return CURRENCY_ANSWER.format(ccy,
                                      toFixed(float(currency_ccy['buy'])),
                                      toFixed(float(currency_ccy['sale'])))


def sale_ccy(ccy, value):
    ccy_format = ccy.split('|')[1]
    ccy = ccy.split('|')[1].split()[0]

    currency_ccy = next(x for x in currency if x["ccy"] == ccy.split()[0])
    sale = float(toFixed(float(currency_ccy['sale']), 2))
    if ccy_format != BTC:
        return CONVERT.format(UAN,
                              ccy_format,
                              toFixed(value/sale, 2),
                              ccy_format.split()[1])
    else:
        return CONVERT.format(USD,
                              ccy_format,
                              toFixed(value/sale, 2),
                              ccy_format.split()[1])


def buy_ccy(ccy, value):
    ccy_format = ccy.split('|')[1]
    ccy = ccy.split('|')[0]

    currency_ccy = next(x for x in currency if x["ccy"] == ccy.split()[0])
    buy = float(toFixed(float(currency_ccy['buy']), 2))

    if ccy != BTC:
        return CONVERT.format(ccy,
                              ccy_format,
                              toFixed(value * buy, 2),
                              ccy_format.split()[1])
    else:
        return CONVERT.format(ccy,
                              USD,
                              toFixed(value * buy, 2),
                              USD.split()[1])

# print(next(x for x in stud_obj if x["ccy"] == "USD"))
# print([x for x in stud_obj if x['ccy'] == 'USD'][0])
