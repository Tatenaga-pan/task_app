import requests
from django.conf import settings
from django.utils import timezone

LINE_PUSH_URL = "https://api.line.biz/v2/bot/message/push"


def send_line_message(text: str) -> bool:
    """LINE Messaging API を使ってテキストメッセージを送信する"""
    token = getattr(settings, "LINE_CHANNEL_ACCESS_TOKEN", "")
    user_id = getattr(settings, "LINE_USER_ID", "")

    if not token or not user_id:
        print("[LINE通知スキップ] トークンまたはユーザーIDが未設定です。")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    try:
        response = requests.post(
            LINE_PUSH_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[LINE通知エラー] {e}")
        return False


def format_task_notification(task, action_label: str = "期限リマインダー") -> str:
    """就活タスクの内容をLINE通知向けテキストに整形する"""
    interest_map = {
        3: "★★★（高）",
        2: "★★☆（中）",
        1: "★☆☆（低）",
    }
    interest_text = interest_map.get(task.interest_level, "★★☆（中）")

    if task.due_date:
        local_dt = (
            timezone.localtime(task.due_date)
            if timezone.is_aware(task.due_date)
            else task.due_date
        )
        due_text = local_dt.strftime("%Y/%m/%d %H:%M")

        now = timezone.localtime(timezone.now())
        diff = local_dt - now
        total_minutes = int(diff.total_seconds() // 60)

        if total_minutes < 0:
            remaining_text = "（⚠️ 期限を過ぎています）"
        elif total_minutes < 60:
            remaining_text = f"（あと約{total_minutes}分）"
        else:
            hours = total_minutes // 60
            remaining_text = f"（あと約{hours}時間）"
    else:
        due_text = "未設定"
        remaining_text = ""

    lines = [
        f"【就活予定：{action_label}】",
        f"企業名: {task.company_name}",
        f"次の予定: {task.next_action}",
        f"日時: {due_text} {remaining_text}".strip(),
        f"興味度: {interest_text}",
    ]
    if task.memo:
        lines.append(f"メモ: {task.memo}")

    return "\n".join(lines)