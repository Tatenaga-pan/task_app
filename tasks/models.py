from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=100)  # 企業名
    next_action = models.CharField(max_length=200)   # 次の予定
    due_date = models.DateTimeField()                # 日時
    interest_level = models.IntegerField(default=2)  # 興味度 (3:高, 2:中, 1:低)
    
    # 自由記述のメモ欄を追加
    memo = models.TextField(blank=True, null=True)

    completed = models.BooleanField(default=False)     # 完了フラグ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.next_action}"