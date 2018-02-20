from member.models import User

__all__=(
    'FacebookBackend',
    'GoogleBackend',
    'TwitterBackend',
    'SecondPasswordBackend'
)


class FacebookBackend:
    def authenticate(facebook_user_id):
        print(f'fb_{facebook_user_id}')
        try:
            return User.objects.get(social_id=f'fb_{facebook_user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class GoogleBackend:
    def authenticate(google_user_id):
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
    def authenticate(self,request,user_id):
        pass

    pass