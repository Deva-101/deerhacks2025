import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .groq import get_groq_response  # Import chatbot function

@csrf_exempt  # Disable CSRF for simplicity (enable it in production)
def chat_with_groq(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request body
            user_input = data.get("user_input")

            if not user_input:
                return JsonResponse({"error": "Missing 'user_input' parameter"}, status=400)

            response_text = get_groq_response(user_input)  # Call the function

            return JsonResponse({"response": response_text})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return HttpResponse("Invalid request method", status=405)


from django.shortcuts import render

def home(request):
    return render(request, 'brain.html')  # This looks inside 'brainrot/templates/brain.html'
