
import os
import django
import requests

# Djangoの仕組みをこのファイル単体で動かすための設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

# Djangoのモデルを呼び出す
from tasks.models import Task

def send_weekly_remind():
   
    uncompleted_tasks = Task.objects.filter(completed=False)
    
    if not uncompleted_tasks.exists():
        print("未完了のタスクはありませんでした。LINEは送信しません。")
        return
    
    msg = "\n【毎週のTodoリマインド】\n現在、以下の課題が残っています。"
    
    for task in uncompleted_tasks:
    
        msg += f"\n・ {task.title}"

   
    line_url = "https://api.line.me/v2/bot/message/push"
    my_token = "PbK7og5BYICRZl161jMvfGhB8TWj8wxwmlnclMmqEsxDw5DYHwAljp8svS3OfmzTeNp9yOB5Jpuw5IY8Dsh3t5Fdo3njNEkcDlZlHxbxQ48vP9MAZrgPDXKFOrGfrxtu2t/UD51FsT9nvKsSmbsdVQdB04t89/1O/w1cDnyilFU="

    headers = {"Authorization": f"Bearer {my_token}"}
    payload = {"message": msg}

    try:
        requests.post(line_url, headers=headers, data=payload)
        print("毎週のリマインドLINEを送信しました")
    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    send_weekly_remind()