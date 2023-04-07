from typing import Union, Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message
from aiogram.utils.exceptions import MessageNotModified

import db.db_manager as db
from bot import reminders
from bot.buttons.inline_buttons import inline_kb_edit1_back
from bot.buttons.reply_buttons import mainMenu
from bot.identifier import reminder_recognize_from_id
from bot.emojis import emojis_recognize, EMOJI_DONE, EMOJI_NOT_DONE

from db.models import *


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
                                              ReplyKeyboardMarkup] = None
                                ) -> None:
    text, id = reminder_recognize_from_id(callback_query.message.text)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=data,
                                reply_markup=markup)


async def handler_edit_reminder(callback_query: CallbackQuery, bot: Bot) -> None:
    id = callback_query.data[5:]
    reminder = db.find_by_id(id=id)
    stick_done, stick_type = emojis_recognize(reminder.is_done, reminder.notification_type)
    if reminder.notification_type != 'book':
        result_string = f'{stick_done} {stick_type} - {reminder.text}:\n{reminder.time}\n id:{reminder.notification_id}'
    else:
        result_string = f'{stick_done} {stick_type} - {reminder.text}\n id:{reminder.notification_id}'
    
    attachments = list()
    files = list()
    if not reminder.attachments is None:
        attachments = reminder.attachments.split(';')
        attachments.pop(-1)
        for attachment in attachments:
            file_info = attachment.split(',')
            files.append({'id':file_info[0],
                          'type':file_info[1]})
    
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=result_string,
                                reply_markup=inline_kb_edit1_back)
    
    for idx, file in enumerate(files):
        print(file['type'])
        if file['type'] == 'document':
            await bot.send_document(chat_id=reminder.user_id, document=file['id'], caption=f"{idx+1}")
            # media.attach_document(document=file['id'])
        if file['type'] == 'photo':
            await bot.send_photo(chat_id=reminder.user_id, photo=file['id'], caption=f"{idx+1}")
            # media.attach_photo(photo=file['id'])
        if file['type'] == 'video':
            await bot.send_video(chat_id=reminder.user_id, video=file['id'], caption=f"{idx+1}")
            # media.attach_video(video=file['id'])
        if file['type'] == 'audio':
            await bot.send_audio(chat_id=reminder.user_id, audio=file['id'], caption=f"{idx+1}")


async def handler_done_reminder(callback_query: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback_query.id, text="Статус изменен")
    text, id = reminder_recognize_from_id(callback_query.message.text)
    reminder = reminders.done_reminder(id)
    print(reminder)
    if text[:14] == 'Напоминание:\n\n':
        text = text.split('Напоминание:\n\n')[1]
    if reminder.is_done == 0:
        not_done_text = text[1:]
        result_string = EMOJI_NOT_DONE + not_done_text
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=result_string,
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
        result_string = f'Напоминание "{reminder.title}" было удалено'

    await send_callback_answer(bot=bot,
                               callback_query=callback_query,
                               data="Выберите в меню:",
                               markup=mainMenu,
                               query=result_string)
