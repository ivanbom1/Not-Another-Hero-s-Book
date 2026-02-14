from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from game.models import UserProfile


class RegisterView(View):

    def get(self, request):
        return render(request, 'auth/registration.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role', 'reader')

        if not username or not email or not password:
            return render(request, 'auth/register.html', {
                'error': 'All fields are required'
            })

        if password != password_confirm:
            return render(request, 'auth/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                'error': 'Username already exists'
            })


        user = User.objects.create_user(username=username, email=email, password=password)

        UserProfile.objects.create(user=user, role=role)

        login(request, user)
        return redirect('stories_list')


class LoginView(View):

    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('stories_list')
        else:
            return render(request, 'auth/login.html', {
                'error': 'Invalid username or password'
            })

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('stories_list')