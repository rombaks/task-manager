# Generated by Django 4.1.1 on 2022-10-06 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated_to',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]