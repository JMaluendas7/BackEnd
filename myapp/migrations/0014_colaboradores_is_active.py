# Generated by Django 5.0 on 2024-02-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_colaboradores_oficina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaboradores',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
