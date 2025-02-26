from typing import Optional

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def reply_builder(text: str | list[str], sizes: int | list[int] = 2,
                        send_loc: Optional[bool] = False, placeholder: Optional[str] = None,
                        otk: Optional[bool] = None) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    text = [text] if isinstance(text, str) else text
    sizes = [sizes] if isinstance(sizes, int) else sizes
    [builder.button(text=txt, request_location=send_loc) for txt in text]
    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder=placeholder, one_time_keyboard=otk)
