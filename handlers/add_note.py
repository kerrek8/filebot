from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from db.dao import add_note
from keyboards.others import main_note_kb, stop_fsm, add_note_check
# from loader import bot
from misk.utils import get_content_info, send_message_user

router = Router()


class AddNoteStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    check_state = State()  # Финальна проверка


@router.message(F.text == '📝 Заметки')
async def start_note(message: Message, state: FSMContext):
    await state.clear()
    kb = await main_note_kb()
    await message.answer('Ты в меню добавления заметок. Выбери необходимое действие.',
                         reply_markup=kb)


@router.message(F.text == '📝 Добавить заметку')
async def start_add_note(message: Message, state: FSMContext):
    await state.clear()
    kb = await stop_fsm()
    await message.answer('Отправь сообщение в любом формате (текст, медиа или медиа + текст). '
                         'В случае если к медиа требуется подпись - оставь ее в комментариях к медиа-файлу ',
                         reply_markup=kb)
    await state.set_state(AddNoteStates.content)


@router.message(AddNoteStates.content)
async def handle_user_note_message(message: Message, state: FSMContext):

    content_info = get_content_info(message)
    print(content_info)
    if content_info.get('content_type'):
        await state.update_data(**content_info)

        text = (f"Получена заметка:\n"
                f"Тип: {content_info['content_type']}\n"
                f"Подпись: {content_info['content_text'] if content_info['content_text'] else 'Отсутствует'}\n"
                f"File ID: {content_info['file_id'] if content_info['file_id'] else 'Нет файла'}\n\n"
                f"Все ли верно?")
        await send_message_user(m=message, content_type=content_info['content_type'], content_text=text,
                                file_id=content_info['file_id'],
                                kb=add_note_check())

        await state.set_state(AddNoteStates.check_state)
    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )
        await state.set_state(AddNoteStates.content)


@router.message(AddNoteStates.check_state, F.text == '✅ Все верно')
async def confirm_add_note(message: Message, state: FSMContext):
    note = await state.get_data()
    kb = await main_note_kb()
    await add_note(user_id=message.from_user.id, content_type=note.get('content_type'),
                   content_text=note.get('content_text'), file_id=note.get('file_id'))
    await message.answer('Заметка успешно добавлена!', reply_markup=kb)
    await state.clear()


@router.message(AddNoteStates.check_state, F.text == '❌ Отменить')
async def cancel_add_note(message: Message, state: FSMContext):
    kb = await main_note_kb()
    await message.answer('Добавление заметки отменено!', reply_markup=kb)
    await state.clear()
