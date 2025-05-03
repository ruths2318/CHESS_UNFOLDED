# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code defines a table to store each game in the database.

from django.db import models

# Create your models here.

class Game(models.Model):
    """
    Represents a chess game stored in the database.

    Fields:
        pgn_text (TextField): The full PGN text of the game.
        date (DateField): The date on which the game was played.
        player_1 (CharField): Name of the white player.
        player_2 (CharField): Name of the black player.
        result (CharField): Result of the game.
    """
    pgn_text = models.TextField()  
    date = models.DateField()

    player_1 = models.CharField(max_length=100)
    player_2 = models.CharField(max_length=100)

    result = models.CharField(max_length=100)

