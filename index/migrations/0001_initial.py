# Generated by Django 4.0.3 on 2023-05-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField(db_column='key')),
                ('year', models.IntegerField(db_column='year')),
                ('month', models.IntegerField(db_column='month')),
                ('day', models.IntegerField(db_column='day')),
                ('weekday', models.TextField(db_column='weekday')),
                ('team1_name', models.TextField(db_column='team1_name')),
                ('team2_name', models.TextField(db_column='team2_name')),
                ('team1_score', models.IntegerField(db_column='team1_score')),
                ('team2_score', models.IntegerField(db_column='team2_score')),
                ('hour', models.IntegerField(db_column='hour')),
                ('min', models.IntegerField(db_column='min')),
                ('ampm', models.TextField(db_column='ampm')),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
    ]
