from django.db import models

class Schedule(models.Model):
    key = models.IntegerField(db_column='key', primary_key=True, default=0)
    year = models.IntegerField(db_column='year')
    month = models.IntegerField(db_column='month')
    day = models.IntegerField(db_column='day')
    weekday = models.TextField(db_column='weekday')
    team1_name = models.TextField(db_column='team1_name')
    team2_name = models.TextField(db_column='team2_name')
    team1_score = models.IntegerField(db_column='team1_score')
    team2_score = models.IntegerField(db_column='team2_score')
    hour = models.IntegerField(db_column='hour')
    min = models.IntegerField(db_column='min')
    ampm = models.TextField(db_column='ampm')
    etc = models.TextField(db_column='etc', default="-")

    class Meta:
        db_table = 'schedule'
        
class Ranking_23_spring_regular(models.Model):
    key = models.IntegerField(db_column="key", primary_key=True, default=0)
    name = models.TextField(db_column="name")
    tricode = models.TextField(db_column="tricode")
    game_win = models.IntegerField(db_column="game_win", default=0)
    game_lose = models.IntegerField(db_column="game_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default="-")
    
    class Meta:
        db_table = "ranking_23_spring_regular"