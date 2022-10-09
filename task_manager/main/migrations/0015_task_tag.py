# Generated by Django 4.1.1 on 2022-10-06 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_task_assignee_alter_task_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tag',
            field=models.ForeignKey(default='backend', on_delete=django.db.models.deletion.PROTECT, related_name='task_tag', to='main.tag'),
        ),
    ]