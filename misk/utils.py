import asyncio
from keyboards.others import rule_note_kb
from aiogram.types import Message


def get_content_info(message: Message):
    content_type = None
    file_id = None

    if message.photo:
        content_type = "photo"
        file_id = message.photo[-1].file_id
    elif message.video:
        content_type = "video"
        file_id = message.video.file_id
    elif message.audio:
        content_type = "audio"
        file_id = message.audio.file_id
    elif message.document:
        content_type = "document"
        file_id = message.document.file_id
    elif message.voice:
        content_type = "voice"
        file_id = message.voice.file_id
    elif message.text:
        content_type = "text"

    content_text = message.text or message.caption
    return {'content_type': content_type, 'file_id': file_id, 'content_text': content_text}


async def send_message_user(m: Message, content_type, content_text=None, file_id=None, kb=None):
    match content_type:
        case 'text':
            await m.answer( text=content_text, reply_markup=kb)
        case 'photo':
            await m.answer_photo( photo=file_id, caption=content_text, reply_markup=kb)
        case 'document':
            await m.answer_document( document=file_id, caption=content_text, reply_markup=kb)
        case 'video':
            await m.answer_video( video=file_id, caption=content_text, reply_markup=kb)
        case 'audio':
            await m.answer_audio( audio=file_id, caption=content_text, reply_markup=kb)
        case 'voice':
            await m.answer_voice( voice=file_id, caption=content_text, reply_markup=kb)


async def send_many_notes(all_notes, m: Message, ):
    for note in all_notes:
        try:
            await send_message_user(m=m, content_type=note['content_type'],
                                    content_text=note['content_text'],
                                    file_id=note['file_id'],
                                    kb=rule_note_kb(note['id']))
        except Exception as E:
            print(f'Error: {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)
