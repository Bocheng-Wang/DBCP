# Generated by Django 3.2 on 2021-06-14 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBCPOnline', '0014_alter_modalinfo_uuidstr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalinfo',
            name='uuidStr',
            field=models.CharField(default='9a4eec4b-d3c6-4fb6-af05-c2c28d8ab1a1', max_length=50),
        ),
    ]