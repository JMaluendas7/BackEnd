# Generated by Django 4.2.7 on 2023-11-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_alter_login_documento_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='documento_num',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]