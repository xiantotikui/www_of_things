# Generated by Django 2.1.5 on 2019-01-26 19:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32)),
                ('task_refresh', models.IntegerField()),
                ('workers_names', models.TextField()),
                ('task_cron_value', models.CharField(max_length=32)),
                ('task_exe_time', models.IntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]