# Generated by Django 4.0.3 on 2023-05-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_schedule_team1_tricode_schedule_team2_tricode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='ampm',
            field=models.TextField(db_column='ampm', default='-'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='team1_name',
            field=models.TextField(db_column='team1_name', default='-'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='team1_tricode',
            field=models.TextField(db_column='team1_tricdoe', default='-'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='team2_name',
            field=models.TextField(db_column='team2_name', default='-'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='team2_tricode',
            field=models.TextField(db_column='team2_tricode', default='-'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='weekday',
            field=models.TextField(db_column='weekday', default='-'),
        ),
    ]
