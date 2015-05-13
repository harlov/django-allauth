import requests
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from .provider import YandexOAuth2Provider

class YandexOAuth2Adapter(OAuth2Adapter):
    provider_id = YandexOAuth2Provider.id
    access_token_url = 'https://oauth.yandex.ru/token'
    authorize_url = 'https://oauth.yandex.ru/authorize'
    profile_url = 'https://login.yandex.ru/info'
    supports_state = False

    access_token_method = 'POST'

    def complete_login(self, request, app, token, **kwargs):
        provider = providers.registry.by_id(YandexOAuth2Provider.id)
        extra_data = self.get_user_info(token)
        user,domain = extra_data['default_email'].split('@')
        only_domain = provider.get_settings().get('ONLY_DOMAIN')
        if domain is not only_domain:
            print('BAD DOMAIN')
            return redirect(provider.get_settings().get('BAD_DOMAIN_REDIRECT'))
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_user_info(self, token):
        fields = providers.registry \
            .by_id(YandexOAuth2Provider.id) \
            .get_profile_fields()
        url = self.profile_url + '?format=json'
        resp = requests.get(url, params={'oauth_token': token.token})
        return resp.json()

oauth2_login = OAuth2LoginView.adapter_view(YandexOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(YandexOAuth2Adapter)
