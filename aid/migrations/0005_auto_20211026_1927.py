# Generated by Django 3.2.5 on 2021-10-26 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aid', '0004_auto_20211026_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='aid_details',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aid.hospital'),
        ),
    ]
