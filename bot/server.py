import datetime
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

import bot.buttons.inline_buttons as i_btn
import bot.buttons.reply_buttons as r_btn
from bot import dp, bot, reminders, storage
from bot.handlers.callback_handlers import handler_edit_reminder, handler_done_reminder, handler_delete_reminder
from bot.handlers.show_handlers import handler_show_all, handler_show_permanent, \
    handler_show_temporary, handler_show_bookmarks
from bot.forms.answer_forms import answer_forms
from bot.forms.forms import FormTemp, FormPerm, FormBookmark, Edit
from bot.handlers import buttons_handlers as hand_btn, callback_handlers as hand_clb
from bot.access import back_access
from bot.identifier import reminder_recognize_from_id
import db.db_manager as db
from .identifier import reminder_recognize_from_id
from .upload_to_yadisk import upload
# from run import gauth



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
        data['attachments'] = ''

    await FormTemp.next()
    await hand_clb.send_forms_answer(bot=bot,
                                     message=message,
                                     data=f"Напишите дату (опционально) и время напоминания в формате yyyy-mm-dd HH:MM:SS {data['title']}",
                                     markup=i_btn.inline_kb2)


@dp.message_handler(state=FormTemp.date)
async def process_date_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

        # answer = reminders.add_reminder(user_id=message.from_id,
        #                                 notification_type='temp',
        #                                 text=data['title'],
        #                                 date=data['date'],)
        
        # await hand_clb.send_forms_answer(bot=bot,
        #                                  message=message,
        #                                  data=answer_forms(answer),
        #                                  markup=i_btn.inline_kb_edit1)
    SkipBtn = KeyboardButton("Пропустить")
    SkipKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(SkipBtn)
    await message.answer("Если хотите добавить вложения, то пришлите файл. Иначе нажмите кнопку пропустить.", reply_markup=SkipKeyboard)
    await FormTemp.next()


@dp.message_handler(lambda message: message.text.startswith('Пропустить') or message.text.startswith('Завершить'), state=FormTemp.attachments)
async def cancel_attachments_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = reminders.add_reminder(user_id=message.from_id,
                                            notification_type='temp',
                                            text=data['title'],
                                            date=data['date'],
                                            attachments=data['attachments'])
        await message.answer(text=f"Напоминание успешно создано.\nМестное время: {str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))))[:-9] + '00'}", reply_markup=r_btn.mainMenu)
        await hand_clb.send_forms_answer(bot=bot,
                                            message=message,
                                            data=answer_forms(answer),
                                            markup=i_btn.inline_kb_edit1)
    await state.finish()


@dp.message_handler(state=FormTemp.attachments, content_types=["document", "photo", "video", "audio", "voice"])
async def add_attachments_temp(message: types.Message, state: FSMContext):
    # await message.answer("я тут")
    # if message.text == "Пропустить":
    #     return
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()
    try:
        # gdrive = GoogleDrive(gauth)
        async with state.proxy() as data:
            filename = ''
            file = None
            file_type = None
            if not message.document is None:
                file = message.document
                file_type = 'document'
                # filename = message.document.file_name + message.document.file_id
                filename = message.document.file_id
            elif not message.photo is None:
                file = message.photo[0]
                file_type = 'photo'
                filename = message.photo[0].file_id
            elif not message.video is None:
                file = message.video
                file_type = 'video'
                # filename = message.video.file_name + message.video.file_id
                filename = message.video.file_id
            elif not message.audio is None:
                file = message.audio
                file_type = 'audio'
                # filename = message.audio.file_name + message.audio.file_id
                filename = message.audio.file_id
            # elif not message.voice is None:
            #     file = message.voice
            #     file_type = 'voice'
            #     filename = message.voice.file_id
            else:
                await message.answer("Файл данного типа нельзя сохранить.")
                file = None
                return

            # dir_path = os.getcwd()
            # doc_dir = "documents"
            # await file.download(destination_file=os.path.join(dir_path, doc_dir, filename))
            # new_file = gdrive.CreateFile({'title': f'{filename}', 'parents': [{'id': '1y5Zs-VIlg_U935EHQDxLHdWXfHa5gCG3'}]})
            # new_file.SetContentFile(os.path.join(dir_path, doc_dir, filename))
            # new_file.Upload()
            # link = new_file['alternateLink']
            # i = link.find("view?usp=")
            # link = link[:i]

            # link = new_file['id']
            

            # new_file = None
            # if os.path.isfile(os.path.join(dir_path, doc_dir, filename)):
            #     os.remove(os.path.join(dir_path, doc_dir, filename))
            data['attachments'] += str(filename) + "," + file_type + ";"
            await upload(message)
            CompleteBtn = KeyboardButton("Завершить")
            CompleteKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(CompleteBtn)
            await message.answer("Файл успешно загружен. Если вы больше не хотите загружать файлы, то нажмите Завершить.", reply_markup=CompleteKeyboard)
    except Exception as ex:
        await message.answer(f"Что-то не так с файлом.\n{ex}")
        return

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
        data['attachments'] = ''

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

        # answer = reminders.add_reminder(user_id=message.from_id,
        #                                 notification_type='perm',
        #                                 text=data['title'],
        #                                 date=data['date'],
        #                                 frequency=data['frequency'])

        # await hand_clb.send_forms_answer(bot=bot,
        #                                  message=message,
        #                                  data=answer_forms(answer),
        #                                  markup=i_btn.inline_kb_edit1)
    # await state.finish()
    SkipBtn = KeyboardButton("Пропустить")
    SkipKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(SkipBtn)
    await message.answer("Если хотите добавить вложения, то пришлите файл. Иначе нажмите кнопку пропустить.", reply_markup=SkipKeyboard)
    await FormPerm.next()


@dp.message_handler(lambda message: message.text.startswith('Пропустить') or message.text.startswith('Завершить'), state=FormPerm.attachments)
async def cancel_attachments_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = reminders.add_reminder(user_id=message.from_id,
                                        notification_type='perm',
                                        text=data['title'],
                                        date=data['date'],
                                        frequency=data['frequency'],
                                        attachments=data['attachments'])
        await message.answer(text="Напоминание успешно создано.", reply_markup=r_btn.mainMenu)
        await hand_clb.send_forms_answer(bot=bot,
                                         message=message,
                                         data=answer_forms(answer),
                                         markup=i_btn.inline_kb_edit1)
    await state.finish()


@dp.message_handler(state=FormPerm.attachments, content_types=["document", "photo", "video", "audio", "voice"])
async def add_attachments_perm(message: types.Message, state: FSMContext):
    # await message.answer("я тут")
    # if message.text == "Пропустить":
    #     return
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()
    try:
        # gdrive = GoogleDrive(gauth)
        async with state.proxy() as data:
            filename = ''
            file = None
            file_type = None
            if not message.document is None:
                file = message.document
                file_type = 'document'
                # filename = message.document.file_name + message.document.file_id
                filename = message.document.file_id
            elif not message.photo is None:
                file = message.photo[0]
                file_type = 'photo'
                filename = message.photo[0].file_id
            elif not message.video is None:
                file = message.video
                file_type = 'video'
                # filename = message.video.file_name + message.video.file_id
                filename = message.video.file_id
            elif not message.audio is None:
                file = message.audio
                file_type = 'audio'
                # filename = message.audio.file_name + message.audio.file_id
                filename = message.audio.file_id
            # elif not message.voice is None:
            #     file = message.voice
            #     file_type = 'voice'
            #     filename = message.voice.file_id
            else:
                await message.answer("Файл данного типа нельзя сохранить.")
                file = None
                return

            # dir_path = os.getcwd()
            # doc_dir = "documents"
            # await file.download(destination_file=os.path.join(dir_path, doc_dir, filename))
            # new_file = gdrive.CreateFile({'title': f'{filename}', 'parents': [{'id': '1y5Zs-VIlg_U935EHQDxLHdWXfHa5gCG3'}]})
            # new_file.SetContentFile(os.path.join(dir_path, doc_dir, filename))
            # new_file.Upload()
            # link = new_file['alternateLink']
            # i = link.find("view?usp=")
            # link = link[:i]

            # link = new_file['id']
            # link = filename

            # new_file = None
            # if os.path.isfile(os.path.join(dir_path, doc_dir, filename)):
            #     os.remove(os.path.join(dir_path, doc_dir, filename))
            data['attachments'] += str(filename) + "," + file_type + ";"
            await upload(message)
            CompleteBtn = KeyboardButton("Завершить")
            CompleteKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(CompleteBtn)
            await message.answer("Файл успешно загружен. Если вы больше не хотите загружать файлы, то нажмите Завершить.", reply_markup=CompleteKeyboard)
    except Exception as ex:
        await message.answer(f"Что-то не так с файлом.\n{ex}")
        return


#################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_book')
async def process_callback_btn_book(callback_query: types.CallbackQuery):
    await FormBookmark.title.set()
    await hand_clb.send_callback_answer(bot=bot,
                                        callback_query=callback_query,
                                        data="Введите текст заметки:",
                                        markup=i_btn.inline_kb2,
                                        delete=True)


@dp.message_handler(state=FormBookmark.title)
async def process_title_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        data['attachments'] = ''
    SkipBtn = KeyboardButton("Пропустить")
    SkipKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(SkipBtn)
    await message.answer("Если хотите добавить вложения, то пришлите файл. Иначе нажмите кнопку пропустить.", reply_markup=SkipKeyboard)
    await FormBookmark.next()

    #     answer = reminders.add_reminder(user_id=message.from_id,
    #                                     notification_type='book',
    #                                     text=data['title'],
    #                                     date=None)

    #     await hand_clb.send_forms_answer(bot=bot,
    #                                      message=message,
    #                                      data=answer_forms(answer),
    #                                      markup=i_btn.inline_kb_edit1)
    # await state.finish()


@dp.message_handler(lambda message: message.text.startswith('Пропустить') or message.text.startswith('Завершить'), state=FormBookmark.attachments)
async def cancel_attachments_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = reminders.add_reminder(user_id=message.from_id,
                                        notification_type='book',
                                        text=data['title'],
                                        date=None,
                                        # frequency=data['frequency'],
                                        attachments=data['attachments'])
        await message.answer(text="Напоминание успешно создано.", reply_markup=r_btn.mainMenu)
        await hand_clb.send_forms_answer(bot=bot,
                                         message=message,
                                         data=answer_forms(answer),
                                         markup=i_btn.inline_kb_edit1)
    await state.finish()


@dp.message_handler(state=FormBookmark.attachments, content_types=["document", "photo", "video", "audio"])
async def add_attachments_book(message: types.Message, state: FSMContext):
    # await message.answer("я тут")
    # if message.text == "Пропустить":
    #     return
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()
    try:
        # gdrive = GoogleDrive(gauth)
        async with state.proxy() as data:
            filename = ''
            file = None
            file_type = None
            if not message.document is None:
                file = message.document
                file_type = 'document'
                # filename = message.document.file_name + message.document.file_id
                filename = message.document.file_id
            elif not message.photo is None:
                file = message.photo[0]
                file_type = 'photo'
                filename = message.photo[0].file_id
            elif not message.video is None:
                file = message.video
                file_type = 'video'
                # filename = message.video.file_name + message.video.file_id
                filename = message.video.file_id
            elif not message.audio is None:
                file = message.audio
                file_type = 'audio'
                # filename = message.audio.file_name + message.audio.file_id
                filename = message.audio.file_id
            # elif not message.voice is None:
            #     file = message.voice
            #     file_type = 'voice'
            #     filename = message.voice.file_id
            else:
                await message.answer("Файл данного типа нельзя сохранить.")
                file = None
                return

            # dir_path = os.getcwd()
            # doc_dir = "documents"
            # await file.download(destination_file=os.path.join(dir_path, doc_dir, filename))
            # new_file = gdrive.CreateFile({'title': f'{filename}', 'parents': [{'id': '1y5Zs-VIlg_U935EHQDxLHdWXfHa5gCG3'}]})
            # new_file.SetContentFile(os.path.join(dir_path, doc_dir, filename))
            # new_file.Upload()
            # link = new_file['alternateLink']
            # i = link.find("view?usp=")
            # link = link[:i]

            # link = new_file['id']
            # link = filename
            
            # new_file = None
            # if os.path.isfile(os.path.join(dir_path, doc_dir, filename)):
            #     os.remove(os.path.join(dir_path, doc_dir, filename))
            data['attachments'] += str(filename) + "," + file_type + ";"
            await upload(message)
            CompleteBtn = KeyboardButton("Завершить")
            CompleteKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(CompleteBtn)
            await message.answer("Файл успешно загружен. Если вы больше не хотите загружать файлы, то нажмите Завершить.", reply_markup=CompleteKeyboard)
    except Exception as ex:
        await message.answer(f"Что-то не так с файлом.\n{ex}")
        return


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
    _, id = reminder_recognize_from_id(callback_query.message.text)
    notification = db.find_by_id(id=id)
    if notification.notification_type == 'temp':
        await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit2)
    if notification.notification_type == 'perm':
        await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit_perm)
    if notification.notification_type == 'book':
        await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit_book)


@dp.callback_query_handler(lambda c: c.data == 'btn_back')
async def process_callback_btn_back(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data=callback_query.message.text,
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_text')
async def process_callback_btn_edit_text(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.id.set()
    current_state = await state.get_state()
    id = int()
    if not current_state is None:
        _, id = reminder_recognize_from_id(callback_query.message.text)
        async with state.proxy() as data:
            data['id'] = id
        await Edit.title.set()
    await hand_clb.send_callback_answer(bot=bot,
                                        data="Введите новый текст",
                                        callback_query=callback_query,
                                        delete=True)
    # await hand_clb.edit_callback_message(bot=bot,
    #                                      callback_query=callback_query,
    #                                      data="Введите новый текст",)
                                        #  markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_date')
async def process_callback_btn_edit_date(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.id.set()
    current_state = await state.get_state()
    id = int()
    if not current_state is None:
        _, id = reminder_recognize_from_id(callback_query.message.text)
        async with state.proxy() as data:
            data['id'] = id
        await Edit.date.set()
    await hand_clb.send_callback_answer(bot=bot,
                                    data="Введите новую дату",
                                    callback_query=callback_query,
                                    delete=True)
    # await hand_clb.edit_callback_message(bot=bot,
    #                                      callback_query=callback_query,
    #                                      data="Введите новую дату/время",
    #                                      markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_type')
async def process_callback_btn_edit_type(callback_query: types.CallbackQuery):
    await hand_clb.edit_callback_message(bot=bot,
                                         callback_query=callback_query,
                                         data="EDIT TYPE",
                                         markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_frq')
async def process_callback_btn_edit_frq(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.id.set()
    current_state = await state.get_state()
    id = int()
    if not current_state is None:
        _, id = reminder_recognize_from_id(callback_query.message.text)
        async with state.proxy() as data:
            data['id'] = id
        await Edit.frequency.set()
    await hand_clb.send_callback_answer(bot=bot,
                                    data="Введите новую периодичность в минутах",
                                    callback_query=callback_query,
                                    delete=True)
    # await hand_clb.edit_callback_message(bot=bot,
    #                                      callback_query=callback_query,
    #                                      data="Введите новую периодичность в минутах",
    #                                      markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_att')
async def process_callback_btn_edit_attachments(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.id.set()
    current_state = await state.get_state()
    id = int()
    if not current_state is None:
        _, id = reminder_recognize_from_id(callback_query.message.text)
        async with state.proxy() as data:
            data['id'] = id
            data['attachments'] = ''
        await Edit.attachments.set()
    await hand_clb.send_callback_answer(bot=bot,
                                    data="Выберите вариант редактирования",
                                    callback_query=callback_query,
                                    delete=True,
                                    markup=i_btn.inline_kb_edit_attachments)
    

@dp.callback_query_handler(lambda c: c.data == 'btn_add_att', state=Edit.attachments)
async def process_callback_btn_add_attachments(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.add_attachemnts.set()
    await hand_clb.send_callback_answer(bot=bot,
                                    data="Прикрепите новые вложения по одному",
                                    callback_query=callback_query,
                                    delete=True)
    

@dp.callback_query_handler(lambda c: c.data == 'btn_del_att', state=Edit.attachments)
async def process_callback_btn_del_attachments(callback_query: types.CallbackQuery, state: FSMContext):
    await Edit.del_attachments.set()
    notification = None
    async with state.proxy() as data:
        notification = db.find_by_id(data['id'])
    if len(notification.attachments) > 0:
        await hand_clb.send_callback_answer(bot=bot,
                                        data="Пришлите номера файлов для удаления, разделяя числа проеблом.",
                                        callback_query=callback_query,
                                        delete=True)
    else:
        await hand_clb.send_callback_answer(bot=bot,
                                        data="Вложений нет, удалить ничего нельзя.",
                                        callback_query=callback_query,
                                        delete=True)


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
                                            data="Выберите из меню:",
                                            markup=r_btn.mainMenu,
                                            delete=True)


@dp.message_handler(state=Edit.title)
async def edit_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
        db.edit_title_with_id(id=data['id'], data=data['title'])

        await message.answer("Текст напоминания обновлен", reply_markup=r_btn.mainMenu)
        await state.finish()


@dp.message_handler(state=Edit.date)
async def edit_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
        db.edit_date_with_id(id=data['id'], date=data['date'])

        await message.answer("Дата напоминания обновлена", reply_markup=r_btn.mainMenu)
        await state.finish()


@dp.message_handler(state=Edit.frequency)
async def edit_frequency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['frequency'] = message.text
        db.edit_frequency_with_id(id=data['id'], frequncy=data['frequency'])

        await message.answer("Периодичность напоминания обновлена", reply_markup=r_btn.mainMenu)
        await state.finish()


@dp.message_handler(lambda message: message.text.startswith('Завершить редактирование'), state=Edit.add_attachemnts)
async def edit_add_attachments(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Редактирование вложений успешно завершено.", reply_markup=r_btn.mainMenu)


@dp.message_handler(state=Edit.add_attachemnts, content_types=["document", "photo", "video", "audio"])
async def edit_add_attachments(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        filename = ''
        file = None
        file_type = None
        if not message.document is None:
            file = message.document
            file_type = 'document'
            filename = message.document.file_id
        elif not message.photo is None:
            file = message.photo[0]
            file_type = 'photo'
            filename = message.photo[0].file_id
        elif not message.video is None:
            file = message.video
            file_type = 'video'
            filename = message.video.file_id
        elif not message.audio is None:
            file = message.audio
            file_type = 'audio'
            filename = message.audio.file_id

        else:
            await message.answer("Файл данного типа нельзя сохранить.")
            file = None
            return
        link = filename
        
        data['attachments'] = str(link) + "," + file_type + ";"
        print("new = ", data['attachments'])
        db.add_attachment_with_id(id=data['id'], attachment=data['attachments'])
        comlete_att_editing_btn = KeyboardButton("Завершить редактирование")
        comlete_att_editing_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(comlete_att_editing_btn)
        await message.answer("Файл добавлен. Если хотите завершить редактирование, нажмите соответствующую кнопку.", reply_markup=comlete_att_editing_kb)
        # await state.finish()


@dp.message_handler(state=Edit.del_attachments)
async def edit_del_attachments(message: types.Message, state: FSMContext):
    # res = 0   OK
    # res = -1  OUT OF RANGE
    # res = -2  INVALID INPUT
    res = -1
    async with state.proxy() as data:
        data['attachments'] = message.text
        nums = message.text.split(' ')
        if all(list(map(str.isdigit, nums))):
            nums = list(map(lambda x: int(x)-1, nums))
            res = db.del_attachments_with_id(data['id'], nums)
        else:
            res = -2
    if res == 0:
        await message.answer("Выбранные файлы удалены.", reply_markup=r_btn.mainMenu)
    elif res == -1:
        await message.answer("Номера не соответствуют существующим вложениям.", reply_markup=r_btn.mainMenu)
    elif res == -2:
        await message.answer("Неверный ввод: возможно вы ввели буквы вместо цифр.", reply_markup=r_btn.mainMenu)
    await state.finish()


@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Вас приветствует бот-напоминалка Urban Potato! сыр",
        reply_markup=r_btn.mainMenu)


# @dp.message_handler(lambda message: message.text.startswith('/del'))
# async def del_reminder(message: types.Message):
#     """Delete only 1 reminder by identificator"""
#     try:
#         row_id = int(message.text[4:])
#     except ValueError:
#         await message.answer("Дядь, ну айдишник то передай а...")
#         return
#     answer_message = reminders.delete_reminder(row_id)
#     await message.answer(answer_message)


# @dp.message_handler(lambda message: message.text.startswith('/done'))
# async def add_task_to_done(message: types.Message):
#     """Delete only 1 reminder by identificator"""
#     try:
#         row_id = int(message.text[5:])
#     except ValueError:
#         await message.answer("Дядь, ну айдишник то передай а...")
#         return
#     answer_message = reminders.done_reminder(row_id)
#     await message.answer(answer_message)


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
                                data=reminders.delete_done_reminders(user_id=message.from_id),
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
