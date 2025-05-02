# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code defines a table to store each game in the database.

from django.db import models

# Create your models here.

class Game(models.Model):
    pgn_text = models.TextField()  
    date = models.DateField()

    player_1 = models.CharField(max_length=100)
    player_2 = models.CharField(max_length=100)

    result = models.CharField(max_length=100)

