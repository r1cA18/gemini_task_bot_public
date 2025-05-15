# イベントやコマンドの処理を適切な処理クラスに振り分ける中継

import config.settings as KEY
from modules.gemini.gemini_client import GeminiClient
from modules.notion.notion_task_fetcher import NotionTaskFetcher
from modules.reminder.reminder_manager import ReminderManager

class Dispatcher:
    def __init__(self):
        self.gemini = GeminiClient(KEY.GEMINI_TOKEN)
        self.notion_task_fetcher = NotionTaskFetcher(KEY.NOTION_TOKEN, KEY.NOTION_DATABASE_ID_TASKS)
        self.reminder_manager = ReminderManager()
        print("dispatcher OK")

    def get_gemini(self):
        return self.gemini
    
    def get_notion_task_fetcher(self):
        return self.notion_task_fetcher
    
    def get_reminder_manager(self):
        return self.reminder_manager