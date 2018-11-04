"""Client rest api urls."""
from rest_framework.routers import SimpleRouter
from .apis import player_signup, player_login


urlpatterns = [
]
router = SimpleRouter(trailing_slash=False)

# Player Signup API's
router.register(r'player_signup_api', player_signup.PlayerSignupAPI, "player_signup_api")
router.register(r'player_name_check_api', player_signup.PlayerNameCheckAPI, "player_name_check_api")

# Player Login API's
router.register(r'player_login_api', player_login.PlayerLoginAPI, "player_login_api")
router.register(r'player_logout_api', player_login.PlayerLogoutAPI, "player_logout_api")

urlpatterns += router.urls