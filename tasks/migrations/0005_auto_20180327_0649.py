# Generated by Django 2.0 on 2018-03-27 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20180208_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
