from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from .models import User

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')