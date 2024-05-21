from django.db import models
from datetime import datetime

class Schedule(models.Model):
    key = models.AutoField(db_column='key', primary_key=True)
    team1_name = models.TextField(db_column='team1_name', default='-')
    team2_name = models.TextField(db_column='team2_name', default='-')
    team1_score = models.IntegerField(db_column='team1_score', default=0)
    team2_score = models.IntegerField(db_column='team2_score', default=0)
    datetime = models.DateTimeField(db_column='datetime', default=datetime(2000, 1, 1))
    etc = models.TextField(db_column='etc', default='-')

    class Meta:
        db_table = 'schedule'
    
class Ranking_2023_LCK_spring(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_2023_LCK_spring"
        
class Ranking_2023_LCK_summer(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_2023_LCK_summer"
        
class Ranking_2024_LCK_spring(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_2024_LCK_spring"

class Ranking_2024_LCK_spring_player(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    nickname = models.TextField(db_column="nickname", default="-")
    name = models.TextField(db_column="name", default="-")
    team = models.TextField(db_column="team", default="-")
    position = models.TextField(db_column="position", default="-")
    POG_point = models.IntegerField(db_column="POG_point", default=0)
    
    class Meta :
        db_table = "ranking_2024_LCK_spring_player"

class Champion_2023_LCK_summer(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_2023_LCK_summer"
        
class Champion_2024_LCK_spring(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_2024_LCK_spring"

class Version(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    league_version = models.TextField(db_column="league_version", default="-")
    live_version = models.TextField(db_column="live_version", default="-")
    
    class Meta:
        db_table = "version"

