from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def login_page(request):
    return render(request, 'core/login.html')

def forgot_password_page(request):
    return render(request, 'core/forgot-password.html')

