from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model class.
    """
    title = models.CharField(max_length=50)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title