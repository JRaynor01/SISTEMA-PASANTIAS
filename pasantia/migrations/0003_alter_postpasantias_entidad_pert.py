# Generated by Django 3.2.2 on 2022-09-29 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pasantia', '0002_postpasantias_entidad_pert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpasantias',
            name='entidad_pert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='pasantia.entidad'),
        ),
    ]
