# Generated by Django 4.0.3 on 2023-03-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule23Spring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('team1', models.TextField()),
                ('team2', models.TextField()),
                ('team1_score', models.IntegerField()),
                ('team2_score', models.IntegerField()),
            ],
            options={
                'db_table': 'schedule_23spring',
                'managed': False,
            },
        ),
    ]
