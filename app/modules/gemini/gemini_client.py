from google import genai
from google.genai import types
from core.storage import JsonStorage

class GeminiClient():
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.history = []
        self.history_storage = JsonStorage("data/gemini/history.json")

        # 履歴の読み込み
        data = self.history_storage.load()
        if isinstance(data, dict) and "history" in data:
            self._load_history(data["history"])

    def _get_system_instruction(self) -> str:
        storage = JsonStorage("data/gemini/system_instruction.json")
        return str(storage.load())

    def _append_history_entry(self, role: str, parts: str):
        message = {"role": role, "parts": parts}
        self.history_storage.append_history(message)

    def _load_history(self, dict_list):
        self.history = [
            types.Content(
                role=entry["role"],
                parts=[types.Part.from_text(text=entry["parts"])]
            )
            for entry in dict_list
        ]

    def add_history(self, role: str, text: str):
        content = types.Content(
            role=role,
            parts=[types.Part.from_text(text=text)]
        )
        self.history.append(content)
        self._append_history_entry(role, text)

    async def talk(self, contents):
        # ユーザーのメッセージを履歴に追加
        self.add_history("user", contents)

        # システムプロンプトを取得
        system_instruction = self._get_system_instruction()

        # 応答を生成
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            ),
            contents=self.history
        )

        # AIの応答を履歴に追加
        self.add_history("assistant", response.text)

        return response.text