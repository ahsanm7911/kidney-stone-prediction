from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import date
import datetime

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

TIME_SLOTS = [(datetime.time(hour, minute).strftime("%H:%M:%S"), datetime.time(hour, minute).strftime("%I:%M %p")) for hour in range(8, 18) for minute in [0, 30]
]

DAY_CHOICES = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]

BLOOD_GROUP_CHOICES= [
    ('A+', 'A+'), 
    ('A-', 'A-'), 
    ('B+', 'B+'), 
    ('B-', 'B-'), 
    ('O+', 'O+'), 
    ('O-', 'O-'), 
    ('AB+', 'AB+'), 
    ('AB-', 'AB-')
]


def validate_dob(value):
    if value > now().date():
        raise ValidationError("Date of birth cannot be in the future")
    
def calculate_age(dob):
    """Calculate age based on date of birth"""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def is_date_passed(input_date):
    try:
        # Convert string date to datetime object 
        given_date = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")

        # Get current date (without time for fair comparison)
        current_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Compare dates 
        if given_date < current_date:
            return "passed"
        elif given_date > current_date:
            return "upcoming"
        else:
            return "today"
        
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD"
    

def format_date(input_date):
    print(f"Date format: {input_date}")
    try:
        # Convert string date to datetime object 
        date_obj = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")

        # Get day name and day number 
        day_name = date_obj.strftime("%A") # Full day name 
        day_number = date_obj.strftime("%d") # Day of Month

        # Return formatted string 
        return f"{day_name}, {day_number}"
    
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD"
    

def get_time_greeting():
    # Get current hour (24-hour format)
    current_hour = datetime.datetime.now().hour

    # Determine appropriate greeting based on hour 
    if 5 <= current_hour < 12:      # 5:00 AM to 11:59AM
        return "Good Morning"
    elif 12 <= current_hour < 17:   # 12:00 PM to 4:59 PM
        return "Good Afternoon"
    else:                           # 5:00 PM to 4:59 AM
        return "Good Evening"