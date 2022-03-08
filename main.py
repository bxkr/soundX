from datetime import datetime
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from constants import *
from data import Data
from os import path

with open(__file__.replace('main.py', 'token'), 'r') as f:
    bot = Bot(f.read())
dp = Dispatcher()


async def answer(message: Message, text: str):
    user = Data(message.from_user.id)
    await message.answer(text + CURRENT_QUOTA.format(user.quota))


@dp.message(~F.from_user.id.in_(ALLOWED_IDS))
async def no_access(message: Message):
    await message.answer(NO_ACCESS)


@dp.message(commands={'start'})
async def start_handler(message: Message):
    await answer(message, START_ANSWER)


@dp.message(commands={'import'})
async def import_handler(message: Message):
    data = Data(message.from_user.id)
    data.mode = 'import'
    await answer(message, IMPORT_START)


@dp.message(commands={'reset_quota'})
async def reset_quota(message: Message):
    data = Data(message.from_user.id)
    if (datetime.now().timestamp() - data.last_quota_reset) >= QUOTA_RESET_CD:
        data.quota = 50
        data.last_quota_reset = datetime.now().timestamp()
        await answer(message, QUOTA_SUCCESSFULLY_RESET)
    else:
        await answer(message, TOO_FAST_QUOTA_RESET)


@dp.message(F.document | F.audio)
async def import_audio(message: Message):
    sec_message = await message.answer(SENDING_FILE)
    data = Data(message.from_user.id)
    file_id = None
    ext = None
    if message.document:
        file_id = message.document.file_id
        ext = path.splitext(message.document.file_name)[1]
    elif message.audio:
        file_id = message.audio.file_id
        ext = path.splitext(message.audio.file_name)[1]
    if (file_id is not None) and ext:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        if data.quota > file.file_size / 10**6:
            await bot.download_file(file_path, DOWNLOAD_PATH + f'{message.from_user.id}_{data.files}{ext}')
            data.files += 1
            data.quota -= round(file.file_size / 10**6, 2)
            data.mode = 'editing'
            data.file_id = data.files
            await sec_message.edit_text(FILE_UPLOADED.format(data.quota))
        else:
            await sec_message.edit_text(TOO_BIG_FILE)


def main() -> None:
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
