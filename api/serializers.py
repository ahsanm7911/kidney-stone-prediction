from rest_framework import serializers
from datetime import datetime
from appointments.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    appointment_time = serializers.CharField() # Accept time as a string 

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointment_date', 'appointment_time', 'report']

        def validate_time(self, value):
            """ Convert 12-hour format (10:00 AM) to 24-hour format (10:00:00)"""
            try:
                # Convert to 24-hour format 
                converted_time = datetime.strptime(value, "%I:%M %p").time()
                return converted_time # Returns correct format: 10:00:00
            except ValueError:
                raise serializers.ValidationError("Invalid time format. Use 'HH:MM AM/PM'")

        def validate(self, data):
            """ Ensure the selected appointment slot is available."""
            doctor = data.get('doctor')
            date = data.get('appointment_date')
            time = data.get('appointment_time')
            print("Time format: ", time)
            # Check if the slot is already booked.
            if Appointment.objects.filter(doctor=doctor, appointment_date=date, appointment_time=time).exists():
                raise serializers.ValidationError("This time slot is already booked. Please choose another time.")
            
            return data