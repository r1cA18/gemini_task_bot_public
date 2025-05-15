from datetime import datetime, timedelta
import re

class ReminderTask():
  def __init__(self, task_name: str, time_str: str, total_seconds: int = None, execution_time = None):
    self.task_name = task_name
    self.time_str = time_str
    
    if total_seconds == None:
       self.total_seconds = self._parse_time()
    else:
       self.total_seconds = total_seconds
    
    if execution_time == None:
      self.execution_time = self._calc_execution_time()
    else:
       self.execution_time = execution_time

  def _parse_time(self):
    total_seconds = 0
    # 日、時間、分、秒を正規表現で抽出
    relative_pattern = re.findall(r'(\d+)([dhms])', self.time_str)
    time_pattern = re.match(r'^(\d{1,2}):(\d{2})$', self.time_str)

    if time_pattern:
      # HH:MM方式の場合
      current_time = datetime.now()

      hour = int(time_pattern.group(1))
      minute = int(time_pattern.group(2))

      # 指定された時刻のdatetimeオブジェクトを作成
      target_time = current_time.replace(
          hour=hour,
          minute=minute,
          second=0,
          microsecond=0
      )

      print(f"current_time: {current_time}")
      print(f"target_time: {target_time}")

      # 指定時刻が現在時刻より前の場合、翌日の同時刻に設定
      if target_time <= current_time:
          target_time += timedelta(days=1)

      # 現在時刻からの差分を秒数で計算
      total_seconds = int((target_time - current_time).total_seconds())
    elif relative_pattern:
      # 1d2h3m4s方式の場合
      for value, unit in relative_pattern:
          if unit == 'd':
              total_seconds += int(value) * 86400 # 日を秒に変換
          elif unit == 'h':
              total_seconds += int(value) * 3600 # 時間を秒に変換
          elif unit == 'm':
              total_seconds += int(value) * 60 #分を秒に変換
          elif unit == 's':
              total_seconds += int(value) #秒はそのまま

    return total_seconds
  
  def _calc_execution_time(self):
     execution_time = datetime.now() + timedelta(seconds=self.total_seconds)
     return execution_time.replace(microsecond=0)

  def to_dict(self):
     return {
        "task_name": self.task_name,
        "time_str": self.time_str,
        "total_seconds": self.total_seconds,
        "execution_time": self.execution_time.isoformat()
     }
  
  def from_dict(data):
     return ReminderTask(
        data["task_name"],
        data["time_str"],
        data["total_seconds"],
        datetime.fromisoformat(data["execution_time"])
     )