# Generated by Django 5.0.1 on 2024-01-05 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_alter_subasta_precio_inicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subasta',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
