from django.db import models
from auth_users.models import AuthUser

from utils import generate_custom_id


class Category(models.Model):
    category_id = models.CharField(unique=True, primary_key=True, max_length=100)
    category_name = models.CharField(unique=True, max_length=25)

    def save(self, **kwargs):
        self.category_id = generate_custom_id(self.category_name)
        super().save(**kwargs)


class Task(models.Model):
    task_id = models.CharField(unique=True, primary_key=True, max_length=100)
    task_title = models.CharField(max_length=50)
    task_description = models.TextField(max_length=1000)
    task_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    is_check = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.task_id = generate_custom_id(self.task_title)
        super().save(**kwargs)