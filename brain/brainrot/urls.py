from django.urls import path
from . import views  # Import views correctly

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat_with_groq, name='chat_with_groq'),
]