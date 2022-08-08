from django.conf import settings
from core.models import Profile
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication 

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        perfil = None
        api_key = request.GET.get('api_key')
        
        if not api_key:
            raise exceptions.AuthenticationFailed('api_key no especificado.')

        if api_key == settings.TEST_API_KEY:
            instance = Profile.objects.filter(user__username="admin_test").first()
        else:
            try:
                instance = Profile.objects.get(api_key=api_key)
            except Profile.DoesNotExist:
                raise exceptions.AuthenticationFailed(f'api_key is invalid. {api_key}')

        return (instance.user, None)



class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening        