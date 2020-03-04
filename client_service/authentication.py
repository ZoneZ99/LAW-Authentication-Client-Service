from datetime import datetime

from django.contrib.auth.backends import BaseBackend
from django.db import models
from rest_framework.authentication import get_authorization_header, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from auth_token.models import LAWAuthToken


class LAWAuthenticationBackend(BaseBackend):
    keyword = "Bearer"
    model = None

    def authenticate(self, request, **kwargs):
        pass

    def get_model(self):
        if self.model is not None:
            return self.model
        return LAWAuthToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if datetime.now() >= token.expired:
            raise AuthenticationFailed("Stale token given.")

        return token.user, token
