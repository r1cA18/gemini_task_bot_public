# Debug（ここのファイルで動かすためのパス指定）
# import sys
# sys.path.append("/workspaces/genai-assistant/app")

from modules.reminder.reminder_task import ReminderTask
from core.storage import JsonStorage
from datetime import datetime

class ReminderManager():
  def __init__(self, storage_path="data/reminder/reminders.json"):
    self.storage_path = storage_path  # self.storageでしか使わなかったら消す
    self.storage = JsonStorage(storage_path)
    self.tasks = self.load_tasks()

  def add_reminder(self, task_name: str, time_str: str):
    task = ReminderTask(task_name, time_str)
    self.tasks.append(task)
    self.save_tasks()
    
  def save_tasks(self):
    self.storage.save([t.to_dict() for t in self.tasks])

  def load_tasks(self):
    raw = self.storage.load()
    return [ReminderTask.from_dict(item) for item in raw]
  
  def dalete_task(self, task_name: str):
    self.tasks = [t for t in self.tasks if t.task_name != task_name]
    self.save_tasks()
  
  async def monitor_reminder(self):
    now = datetime.now().replace(microsecond=0)
    for task in self.tasks:
      if task.execution_time == now:
        return task.task_name

# Debug  
# reminder_manager = ReminderManager()
# reminder_manager.add_reminder("test", "1d2h3m4s")