from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from SalesGoApp.dao.signupdao import RegisterUserDao
from SalesGoApp.dao.postdao import PostDao
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post
from django.core.paginator import Paginator
from django.conf import settings


class LoginView(View):
    """
    Class responsible for login the user.
    """
    template_name = 'login.html'

    def get(self, request):
        """
        Render the login page on GET Request.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Process the login form on POST request.
        """
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_view')  # Redirect to the home page on successful login
        else:
            # If authentication fails, return to the login page with an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)


class SignUpView(View):
    """
    class responsible to render for sign in the user.
    """
    template_name = 'signup.html'

    def get(self, request):
        """
        Render the signin page on GET Request.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Handle post request to register new user.
        """
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        context = {'email': email, 'username': username}
        error = self.validate_mandatory_and_len_check(username, email, password1, password2)
        if error:
            context['error'] = error
            return render(request, self.template_name, context)

        error = self.validate_passwords(password1, password2)
        if error:
            context['error'] = error
            return render(request, self.template_name, context)

        error = self.validate_username(username)
        if error:
            context['error'] = error
            return render(request, self.template_name, context)

        error = self.validate_email(email)
        if error:
            context['error'] = error
            return render(request, self.template_name, context)

        user = RegisterUserDao().register_user(username, email, password1)
        if user:
            messages.success(request, 'Successfully registered please login!')
            return redirect('login_view')

        messages.error(request, 'An error occurred while creating your account.')
        return render(request, self.template_name, context)

    def validate_mandatory_and_len_check(self, username, email, password1, password2):
        """
        Method to validate mandatory and length check.
        """
        if not username:
            error = "Username should not be empty."
            return error
        if len(username.strip()) > 20:
            error = "Username should not more than 20 characters."
            return error
        if not email:
            error = "Email should not be empty."
            return error
        if len(email.strip()) > 30:
            error = "Email should not more than 30 characters."
            return error
        if not password1:
            error = "Password should not be empty."
            return error
        if len(password1.strip()) > 10:
            error = "Password should not more than 10 characters."
            return error
        if not password2:
            error = "Confirm password should not be empty."
            return error
        if len(password2.strip()) > 10:
            error = "Confirm password should not more than 10 characters."
            return error
        return False

    def validate_passwords(self, password1, password2):
        """
        Method to check if password and confirm password is same.
        """
        if password1 != password2:
            error = "Passwords do not match."
            return error
        return False

    def validate_username(self, username):
        """
        Method to check id user already exists.
        """
        if User.objects.filter(username=username).exists():
            error = "Username already exists."
            return error
        return False

    def validate_email(self, email):
        """
        Method to check if email already exists.
        """
        if User.objects.filter(email=email).exists():
            error = "Email already registered."
            return error
        return False


class DashboardView(View):
    """
    Class responsible to render the dashboard page.
    """

    def get(self, request):
        # Pass the username to the context
        context = {
            'username': request.user.username
        }
        return render(request, 'dashboard.html', context)


class PostListView(View):
    """
    Class responsible for get and post method on posts.
    """

    def get(self, request):
        posts = PostDao().get_posts(request.user)
        paginator = Paginator(posts, settings.NO_OF_ROW_PER_PAGE)

        page_number = request.GET.get('page')
        page_objs = paginator.get_page(page_number)
        return render(request, 'posts.html', {'page_objs': page_objs, 'username': request.user})


class PostBaseClass:

    def __init__(self):
        pass

    def validate_post_data(self, title, body):
        if not title:
            error = "Title should not be empty."
            return error
        if not body:
            error = "Body should not be empty."
            return error
        if len(title.strip()) > 50:
            error = "Title should not be more than 50 characters."
            return error
        if len(body.strip()) > 100:
            error = "Body should not be more than 100 characters."
            return error
        return False


class PostCreateView(View, PostBaseClass):
    """
    View to handle the creation of a new post.
    """
    template_name = 'post.html'

    def get(self, request):
        return render(request, self.template_name, {'username': request.user})

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        context = {'title': title, 'body': body, 'username': request.user}
        error = super().validate_post_data(title, body)
        if error:
            context['error'] = error
            return render(request, self.template_name, context)
        post = PostDao().create_or_update_post(title, body, request.user)
        if post:
            return redirect('posts_view')  # Redirect to the list of posts
        messages.error(request, 'An error occurred while creating your post.')
        return render(request, self.template_name, context)


class PostEditView(View, PostBaseClass):
    """
    View to handle editing an existing post.
    """
    template_name = 'post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, self.template_name, {'post': post, 'username': request.user})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        title = request.POST.get('title')
        body = request.POST.get('body')
        context = {'username': request.user}
        error = super().validate_post_data(title, body)
        if error:
            context['error'] = error
            context['post'] = post
            return render(request, self.template_name, context)
        post = PostDao().create_or_update_post(title, body, request.user, pk)
        if post:
            return redirect('posts_view')  # Redirect to the list of posts
        messages.error(request, 'An error occurred while updating your post.')
        return render(request, self.template_name, context)


class PostDeleteView(View):
    """
    View to handle deleting an existing post.
    """
    def get(self, request, pk):
        print("pk", pk)
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('posts_view')





