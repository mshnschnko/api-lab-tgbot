from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from models import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Посмотреть список текущих дел")
    keyboard.add(button_1)
    button_2 = types.KeyboardButton(text="Посмотреть список выполненных дел")
    keyboard.add(button_2)
    await bot.send_message(message.from_user.id, "Привет!\nНапиши мне что-нибудь!", reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler(commands=['set_reminder'])
async def process_set_reminder_command(message: types.Message):
    await message.answer("Введите текст напоминания:")

@dp.message_handler()
async def echo_message(msg: types.Message):
    notification = Notification(user_id=msg.from_user.id, text=msg.text)
    notification.save()
    await bot.send_message(msg.from_user.id, "Напоминание создано")

if __name__ == '__main__':
    executor.start_polling(dp)