# Generated by Django 3.2.5 on 2021-10-28 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aid', '0008_alter_ambulance_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulance',
            name='aid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aid.aid'),
        ),
        migrations.AlterField(
            model_name='ambulance',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aid.driver'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='assgn',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aid.aid'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aid.hospital'),
        ),
    ]
