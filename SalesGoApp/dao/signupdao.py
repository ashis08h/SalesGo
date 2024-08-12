from django.contrib.auth.models import User


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
            messages.error(self.request, f"An error occurred: {e}")
            return None