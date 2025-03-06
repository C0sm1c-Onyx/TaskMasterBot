from django.db import models

from core.models import Task
from auth_users.models import AuthUser
from utils import generate_custom_id


class Comment(models.Model):
    comment_id = models.CharField(unique=True, primary_key=True, max_length=100)
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.task_id = generate_custom_id(self.task_title)
        super().save(**kwargs)