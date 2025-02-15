from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .groq import get_groq_response  # Ensure this function is implemented

@csrf_exempt
def home(request):
    """
    Displays the initial input field where users enter their message.
    """
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            # Get AI response
            bot_response = get_groq_response(user_message)

            # Store user input and bot response in session for the next page
            request.session["user_message"] = user_message
            request.session["bot_response"] = bot_response

            return redirect('/brain')  # Redirect to brain.html

    return render(request, 'home.html')  # Show input field first

def brain(request):
    """
    Displays the chatbot's response after redirection.
    """
    user_message = request.session.pop("user_message", None)  # Retrieve and remove session data
    bot_response = request.session.pop("bot_response", None)

    if not user_message or not bot_response:
        return redirect('/')  # If no data is available, redirect back to home

    return render(request, 'brain.html', {"query": user_message, "reply": bot_response})
