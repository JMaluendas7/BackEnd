# Generated by Django 4.2.7 on 2023-11-10 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_login_colaborador_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='colaborador_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.colaboradores', to_field='num_documento', verbose_name='Col'),
        ),
    ]
