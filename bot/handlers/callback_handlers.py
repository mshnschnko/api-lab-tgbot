from typing import Union, Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message
from aiogram.utils.exceptions import MessageNotModified

import db.db_manager as db
from bot import reminders
from bot.buttons.inline_buttons import inline_kb_edit1_back
from bot.buttons.reply_buttons import mainMenu
from bot.identifier import reminder_recognize_from_id
from bot.emojis import emojis_recognize, EMOJI_DONE


async def send_callback_answer(bot: Bot,
                               data: str,
                               markup: Optional[Union[InlineKeyboardMarkup,
                                                ReplyKeyboardMarkup]] = None,
                               callback_query: Optional[CallbackQuery] = None,
                               query: Optional[str] = None,
                               delete: Optional[bool] = True
                               ) -> None:
    if query:
        await bot.answer_callback_query(callback_query.id, text=query)
    else:
        await bot.answer_callback_query(callback_query.id)
    if delete:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=data,
                           reply_markup=markup)


async def send_forms_answer(bot: Bot,
                            message: Message,
                            data: str,
                            markup: Union[InlineKeyboardMarkup,
                                          ReplyKeyboardMarkup]
                            ) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text=data,
        reply_markup=markup
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )


async def edit_callback_message(bot: Bot,
                                callback_query: CallbackQuery,
                                data: str,
                                markup: Union[InlineKeyboardMarkup,
                                              ReplyKeyboardMarkup]
                                ) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=data,
                                reply_markup=markup)


async def handler_edit_reminder(callback_query: CallbackQuery, bot: Bot) -> None:
    id = callback_query.data[5:]
    reminder = db.find_by_id(id=id)
    stick_done, stick_type = emojis_recognize(reminder[4], reminder[2])
    if reminder[2] != 'book':
        result_string = f'{stick_done} {stick_type} - {reminder[1]}:\n{reminder[3]}\n id:{reminder[0]}'
    else:
        result_string = f'{stick_done} {stick_type} - {reminder[1]}\n id:{reminder[0]}'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=result_string,
                                reply_markup=inline_kb_edit1_back)


async def handler_done_reminder(callback_query: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback_query.id, text="Reminder was done.")
    text, id = reminder_recognize_from_id(callback_query.message.text)
    reminder = reminders.done_reminder(id)
    print(reminder)
    if text[1] == '*':
        text = text.split('**NOTIFICATION**\n\n')[1]
    if reminder.is_done == 0:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=callback_query.message.text,
                                    reply_markup=callback_query.message.reply_markup)
    else:
        done_text = text[1:]
        result_string = EMOJI_DONE + done_text
        try:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=result_string,
                                        reply_markup=callback_query.message.reply_markup)
        except MessageNotModified:
            pass


async def handler_delete_reminder(callback_query: CallbackQuery, bot: Bot) -> None:
    _, id = reminder_recognize_from_id(callback_query.message.text)
    reminder = reminders.delete_reminder(id)

    if isinstance(reminder, str):
        result_string = reminder
    else:
        result_string = f'Reminder "{reminder.title}" was deleted'

    await send_callback_answer(bot=bot,
                               callback_query=callback_query,
                               data="Choose in menu:",
                               markup=mainMenu,
                               query=result_string)
