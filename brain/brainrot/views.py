from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .groq import get_groq_response  # Ensure this function is implemented
import re
from .firebase_config import get_database_ref  # Import Firebase config

@csrf_exempt
def home(request):
    """
    Displays the initial input field where users enter their message.
    On POST, calls Groq's API to get a response, converts that response
    to HTML, and also extracts a single region ID from the user's text.
    Saves the request details in Firebase.
    """
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            # 1) Get AI response from Groq
            bot_response = get_groq_response(user_message)

            # 2) Convert bot response to HTML
            formatted_response = convert_dream_text_to_html(bot_response)

            # 3) Extract exactly one region ID from the user's message
            extracted_region = extract_brain_region(user_message)

            # 4) Store data in Firebase Realtime Database with an ordered index
            save_request_to_firebase(user_message, formatted_response, extracted_region)

            # 5) Store data in session for the next page
            request.session["user_message"] = user_message
            request.session["bot_response"] = formatted_response  # Store as formatted HTML
            request.session["brain_region"] = extracted_region

            return redirect('/brain')

    # On GET, just show the input form
    return render(request, 'home.html')


def brain(request):
    """
    Displays the chatbot's response after redirection,
    along with any extracted region ID (in bold),
    and retrieves past conversation history.
    """
    # Retrieve latest response from session
    user_message = request.session.pop("user_message", None)
    formatted_response = request.session.pop("bot_response", None)
    region_id = request.session.pop("brain_region", None)

    # If no data available, go back to home
    if not user_message or not formatted_response:
        return redirect('/')

    # Fetch conversation history from Firebase
    history = get_conversation_history()

    return render(request, 'brain.html', {
        "query": user_message,
        "reply": formatted_response,
        "region_display": region_id,
        "history": history  # Pass conversation history to template
    })


def save_request_to_firebase(user_message, bot_response, region_id):
    """
    Saves the request details to Firebase Realtime Database with an ordered index.
    """
    ref = get_database_ref()
    requests_ref = ref.child("requests")

    # Fetch current data to determine the next index
    existing_requests = requests_ref.get()

    if isinstance(existing_requests, dict):  # Expected format
        next_index = max(map(int, existing_requests.keys())) + 1
    elif isinstance(existing_requests, list):  # Handle list case
        next_index = len(existing_requests) + 1
    else:  # If no previous data exists, start at index 1
        next_index = 1

    # Data structure
    new_request = {
        "user_query": user_message,
        "ai_response": bot_response,
        "brain_region": region_id
    }

    # Store in Firebase using ordered index
    requests_ref.child(str(next_index)).set(new_request)


def get_conversation_history():
    """
    Fetches all past conversations stored in Firebase.
    """
    ref = get_database_ref()
    requests_ref = ref.child("requests")
    history = requests_ref.get()

    if isinstance(history, dict):  # Expected format
        return [
            {"id": int(k), "user_query": v["user_query"], "ai_response": v["ai_response"], "brain_region": v["brain_region"]}
            for k, v in sorted(history.items(), key=lambda x: int(x[0]))  # Sort by index
        ]
    elif isinstance(history, list):  # Handle list case
        return [
            {"id": i + 1, "user_query": entry.get("user_query", ""), "ai_response": entry.get("ai_response", ""), "brain_region": entry.get("brain_region", "")}
            for i, entry in enumerate(history)
            if isinstance(entry, dict)  # Ensure valid data
        ]
    else:  # If no data exists
        return []


def convert_dream_text_to_html(dream_text: str) -> str:
    """
    Convert plain dream analysis text into HTML, applying these rules:
      - '**text**' => <h1>text</h1>
      - '*text*' => <p><b>text</b></p>
      - '\n' => <br>
    """
    # 1) Convert '**...**' to <h1>...</h1>
    html_text = re.sub(r'\*\*(.+?)\*\*', r'<h1>\1</h1>', dream_text)

    # 2) Convert '*...*' to <p><b>...</b></p>
    html_text = re.sub(r'\*(.+?)\*', r'<p><b>\1</b></p>', html_text)

    # 3) Convert newline characters "\n" to <br>
    html_text = html_text.replace('\n', '<br>')

    return html_text


def extract_brain_region(dream_text: str) -> str:
    """
    Calls Groq's AI to extract exactly ONE region from:
      'frontal-lobe', 'parietal-lobe', 'temporal-lobe',
      'occipital-lobe', 'cerebellum', 'brain-stem'.

    Returns just the region ID string (e.g. "temporal-lobe"),
    or an empty string if none was confidently identified.
    """

    # Define a system prompt that instructs the AI to pick exactly one from the list.
    system_prompt = f"""
You are an advanced AI with knowledge of neuroscience.
Given the user's dream text: "{dream_text}"

Select EXACTLY one best matching region from this list:
[frontal-lobe, parietal-lobe, temporal-lobe, occipital-lobe, cerebellum, brain-stem].

Output only the region name, with no extra text.
"""

    # Pass an empty user input, but use the system prompt
    region_response = get_groq_response(user_input="", system_prompt=system_prompt)

    region_id = region_response.strip().lower()

    valid_regions = {
        "frontal-lobe", "parietal-lobe", "temporal-lobe",
        "occipital-lobe", "cerebellum", "brain-stem"
    }
    if region_id not in valid_regions:
        return ""  # fallback if AI doesn't comply

    return region_id
