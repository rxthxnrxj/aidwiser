# Generated by Django 3.2.5 on 2021-10-29 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aid', '0014_alter_ambulance_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulance',
            name='driver',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
    ]
