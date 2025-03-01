from keyboards.inlinebuilder import inline_builder
from keyboards.replybuilder import reply_builder


async def main_kb():
    kb = await reply_builder(text=['📝 Заметки'], sizes=1, placeholder='Воспользуйся меню👇', otk=True)
    return kb


async def main_note_kb():
    kb = await reply_builder(text=["📝 Добавить заметку", "📋 Просмотр заметок", "🏠 Главное меню"], sizes=[2, 1],
                             placeholder='Воспользуйся меню👇', otk=True)
    return kb


async def stop_fsm():
    kb = await reply_builder(text=["❌ Остановить сценарий", "🏠 Главное меню"], sizes=[1, 1],
                             placeholder="Для того чтоб остановить сценарий нажми на одну из двух кнопок👇", otk=True)
    return kb


async def add_note_check():
    kb = await reply_builder(text=["✅ Все верно", "❌ Отменить"], sizes=[1],
                             placeholder="Воспользуйся меню👇", otk=True)
    return kb


async def find_note_kb():
    kb = await reply_builder(
        text=["📋 Все заметки", "📅 По дате добавления", "🔍 Поиск по тексту", "📝 По типу контента", "🏠 Главное меню"],
        sizes=[2, 2, 1],
        placeholder="Выберите опцию👇", otk=True)
    return kb


async def rule_note_kb(note_id: int):
    kb = await inline_builder(text=["Изменить текст", "Удалить"],
                              callback_data=[f"edit_note_text_{note_id}", f"dell_note_{note_id}"], sizes=[1, 1])
    return kb


async def generate_date_keyboard(notes):
    unique_dates = [note['date_created'].strftime('%Y-%m-%d') for note in notes]
    texts = []
    callbacks_d = []
    for d in unique_dates:
        texts.append(d)
        callbacks_d.append(f"date_note_{d}")
    texts.append("Главное меню")
    callbacks_d.append("main_menu")
    kb = await inline_builder(text=texts, callback_data=callbacks_d)
    return kb


async def generate_type_content_keyboard(notes):
    unique_content = [note['content_type'] for note in notes]
    texts = []
    callbacks_d = []
    for d in unique_content:
        texts.append(d)
        callbacks_d.append(f"content_type_note_{d}")
    texts.append("Главное меню")
    callbacks_d.append("main_menu")
    kb = await inline_builder(text=texts, callback_data=callbacks_d)
    return kb

