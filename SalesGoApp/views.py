from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from SalesGoApp.dao.signupdao import RegisterUserDao
from django.contrib import messages
from django.contrib.auth.models import User


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
        # Process the login form on POST request
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_view')  # Redirect to the home page on successful login
        else:
            # If authentication fails, return to the login page with an error message
            return render(request, self.template_name, {'error': 'Invalid username or password'})


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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        context = {'email': email, 'username': username}
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
            return redirect('login_view')

        context['error'] = "An error occurred while creating your account."
        return render(request, self.template_name, context)

    def validate_passwords(self, password1, password2):
        if password1 != password2:
            error = "Passwords do not match."
            return error
        return False

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            error = "Username already exists."
            return error
        return False

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            error = "Email already registered."
            return error
        return False


