# Generated by Django 3.2 on 2021-06-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBCPOnline', '0008_alter_modalinfo_uuidstr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalinfo',
            name='uuidStr',
            field=models.CharField(default='933683f8-d72f-4dc2-9c05-3e02afe1cdf1', max_length=50),
        ),
    ]