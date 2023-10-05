import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot('6418840174:AAGFGrWDJC1hezkOuZ-M_k9hZArMLCJqCSc')


'''----Урок 2.----'''
'''отправка видео или фото'''
'''Создание кнопок возле сообщения'''

#Кнопки для отображения при вводе
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()#разметка
    btn1 = types.KeyboardButton('Переити на сайт ☺️')
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')

    markup.row(btn1)
    markup.row(btn2,btn3)
    #отправка файла
    # 1. send_photo, _audio, _video
    file_photo = open('./photo.jpg','rb')
    bot.send_message(message.chat.id, 'Привет!')
    bot.send_photo(message.chat.id, file_photo, reply_markup=markup)
    

    
    bot.register_next_step_handler(message, on_click)# регестрация следующей функции

def on_click(message):
    if message.text == 'Переити на сайт': #принимает значение введенное пользователем
        bot.send_message(message.chat.id, 'Вы перешли на сайт')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Удаление...')


@bot.message_handler(content_types=['photo'] )
def get_photo(message):
    markup = types.InlineKeyboardMarkup()#разметка
    #add - просто для добавления
    #row - для добавления и расположения по строкам
    '''markup.add(types.InlineKeyboardButton('Переити на сайт', url='https://google.com'))
    markup.add(types.InlineKeyboardButton('Удалить фото', callback_data = 'delete'))
    markup.add(types.InlineKeyboardButton('Изменить текст', callback_data = 'edit'))'''

    btn1 = types.InlineKeyboardButton('Переити на сайт', url='https://google.com')
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data = 'delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data = 'edit')

    markup.row(btn1)
    markup.row(btn2,btn3)
    
    bot.reply_to(message,'Красивое фото', reply_markup=markup)#передаем значение разметки вместе с сообщением

# декоратор для обработки кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
        # Удаляет предпоследнее сообщение 1. получаем id чата, 2. id Сообщения для удаления 
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id) 
        #Изменяем сообщение 1. Текст для изменения 2. получаем id чата 3. id Сообщения для удаления  

'''-----Урок 1.------'''
#@bot.message_handler(commands=['start','hello'] ) #Дикаратор для функции 
#def main(message):#Хранит информацию про чат
    #bot. send_message(message.chat.id, message)# Просмотр всех данных о пользователе и о боте
'''@bot.message_handler(commands=['start'] ) #Дикаратор для функции 
def main(message):#Хранит информацию про чат
    bot. send_message(message.chat.id, 'Привет!')'''

@bot.message_handler(commands=['help'] )
 
def main(message):#Хранит информацию про чат
    bot. send_message(message.chat.id, '<u><b>Помощь</b></u>', parse_mode='html')# parse_mode - для форматированиея   

@bot.message_handler(commands=['hello'] ) 
def main(message):
    bot. send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
# f - Форматированная строка


'''Отправка на сайт'''
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://itproger.com')


'''Обработка обычного текста'''
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':#обязательно приводим к одному регистру
        bot. send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID:{message.from_user.id}' )#ответ на предыдущее сообщение


bot.polling(none_stop=True)



'''1.Чтоб сделать кнопки в боте нужно обратиться к фазер боту
прописать /setcomands пишем название-описание'''