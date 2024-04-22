import telebot
from telebot import types

from rim_pizza import get_rim_pizza


token = '7194759653:AAHIBWsVCWJX6ydlVEiguv0DkDPPjSHMtGw'
bot = telebot.TeleBot(token=token, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Domino приветствует вас!')
    
    murkup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Риская пицца')
    btn2 = types.KeyboardButton('Mod пицца')
    btn3 = types.KeyboardButton('Сэндвичи')
    btn4 = types.KeyboardButton('Десерты')
    murkup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=murkup)


@bot.message_handler(func=lambda x: True)
def echo_all(message):
    if message.text == 'Риская пицца':
        pizza_rim_list = get_rim_pizza()

        for pizza in pizza_rim_list:
            text = f'Название: {pizza["name"]}\n' \
                   f'Описание: {pizza["description"]}\n' \
                   f'Цена: {pizza["price"]}'
            bot.send_photo(
                message.chat.id, 
                f'https://static.dodomino.ru/images/3024-1311-picca-s-zapecenoi-goviadinoi-i-gorcicnym-sousom-300.webp'
            )
            bot.send_message(message.chat.id, text)


bot.polling()
