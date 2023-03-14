# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
# import time
# import logging
# from config import TOKEN
# from models import *

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)

# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button_1 = types.KeyboardButton(text="Посмотреть список текущих дел")
#     keyboard.add(button_1)
#     button_2 = types.KeyboardButton(text="Посмотреть список выполненных дел")
#     keyboard.add(button_2)
#     await bot.send_message(message.from_user.id, "Привет!\nНапиши мне что-нибудь!", reply_markup=keyboard)

# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

# @dp.message_handler(commands=['set_reminder'])
# async def process_set_reminder_command(message: types.Message):
#     await message.answer("Введите текст напоминания:")

# @dp.message_handler()
# async def defalut_text_handler(msg: types.Message):
#     if msg.text == "Посмотреть список текущих дел":
#         for active_nots in Notification.select().where((Notification.user_id == msg.from_user.id) & (Notification.is_done == False)).dicts():
#             # await bot.send_message(msg.from_user.id, mess.message_id)
#             keyboard = types.InlineKeyboardMarkup(row_width=2)
#             edit_button = types.InlineKeyboardButton(text="📝 Редактировать", callback_data="edit")
#             complete_button = types.InlineKeyboardButton(text="✅ Выполнено", callback_data="done")
#             keyboard.add(edit_button, complete_button)
#             mess = await bot.send_message(msg.from_user.id, f"id напоминания: {active_nots['notification_id']}\n\n{active_nots['text']}\n\nВремя напоминания: {active_nots['time']}", reply_markup=keyboard)
#         # active_nots = query.dicts()
#         # print(query)
#     elif msg.text == "Посмотреть список выполненных дел":
#         for completed_nots in Notification.select().where((Notification.user_id == msg.from_user.id) & (Notification.is_done == True)).dicts():
#             mess = await bot.send_message(msg.from_user.id, f"id напоминания: {completed_nots['notification_id']}\n\n{completed_nots['text']}\n\nВремя напоминания: {completed_nots['time']}")
#             await bot.send_message(msg.from_user.id, mess.message_id)
#     else:
#         notification = Notification(user_id=msg.from_user.id, text=msg.text)
#         notification.save()
#         await bot.send_message(msg.from_user.id, f"Напоминание создано {msg.from_user.id}")

# @dp.callback_query_handler(text="edit")
# async def edit_notification(callback: types.CallbackQuery):
#     not_id_start = callback.message.text.find("id напоминания: ") + len("id напоминания: ")
#     not_id_end = callback.message.text.find("\n")
#     not_id = int(callback.message.text[not_id_start:not_id_end])
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     finish_edit_button = types.InlineKeyboardButton(text="Редактировать текст", callback_data="finish_edit")
#     finish_edit_button = types.InlineKeyboardButton(text="Завершить редактирование", callback_data="finish_edit")
#     keyboard.add(finish_edit_button)
#     await callback.message.answer(f"Выбрано напоминание №{not_id}. Для завершения редактирования отправьте сообщение с новым текстом и нажмите кнопку ниже", reply_markup=keyboard)

# @dp.callback_query_handler(text="done")
# async def done_notification(callback: types.CallbackQuery):
#     not_id_start = callback.message.text.find("id напоминания: ") + len("id напоминания: ")
#     not_id_end = callback.message.text.find("\n")
#     not_id = int(callback.message.text[not_id_start:not_id_end])
#     notification = Notification(is_done = True)
#     notification.notification_id = not_id
#     notification.save()
#     await callback.message.answer("Готово!")

# @dp.callback_query_handler(text="finish_edit")
# async def finish_edit_notification(callback: types.CallbackQuery):
#     not_id_start = callback.message.text.find("Выбрано напоминание №") + len("Выбрано напоминание №")
#     not_id_end = callback.message.text.find(". Для")
#     not_id = int(callback.message.text[not_id_start:not_id_end])
#     await bot.copy_message(chat_id=callback.message.chat.id, from_chat_id=callback.message.chat.id, message_id=callback.message.message_id+1)
#     # await callback.message.answer(rep_mes)

# if __name__ == '__main__':
#     executor.start_polling(dp)