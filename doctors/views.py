from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from helpers import get_time_greeting, is_date_passed, format_date
from accounts.forms import DoctorForm
from appointments.models import Appointment
from .models import Doctor
from appointments.forms import AppointmentActionForm, AppointmentFilterForm
from datetime import datetime, timedelta



# Doctor views
@login_required
def overview(request):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return "Doctor profile doesnot exists for this user."
    
    # Default date range: last 30 days
    default_end_date = datetime.today().date()
    default_start_date = default_end_date - timedelta(days=30)

    # Filter form for date range
    filter_form = AppointmentFilterForm(request.GET or None)
    appointments = doctor.appointments.all()

    if filter_form.is_valid():
        start_date = filter_form.cleaned_data['start_date'] or default_start_date
        end_date = filter_form.cleaned_data['end_date'] or default_end_date
    else:
        start_date = default_start_date
        end_date = default_end_date

    # Filter appointments by date range
    filtered_appointments = appointments.filter(appointment_date__gte=start_date, appointment_date__lte=end_date)

    # Analytics
    total_patients = filtered_appointments.values('patient').distinct().count()
    completed_appointments = filtered_appointments.filter(status='completed').count()
    cancelled_appointments = filtered_appointments.filter(status='cancelled').count()
    pending_appointments = filtered_appointments.filter(status='pending').count()
    confirmed_appointments = filtered_appointments.filter(status='confirmed').count()

    # Average appointments per day
    days_in_range = (end_date - start_date).days + 1  # Inclusive range
    total_appointments = filtered_appointments.count()
    avg_appointments_per_day = total_appointments / days_in_range if days_in_range > 0 else 0

    # Data for line chart: appointments per day
    date_labels = []
    daily_appointments = []
    current_date = start_date
    while current_date <= end_date:
        date_labels.append(current_date.strftime('%Y-%m-%d'))
        count = filtered_appointments.filter(appointment_date=current_date).count()
        daily_appointments.append(count)
        current_date += timedelta(days=1)

    context = {
        'greeting': get_time_greeting(),
        'doctor': doctor,
        'filter_form': filter_form,
        'total_patients': total_patients,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'avg_appointments_per_day': round(avg_appointments_per_day, 2),
        'start_date': start_date,
        'end_date': end_date,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'date_labels': date_labels,
        'daily_appointments': daily_appointments,
    }
    return render(request, "doctors/overview.html", context)

@login_required
def appointments(request):
    user = request.user
    try:
        doctor = user.doctor_profile
    except Doctor.DoesNotExist:
        return "Doctor Profile doesnot exist for this user."

    today = datetime.today().date()
    # Appointment filter form 
    filter_form = AppointmentFilterForm(request.GET or None)
    appointments = doctor.appointments.all()
    
    if filter_form.is_valid():
        status = filter_form.cleaned_data['status']
        start_date = filter_form.cleaned_data['start_date']
        end_date = filter_form.cleaned_data['end_date']

        if status and status != 'all':
            appointments = appointments.filter(status=status)
        if start_date:
            appointments = appointments.filter(appointment_date__gte=start_date)
        if end_date:
            appointments = appointments.filter(appointment_date__lte=end_date)

    if request.method == 'POST':
        print("Post request: ", request.POST)
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
        form = AppointmentActionForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            msg = f"Appointment has been {form.cleaned_data['status']}."
            print(msg)
            messages.success(request, msg)
            return redirect('appointments_for_doctor')
        else:
            print(f"Form validation not passed, Errors: {form.errors}")
    else:
        form = AppointmentActionForm()
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'filter_form':  filter_form,
        'form': form,
        'today': today,
    }
    return render(request, 'doctors/appointments.html', context)

@login_required
def appointment_detail(request, appointment_id):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return "No Doctor profile for this user."
    
    # Ensure the appointment belongs to this doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    patient = appointment.patient

    return render(request, 'doctors/appointment_detail.html', {
        'appointment': appointment,
        'patient': patient,
    })

@login_required
def settings(request):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        doctor = Doctor(user=request.user)
        doctor.save()

    profile_form = DoctorForm(instance=doctor)
    has_password = request.user.has_usable_password()
    if has_password:
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
    else:
        password_form = SetPasswordForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = DoctorForm(request.POST, instance=doctor)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if profile_form.is_valid() and first_name and last_name:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully!")
            else:
                if not first_name or not last_name:
                    messages.error(request, "First name and last name are required.")
        elif 'change_password' in request.POST:
            if has_password:
                password_form = PasswordChangeForm(user=request.user, data=request.POST)
                password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
            else:
                password_form = SetPasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Your password has been {} successfully!".format("changed" if has_password else "set"))
                return redirect('settings_for_doctor')
            else:
                messages.error(request, "Please correct the errors below.")

    return render(request, 'doctors/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'doctor': doctor,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'has_password': has_password,
    })