# Generated by Django 3.2.2 on 2022-10-03 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasantia', '0005_auto_20221003_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidad',
            name='estado',
            field=models.CharField(choices=[('REVISION', 'REVISION'), ('ASIGNADO', 'ASIGNADO')], default='PENDIENTE', max_length=20),
        ),
    ]
