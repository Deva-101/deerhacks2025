from django.urls import path
from .views import home, brain  # Import the views

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('brain/', brain, name='brain'),  # Brain page
]
