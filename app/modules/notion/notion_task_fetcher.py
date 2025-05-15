from notion_client import Client
from modules.notion.notion_properties import NotionProperties as NP
import datetime

from core.storage import JsonStorage

class NotionTaskFetcher():
    def __init__(self, api_key: str, database_id: str):
        self.client = Client(auth=api_key)
        self.database_id = database_id
        self.tasks = []

    # 今日以降のタスクをすべて取得
    def _fetch_all_future_tasks(self):
        try:
            filter_conditions = {
                "property": NP.Timestamp,
                "date": {
                    "on_or_after": datetime.date.today().isoformat()
                }
            }

            response = self.client.databases.query(
                database_id=self.database_id,
                filter=filter_conditions
            )

            # 取得したNotionデータをjsonに保存
            storage = JsonStorage("data/notion/response.json")
            storage.save(response)

            self._parse_notion_response(response)
            # print(f"self.tasks: {self.tasks}")
        
        except Exception as e:
            print(f"タスク取得エラー: {e}")

    # notion queryを辞書型に変換
    def _parse_notion_response(self, response):
        # 初期化
        self.tasks = []

        for page in response["results"]:
            properties = page["properties"]
            page_data = {}

            for prop_name, prop_value in properties.items():
                prop_type = prop_value["type"]
                
                # 各タイプに応じて値を取得
                if prop_type == "title":
                    page_data[prop_name] = prop_value["title"][0]["text"]["content"] if prop_value["title"] else None
                elif prop_type == "date":
                    page_data[prop_name] = prop_value["date"]["start"] if prop_value["date"] else None
                elif prop_type == "select":
                    page_data[prop_name] = prop_value["select"]["name"] if prop_value["select"] else None
                elif prop_type == "multi_select":
                    page_data[prop_name] = [item["name"] for item in prop_value["multi_select"]] if prop_value["multi_select"] else []
                elif prop_type == "checkbox":
                    page_data[prop_name] = prop_value["checkbox"]
                elif prop_type == "rich_text":
                    page_data[prop_name] = prop_value["rich_text"][0]["text"]["content"] if prop_value["rich_text"] else None
                elif prop_type == "status":
                    page_data[prop_name] = prop_value["status"]["name"] if prop_value["status"] else None                
                else:
                    # print("対応していないプロパティです")
                    page_data[prop_name] = None
                # 必要に応じて他のプロパティも追加

            self.tasks.append(page_data)

    # 締切日が◯◯日後のタスクを取得
    async def fetch_deadline_tasks(self, days: int):
        # 初期化
        self._fetch_all_future_tasks()  # 最新の情報を取得
        days += days

        # ◯日後の日付を計算
        deadline = datetime.date.today() + datetime.timedelta(days=days)
        print(deadline.isoformat())

        filtered_tasks = [
            task for task in self.tasks
            if task.get("Deadline") == deadline.isoformat()
        ]

        return filtered_tasks