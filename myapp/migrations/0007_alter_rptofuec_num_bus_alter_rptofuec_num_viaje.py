# Generated by Django 5.0 on 2024-01-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rptofuec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rptofuec',
            name='num_bus',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rptofuec',
            name='num_viaje',
            field=models.IntegerField(),
        ),
    ]
