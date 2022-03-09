from os import rename, remove
from datetime import datetime
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from constants import *
from data import Data
from utils import *
import re

from pydub import AudioSegment

with open(__file__.replace('main.py', 'token'), 'r') as f:
    bot = Bot(f.read())
dp = Dispatcher()


async def answer_with_quota(message: Message, main_text: str, **other):
    user = Data(message.from_user.id)
    await message.answer(main_text + CURRENT_QUOTA.format(round(user.quota, 2)), **other)


async def return_to_menu(message: Message):
    await message.answer(EDITING_MENU, reply_markup=EDITING_KEYBOARD)


def reset_data(data: Data):
    del data.mode
    del data.file_id
    del data.ext
    del data.old_name


@dp.message(~F.from_user.id.in_(ALLOWED_IDS))
async def no_access(message: Message):
    await message.answer(NO_ACCESS)


@dp.message(commands={'start'})
async def start_handler(message: Message):
    await answer_with_quota(message, START_ANSWER)
    data = Data(message.from_user.id)
    reset_data(data)


@dp.message(commands={'import'})
async def import_handler(message: Message):
    data = Data(message.from_user.id)
    reset_data(data)
    data.mode = 'import'
    await answer_with_quota(message, IMPORT_START)


@dp.message(commands={'reset_quota'})
async def reset_quota(message: Message):
    data = Data(message.from_user.id)
    if (datetime.now().timestamp() - data.last_quota_reset) >= QUOTA_RESET_CD:
        data.quota = 50
        data.last_quota_reset = datetime.now().timestamp()
        await answer_with_quota(message, QUOTA_SUCCESSFULLY_RESET)
    else:
        await answer_with_quota(message, TOO_FAST_QUOTA_RESET)


@dp.message((F.document | F.audio) & F.from_user.id.func(lambda uid: Data(uid).mode == 'import'))
async def import_audio(message: Message):
    data = Data(message.from_user.id)
    sec_message = await message.answer(SENDING_FILE)
    file_id = None
    ext = None
    old_name = None
    if message.document:
        file_id = message.document.file_id
        old_name = message.document.file_name
        ext = extract_extension(message.document.file_name)
    elif message.audio:
        file_id = message.audio.file_id
        old_name = message.audio.file_name
        ext = extract_extension(message.audio.file_name)
    if (file_id is not None) and (ext in ALLOWED_FORMATS):
        file = await bot.get_file(file_id)
        file_path = file.file_path
        if data.quota > file.file_size / 10 ** 6:
            await bot.download_file(file_path, DOWNLOAD_PATH + f'user{message.from_user.id}_{data.files}.{ext}')
            data.files += 1
            data.quota -= file.file_size / 10 ** 6
            data.mode = 'editing'
            data.ext = ext
            data.old_name = old_name
            data.file_id = data.files - 1
            await sec_message.edit_text(FILE_UPLOADED.format(round(data.quota, 2)))
            await message.answer(EDITING_MENU, reply_markup=EDITING_KEYBOARD)
        else:
            await sec_message.edit_text(TOO_BIG_FILE)


@dp.message((F.text == AUDIO) & F.from_user.id.func(lambda uid: Data(uid).mode == 'editing'))
async def audio_refresh(message: Message):
    data = Data(message.from_user.id)
    song = AudioSegment.from_file(__file__.replace('main.py', f'user{data.suid}_{data.file_id}.{data.ext}'), data.ext)
    await message.answer(REFRESH_AUDIO.format(data.file_id, data.old_name, data.ext, min_sec(song.duration_seconds)),
                         reply_markup=EXPORT_KEYBOARD, parse_mode='html')


@dp.message((F.text == TRIM) & F.from_user.id.func(lambda uid: Data(uid).mode == 'editing'))
async def trim_mode(message: Message):
    data = Data(message.from_user.id)
    data.mode = 'trim'
    await message.answer(TRIM_SEND, reply_markup=SIMPLE_KEYBOARD(CANCEL + C_TRIMMING), parse_mode='html')


@dp.message(F.from_user.id.func(lambda uid: Data(uid).mode in ['trim', 'pitch', 'volume']) &
            (F.text.startswith(CANCEL) | (F.text == '/cancel')))
async def return_to_editing(message: Message):
    data = Data(message.from_user.id)
    data.mode = 'editing'
    await message.answer(CANCELED + EDITING_MENU, reply_markup=EDITING_KEYBOARD)


@dp.message(F.from_user.id.func(lambda uid: Data(uid).mode == 'trim') & F.text.regexp('\d+:\d\d - \d+:\d\d'))
async def trim_confirm(message: Message):
    await message.answer(CONFIRM_TRIM.format(message.text), reply_markup=CONFIRM_KEYBOARD('trim' + message.text))


@dp.callback_query(F.from_user.id.func(lambda uid: Data(uid).mode == 'trim') &
                   F.data.regexp('trim\d+:\d\d - \d+:\d\d'))
async def trim(callback_query: CallbackQuery):
    await callback_query.answer(CATCH_TRIM)
    data = Data(callback_query.from_user.id)
    query = re.search(r'(\d+):(\d\d) - (\d+):(\d\d)', callback_query.data)
    seconds_start = int(query[1]) * 60 + int(query[2])
    seconds_end = int(query[3]) * 60 + int(query[4])
    song = AudioSegment.from_file(__file__.replace('main.py', f'user{data.suid}_{data.file_id}.{data.ext}'),
                                  data.ext)
    if seconds_start > seconds_end:
        await callback_query.message.answer(X_BIGGER_THAN_Y)
        return
    if seconds_end > song.duration_seconds:
        await callback_query.message.answer(Y_BIGGER_THAN_LENGTH)
        return
    if seconds_start == seconds_end:
        await callback_query.message.answer(X_EQUALS_Y)
        return
    del song
    rename(f'user{data.suid}_{data.file_id}.{data.ext}', f'user{data.suid}_{data.file_id}_old.{data.ext}')
    song = AudioSegment.from_file(__file__.replace('main.py', f'user{data.suid}_{data.file_id}_old.{data.ext}'),
                                  data.ext)
    new_song = song[seconds_start * 1000:seconds_end * 1000]
    new_song.export(f'user{data.suid}_{data.file_id}.{data.ext}', data.ext)
    remove(f'user{data.suid}_{data.file_id}_old.{data.ext}')
    await callback_query.message.answer(TRIM_COMPLETED.format(min_sec(new_song.duration_seconds)))
    await return_to_menu(callback_query.message)
    data.mode = 'editing'


@dp.callback_query((F.data == 'export') & F.from_user.id.func(lambda uid: Data(uid).mode == 'editing'))
async def export(callback_query: CallbackQuery):
    data = Data(callback_query.from_user.id)
    document = FSInputFile(f'user{data.suid}_{data.file_id}.{data.ext}', data.old_name)
    await callback_query.message.answer_document(document)


@dp.message(F.text.in_([PITCH, VOLUME]) &
            F.from_user.id.func(lambda uid: (Data(uid).mode is not None) and Data(uid).mode != 'import'))
async def not_implemented(message: Message):
    await message.answer('not implemented')


def main() -> None:
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
