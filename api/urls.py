from django.urls import path 
from .views import get_available_slots, book_appointment

urlpatterns = [
    path('available-slots/<int:doctor_id>/', get_available_slots, name='get_available_slots_api'),
    path('book-appointment/', book_appointment, name="book_appointment_api")
]
