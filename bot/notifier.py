import asyncio
import datetime

import aioschedule
from aiogram.types import InlineKeyboardMarkup

from bot import bot
import db.db_manager as db
import bot.buttons.inline_buttons as i_btn
from bot.emojis import emojis_recognize


async def job():
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

            answer_message = f"**NOTIFICATION**\n\n" \
                             + f"{stick_done} {stick_type} - {elem['text']}:\n{elem['time']}\n id:{elem['notification_id']}"
            await bot.send_message(chat_id=elem['user_id'], text=answer_message, reply_markup=i_btn.inline_kb_edit1)

async def scheduler():
    aioschedule.every(58).seconds.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
