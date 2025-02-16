from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import re
from .groq import get_groq_response, dream_analysis_to_image_prompt, generate_image
from .firebase_config import get_database_ref  # Import Firebase config

@csrf_exempt
def home(request):
    """
    Displays the initial input field where users enter their message.
    On POST, calls Groq's API to get a response, converts that response
    to HTML, extracts a brain region, and saves details in Firebase.
    """
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            # 1) Get AI response from Groq
            bot_response = get_groq_response(user_message)

            # 2) Convert bot response to HTML
            formatted_response = convert_dream_text_to_html(bot_response)

            # 3) Extract brain region from dream text
            extracted_region = extract_brain_region(user_message)

            # 4) Generate image prompt based on AI response
            image_prompt = dream_analysis_to_image_prompt(bot_response)

            # 5) Generate dream image
            image_url = generate_image(image_prompt) if image_prompt else None

            # 6) Store data in Firebase
            save_request_to_firebase(user_message, formatted_response, extracted_region)

            # 7) Store session data for rendering on the next page
            request.session["user_message"] = user_message
            request.session["bot_response"] = formatted_response  # Store formatted HTML
            request.session["brain_region"] = extracted_region
            request.session["image_prompt"] = image_prompt
            request.session["image_url"] = image_url  # Save image path for display

            return redirect('/brain')

    return render(request, 'home.html')


def brain(request):
    """
    Displays the chatbot's response after redirection,
    along with any extracted brain region, generated dream image, and history.
    """
    user_message = request.session.pop("user_message", None)
    formatted_response = request.session.pop("bot_response", None)
    region_id = request.session.pop("brain_region", None)
    image_prompt = request.session.pop("image_prompt", None)
    image_url = request.session.pop("image_url", None)

    if not user_message or not formatted_response:
        return redirect('/')

    # Fetch conversation history from Firebase
    history = get_conversation_history()

    return render(request, 'brain.html', {
        "query": user_message,
        "reply": formatted_response,
        "region_display": region_id,
        "image_prompt": image_prompt,
        "image_url": image_url,  # Pass image URL to template
        "history": history
    })


def save_request_to_firebase(user_message, bot_response, region_id):
    """
    Saves the request details to Firebase Realtime Database with an ordered index.
    """
    ref = get_database_ref()
    requests_ref = ref.child("requests")

    existing_requests = requests_ref.get()
    if isinstance(existing_requests, dict):
        next_index = max(map(int, existing_requests.keys())) + 1
    elif isinstance(existing_requests, list):
        next_index = len(existing_requests) + 1
    else:
        next_index = 1

    new_request = {
        "user_query": user_message,
        "ai_response": bot_response,
        "brain_region": region_id
    }

    requests_ref.child(str(next_index)).set(new_request)


def get_conversation_history():
    """
    Fetches all past conversations stored in Firebase.
    """
    ref = get_database_ref()
    requests_ref = ref.child("requests")
    history = requests_ref.get()

    if isinstance(history, dict):
        return [{"id": int(k), "user_query": v["user_query"], "ai_response": v["ai_response"], "brain_region": v["brain_region"]}
                for k, v in sorted(history.items(), key=lambda x: int(x[0]))]
    elif isinstance(history, list):
        return [{"id": i + 1, "user_query": entry.get("user_query", ""), "ai_response": entry.get("ai_response", ""), "brain_region": entry.get("brain_region", "")}
                for i, entry in enumerate(history) if isinstance(entry, dict)]
    else:
        return []


def convert_dream_text_to_html(dream_text: str) -> str:
    """
    Converts dream text into formatted HTML.
    """
    html_text = re.sub(r'\*\*(.+?)\*\*', r'<h1>\1</h1>', dream_text)
    html_text = re.sub(r'\*(.+?)\*', r'<p><b>\1</b></p>', html_text)
    html_text = html_text.replace('\n', '<br>')
    return html_text


def extract_brain_region(dream_text: str) -> str:
    """
    Extracts a single brain region based on AI response.
    """
    system_prompt = f"""
    You are an advanced AI with knowledge of neuroscience.
    Given the user's dream text: "{dream_text}"
    Select EXACTLY one best matching region from this list:
    [frontal-lobe, parietal-lobe, temporal-lobe, occipital-lobe, cerebellum, brain-stem].
    Output only the region name, with no extra text.
    """
    region_response = get_groq_response(user_input="", system_prompt=system_prompt)
    region_id = region_response.strip().lower()
    valid_regions = {"frontal-lobe", "parietal-lobe", "temporal-lobe", "occipital-lobe", "cerebellum", "brain-stem"}
    return region_id if region_id in valid_regions else ""
