from SalesGoApp.models import Post
from django.contrib import messages


class PostDao:
    """
    This class provides method to perform CRUD operations on Post.
    """

    def get_posts(self, user):
        posts = Post.objects.filter(user=user)
        return posts

    def get_post_by_title(self, user, title):
        try:
            post = Post.objects.get(user=user, title=title)
            return post
        except Post.DoesNotExist:
            return None

    def create_or_update_post(self, title, body, user, post_id=None):
        try:
            if post_id:
                post = Post.objects.get(user=user, id=post_id)
            else:
                post = Post()
            post.title = title
            post.body = body
            post.user = user
            post.save()
            return post
        except Exception as e:
            return None

