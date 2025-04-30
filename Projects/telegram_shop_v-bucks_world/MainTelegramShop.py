import time
import telebot
from cafig import *
from telebot import types
from collections import defaultdict
import random, sqlite3



# инициализация бота в телеграм
bot = telebot.TeleBot(bot_TOKEN)
# message.chat.username message.chat.id price products account_data "not" num_ticket
prices = {
    "13500VB": 37,
    "5000VB": 200,
    "2800VB": 140,
    "1000VB": 65,
    "crew": 80,
    "pack_touch": 100,
    "pack_value_agents": 150
}

finish_products = []
products = ''
finish_price = 0
price = 0
quantity = defaultdict(int)
account_data = ''

def receiver() -> int:
    db = sqlite3.connect("V-BucksWorld.db")
    cursor = db.cursor()
    cursor.execute("SELECT num_ticket FROM shop")
    row = cursor.fetchall()
    result = row[-1][0]
    db.commit()
    db.close() 
    return result + 1

def create_db():
    db = sqlite3.connect("V-BucksWorld.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS shop (username STRING, user_id INTEGER, finish_price INTEGER, finish_products STRING, account_data STRING, status_payment STRING, num_ticket INTEGER)")
    db.commit()
    db.close()

def send_db(username:str, user_id:int, finish_price:int, finish_products:str, account_data:str, status_payment:str, num_ticket:int):
    # инициализация базы данных
    db = sqlite3.connect("V-BucksWorld.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO shop VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, user_id, finish_price, finish_products, account_data, status_payment, num_ticket))
    db.commit()
    db.close()

def edit(shop_message_chat_id, shop_message_id, price_quantity):
    bot.edit_message_text(chat_id=shop_message_chat_id, message_id=shop_message_id,
                          text=f"""Это самые низкие цена на VB во всей Украине:    
    {quantity["1000VB"]} шт. 1000VB - 65 грн     
    {quantity["2800VB"]} шт. 2800VB - 140 грн   
    {quantity["5000VB"]} шт. 5000VB - 200 грн   
    {quantity["13500VB"]} шт. 13500VB - 370 грн 
    {quantity["crew"]} шт. Crew - 80 грн     
    {quantity["pack_touch"]} шт. Прикосновение пустоты - 100 грн 
    {quantity["pack_value_agents"]} шт. Ценные агенты - 150 грн  """,
                          reply_markup=price_quantity)

@bot.message_handler(commands=['start'])
def start_work(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Магазин", callback_data="shop_button")
    button2 = types.InlineKeyboardButton(text="Discord", url="https://discord.gg/b3zMGdfy")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Привет! Это магазин САМЫХ ДЕШЕВЫХ V-BUCKS В МИРЕ', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    user_id = 1260362938
    user_name = "Z1VERTZ"

    # Создаем ссылку на профиль пользователя
    user_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'

    # Добавляем ссылку в текст сообщения
    reply_text = f'Привет, обратитесь к {user_link} по дальнейшим вопросам!'

    # Отправляем обновленное сообщение с ссылкой
    bot.send_message(message.chat.id, reply_text, parse_mode='HTML')

@bot.message_handler(commands=["insert"])
def insert(message):
    global account_data
    account_data = message.text[message.text.find(' '):]

@bot.message_handler(commands=['shop'])
def shop(message):
    global shop_message_chat_id, shop_message_id, price_quantity, quantity, finish_price, finish_products, account_data, products, price
    finish_products = []
    products = ''
    finish_price = 0
    price = 0
    quantity = defaultdict(int)
    account_data = ''

    # Подготовка и создания кнопок ассортимента
    price_quantity = types.InlineKeyboardMarkup()

    vb1000 = types.InlineKeyboardButton(text="1000VB",callback_data="1000VB")

    vb2800 = types.InlineKeyboardButton(text="2800VB",callback_data="2800VB")

    vb5000 = types.InlineKeyboardButton(text="5000VB",callback_data="5000VB")

    vb13500 = types.InlineKeyboardButton(text="13500VB",callback_data="13500VB")

    crew = types.InlineKeyboardButton(text="Crew",callback_data="crew")

    pack_touch = types.InlineKeyboardButton(text="Прикосновение пустоты",callback_data="pack_touch")

    pack_value_agents = types.InlineKeyboardButton(text="Ценные агенты",callback_data="pack_value_agents")

    clear_button = types.InlineKeyboardButton(text="Clear",callback_data="clear")

    pay_button = types.InlineKeyboardButton(text="Pay",callback_data="pay")

    # Прикрепление кнопок к сообщению с ценами
    price_quantity.row(vb1000, vb2800, vb5000, vb13500)
    price_quantity.add(crew)
    price_quantity.row(pack_touch, pack_value_agents)
    price_quantity.row(clear_button, pay_button)
    shop_message = bot.send_message(message.chat.id,
                                    text=f"""Это самые низкие цена на VB во всей Украине:    
    {quantity["1000VB"]} шт. 1000VB - 65 грн     
    {quantity["2800VB"]} шт. 2800VB - 140 грн   
    {quantity["5000VB"]} шт. 5000VB - 200 грн   
    {quantity["13500VB"]} шт. 13500VB - 370 грн 
    {quantity["crew"]} шт. Crew - 80 грн     
    {quantity["pack_touch"]} шт. Прикосновение пустоты - 100 грн 
    {quantity["pack_value_agents"]} шт. Ценные агенты - 150 грн  """,
                                    reply_markup=price_quantity)

    # Получение нужних данных о сообщении с ценами для
    # дальнейшого изменения текста для экранизирования количества взятого товара
    shop_message_chat_id = message.chat.id
    shop_message_id = shop_message.message_id



@bot.message_handler()
def pay(message):
    global price, products, account_data, pay_message
    try:
        finish_price = 0
        for key in quantity:
            if quantity[key] != 0:
                finish_price = round((finish_price + (quantity[key] * prices[key])) + (random.randint(1, 100) / 100), 2)
                finish_products.append(f'{key}x{quantity[key]}')
        price = finish_price
        products = ','.join(finish_products)
    except:
        bot.send_message(message.chat.id, text="Что-то не так, напишите /help")
    else:
        if finish_price != 0:
            create_ticket = types.InlineKeyboardMarkup()
            create_button = types.InlineKeyboardButton(
                text="Создать тикет",
                callback_data="create_ticket"
            )
            create_ticket.add(create_button)
            pay_message = bot.send_message(message.chat.id, text=f"""Это конечная сумма оплаты --{finish_price}--
(необходимо отправить именно такую сумму) 
{deposit_card} - реквизиты для оплаты
После этого отправте данные от Microsoft(Xbox) по примеру
             /insert example@gmail.com:example1234
            КОГДА ВВЕЛИ НАЖМИТЕ КНОПКУ СОЗДАТЬ ТИКЕТ""", reply_markup=create_ticket)

        else:
            bot.delete_message(chat_id=shop_message_chat_id, message_id=shop_message_id)
            shop(message)

@bot.callback_query_handler(func=lambda call: True)
def caller(call):
    global quantity, products, price, inter
    # Функции срабатующии при нажатии кнопки при совпадении callback значений
    if call.data == "shop_button":
        shop(call.message)
    # добавления к общему заказу количество товара
    elif call.data in {"1000VB", "2800VB", "5000VB", "13500VB"}:
        quantity[call.data] += 1
        print(quantity)
        edit(shop_message_chat_id, shop_message_id, price_quantity)
        # Добавление наборов в одинарном количестве
    elif call.data in {"crew", "pack_touch", "pack_value_agents"}:
        if quantity[call.data] != 1:
            quantity[call.data] += 1
            print(quantity)
            edit(shop_message_chat_id, shop_message_id, price_quantity)
    elif call.data == "clear":
        quantity = defaultdict(int)  # Reset to default values
        print(quantity)
        edit(shop_message_chat_id, shop_message_id, price_quantity)
    elif call.data == "pay":
        pay(call.message)
        bot.delete_message(chat_id=shop_message_chat_id, message_id=shop_message_id)
    elif call.data == "create_ticket":
        if account_data != '':
             print(account_data)
             send_db(
                    call.message.chat.username,
                    call.message.chat.id,
                    price,
                    products,
                    account_data,
                    "not",
                    receiver()
             )
             bot.send_message(call.message.chat.id, text="Тикет успешно создан✅")
        else:
            help_message = bot.send_message(call.message.chat.id, text="Вы скорее всего не ввели данные от аккаунта Microsoft по указаному примеру выше⬆ ")
            time.sleep(10)
            bot.delete_message(chat_id=call.message.chat.id, message_id=help_message.message_id)
    else:
        pass

create_db()
print("turned on")

bot.polling(none_stop=True)