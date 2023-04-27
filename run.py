import asyncio
from aiogram.utils import executor

import os

from bot.server import dp
from bot.notifier import scheduler


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
