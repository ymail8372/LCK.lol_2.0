# Generated by Django 4.0.3 on 2023-05-15 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_ranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ranking',
            name='id',
        ),
        migrations.AddField(
            model_name='ranking',
            name='key',
            field=models.IntegerField(db_column='key', default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='etc',
            field=models.TextField(db_column='etc', default=' - '),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='game_lose',
            field=models.IntegerField(db_column='game_lose', default=0),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='game_win',
            field=models.IntegerField(db_column='game_win', default=0),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='set_lose',
            field=models.IntegerField(db_column='set_lose', default=0),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='set_win',
            field=models.IntegerField(db_column='set_win', default=0),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='key',
            field=models.IntegerField(db_column='key', default=0, primary_key=True, serialize=False),
        ),
    ]
