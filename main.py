# - *- coding: utf- 8 - *-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Bot, ReplyKeyboardMarkup
import json
import random
import requests
from bs4 import BeautifulSoup
import urllib



def start(bot, update):
  update.message.reply_text("Не знаете что спросить у собеседника? Я сгенерирую вопрос!")
  print 'start'
  generate_button = KeyboardButton(text="/generate")
  custom_keyboard = [[ generate_button ]] #creating keyboard object
  reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
  bot.send_message(chat_id=update.message.chat_id, reply_markup=reply_markup, text='Генерируем!')
  



def generate_question(bot='', update=''):
    read_line = random.choice(open("questions.txt").readlines())
    print "generate"
    update.message.reply_text(read_line)
 


def convert_uppercase(bot, update):
  if (update.message.text == 'Генерировать вопрос'):
    update.message.reply_text(generate_question())



def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]



    proxies = []

    for tr in trs:

        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    return random.choice(proxies)


def check_proxy(proxy_now):
  
  try:
      urllib.urlopen(
          "https://telegram.org",
          proxies={'http':'http://'+ proxy_now }
      )
      print "Success"
  except Exception:
      print "Failed"

def main():

  # while(True):

  #   proxy_now = get_proxy()['address']
  #   print proxy_now
  #   if check_proxy(proxy_now):
  #     break

  # REQUEST_KWARGS={
  # 'proxy_url': 'http://'+proxy_now,
  # }
  REQUEST_KWARGS={
  'proxy_url': 'http://93.170.4.145:50697',
  }

  # Create Updater object and attach dispatcher to it
  updater = Updater(token="769035753:AAFnB6QZHXegEhreBQ_LFGHzMhwdaCN2ZTs", request_kwargs=REQUEST_KWARGS)
  check_proxy('93.170.4.145:50697')
  dispatcher = updater.dispatcher
  print "Bot started"


  # Add command handler to dispatcher
  start_handler = CommandHandler('start',start)
  generate_handler = CommandHandler('generate', generate_question)
  upper_case = MessageHandler(Filters.text, convert_uppercase)
  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(upper_case)
  dispatcher.add_handler(generate_handler)


  # Start the bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

if __name__ == '__main__':
  main()