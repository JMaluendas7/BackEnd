# Generated by Django 4.2.7 on 2023-11-03 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_login_groups_alter_login_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='colaborador_id',
            field=models.IntegerField(),
        ),
    ]
