# Generated by Django 3.2.5 on 2021-10-29 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aid', '0015_auto_20211030_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amb_assgn', models.BooleanField(default=False, null=True)),
                ('aid_assgn', models.BooleanField(default=False, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('performance', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ambulance',
            name='driver',
        ),
    ]
