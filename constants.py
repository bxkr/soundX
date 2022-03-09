from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

DATA_PATH = __file__.replace('constants.py', 'database.json')
NO_ACCESS = 'К сожалению, работа этого бота связана с файлами больших размеров. Для публичного доступа к боту ' \
            'потребуются хранилища. У разработчика недостаточно средств, чтобы развернуть их, поэтому пока, доступ к ' \
            'боту ограничен.'
ALLOWED_IDS = {692755648}
START_ANSWER = 'Привет! Этот бот может делать всякие штуки с аудио.\nЧтобы начать, используй /import.'
ALLOWED_FORMATS = ['mp3', 'wav', 'flac', 'aac', 'mp4a', 'opus', 'ogg', 'aiff', 'wma']
IMPORT_START = f'Отправь файл размером не более 10 мегабайт.\nРазрешённые форматы файла: {", ".join(ALLOWED_FORMATS)}.'
CURRENT_QUOTA = '\n\nТекущая квота на файлы: {} мегабайт.'
QUOTA_RESET_CD = 86400
TOO_FAST_QUOTA_RESET = 'Вы слишком часто сбрасываете квоту.\nКвоту можно сбрасывать раз в 24 часа.'
QUOTA_SUCCESSFULLY_RESET = 'Квота успешно сброшена.'
DOWNLOAD_PATH = __file__.replace('constants.py', '')
SENDING_FILE = 'Отправка файла на сервер...'
TOO_BIG_FILE = 'Файл слишком большой. Загрузка остановлена.'
FILE_UPLOADED = 'Файл успешно загружен!\nОставшаяся квота: {}'
AUDIO = 'Аудио'
TRIM = 'Обрезать'
VOLUME = 'Громкость'
PITCH = 'Высота (питч)'
EDITING_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=AUDIO)
    ],
    [
        KeyboardButton(text=TRIM),
        KeyboardButton(text=VOLUME),
    ],
    [
        KeyboardButton(text=PITCH),
    ]
])
REFRESH_AUDIO = 'Вы в режиме обработки аудио.\n\n' \
                'Идентификатор файла: {}\n' \
                'Формат аудио: {}\n' \
                'Длина: {}'


class TooFastQuotaResetException(BaseException):
    def __init__(self):
        super().__init__()
