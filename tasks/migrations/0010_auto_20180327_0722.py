# Generated by Django 2.0 on 2018-03-27 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20180327_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.Lesson', verbose_name='Урок'),
        ),
    ]
