from os import path


def extract_extension(name: str) -> str:
    return path.splitext(name)[1][1:]


def min_sec(secs_r: float) -> str:
    secs = int(secs_r)
    minutes = secs // 60
    seconds = secs - minutes * 60
    return f'{minutes}:{seconds}'
