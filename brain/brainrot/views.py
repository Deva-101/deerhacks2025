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
            # Get AI response from Groq API
            bot_response = get_groq_response(user_message)

            # Store user input and bot response in session for the next page
            request.session["user_message"] = user_message
            request.session["bot_response"] = bot_response

            return redirect('/brain')  # Redirect to brain.html to show the response

    # Display the input field on GET request
    return render(request, 'home.html')  

def brain(request):
    """
    Displays the chatbot's response after redirection.
    """
    # Retrieve user message and bot response from session
    user_message = request.session.get("user_message")  # Using .get() to avoid KeyError
    bot_response = request.session.get("bot_response")

    # If no message or response in the session, redirect back to home
    if not user_message or not bot_response:
        return redirect('/')  # Redirect to home if no data is available

    # Pass the user message and bot response to the template
    return render(request, 'brain.html', {"query": user_message, "reply": bot_response})
