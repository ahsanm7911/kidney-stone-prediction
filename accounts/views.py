from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .models import CustomUser

# Create your views here.

@login_required
def doctor_dashboard(request):
    return HttpResponse("Welcome to doctor's dashboard")

@login_required
def patient_dashboard(request):
    return HttpResponse("Welcome to patient's dashboard")


@login_required
def choose_role(request):
    if request.user.user_type == 'patient':
        return redirect('patient_dashboard')

    if request.user.user_type == 'doctor':
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.user.user_type = user_type 
        request.user.save()
        return redirect('choose_role')

    return render(request, 'account/choose_role.html')
        
