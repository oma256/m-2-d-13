import telebot
from telebot import types

from parse_domino_pizza import get_pizza_list


token = '7194759653:AAHIBWsVCWJX6ydlVEiguv0DkDPPjSHMtGw'
bot = telebot.TeleBot(token=token, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Domino приветствует вас!')
    
    murkup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Римская пицца')
    btn2 = types.KeyboardButton('Mod пицца')
    btn3 = types.KeyboardButton('Сэндвичи')
    btn4 = types.KeyboardButton('Десерты')
    murkup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=murkup)


def send_bot_message(chat_id, pizza_list):
    for pizza in pizza_list:
        text = f'`Название`: _{pizza["name"]}_\n' \
               f'`Описание`: _{pizza["description"]}_\n' \
               f'`Цена`: _{pizza["price"]}_\n' \
               f'[----------------------------------------]({pizza["picture"]})'
        keyboard = types.InlineKeyboardMarkup()
        button_order = types.InlineKeyboardButton(
            text='Заказать', callback_data=f'order_{pizza["id"]}'
        )
        keyboard.add(button_order)
        bot.send_message(chat_id=chat_id, 
                         text=text, 
                         parse_mode='Markdown', 
                         reply_markup=keyboard)


product_categories = {
    'Римская пицца': 'rimskaya',
    'Mod пицца': 'moodpizza',
    'Сэндвичи': 'sendvitchi',
    'Десерты': 'deserti',
}


@bot.message_handler(func=lambda x: True)
def echo_all(message):
    pizza_id = product_categories.get(message.text)
    pizza_list = get_pizza_list(pizza_id=pizza_id)
    send_bot_message(message.chat.id, pizza_list)


def save_order(from_user, product_info):
    content = f'Новый заказ от {from_user}:\n\n{product_info}\n\n'

    with open('orders.txt', '+a') as f:
        f.write(content)

@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def order_pizza(call):
    from_user = f'{call.message.chat.first_name} {call.message.chat.last_name}'
    product_info = call.message.text
    save_order(from_user=from_user, product_info=product_info)


bot.polling()
