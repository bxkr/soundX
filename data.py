import datetime
import json
from constants import DATA_PATH


class Data:
    def __init__(self, uid: int):
        current = json.load(open(DATA_PATH, 'r'))
        self.suid = str(uid)
        if self.suid not in current:
            current[self.suid] = {
                'mode': None,
                'quota': 50,
                'last_quota_reset': datetime.datetime.now().timestamp(),
                'file_id': None,
                'ext': None,
                'files': 0
            }
        json.dump(current, open(DATA_PATH, 'w'))

    def __getattribute__(self, item):
        if item == 'suid':
            return object.__getattribute__(self, item)
        current = json.load(open(DATA_PATH, 'r'))
        return current[self.suid][item]

    def __setattr__(self, key, value):
        if key == 'suid':
            object.__setattr__(self, key, value)
        current = json.load(open(DATA_PATH, 'r'))
        current[self.suid][key] = value
        json.dump(current, open(DATA_PATH, 'w'))
