# Generated by Django 5.1.6 on 2025-03-07 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TGbotUser',
            fields=[
                ('username_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('chat_id', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('task_title', models.CharField(max_length=50)),
                ('task_description', models.TextField(max_length=1000)),
                ('start_date', models.DateField()),
                ('is_check', models.BooleanField(default=False)),
                ('create_data', models.DateField(auto_now_add=True)),
                ('task_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tgbotuser')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('comment', models.CharField(max_length=250)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.task')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tgbotuser')),
            ],
        ),
    ]
