import telebot
import sqlite3

bot = telebot.TeleBot('6418840174:AAGFGrWDJC1hezkOuZ-M_k9hZArMLCJqCSc')
name = None
#подключение к базе данных
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), password varchar(50))')
    #Подготавливает sql команду

    conn.commit()
    cur.close()
    conn.close()
    #соеденили и все закрыли
    
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Выедите ваше имя:')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()# - strip-удаляет пробелы до и после
    bot.send_message(message.chat.id, 'Выедите ваше пароль:')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users(name, password) VALUES ('%s','%s')" %(name, password))
   
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
   
    list_users = cur.fetchall()

    info = ''
    for el in list_users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)



bot.polling(none_stop=True)