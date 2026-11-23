from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Task

@login_required
def task_list(request):
    # 未完了のタスクだけを取得
    tasks = Task.objects.filter(user=request.user, completed=False).order_by('due_date')
    return render(request, 'tasks/index.html', {'tasks': tasks})

@login_required
def completed_task_list(request):
    # 完了済みのタスクだけを取得
    tasks = Task.objects.filter(user=request.user, completed=True).order_by('-due_date')
    return render(request, 'tasks/completed.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        next_action = request.POST.get('next_action')
        due_date_text = request.POST.get('due_date')
        interest_level = request.POST.get('interest_level', 2)
        memo = request.POST.get('memo', '')

        Task.objects.create(
            user=request.user,
            company_name=company_name,
            next_action=next_action,
            due_date=due_date_text,
            interest_level=interest_level,
            memo=memo
        )
        
    return redirect('task_list')

@login_required
@transaction.atomic
def toggle_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()

        # 完了状態になったら完了ページへ、未完了に戻ったら未完了ページへ自動リダイレクト
        if task.completed:
            return redirect('completed_task_list')
        else:
            return redirect('task_list')

    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        # 削除されたときの所属ページに応じて戻すこともできますが、一旦安全にリファラまたは一覧へ
        is_completed = task.completed
        task.delete()
        
        if is_completed:
            return redirect('completed_task_list')
        else:
            return redirect('task_list')

    return redirect('task_list')

@login_required
def edit_task(request, task_id):
    # ログインユーザーのタスクを1件取得（なければ404エラー）
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        # フォームから送られてきたデータを取得して上書き
        task.company_name = request.POST.get('company_name')
        task.next_action = request.POST.get('next_action')
        task.due_date = request.POST.get('due_date')
        task.interest_level = request.POST.get('interest_level', 2)
        task.memo = request.POST.get('memo', '')
        task.reminded = False
        task.save()

        # 編集完了後、もともと完了していたか未完了かによって戻り先を分岐させると便利です
        if task.completed:
            return redirect('completed_task_list')
        else:
            return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {'task': task})