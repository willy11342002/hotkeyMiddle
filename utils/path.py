from pathlib import Path
import pickle
import yaml
import json


class FileHandler:
    '''各種檔案格式存讀'''
    @classmethod
    def load_pickle(cls, file_path):
        with open(file_path, 'rb') as f:
            return cls(pickle.load(f))
    def dump_pickle(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_json(cls, file_path, **kwargs):
        with open(file_path, 'r', **kwargs) as f:
            return cls(json.load(f))
    def dump_json(self, file_path, **kwargs):
        with open(file_path, 'w', **kwargs) as f:
            json.dump(self, f)

    @classmethod
    def load_yaml(cls, file_path, Loader=yaml.CFullLoader, **kwargs):
        with open(file_path, 'r', **kwargs) as f:
            return cls(yaml.load(f, Loader))
    def dump_yaml(self, file_path, **kwargs):
        with open(file_path, 'w', **kwargs) as f:
            yaml.dump(self, f)

    def __getstate__(self):
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)


class Dict(dict, FileHandler):
    '''JS Like Dict, 提供attribute的方式取值'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = Dict(value)
            if type(value) == list:
                self[key] = [
                    Dict(v) if isinstance(v, dict) else v
                    for v in value
                ]

    def sub(self, keys):
        return {k: v for k, v in self.items() if k in keys}

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError as e:
            return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


def walk(path):
    '''
    遞迴取出資料夾內所有文件
    傳出格式為： dirpath, dirnames, filenames
    '''
    dirs = [p for p in Path(path).iterdir() if p.is_dir()]
    files = [p for p in Path(path).iterdir() if not p.is_dir()]
    yield path, dirs, files
    for p in dirs:
        yield from walk(p)
        continue
