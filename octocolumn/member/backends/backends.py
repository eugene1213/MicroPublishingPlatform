from member.models import User

__all__=(
    'FacebookBackend',
    'GoogleBackend',
    'TwitterBackend',
    'SecondPasswordBackend'
)


class FacebookBackend:
    def authenticate(self, request, facebook_user_id):
        try:
            return User.objects.get(username=f'fb_{facebook_user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class GoogleBackend:
    def authenticate(self, request, google_user_id):
        try:
            return User.objects.get(username=f'g_{google_user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class TwitterBackend:
    def authenticate(self, request, twitter_user_id):
        try:
            return User.objects.get(username=f't_{twitter_user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SecondPasswordBackend:
    pass