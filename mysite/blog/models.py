from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

class Player(models.Model):
    id       = models.AutoField(primary_key=True)
    name     = models.CharField(max_length=20)
    account  = models.CharField(max_length=20)
    pwd      = models.CharField(max_length=20)
    ranking  = models.IntegerField(default=999)
    winCount = models.IntegerField(default=0)
    

    def check_password(self, player_id, raw_password):
        """檢查密碼是否正確"""
        player = Player.objects.get(id=player_id)
        return player.pwd == raw_password
# Create your models here.
class Match(models.Model):
    match_time = models.DateTimeField()
    player1    = models.CharField(max_length=100)
    player2    = models.CharField(max_length=100)
    winner     = models.CharField(max_length=100, default="None") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2} at {self.match_time}"