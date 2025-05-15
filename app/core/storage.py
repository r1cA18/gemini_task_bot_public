import json
import os
from datetime import datetime

class JsonStorage:
    def __init__(self, relative_path):
        # このファイルの位置を基準に絶対パスを作成
        base_dir = os.path.dirname(__file__)
        self.filepath = os.path.abspath(os.path.join(base_dir, "..", relative_path))

        self._emsure_file_exists()

    def _emsure_file_exists(self):
        # ファイルがなければ空のJSONを作る
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)

    def load(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        
    def save(self, data):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            return json.dump(data, f, ensure_ascii=False, indent=2)
        
    def get(self, key, default=None):
        data = self.load()
        return data.get(key, default)
        
    def set(self, key, value):
        data = self.load()
        data[key] = value
        self.save(data)

    def delete(self, key):
        data = self.load()
        if key in data:
            del data[key]
            self.save(data)

    def append_history(self, message):
        # geminiの履歴に新しいメッセージを追加
        data = self.load()
        history = data.get("history", [])
        
        if not isinstance(history, list):
            history = []

        shaped_message = {
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
            "role": message["role"],
            "parts": message["parts"]
        }
        
        history.append(shaped_message)
        data["history"] = history
        self.save(data)