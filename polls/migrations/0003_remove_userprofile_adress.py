# Generated by Django 3.2.25 on 2024-12-19 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='adress',
        ),
    ]
