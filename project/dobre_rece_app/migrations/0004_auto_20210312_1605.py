# Generated by Django 2.2.19 on 2021-03-12 16:05

from django.db import migrations
import dobre_rece_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('dobre_rece_app', '0003_auto_20210312_1131'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', dobre_rece_app.models.UserManager()),
            ],
        ),
    ]
