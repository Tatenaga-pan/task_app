from django.contrib import admin
from .models import Task  # さっき作ったTaskを読み込む

admin.site.register(Task)
