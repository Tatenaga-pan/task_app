from django.urls import path
from . import views

urlpatterns = [
    # トップページ（ http://127.0.0.1:8000/ ）にアクセスしたときにtask_listビューを呼ぶ
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'), # ← 追加！
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]