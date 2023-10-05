import telebot
import requests # позволяет отправлять затрос по url адрессу
import json

bot = telebot.TeleBot('6418840174:AAGFGrWDJC1hezkOuZ-M_k9hZArMLCJqCSc')
API = ''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, напиши название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()# - strip-удаляет пробелы до и после, lower - приводит к нижнему регистру 
    res = requests.get(f'ссылка')
    #bot.reply_to(message, f'Сейчас в городе: {res.json()}')
    if res.status_code == 200: # 200 - это хорошая обработка
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас в городе: {temp}')
        #Изображение о погоде
        imag = 'sunny.png' if temp>5.0 else 'sun.png'
        file = open('./' + imag, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message,'Город указан не верно')
bot.polling(none_stop=True)