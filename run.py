import asyncio
from aiogram.utils import executor
# import threading
# import uvicorn

# from fastapi import FastAPI
import os

from bot.server import dp, bot
from bot.notifier import scheduler, job


# app = FastAPI()
# # uvicorn.run(app, host="0.0.0.0", port=8000)

# def run_app():
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# thr = threading.Thread(target=run_app)


# @app.get('/api/send_notifications')
# async def send_notifications():
#     # thr.join()
#     await job()
#     # thr.start()
#     print("GET")


async def on_startup(_):
    # run_app()
    # thr.start()
    asyncio.create_task(scheduler())

# async def on_shutdown(_):
    # thr.join()


# def start_bot(dp, loop):
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(executor.start_polling(dp, skip_updates=True))

# async def start():
#     await dp.start_polling(bot)

if __name__ == '__main__':
    # thr.start()
    # loop = asyncio.new_event_loop()
    # t1 = threading.Thread(target=lambda dp, loop: start_bot(dp, loop), args=([dp, loop]))
    # t1.start()
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # t1.join()
    # thr.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # thr.join()