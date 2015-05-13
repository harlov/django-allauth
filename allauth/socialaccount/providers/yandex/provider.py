from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount import app_settings


class YandexOAuth2Account(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('publicProfileUrl')

    def get_avatar_url(self):
        # try to return the higher res picture-urls::(original) first
        try:
            return self.account.extra_data['pictureUrls']['values'][0]
        except:
            pass  # if we can't get higher res for any reason, we'll just return the low res
        return self.account.extra_data.get('pictureUrl')

    def to_str(self):
        dflt = super(YandexOAuth2Account, self).to_str()
        name = self.account.extra_data.get('name', dflt)
        first_name = self.account.extra_data.get('firstName', None)
        last_name = self.account.extra_data.get('lastName', None)
        if first_name and last_name:
            name = first_name + ' ' + last_name
        return name


class YandexOAuth2Provider(OAuth2Provider):
    id = 'yandex'
    # Name is displayed to ordinary users -- don't include protocol
    name = 'Yandex'
    package = 'allauth.socialaccount.providers.yandex'
    account_class = YandexOAuth2Account

    def extract_uid(self, data):
        return str(data['id'])

    def get_profile_fields(self):
        default_fields = ['id',
                          'first-name',
                          'last-name',
                          'email-address',
                          'picture-url',
                          'picture-urls::(original)',  # picture-urls::(original) is higher res
                          'public-profile-url']
        fields = self.get_settings().get('PROFILE_FIELDS',
                                         default_fields)
        return fields

    def get_default_scope(self):
        scope = []
        return scope

    def extract_common_fields(self, data):
        return dict(email=data.get('emailAddress'),
                    first_name=data.get('firstName'),
                    last_name=data.get('lastName'))


providers.registry.register(YandexOAuth2Provider)
