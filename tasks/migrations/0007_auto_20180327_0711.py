# Generated by Django 2.0 on 2018-03-27 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20180327_0655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='lesson',
        ),
        migrations.AddField(
            model_name='lesson',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.Task', verbose_name='Задачи'),
            preserve_default=False,
        ),
    ]
