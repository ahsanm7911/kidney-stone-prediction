from django.urls import path 
from .views import choose_role, check_profile, complete_profile

urlpatterns = [
    path('', choose_role, name='choose_role' ),
    path('check-profile/', check_profile, name='check_profile'),
    path('complete-profile/', complete_profile, name='complete_profile'),
]
