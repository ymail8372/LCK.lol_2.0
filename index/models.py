from django.db import models

class Schedule(models.Model):
    key = models.AutoField(db_column='key', primary_key=True)
    year = models.TextField(db_column='year', default='-')
    month = models.IntegerField(db_column='month', default=0)
    day = models.IntegerField(db_column='day', default=0)
    weekday = models.TextField(db_column='weekday', default='-')
    team1_name = models.TextField(db_column='team1_name', default='-')
    team2_name = models.TextField(db_column='team2_name', default='-')
    team1_tricode = models.TextField(db_column='team1_tricdoe', default='-')
    team2_tricode = models.TextField(db_column='team2_tricode', default='-')
    team1_score = models.IntegerField(db_column='team1_score', default=0)
    team2_score = models.IntegerField(db_column='team2_score', default=0)
    hour = models.IntegerField(db_column='hour', default=0)
    min = models.IntegerField(db_column='min', default=0)
    ampm = models.TextField(db_column='ampm', default='-')
    etc = models.TextField(db_column='etc', default='-')

    class Meta:
        db_table = 'schedule'
    
class Ranking_23_spring_regular(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    game_win = models.IntegerField(db_column="game_win", default=0)
    game_lose = models.IntegerField(db_column="game_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_23_spring_regular"
        
class Ranking_23_summer_regular(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    game_win = models.IntegerField(db_column="game_win", default=0)
    game_lose = models.IntegerField(db_column="game_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_23_summer_regular"
        
class Ranking_24_spring_regular(models.Model):
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default='-')
    tricode = models.TextField(db_column="tricode", default='-')
    game_win = models.IntegerField(db_column="game_win", default=0)
    game_lose = models.IntegerField(db_column="game_lose", default=0)
    set_win = models.IntegerField(db_column="set_win", default=0)
    set_lose = models.IntegerField(db_column="set_lose", default=0)
    etc = models.TextField(db_column="etc", default='-')
    
    class Meta:
        db_table = "ranking_24_spring_regular"

class Ranking_24_spring_player(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    date = models.TextField(db_column="date", default="-")
    name = models.TextField(db_column="name", default="-")
    nickname = models.TextField(db_column="nickname", default="-")
    team = models.TextField(db_column="team", default="-")
    position = models.TextField(db_column="position", default="-")
    
    class Meta :
        db_table = "ranking_24_spring_player"

class Champion_23_LCK_summer(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_23_LCK_summer"
        
class Champion_24_LCK_spring(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    name = models.TextField(db_column="name", default="-")
    pick = models.IntegerField(db_column="pick", default=0)
    ban = models.IntegerField(db_column="ban", default=0)
    win = models.IntegerField(db_column="win", default=0)
    lose = models.IntegerField(db_column="lose", default=0)
    patch = models.TextField(db_column="patch", default="-")
    
    class Meta:
        db_table = "champion_24_LCK_spring"
        
class Version(models.Model) :
    key = models.AutoField(db_column="key", primary_key=True)
    league_version = models.TextField(db_column="league_version", default="-")
    live_version = models.TextField(db_column="live_version", default="-")
    
    class Meta:
        db_table = "version"