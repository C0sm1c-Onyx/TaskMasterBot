from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
import os
from datetime import datetime
from dotenv import load_dotenv
from notifiers import get_notifier


load_dotenv()


logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')

import django
django.setup()

app = Celery("notification")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    timezone='Europe/Moscow',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'generate_and_send_message': {
        'task': 'todo_list.celery.generate_and_send_message',
        'schedule': crontab(hour='8', minute='0'),
    }
}


def send_message_to_tg(subject, body, recipient):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram = get_notifier('telegram')
    telegram.notify(token=token, chat_id=recipient, message=f"{body}\n{subject}")


def get_started_task(model_user, model_task):
    user_task = {}

    tasks = model_task.objects.all()
    for task in tasks:
        if task.is_check:
            continue

        start_date = task.start_date
        current_date = datetime.now().date()

        if str(start_date) == str(current_date):
            user = model_user.objects.get(username_id=task.user_id)
            chat_id = user.chat_id

            if user in user_task:
                user_task[chat_id].append(task)
            else:
                user_task[chat_id] = [task]

            task.is_check = True
            task.save()

    return user_task


@app.task
def generate_and_send_message():
    from core.models import Task, TGbotUser

    user_task = get_started_task(TGbotUser, Task)

    body = "Пришло время к выполнению поставленных задач! :)"

    for chat_id in user_task:
        subject = "Твои задачи на сегодня:\n\n"

        tasks = user_task[chat_id]
        subject += '\n\n'.join([f"Название: {task.task_title}\nОписание: {task.task_description}" for task in tasks])

        send_message_to_tg(subject, body, chat_id)