# Generated by Django 3.2 on 2021-06-13 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBCPOnline', '0013_alter_modalinfo_uuidstr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalinfo',
            name='uuidStr',
            field=models.CharField(default='80451e71-4a52-479e-9c8c-0e6f80f693e7', max_length=50),
        ),
    ]