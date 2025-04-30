import sqlite3
import telebot
from telebot import types
from cafig import bot_TOKEN2

bot2 = telebot.TeleBot(bot_TOKEN2)
print("turned on")

def create_connection():
    conn = sqlite3.connect("V-BucksWorld.db")
    return conn

@bot2.message_handler(commands=['start'])
def start(message):
    bot2.send_message(message.chat.id, text="Этот бот призначен для Владельца магазина RYZE, если вы не он, пошли нахуй, не для вас хуярил бота")

@bot2.message_handler(commands=['list'])
def list(message):
    global ticket_ids
    ticket_ids = dict()
    conn = create_connection()
    db = conn.cursor()
    db.execute("SELECT * FROM shop WHERE status_payment == 'not'")
    rows = db.fetchall()
    for row in rows:
        ticket = bot2.send_message(message.chat.id, text=f"""
        Покупатель: {row[0]}
        Телеграмм id: {row[1]}
        Сумма заказа: {row[2]}
        Заказаный товар: {row[3]}
        Данные Xbox: {row[4]}
        Номер заказа: {row[-1]}""")
        ticket_id = ticket.message_id
        ticket_ids.setdefault(str(row[-1]), ticket_id)
        for i in ticket_ids:
            print(type(ticket_ids[i]), ticket_ids[i])
    conn.commit()
    conn.close()
    

@bot2.message_handler(commands=['close'])
def close(message):
    try:
        numer = message.text[message.text.find(' '):]
        bot2.delete_message(chat_id=message.chat.id, message_id=ticket_ids[numer[1:]])
    except:
        pass

@bot2.message_handler(commands=['finish'])
def finish(message):
    conn = create_connection()
    db = conn.cursor()
    try:
        numer = message.text[message.text.find(' '):]
        bot2.delete_message(chat_id=message.chat.id, message_id=ticket_ids[numer[1:]])
    except:
        pass
    else:
        db.execute(f"UPDATE shop SET status_payment = 'yes' WHERE order_id = {numer[1:]}")
    conn.commit()
    conn.close()

@bot2.message_handler(commands=['delete'])
def finish(message):
    conn = create_connection()
    db = conn.cursor()
    try:
        numer = message.text[message.text.find(' '):]
        bot2.delete_message(chat_id=message.chat.id, message_id=ticket_ids[numer[1:]])
    except:
        pass
    else:
        db.execute(f"UPDATE shop SET status_payment = 'deleted' WHERE order_id = {numer[1:]}")
    conn.commit()
    conn.close()



bot2.polling(none_stop=True)