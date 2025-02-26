from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.dao import set_user
from keyboards.others import main_kb

router = Router()


@router.message(F.text == '🏠 Главное меню')
@router.message(CommandStart())
async def start(m: Message, state: FSMContext):
    await state.clear()
    user = await set_user(tg_id=m.from_user.id, username=m.from_user.username,
                          full_name=m.from_user.full_name)
    greeting = f"Привет {m.from_user.full_name}! Выбери необходимое действие"
    if user is None:
        greeting = f"Привет, новый пользователь! Выбери необходимое действие"
    kb = await main_kb()
    await m.answer(greeting, reply_markup=kb)


@router.message(F.text == '❌ Остановить сценарий')
async def stop_fsm(message: Message, state: FSMContext):
    await state.clear()
    kb = await main_kb()
    await message.answer(f"Сценарий остановлен. Для выбора действия воспользуйся клавиатурой ниже",
                         reply_markup=kb)


@router.callback_query(F.data == 'main_menu')
async def main_menu_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы вернулись в главное меню.')
    kb = await main_kb()
    await call.message.answer(f"Привет, {call.from_user.full_name}! Выбери необходимое действие",
                              reply_markup=kb)
