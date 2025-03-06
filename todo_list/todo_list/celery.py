import os
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger


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


import smtplib
import os

from datetime import datetime

from auth_users.models import AuthUser
from core.models import Task


def send_message_to_email(subject, body, recipient):
    server = smtplib.SMTP('smtp.yandex.ru', 465)
    server.starttls()
    server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(os.getenv('EMAIL_HOST_USER'), recipient, message)
    server.quit()


def get_started_task(model_user, model_task):
    email_task = {}

    tasks = model_task.objects.all()
    for task in tasks:
        if task.is_check:
            continue

        start_date = task.start_date
        current_date = datetime.now().date()

        if str(start_date) == str(current_date):
            user = model_user.objects.get(user_id=task.user)
            email = user.email

            if email in email_task:
                email_task[email].append(task)
            else:
                email_task[email] = [task]

            task.is_check = True
            task.save()

    return email_task


@app.task
def generate_and_send_message():
    email_task = get_started_task(AuthUser, Task)

    body = "Пришло время к выполнению поставленных задач! :)"

    for email in email_task:
        subject = "Твои задачи на сегодня:\n\n"

        tasks = email_task[email]
        subject += '\n\n'.join([f"{task.title}\n{task.description}" for task in tasks])

        send_message_to_email(subject, body, email)


app.conf.beat_schedule = {
    'generate_and_send_message': {
        'task': 'notification.generate_and_send_message',
        'schedule': crontab(hour='5', minute='21'),
    }
}
