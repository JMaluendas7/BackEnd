# Generated by Django 5.0 on 2024-01-26 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_imagenusuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaboradores',
            name='cargo_id',
        ),
    ]
