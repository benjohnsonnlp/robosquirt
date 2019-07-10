# Generated by Django 2.0.6 on 2019-07-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WateringSession',
            fields=[
                ('identifier', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField()),
                ('session_start', models.DateTimeField()),
                ('session_end', models.DateTimeField()),
                ('device_identifier', models.IntegerField()),
                ('originator', models.TextField()),
                ('reason', models.TextField()),
            ],
            options={
                'get_latest_by': ['created_time'],
            },
        ),
    ]