from aiogram.types import Message

from bot.core.loader import dp

@dp.channel_post()
async def handle_channel_post(message: Message):
    if message.text:
        print(f"[TEXT] {message.text}")

    if message.audio:
        print(f"[AUDIO] file_id: {message.audio.file_id}")
    
    if message.voice:
        print(f"[VOICE] file_id: {message.voice.file_id}")
    
    if message.photo:
        file_id = message.photo[-1].file_id
        print(f"[PHOTO] file_id: {file_id}")
    
    if message.document:
        print(f"[DOCUMENT] file_id: {message.document.file_id}")