from django.shortcuts import render

def home(request):
    return render(request, 'brain.html')  # This looks inside 'brainrot/templates/brain.html'
