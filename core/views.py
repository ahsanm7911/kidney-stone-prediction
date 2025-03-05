from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    user = request.user
    if user.is_authenticated and user.is_patient:
        return redirect("patient_dashboard")
    if user.is_authenticated and user.is_doctor:
        return redirect("doctor_dashboard")
    
    return render(request, 'core/home.html')

def login_page(request):
    return render(request, 'core/login.html')

def forgot_password_page(request):
    return render(request, 'core/forgot-password.html')

