# Generated by Django 5.0 on 2024-02-16 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_rename_direccion_colaboradores_oficina_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaboradores',
            name='oficina',
        ),
        migrations.RemoveField(
            model_name='colaboradores',
            name='telefono',
        ),
    ]
