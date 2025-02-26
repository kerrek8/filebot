from keyboards.replybuilder import reply_builder


async def main_kb():
    kb = await reply_builder(text=['📝 Заметки'], sizes=1, placeholder='Воспользуйся меню👇', otk=True)
    return kb
