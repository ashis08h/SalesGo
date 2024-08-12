from SalesGoApp.models import Post
from django.contrib import messages


class PostDao:
    """
    This class provides method to perform CRUD operations on Post.
    """

    def get_posts(self, user, post_id=None):
        if post_id:
            pass
        else:
            posts = Post.objects.filter(user=user)
        return posts

    def get_post_by_title(self, user, title):
        try:
            post = Post.objects.get(user=user, title=title)
            return post
        except Post.DoesNotExist:
            return None

    def create_post(self, title, body, user):
        try:
            post = Post()
            post.title = title
            post.body = body
            post.user = user
            post.save()
            return post
        except Exception as e:
            return None
