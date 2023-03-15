from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text


bot = Bot(token='5936149193:AAEfsDfqeMaDDLmERqhM1-iJgY73kFO7hyA')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Otpusk', 'Girls with Makarow']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Please, choose the serial', reply_markup=keyboard)


@dp.message_handler(Text(equals='Otpusk'))
async def otpusk(message: types.Message):
    await message.answer('Peasant viewing: https://vsetam.net/9121-otpusk_2021.html')


@dp.message_handler(Text(equals='Girls with Makarow'))
async def girls(message: types.Message):
    await message.answer('pleasant viewing: https://poisk.vsetam.net/9388-devushki-s-makarovym-3-sezon-2022-10-27.html')



if __name__ == '__main__':
    executor.start_polling(dp)