import telebot
import sqlite3
from telebot import types
import datetime

bot = telebot.TeleBot('6418840174:AAGFGrWDJC1hezkOuZ-M_k9hZArMLCJqCSc')
division, surname, name, patronymic, start_date, end_date, type_request  = None, None, None, None, None, None, None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('ArchiveDB.sql')
    cur = conn.cursor()
    #cur.execute('DROP TABLE request')
    cur.execute('CREATE TABLE IF NOT EXISTS request (id int auto_increment PRIMARY KEY, division varchar(10), surname varchar(50), name varchar(50), patronymic varchar(50), start_date int, end_date int, type_request varchar(50))')
    #Подготавливает sql команду

    conn.commit()
    cur.close()
    conn.close()
    #соеденили и все закрыли
    markup_web = types.ReplyKeyboardMarkup()
    btn_web = types.KeyboardButton('Открыть веб-страницу', web_app = types.WebAppInfo('https://vstarostina.github.io/Web_telebot/'))
    markup_web.add(btn_web)
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_division1 = types.InlineKeyboardButton('ПП 1',callback_data='ПП 1')
    btn_division2 = types.InlineKeyboardButton('ПП 2',callback_data='ПП 2')
    btn_division3 = types.InlineKeyboardButton('ПП 3',callback_data='ПП 3')
    btn_division4 = types.InlineKeyboardButton('ПП 4',callback_data='ПП 4')
    btn_division5 = types.InlineKeyboardButton('ПП 5',callback_data='ПП 5')
    btn_division6 = types.InlineKeyboardButton('ПП 6',callback_data='ПП 6')
    btn_divisionPMR = types.InlineKeyboardButton('ПМР',callback_data='ПМР')
    markup.add(btn_division1,btn_division2,btn_division3,btn_division4,btn_division5,btn_division6,btn_divisionPMR)
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!',reply_markup=markup_web)
    bot.send_message(message.chat.id,'Вы перешли на бот регистрации запросов. Какое  поликлиническое подразделение вас интересует? ', reply_markup=markup)

def employee_name(message):
    global surname,name, patronymic
    full_name = message.text.strip().split(' ')
    if len(full_name) == 3:
        surname = full_name[0].capitalize()
        name = full_name[1].capitalize()
        patronymic = full_name[2].capitalize()
        bot.send_message(message.chat.id, f'Имя сотрудника зарегистрировано.\nФамилия: {surname}\nИмя: {name}\nОтчество: {patronymic}\nВедите период работы (формат ввода: ****-****)')
        bot.register_next_step_handler(message, work_period)
    else: 
        bot.reply_to(message,'Ваш ввод не соответствует формату: Фамилия Имя Отчество.')
        bot.send_message(message.chat.id, 'Введите фмилию имя отчество сотрудника:')
        bot.register_next_step_handler(message, employee_name)

def work_period(message):
    global start_date, end_date
    period = message.text.strip().split('-')
    markup_success = types.InlineKeyboardMarkup()
    markup_refusal = types.InlineKeyboardMarkup()
    btn_RequestSalary = types.InlineKeyboardButton('О заработной плате', callback_data = 'RequestSalary')
    btn_RequestOrders = types.InlineKeyboardButton('О стаже работы', callback_data = 'RequestOrders')
    btn_refusalYear = types.InlineKeyboardButton('Ввести период', callback_data = 'refusalYear')
    markup_success.add(btn_RequestSalary,btn_RequestOrders)
    markup_refusal.add(btn_refusalYear)
    #print(datetime.date.year)
    #if int(period[0])<datetime.date.year - 75:
    try:
        if int(period[0])<1965 or int(period[1])>2023:
            bot.send_message(message.chat.id, 'Данных за этот период не существует', reply_markup=markup_refusal)
        else:
            start_date = period[0]
            end_date = period[1]
            bot.send_message(message.chat.id, f'Период работы сотрудника зарегестрирован.\nПериод с {period[0]} по {period[1]}\nКакой запрос вы хотите зарегистрировать?', reply_markup=markup_success)
    except ValueError:
        bot.send_message(message.chat.id,'Вы ввели не числа.\nВведите числовые значения в формате: ****-**** ')
        bot.register_next_step_handler(message, work_period)

def entering_data_request(message):
    #bot.send_message(message.chat.id, 'Запрос зарегестрирован!')
    conn = sqlite3.connect('ArchiveDB.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO request (division, surname, name, patronymic, start_date, end_date, type_request) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(division, surname, name, patronymic, start_date, end_date, type_request))
    
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_list_requests = types.InlineKeyboardButton('Спиок запросов', callback_data='ListRequests')
    btn_data_change = types.InlineKeyboardButton('Изменить данные запроса', callback_data='DataChange')
    markup.add(btn_list_requests,btn_data_change)
    bot.send_message(message.chat.id, 'Запрос зарегестрирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global division
    global type_request

    if callback.data == 'RequestSalary':
        type_request = 'Запрос о заработной плате'
        entering_data_request(callback.message)
    elif callback.data == 'RequestOrders':
        type_request = 'Запрос о стаже работы'
        entering_data_request(callback.message)
    elif callback.data == 'refusalYear':
        bot.register_next_step_handler(callback.message, work_period)
    elif callback.data == 'ListRequests':
        conn = sqlite3.connect('ArchiveDB.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM request')
        list_request = cur.fetchall()
        info = ''
        for el in list_request:
            info+= f'{el[0]}. Подразделение: {el[1]}\nФамилия: {el[2]}, имя: {el[3]}, отчество: {el[4]}\nПериод с {el[5]} по {el[6]}\n {el[7]}\n\n'
        
        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id, info)
    elif callback.data == 'ПП 1' or 'ПП 2' or 'ПП 3' or 'ПП 4' or 'ПП 5' or 'ПП 6' or 'ПМР':
        division = callback.data
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'Вы выбрали {callback.data}.\nВведите фмилию имя отчество сотрудника.')
        bot.register_next_step_handler(callback.message, employee_name)



@bot.message_handler()
def text_reception(message):
    bot.send_message(message.chat.id, 'Введите коректное значение или нажмите на кнопку')


bot.polling(none_stop=True)