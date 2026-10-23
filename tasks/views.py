from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Task
import requests
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404  # ← get_object_or_404を追加


@login_required
def task_list(request):

    # ログイン機能のため削除した行　tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render (request, 'tasks/index.html',{'tasks':tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        # 画面の入力欄（name="title"）から文字を取得する
        title_text = request.POST.get('title')

        due_date_text = request.POST.get('due_date')

        recurrence_text = request.POST.get('recurrence', 'none')

        # データベースに新しいタスクを保存する
        if due_date_text:
            Task.objects.create(title=title_text, user=request.user, due_date=due_date_text, recurrence=recurrence_text)
        else:
            # 入力されていなければ期限なしで保存
            Task.objects.create(title=title_text, user=request.user, recurrence=recurrence_text)
    
        
    # 保存が終わったら、タスク一覧画面に戻る（リダイレクト）
    return redirect('task_list')

@login_required
@transaction.atomic
def toggle_task(request, task_id):
    if request.method == 'POST':
        # URLから渡された task_id を使って、特定のタスクを1件だけ取得する
        task = get_object_or_404(Task, id=task_id, user=request.user)
        # 現在のステータスを反転させる（TrueならFalseに、FalseならTrueに）
        task.completed = not task.completed
        # 変更をデータベースに保存する
        task.save()

    if task.completed and task.recurrence != 'none' and task.due_date:
            # 次の期限を計算する準備
            next_due_date = task.due_date
            
            if task.recurrence == 'daily':
                next_due_date += timedelta(days=1)  # 1日後
            elif task.recurrence == 'weekly':
                next_due_date += timedelta(weeks=1) # 1週間後

            Task.objects.create(
                user=task.user,
                title=task.title,
                due_date=next_due_date,
                recurrence=task.recurrence,
                completed=False)

            
            #繰り返す場合、完了済みのタスクは自動消去されるようにする
            
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        # 対象のタスクを1件取得して、そのまま削除する
        task = get_object_or_404(Task,id=task_id, user=request.user)
        task.delete()

    return redirect('task_list')

