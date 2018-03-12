from member.models import User

__all__=(
    'FacebookBackend',
    'GoogleBackend',
    'KakaoBackend',
    'SecondPasswordBackend'
)


class FacebookBackend:
    def authenticate(self, user_id):
        print(f'fb_{facebook_user_id}')
        try:
            return User.objects.get(social_id=f'fb_{user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class GoogleBackend:
    def authenticate(self, user_id):
        try:
            return User.objects.get(social_id=f'g_{user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class KakaoBackend:
    def authenticate(user_id):
        try:
            return User.objects.get(social_id=f'k_{user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SecondPasswordBackend:
    def authenticate(self,user=None, password=None):
        pass

    pass