from django.db import models
from datetime import datetime

class Schedule(models.Model):
    key = models.AutoField(db_column='key', primary_key=True)
    team1_name = models.TextField(db_column='team1_name', default='-')
    team2_name = models.TextField(db_column='team2_name', default='-')
    team1_tricode = models.TextField(db_column='team1_tricode', default='-')
    team2_tricode = models.TextField(db_column='team2_tricode', default='-')
    team1_score = models.IntegerField(db_column='team1_score', default=0)
    team2_score = models.IntegerField(db_column='team2_score', default=0)
    date = models.DateTimeField(db_column='date', default=datetime(2000, 1, 1))
    tournament = models.TextField(db_column='tournament', default='-')
    etc = models.TextField(db_column='etc')

    class Meta:
        db_table = 'schedule'
    
class Ranking_LCK_2023_Spring(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_LCK_2023_spring"
        
class Ranking_LCK_2023_Summer(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_LCK_2023_summer"
        
class Ranking_LCK_2024_Spring(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    match_win = models.IntegerField(db_column="match_win", default=0)
    match_lose = models.IntegerField(db_column="match_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_LCK_2024_spring"

class Ranking_LCK_2024_Spring_player(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    nickname = models.TextField(db_column="nickname", default="-")
    name = models.TextField(db_column="name", default="-")
    team = models.TextField(db_column="team", default="-")
    tricode = models.TextField(db_column="tricode", default="-")
    position = models.TextField(db_column="position", default="-")
    POG_point = models.IntegerField(db_column="POG_point", default=0)
    
    class Meta :
        db_table = "ranking_LCK_2024_spring_player"

class Champion_LCK_2023_Summer(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_LCK_2023_summer"
        
class Champion_LCK_2024_Spring(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_LCK_2024_spring"

class Champion_MSI_2024(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_MSI_2024"

class Version(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    league_version = models.TextField(db_column="league_version", default="-")
    live_version = models.TextField(db_column="live_version", default="-")
    
    class Meta:
        db_table = "version"

