# Generated by Django 3.2.5 on 2021-07-29 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_recruiter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiter',
            name='image',
        ),
        migrations.RemoveField(
            model_name='studentuser',
            name='image',
        ),
    ]
