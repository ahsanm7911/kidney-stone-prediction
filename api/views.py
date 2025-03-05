from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta, time 
from doctors.models import Doctor
from appointments.models import Appointment
# Rest imports 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from .serializers import AppointmentSerializer

# Create your views here.
def generate_time_slots(start_time, end_time):
    """
    Generate 1-hour slots between the given start and end time.
    """
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)

    while current_time.time() < end_time:
        slots.append(current_time.strftime("%I:%M %p")) # Format as "9:00 AM"
        current_time += timedelta(hours=1)

    return slots 

def get_available_slots(request, doctor_id):
    """
    Get a doctor's available slots exluding already booked ones. 
    Returns JSON response. 
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor_name = f"Dr. {doctor.user.first_name} {doctor.user.last_name}"
    available_days = doctor.available_days
    available_days = [day.capitalize() for day in available_days]
    print("Available days: ", available_days)
    start_time = doctor.available_start_time
    end_time = doctor.available_end_time

    today = datetime.today()
    availability = {}

    # Check for the next 7 days 
    for i in range(7):
        check_date = today + timedelta(days=i)
        day_name = check_date.strftime("%A") # Convert date to a weekday name 

        if day_name in available_days: # Only add slots for working days 
            slots = generate_time_slots(start_time, end_time)

            # Get booked slots for this doctor on this date 
            booked_slots = Appointment.objects.filter(doctor=doctor, appointment_date=check_date.date()).values_list("appointment_time", flat=True)
            booked_slots = {t.strftime("%I:%M %p") for t in booked_slots} # Convert to AM/PM format 
            print("Booked slots: ", booked_slots)
            # Remove booked slots 
            available_slots = [slot for slot in slots if slot not in booked_slots]
            print("Available slots: ", available_slots)

            if available_slots:
                availability[check_date.strftime("%Y-%m-%d")] = available_slots

    response_data = {
        "doctor_id": str(doctor.id),
        "doctor_name": doctor_name, 
        "availability": availability
    }

    return JsonResponse(response_data, safe=False)

@api_view(["POST"])
@permission_classes([IsAuthenticated]) # Only authenticated users can book
def book_appointment(request):
    """
    API to book an appointment with a doctor 
    Required fields: doctor_id, date, time 
    Optional field: report (file upload)
    """
    data = request.data.copy() # Copy request data to modify it.
    print("Data received from frontend: ", data)
    # Ensure the user is a patient 
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'Only patients can book appointments.'}, status=status.HTTP_403_FORBIDDEN)
    
    # Ensure doctor exists 
    try:
        doctor = Doctor.objects.get(id=data.get("doctor_id"))
    except Doctor.DoesNotExist:
        return Response({'error': "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # Add patient and doctor to request data
    data['patient'] = patient.id
    data['doctor'] = doctor.id

    # Validate and save the appointment 
    serializer = AppointmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Appointment booked successfully.", "appointment": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

