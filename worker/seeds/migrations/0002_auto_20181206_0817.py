# Generated by Django 2.1.3 on 2018-12-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seed',
            name='device_token',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]