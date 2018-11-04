from django.db import models
from django.contrib.auth.models import User
from game_library.locale_cache_manager import LocaleCacheModel
from game_library.game_enums import LevelEnum

# Create your models here.

class PlayerLevels(LocaleCacheModel):
    """Player Level model."""

    level = models.IntegerField(choices=LevelEnum.choices(), default=LevelEnum.LEVEL1)
    min_points = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)


class Player(models.Model):
    """Player model."""

    user = models.OneToOneField(User, related_name="player_user", null=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    level = models.ForeignKey(PlayerLevels, related_name="player_level", null=True, on_delete=models.CASCADE)
    reply_channel = models.CharField(max_length=250, null=True, unique=True)
