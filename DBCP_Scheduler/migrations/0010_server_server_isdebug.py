# Generated by Django 3.2 on 2021-06-13 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBCP_Scheduler', '0009_alter_causalityconnectivitytask_task_modal'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='Server_IsDebug',
            field=models.BooleanField(default=False),
        ),
    ]