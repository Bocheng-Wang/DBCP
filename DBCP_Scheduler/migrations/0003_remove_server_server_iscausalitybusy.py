# Generated by Django 3.2 on 2021-06-07 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DBCP_Scheduler', '0002_server_server_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='Server_IsCausalityBusy',
        ),
    ]