from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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
FILE_UPLOADED = 'Файл успешно загружен!\nОставшаяся квота: {} мегабайт.'
EDITING_MENU = 'Вы в меню редактирования. Используйте кнопки клавиатуры под полем ввода для навигации по режимам.'
AUDIO = 'Аудио'
TRIM = 'Обрезать'
VOLUME = 'Громкость'
PITCH = 'Тональность'
EXPORT = 'Экспорт'
CANCEL = 'Отменить'
C_TRIMMING = ' обрезку'
C_VOLUME = ' изменение громкости'
C_PITCH = ' изменение тональности'
CANCELED = 'Операция отменена\n\n'
CONFIRM = 'Подтвердить'
CONFIRM_TRIM = 'Вырезка периода {}.\nПодтвердите сохранение.'
CATCH_TRIM = 'Начинаю обрезку...'
X_BIGGER_THAN_Y = 'Кажется, вы перепутали значения временных меток. Отправьте интервал заново, проверив значения.'
Y_BIGGER_THAN_LENGTH = 'Вторая метка выходит за пределы дорожки. Уместите интервал в рамки трека и отправьте его снова.'
X_EQUALS_Y = 'Конечная дорожка будет иметь нулевую длительность. ' \
             'Перепроверьте отправленный интервал и отправьте его снова.'
TRIM_SEND = 'Вы вошли в режим обрезки аудио. Отправьте начало и конец нового трека в рамках старого, например:\n\n' \
            '<pre>00:35 - 01:04</pre>'
TRIM_COMPLETED = 'Обрезка успешно завершена! Новая длина: {}.'

SIMPLE_KEYBOARD = lambda text: ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=text)
    ]
])
CONFIRM_KEYBOARD = lambda cb_query: InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=CONFIRM, callback_data=cb_query)
    ]
])
EXPORT_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=EXPORT, callback_data='export')
    ]
])
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
                'Идентификатор файла: <i>{}</i>\n' \
                'Название файла: <i>{}</i>\n' \
                'Формат аудио: <i>{}</i>\n' \
                'Длина: <i>{}</i>\n\n' \
                'Чтобы сбросить файл, напишите /start или /import.'
