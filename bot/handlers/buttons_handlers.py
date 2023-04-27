from typing import Union, Optional

from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup


async def send_message(message: Message,
                       data: str,
                       markup: Union[InlineKeyboardMarkup,
                                     ReplyKeyboardMarkup],
                       allow_sending_without_reply: Optional[bool] = None) -> None:
    await message.delete()
    await message.answer(data, reply_markup=markup, allow_sending_without_reply=allow_sending_without_reply)
