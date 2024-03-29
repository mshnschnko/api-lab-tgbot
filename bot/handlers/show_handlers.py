from typing import Tuple

from aiogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton

from bot import reminders
from bot.buttons.reply_buttons import remindersMenu, anyRemindersMenu
from bot.forms.answer_forms import answer_forms


async def handler_show_all(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_all_reminders(user_id=message.from_id)
    temp = 1
    result_string = ''
    await message.delete()
    if data:
        if show_header:
            await message.answer("Все напоминания:", reply_markup=anyRemindersMenu)
        for elem in data:
            print("elem: ", elem)
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem['notification_id']}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("Нет напоминаний в системе.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_permanent(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_permanent_reminders(user_id=message.from_id)
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Напоминания с повторением:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem['notification_id']}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("Нет напоминаний с повторением в системе.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_temporary(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_temporary_reminders(user_id=message.from_id)
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Разовые напоминания:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem['notification_id']}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("Нет разовых напоминаний.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_bookmarks(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_bookmarks(user_id=message.from_id)
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Заметки:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem['notification_id']}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("Нет заметок в системе.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose
