#!/usr/bin/python

import telebot
from requests import Request, Session
import json

key = "Your CoinMarketCap ApiKey"
valuta = "EUR"
sValuta = "€"

API_TOKEN = 'Your Telegram Bot Token' #TOKEN Telegram

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Crypto Bot, per impostare la valuta scrivere /usd o /eur, per ricercare una criptovaluta scrivere il suo tag (es. BTC)\
    """)

@bot.message_handler(commands=['usd'])
def send_welcome(message):
    global valuta 
    valuta = "USD"
    global sValuta
    sValuta = "$"
    bot.reply_to(message, "Valuta settata in USD")

@bot.message_handler(commands=['eur'])
def send_welcome(message):
    global valuta 
    valuta = "EUR"
    global sValuta
    sValuta = "€"
    bot.reply_to(message, "Valuta settata in EUR")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global valuta
    global sValuta
    messageText = message.text.upper()
    print(messageText)
    try:
        url= f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        print(url)
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': key,
        }
        parameters = {
            'symbol': messageText,
            'convert': valuta
        }
        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        response = data['data'][messageText]['name'] + "\t" + str(round(data['data'][messageText]['quote'][valuta]['price'],3))+" "+sValuta
        print(response)
        bot.reply_to(message, response)
    
    except (Exception) as e:
        data = json.loads(response.text)
        bot.reply_to(message, "Errore nella richiesta")

bot.polling()