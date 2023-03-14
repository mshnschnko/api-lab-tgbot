from aiogram import types
from aiogram.dispatcher import FSMContext
import bot.buttons.inline_buttons as i_btn
import bot.buttons.reply_buttons as r_btn
from bot import dp, bot, reminders, storage
from bot.handlers.callback_handlers import handler_edit_reminder, handler_done_reminder, handler_delete_reminder
from bot.handlers.show_handlers import handler_show_all, handler_show_permanent, \
    handler_show_temporary, handler_show_bookmarks
from bot.forms.answer_forms import answer_forms
from bot.forms.forms import FormTemp, FormPerm, FormBookmark
from bot.handlers import buttons_handlers as hand_btn, callback_handlers as hand_clb
from bot.access import back_access


@dp.message_handler(lambda message: message.text.startswith('Создать новое'))
async def send_start_creation(message: types.Message):
    await hand_btn.send_message(message=message,
                                data="Выберите тип напоминания:",
                                markup=i_btn.inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'btn_cancel')
async def process_callback_btn_cancel(callback_query: types.CallbackQuery):
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Отмена",
                                        markup=r_btn.mainMenu)


@dp.callback_query_handler(lambda c: c.data == 'cancel_adding', state='*')
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Отменено",
                                        delete=True)


@dp.callback_query_handler(lambda c: c.data == 'btn_temp')
async def process_callback_btn_temp(callback_query: types.CallbackQuery):
    await FormTemp.title.set()
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Напишите текст напоминания:",
                                        markup=i_btn.inline_kb2,
                                        delete=True)


@dp.message_handler(state=FormTemp.title)
async def process_title_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FormTemp.next()
    await hand_clb.send_forms_answer(bot=bot,
                                     message=message,
                                     data=f"Напишите дату (опционально) и время напоминания в формате yyyy-mm-dd HH:MM:SS {data['title']}",
                                     markup=i_btn.inline_kb2)


@dp.message_handler(state=FormTemp.date)
async def process_date_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

        answer = reminders.add_reminder(user_id=message.from_id,
                                        notification_type='temp',
                                        text=data['title'],
                                        date=data['date'],)
        
        await hand_clb.send_forms_answer(bot=bot,
                                         message=message,
                                         data=answer_forms(answer),
                                         markup=i_btn.inline_kb_edit1)
    await state.finish()


##############################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_perm')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await FormPerm.title.set()
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Напишите текст напоминания:",
                                        markup=i_btn.inline_kb2,
                                        delete=True)


@dp.message_handler(state=FormPerm.title)
async def process_title_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FormPerm.next()
    await hand_clb.send_forms_answer(bot=bot,
                                     message=message,
                                     data="Напишите дату (опционально) и время напоминания в формате yyyy-mm-dd HH:MM:SS:",
                                     markup=i_btn.inline_kb2)


@dp.message_handler(state=FormPerm.date)
async def process_date_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

    await FormPerm.next()
    await hand_clb.send_forms_answer(bot=bot,
                                     message=message,
                                     data="Введите периодичность в минутах:",
                                     markup=i_btn.inline_kb2)


@dp.message_handler(state=FormPerm.frequency)
async def process_frequency_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['frequency'] = message.text

        answer = reminders.add_reminder(user_id=message.from_id,
                                        notification_type='perm',
                                        text=data['title'],
                                        date=data['date'],
                                        frequency=data['frequency'])

        await hand_clb.send_forms_answer(bot=bot,
                                         message=message,
                                         data=answer_forms(answer),
                                         markup=i_btn.inline_kb_edit1)
    await state.finish()


#################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_book')
async def process_callback_btn_book(callback_query: types.CallbackQuery):
    await FormBookmark.title.set()
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Enter title of bookmark:",
                                        markup=i_btn.inline_kb2,
                                        delete=True)


@dp.message_handler(state=FormBookmark.title)
async def process_title_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

        answer = reminders.add_reminder(user_id=message.from_id,
                                        notification_type='book',
                                        text=data['title'],
                                        date=None)

        await hand_clb.send_forms_answer(bot=bot,
                                         message=message,
                                         data=answer_forms(answer),
                                         markup=i_btn.inline_kb_edit1)
    await state.finish()


#################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_done')
async def process_callback_btn_done(callback_query: types.CallbackQuery):
    """Done only 1 reminder by identificator"""
    await handler_done_reminder(callback_query=callback_query, bot=bot)


@dp.callback_query_handler(lambda c: c.data == 'btn_delete')
async def process_callback_btn_delete(callback_query: types.CallbackQuery):
    """Delete only 1 reminder by identificator"""
    await handler_delete_reminder(callback_query=callback_query, bot=bot)
    # Доделать появление списка при удалении


@dp.callback_query_handler(lambda c: c.data == 'btn_edit')
async def process_callback_btn_edit(callback_query: types.CallbackQuery):
    # cделать проверку и переадрессацию на кнопку реплая исходя из темп или перм
    await storage.set_data(chat=callback_query.message.from_user.id, data={"text": callback_query.message.text,
                                                 "markup": i_btn.inline_kb_edit1_back})
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit2)


@dp.callback_query_handler(lambda c: c.data == 'btn_back')
async def process_callback_btn_back(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_text')
async def process_callback_btn_edit_text(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data="EDIT TEXT",
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_date')
async def process_callback_btn_edit_date(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data="EDIT DATE/TIME",
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_type')
async def process_callback_btn_edit_type(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data="EDIT TYPE",
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_frq')
async def process_callback_btn_edit_frq(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data="EDIT FREQUENCY",
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_back_list')
async def process_callback_btn_back_list(callback_query: types.CallbackQuery):
    try:
        data = await storage.get_data(chat=callback_query.message.from_user.id)
        message, markup = await back_access(data=data)
        await hand_clb.edit_callback_message(bot=bot,
                                             callback_query=callback_query,
                                             data=message,
                                             markup=markup)
    except KeyError:
        await hand_clb.send_callback_answer(bot=bot,
                                            callback_query=callback_query,
                                            data="Choose in menu:",
                                            markup=r_btn.mainMenu,
                                            delete=True)


@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Reminder bot",
        reply_markup=r_btn.mainMenu)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_reminder(message: types.Message):
    """Delete only 1 reminder by identificator"""
    try:
        row_id = int(message.text[4:])
    except ValueError:
        await message.answer("Дядь, ну айдишник то передай а...")
        return
    answer_message = reminders.delete_reminder(row_id)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/done'))
async def add_task_to_done(message: types.Message):
    """Delete only 1 reminder by identificator"""
    try:
        row_id = int(message.text[5:])
    except ValueError:
        await message.answer("Дядь, ну айдишник то передай а...")
        return
    answer_message = reminders.done_reminder(row_id)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('Показать напоминания'))
async def show_reminders(message: types.Message):
    await hand_btn.send_message(message=message,
                                data=message.text,
                                markup=r_btn.remindersMenu)


@dp.message_handler(lambda message: message.text.startswith('Все'))
@dp.message_handler(commands=['all'])
async def show_all(message: types.Message):
    """Show all reminders in system."""
    result_string, inline_kb_to_choose = await handler_show_all(message=message)
    await storage.set_data(chat=message.from_user.id, data={"text": result_string,
                                                 "markup": inline_kb_to_choose,
                                                 "type": "all"})


@dp.message_handler(lambda message: message.text.startswith('С повторением'))
@dp.message_handler(commands=['perm'])
async def show_permanent(message: types.Message):
    """Show all permanent reminders in system."""
    result_string, inline_kb_to_choose = await handler_show_permanent(message=message)

    await storage.set_data(chat=message.from_user.id, data={"text": result_string,
                                                 "markup": inline_kb_to_choose,
                                                 "type": "perm"})


@dp.message_handler(lambda message: message.text.startswith('Разовое'))
@dp.message_handler(commands=['temp'])
async def show_temporary(message: types.Message):
    """Show all temporary reminders in system."""
    result_string, inline_kb_to_choose = await handler_show_temporary(message=message)
    await storage.set_data(chat=message.from_user.id, data={"text": result_string,
                                                 "markup": inline_kb_to_choose,
                                                 "type": "temp"})


@dp.message_handler(lambda message: message.text.startswith('Без даты'))
@dp.message_handler(commands=['book'])
async def show_bookmarks(message: types.Message):
    """Show all bookmarks in system."""
    result_string, inline_kb_to_choose = await handler_show_bookmarks(message=message)
    await storage.set_data(chat=message.from_user.id, data={"text": result_string,
                                                 "markup": inline_kb_to_choose,
                                                 "type": "book"})


@dp.message_handler(lambda message: message.text.startswith('Очистить'))
@dp.message_handler(commands=['clean'])
async def clean(message: types.Message):
    """Clean db and delete reminders which were done later."""
    await hand_btn.send_message(message=message,
                                data=reminders.delete_done_reminders(),
                                markup=r_btn.mainMenu)


@dp.message_handler(lambda message: message.text.startswith('Назад'))
async def back(message: types.Message):
    await hand_btn.send_message(message=message,
                                data=message.text,
                                markup=r_btn.mainMenu,
                                allow_sending_without_reply=True)


@dp.message_handler(lambda message: message.text.startswith('Отмена'))
async def cancel(message: types.Message):
    await hand_btn.send_message(message=message,
                                data=message.text,
                                markup=r_btn.mainMenu,
                                allow_sending_without_reply=True)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_'))
async def process_callback_edit_reminder(callback_query: types.CallbackQuery):
    await handler_edit_reminder(callback_query=callback_query, bot=bot)
