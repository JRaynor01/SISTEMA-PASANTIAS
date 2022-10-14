# Generated by Django 3.2.2 on 2022-10-03 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pasantia', '0004_postpasantias_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpasantias',
            name='estado',
            field=models.CharField(choices=[('REVISION', 'REVISION'), ('FINALIZADO', 'FINALIZADO'), ('ASIGNADO', 'ASIGNADO')], default='REVISION', max_length=20),
        ),
        migrations.CreateModel(
            name='Postulantes_Unidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_finalizacion', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pasantia.unidad')),
            ],
        ),
    ]
