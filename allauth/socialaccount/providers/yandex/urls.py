from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import YandexOAuth2Provider

urlpatterns = default_urlpatterns(YandexOAuth2Provider)

