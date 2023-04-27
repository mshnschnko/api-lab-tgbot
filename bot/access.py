from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.reply_buttons import remindersMenu
from bot.reminders import get_all_reminders, get_temporary_reminders, get_bookmarks, get_permanent_reminders
from bot.forms.answer_forms import answer_forms


async def back_access(data: str) -> str:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    temp = 1
    result_string = ''

    if data['type'] == "all":
        data = get_all_reminders()
        type_string = "Напоминания"
    elif data['type'] == "perm":
        data = get_permanent_reminders()
        type_string = "Повторяющиеся напоминания"
    elif data['type'] == "temp":
        data = get_temporary_reminders()
        type_string = "Разовые напоминания"
    elif data['type'] == "book":
        data = get_bookmarks()
        type_string = "Без даты"
    else:
        raise KeyError
    if data:
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1
    else:
        result_string, inline_kb_to_choose = f"В системе нет напоминаний типа {type_string}.", remindersMenu
    return result_string, inline_kb_to_choose
