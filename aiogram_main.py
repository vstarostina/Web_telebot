from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6418840174:AAGFGrWDJC1hezkOuZ-M_k9hZArMLCJqCSc')
dp = Dispatcher(bot)

@dp.message_hendler(commands = ['start'])
async def start(message: types.Message):
    #await bot.send_message(message.chat.id,'Привет')
    await message.answer('Привет')
executor.start_polling(dp)
