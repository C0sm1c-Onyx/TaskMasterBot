import smtplib
import os
from celery import Celery
from dotenv import load_dotenv
from datetime import datetime

from users.models import User
from core.models import Task


load_dotenv()

app = Celery('notifications', broker=os.getenv('EMAIL_HOST_USER'))


@app.task
def send_message_to_email(subject, body, recipient):
    server = smtplib.SMTP('smtp.yandex.ru', 465)
    server.starttls()
    server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(os.getenv('EMAIL_HOST_USER'), recipient, message)
    server.quit()


@app.task
def get_started_task(model_user, model_task):
    email_task = {}

    tasks = model_task.objects.all()
    for task in tasks:
        if not task.is_check:
            continue

        start_date = task.start_date
        current_date = datetime.now().date()

        if start_date == current_date:
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
def generate_and_send_message(model_user, model_task):
    email_task = get_started_task(model_user, model_task)

    body = "Пришло время к выполнению поставленных задач! :)"

    for email in email_task:
        subject = "Твои задачи на сегодня:\n\n"

        tasks = email_task[email]
        subject += '\n\n'.join([f"{task.title}\n{task.description}" for task in tasks])

        send_message_to_email(subject, body, email)


generate_and_send_message.delay(User, Task)