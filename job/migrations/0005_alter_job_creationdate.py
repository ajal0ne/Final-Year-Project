# Generated by Django 3.2.5 on 2021-08-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='creationdate',
            field=models.DateField(),
        ),
    ]
