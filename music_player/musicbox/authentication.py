from django.contrib.auth.backends import BaseBackend

from musicbox.models import User


class EmailBackEnd(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user_object = User.objects.get(email=username)
        if user_object.check_password(password):
            return user_object
        else:
            return None

    def get_user(self, user_id):
        try:
            user_object = User.objects.get(id=user_id)
            return user_object
        except:
            return None
