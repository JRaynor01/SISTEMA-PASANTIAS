# Generated by Django 3.2.2 on 2022-10-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasantia', '0007_alter_unidad_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postulaciones',
            name='estadoest',
            field=models.CharField(choices=[('RECHAZADO', 'RECHAZADO'), ('PENDIENTE', 'PENDIENTE'), ('ACEPTADO', 'ACEPTADO'), ('ASIGNADO', 'ASIGNADO')], default='PENDIENTE', max_length=20),
        ),
    ]
