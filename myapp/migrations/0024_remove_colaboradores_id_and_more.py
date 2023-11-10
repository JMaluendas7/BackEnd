# Generated by Django 4.2.7 on 2023-11-10 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_alter_login_documento_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaboradores',
            name='id',
        ),
        migrations.AlterField(
            model_name='colaboradores',
            name='num_documento',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='login',
            name='documento_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_login', to='myapp.colaboradores'),
        ),
    ]