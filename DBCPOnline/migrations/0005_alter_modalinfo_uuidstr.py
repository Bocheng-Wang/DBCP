# Generated by Django 3.2 on 2021-06-07 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBCPOnline', '0004_alter_modalinfo_uuidstr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalinfo',
            name='uuidStr',
            field=models.CharField(default='c222ca1f-e652-4952-af7e-5dd7b054226b', max_length=50),
        ),
    ]
