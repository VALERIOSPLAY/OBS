import os
import pickle

class CompressedDict:
    def __init__(self, max_size=500000):
        self.max_size = max_size
        self.current_dict = {}
        self.dict_files = []

    def add(self, key, value):
        if len(self.current_dict) >= self.max_size:
            self.dump_current_dict()
        self.current_dict[key] = [value]


    def get(self, key):
        if key in self.current_dict:
            return self.current_dict[key]
        else:
            for file in self.dict_files:
                with open(file, 'rb') as f:
                    print('LOADED DICT', f.name)
                    temp_dict = pickle.load(f)
                    if key in temp_dict:
                        return temp_dict[key]
        raise KeyError(f'Key {key} not found in the CompressedDict')

    def __contains__(self, key):
        if key in self.current_dict:
            return True
        else:
            for file in self.dict_files:
                with open(file, 'rb') as f:
                    temp_dict = pickle.load(f)
                    if key in temp_dict:
                        return True
        return False

    def keys_in_dict(self, keys, dict_file):

        with open(self.dict_files[dict_file], 'rb') as f:
            temp_dict = pickle.load(f)

        result = [key in temp_dict for key in keys]
        return result

    def load_dict(self, dict_path):

        if not os.path.exists(dict_path):
            raise FileNotFoundError(f"Файл {dict_path} не найден")

        with open(dict_path, 'rb') as f:
            temp_dict = pickle.load(f)

        return temp_dict

    def update_values(self, items):
        items_dict = dict(items)

        for dict_path in self.dict_files:
            temp_dict = self.load_dict(dict_path)

            for key in list(temp_dict.keys()):
                if key in items_dict:
                    temp_dict[key].append(items_dict[key])
                    del items_dict[key]

            with open(dict_path, 'wb') as f:
                pickle.dump(temp_dict, f)

            if not items_dict:
                break

        for key, value in items_dict.items():
            self.add(key, value)


    def set(self, key, value):
        if key in self.current_dict:
            self.current_dict[key] = value
        else:
            for file in self.dict_files:
                with open(file, 'rb') as f:
                    temp_dict = pickle.load(f)
                    if key in temp_dict:
                        temp_dict[key] = value
                        with open(file, 'wb') as f:
                            pickle.dump(temp_dict, f)
                        return
        raise KeyError(f'Key {key} not found in the CompressedDict')

    def dump_current_dict(self):
        file_name = f'dict_{len(self.dict_files)}.pkl'
        print('LOADED DICT', file_name)
        with open(file_name, 'wb') as f:
            pickle.dump(self.current_dict, f)
        self.dict_files.append(file_name)
        self.current_dict = {}

    def __del__(self):
        for file in self.dict_files:
            os.remove(file)

    def keys(self):
        keys = list(self.current_dict.keys())
        for file in self.dict_files:
            with open(file, 'rb') as f:
                temp_dict = pickle.load(f)
                keys.extend(temp_dict.keys())
        return keys

    def values(self):
        values = list(self.current_dict.values())
        for file in self.dict_files:
            with open(file, 'rb') as f:
                temp_dict = pickle.load(f)
                values.extend(temp_dict.values())
        return values

    def items(self):
        items = list(self.current_dict.items())
        for file in self.dict_files:
            with open(file, 'rb') as f:
                temp_dict = pickle.load(f)
                items.extend(temp_dict.items())
        return items

    def __len__(self):
        length = len(self.current_dict)
        for file in self.dict_files:
            with open(file, 'rb') as f:
                temp_dict = pickle.load(f)
                length += len(temp_dict)
        return length