from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import DoctorForm, PatientForm

# Create your views here.



@login_required 
def check_profile(request):
    user = request.user 
    if not user.is_profile_complete:
        return redirect("complete_profile")
    
    if user.is_patient:
        return redirect("patient_dashboard")

    if user.is_doctor:
        return redirect("doctor_dashboard")
    
@login_required
def choose_role(request):
    user = request.user 
    if user.is_patient or user.is_doctor:
        return redirect("complete_profile")
    
    if user.is_profile_complete:
        return redirect("check_profile")
    
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.user.user_type = user_type 
        request.user.save()

        return redirect('complete_profile')

    return render(request, 'account/choose_role.html')
        

@login_required
def complete_profile(request):
    user = request.user 

    if user.is_profile_complete:
        return redirect("check_profile")
    
    if user.is_doctor:
        form = DoctorForm(request.POST or None)
    elif user.is_patient:
        form = PatientForm(request.POST or None)
    else:
        return redirect("choose_role")
    
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = user
        profile.save()

        # Mark profile as complete 
        user.is_profile_complete = True 
        user.save()

        return redirect("check_profile")

    return render(request, "account/complete_profile.html", {"form": form})