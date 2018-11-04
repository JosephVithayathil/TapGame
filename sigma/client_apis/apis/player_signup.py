"""Apis for player signup."""
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from game_library.status_codes import GameStatusCodes
from game_library.game_enums import LevelEnum
from sigma_core.models import Player, PlayerLevels


@permission_classes((permissions.AllowAny,))
class PlayerSignupAPI(viewsets.ViewSet):

    def create(self, request, format=None):
        uname = request.data.get("uname", None)
        password = request.data.get("pwd", None)
        email = request.data.get("email", None)
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("first_name", None)
        if None in [uname, email, first_name, last_name]:
            return Response({"st": GameStatusCodes.ERROR})
        if User.objects.filter(username=uname).count() > 0:
            return Response({"st": GameStatusCodes.DUPLICATE_USERNAME})
        player_level = PlayerLevels.objects.cache_get(level=LevelEnum.LEVEL1)
        user = User.objects.create_user(
            username=uname,
            password=password,
            email=email
        )
        Player.objects.create(user=user, level=player_level)
        return Response({"st": GameStatusCodes.OK})



@permission_classes((permissions.AllowAny,))
class PlayerNameCheckAPI(viewsets.ViewSet):

    def create(self, request, format=None):
        uname = request.data.get("uname", None)
        if None in [uname]:
            return Response({"st": GameStatusCodes.ERROR})
        if User.objects.filter(username=uname).count() > 0:
            return Response({"st": GameStatusCodes.DUPLICATE_USERNAME})
        return Response({"st": GameStatusCodes.OK})
