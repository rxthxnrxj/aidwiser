# Generated by Django 3.2.5 on 2021-10-29 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aid', '0018_auto_20211030_0116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambulance',
            name='driver',
        ),
    ]
