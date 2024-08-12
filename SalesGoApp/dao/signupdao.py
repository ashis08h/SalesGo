from django.contrib.auth.models import User
from django.contrib import messages


class RegisterUserDao:
    """
    This class provides method to perform CRUD operations on User.
    """

    def register_user(self, username, email, password):
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return user
        except Exception as e:
            return None