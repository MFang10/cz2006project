# Generated by Django 2.0.1 on 2018-02-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180208_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='license',
            field=models.CharField(max_length=64),
        ),
    ]
