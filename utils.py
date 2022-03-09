from os import path


def extract_extension(name: str) -> str:
    return path.splitext(name)[1][1:]


def min_sec(secs_r: float) -> str:
    secs = int(secs_r)
    minutes = secs // 60
    seconds = secs - minutes * 60
    if len(str(minutes)) < 2:
        minutes = f'0{minutes}'
    if len(str(seconds)) < 2:
        seconds = f'0{seconds}'
    return f'{minutes}:{seconds}'
