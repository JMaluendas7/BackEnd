# Generated by Django 4.2.7 on 2023-11-11 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_alter_login_documento_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='documento_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.colaboradores'),
        ),
    ]
