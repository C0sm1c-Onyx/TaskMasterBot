from django.db import models

from .utils import generate_custom_id


class TGbotUser(models.Model):
    username_id = models.CharField(primary_key=True, unique=True, max_length=100)
    chat_id = models.CharField(max_length=1000)

    class Meta:
        app_label = 'core'


class Category(models.Model):
    category_id = models.CharField(unique=True, primary_key=True, max_length=100)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        app_label = 'core'

    def save(self, **kwargs):
        self.category_id = generate_custom_id(self.category_name)
        super().save(**kwargs)


class Task(models.Model):
    task_id = models.CharField(unique=True, primary_key=True, max_length=100)
    task_title = models.CharField(max_length=50)
    task_description = models.TextField(max_length=1000)
    task_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(TGbotUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    is_check = models.BooleanField(default=False)
    create_data = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'core'

    def save(self, **kwargs):
        self.task_id = generate_custom_id(self.task_title)
        super().save(**kwargs)


class Comment(models.Model):
    comment_id = models.CharField(unique=True, primary_key=True, max_length=100)
    comment = models.CharField(max_length=250)
    username = models.ForeignKey('TGbotUser', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        app_label = 'core'

    def save(self, **kwargs):
        self.comment_id = generate_custom_id(self.comment)
        super().save(**kwargs)
