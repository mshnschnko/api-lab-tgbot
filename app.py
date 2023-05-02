from fastapi import FastAPI
import uvicorn
from aiogram.types import InlineKeyboardMarkup
import datetime

from bot import bot
import db.db_manager as db
from bot.emojis import emojis_recognize
import bot.buttons.inline_buttons as i_btn

app = FastAPI()

@app.get('/api/send_notifications')
async def send_notifications():
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
                db.set_date_with_id(id=elem['notification_id'], date=elem['time'], frequency=elem['frequency'])
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
        return {"message": "notifications have sent"}
    else:
        return {"message": "There are not notifications to send"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)