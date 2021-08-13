# Generated by Django 3.2 on 2021-06-07 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30, verbose_name='IP')),
                ('count', models.IntegerField(default=0, verbose_name='visit')),
                ('visitTime', models.DateTimeField(auto_now_add=True)),
                ('memo', models.CharField(max_length=300, verbose_name='memo')),
            ],
            options={
                'verbose_name': 'visitor',
                'verbose_name_plural': 'visitor',
            },
        ),
        migrations.CreateModel(
            name='VisitNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='total visits')),
            ],
            options={
                'verbose_name': 'total visits',
                'verbose_name_plural': 'total visits',
            },
        ),
    ]
