# Generated by Django 4.0.3 on 2023-05-15 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_remove_ranking_id_ranking_key_alter_ranking_etc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='etc',
            field=models.TextField(db_column='etc', default='-'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='etc',
            field=models.TextField(db_column='etc', default='-'),
        ),
    ]
