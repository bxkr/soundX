import datetime
import json
from constants import DATA_PATH


class Data:
    suid: str
    quota: float | int
    mode: str | None
    last_quota_reset: float
    files: int
    file_id: int
    ext: str | None
    old_name: str | None

    def __init__(self, uid: int):
        current = json.load(open(DATA_PATH, 'r'))
        self.suid = str(uid)
        if self.suid not in current:
            current[self.suid] = {
                'quota': 50,
                'last_quota_reset': datetime.datetime.now().timestamp(),
                'files': 0
            }
        json.dump(current, open(DATA_PATH, 'w'))

    def __getattribute__(self, item):
        if item == 'suid':
            return object.__getattribute__(self, item)
        current = json.load(open(DATA_PATH, 'r'))
        if item in current[self.suid]:
            return current[self.suid][item]

    def __setattr__(self, key, value):
        if key == 'suid':
            object.__setattr__(self, key, value)
            return
        current = json.load(open(DATA_PATH, 'r'))
        current[self.suid][key] = value
        json.dump(current, open(DATA_PATH, 'w'))

    def __delattr__(self, item):
        current = json.load(open(DATA_PATH, 'r'))
        if item in current[self.suid]:
            del current[self.suid][item]
            json.dump(current, open(DATA_PATH, 'w'))
