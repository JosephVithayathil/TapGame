"""Client rest api urls."""
from rest_framework.routers import SimpleRouter
from .apis import player_signup


urlpatterns = [
]
router = SimpleRouter(trailing_slash=False)

# Player Signup API
router.register(r'player_signup_api', player_signup.PlayerSignupAPI, "player_signup_api")
router.register(r'player_name_check_api', player_signup.PlayerNameCheckAPI, "player_name_check_api")

urlpatterns += router.urls