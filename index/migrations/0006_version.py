# Generated by Django 5.0.1 on 2024-02-19 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_ranking_24_spring_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('key', models.AutoField(db_column='key', primary_key=True, serialize=False)),
                ('league_version', models.TextField(db_column='league_version', default='-')),
                ('live_version', models.TextField(db_column='live_version', default='-')),
            ],
            options={
                'db_table': 'version',
            },
        ),
    ]