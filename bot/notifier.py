import asyncio
import datetime
import os
from aiogram import types

import aioschedule
from aiogram.types import InlineKeyboardMarkup

from pydrive.drive import GoogleDrive

from bot import bot
import db.db_manager as db
import bot.buttons.inline_buttons as i_btn
from bot.emojis import emojis_recognize


async def job():
    from run import gauth
    local_time = str(datetime.datetime.now())[:-9] + "00"
    print(datetime.datetime.now().timestamp())
    print(datetime.datetime.now())
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    temp = 1
    result_string = ''
    notifications = db.find_by_date(local_time)

    if notifications:
        for elem in notifications:
            print(elem)
            # print(elem[3])
            if elem['notification_type'] == 'perm':
                db.set_date_with_id(id=elem['notification_id'], date=elem['time'])
            stick_done, stick_type = emojis_recognize(elem['is_done'], elem['notification_type'])

            answer_message = f"Напоминание:\n\n" \
                             + f"{stick_done} {stick_type} - {elem['text']}:\n{elem['time']}\n id:{elem['notification_id']}"
            attachments = list()
            files = list()
            if not elem['attachments'] is None:
                attachments = elem['attachments'].split(';')
                attachments.pop(-1)
                for attachment in attachments:
                    file_info = attachment.split(',')
                    files.append({'id':file_info[0],
                                  'type':file_info[1]})
            # media = types.MediaGroup()
            # paths = list()
            # if not len(files) == 0:
            #     for idx, file in enumerate(files):
            #         print(file)
                    # try:
                    #     dir_path = os.getcwd()
                    #     doc_dir = "documents"
                    #     gdrive = GoogleDrive(gauth)
                    #     file1 = gdrive.CreateFile({'id': file})
                    #     file_to_send_path = os.path.join(dir_path, doc_dir, file)
                    #     paths.append(file_to_send_path)
                    #     file1.GetContentFile(file_to_send_path)
                    #     media.attach_document(types.InputFile(file_to_send_path), f"file_{idx}")
                    # except Exception as ex:
                    #     print(ex)

                    # if file['type'] == 'document':
                    #     media.attach_document(document=file['id'])
                    # if file['type'] == 'photo':
                    #     media.attach_photo(photo=file['id'])
                    # if file['type'] == 'video':
                    #     media.attach_video(video=file['id'])
                    # if file['type'] == 'audio':
                    #     media.attach_audio(audio=file['id'])
            await bot.send_message(chat_id=elem['user_id'], text=answer_message, reply_markup=i_btn.inline_kb_edit1)
            
            for file in files:
                if file['type'] == 'document':
                    await bot.send_document(chat_id=elem['user_id'], document=file['id'])
                    # media.attach_document(document=file['id'])
                if file['type'] == 'photo':
                    await bot.send_photo(chat_id=elem['user_id'], photo=file['id'])
                    # media.attach_photo(photo=file['id'])
                if file['type'] == 'video':
                    await bot.send_video(chat_id=elem['user_id'], video=file['id'])
                    # media.attach_video(video=file['id'])
                if file['type'] == 'audio':
                    await bot.send_audio(chat_id=elem['user_id'], audio=file['id'])
                    # media.attach_audio(audio=file['id'])

            # if not len(files) == 0:
                # await bot.send_media_group(chat_id=elem['user_id'], media=media)
            # for path in paths:
            #     if os.path.isfile(path):
            #         os.remove(path)
            # for file in files:
            #     await bot.send_document(chat_id=elem['user_id'], )

async def scheduler():
    aioschedule.every(59).seconds.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
