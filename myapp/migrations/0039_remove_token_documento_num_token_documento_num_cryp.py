# Generated by Django 4.2.7 on 2023-11-23 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='documento_num',
        ),
        migrations.AddField(
            model_name='token',
            name='documento_num_cryp',
            field=models.CharField(default=2, max_length=60),
            preserve_default=False,
        ),
    ]
