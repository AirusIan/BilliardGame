# Generated by Django 4.2.16 on 2024-09-06 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='member',
        ),
    ]
