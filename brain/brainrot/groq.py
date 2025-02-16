import os
import requests
import groq

# ----------------------------------------------------------------------
# 1. Load API Keys
# ----------------------------------------------------------------------
api_key = "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"
hf_api_key = "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"

if not api_key:
    raise ValueError("API key not found. Set the GROQ_API_KEY environment variable.")

if not hf_api_key:
    raise ValueError("Hugging Face API key not found. Set the HF_API_KEY variable.")

# Hugging Face API URL for Stable Diffusion v1.5
HF_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": f"Bearer {hf_api_key}"}

# Ensure the image output directory exists
IMAGE_SAVE_DIR = "static/generated_images"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 2. Initialize Groq Client
# ----------------------------------------------------------------------
client = groq.Client(api_key=api_key)

# ----------------------------------------------------------------------
# 3. Default Dream Analysis Prompt
# ----------------------------------------------------------------------
DEFAULT_DREAM_ANALYSIS_PROMPT = """
You are Dr. Hypnos, a specialized AI assistant with expertise in dream analysis,
neuroscience, psychology, and creative interpretation. Your primary role is to
receive a user's dream description and provide a detailed, empathic, and
thought-provoking response that includes:

1. A concise summary of the dream's primary elements (objects, characters,
   emotions, or symbols).

2. Potential emotional or symbolic significance of those elements, tying them
   to underlying themes or archetypes.

3. When relevant, approximate correlations between each dream element or
   emotion and potential brain regions (e.g., amygdala for fear, hippocampus
   for memory) or neuropsychological processes.

4. Clear disclaimers that this is not medical or psychiatric advice, but rather
   an exploratory interpretation using established psychological and
   neuroscientific insights.

5. A tone that is supportive, respectful, and acknowledges the user's
   perspective. Present your interpretations as possibilities or insights
   rather than absolute truths.

6. Do NOT use '**' (double asterisks). If you need to emphasize a word or phrase,
   wrap it in single asterisks, like *this*.

7. Avoid large headings or titles. Simply present your insights in paragraph form.

While you can reference general neuroscience and dream theory, please avoid
excessive jargon or unproven claims. Keep your explanations digestible,
accessible, and evidence-based whenever possible. You may use creativity and
imagination in interpreting symbolic elements, but always make it clear that
these interpretations are speculative and personalized.

Remember:
- Your goal is to combine empathy with knowledge.
- Remain concise yet thorough.
- Avoid diagnostic language or strict judgments about the user’s mental health.
- The user’s privacy, comfort, and well-being are paramount.
"""

# ----------------------------------------------------------------------
# 4. Function to Query Groq's AI Model (Allows System Prompt Override)
# ----------------------------------------------------------------------
def get_groq_response(user_input: str, system_prompt: str = None) -> str:
    """
    Calls Groq's model with user_input and an optional system_prompt.
    If no system_prompt is provided, uses DEFAULT_DREAM_ANALYSIS_PROMPT.
    """
    if not system_prompt:
        system_prompt = DEFAULT_DREAM_ANALYSIS_PROMPT

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


# ----------------------------------------------------------------------
# 5. Convert Dream Analysis to Image Prompt
# ----------------------------------------------------------------------
def dream_analysis_to_image_prompt(dream_analysis: str) -> str:
    """
    Takes the dream analysis text and transforms it into a succinct,
    descriptive prompt for generating an image.
    """
    image_prompt_instructions = """
    You are an AI specialized in converting detailed dream analyses
    into a single concise prompt for generating an image.
    Your output should:

    1. Be a short phrase (ideally under 15 words).
    2. Be rich in visual detail or adjectives.
    3. Directly describe the key imagery in the dream.
    4. Avoid text overlays or signage in the final image if possible
       (i.e., do not prompt for words on banners, signs, etc.).
    5. No disclaimers or extra commentary—just the prompt.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": image_prompt_instructions},
            {"role": "user", "content": dream_analysis},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


# ----------------------------------------------------------------------
# 6. Generate Image Using Hugging Face Stable Diffusion
# ----------------------------------------------------------------------
def generate_image(image_prompt: str) -> str:
    """
    Generates an image using Hugging Face's Stable Diffusion v1.5 API.
    Saves the image in the 'static/generated_images' directory and returns the file path.
    """
    data = {"inputs": image_prompt}

    print(f"🔄 Generating image for prompt: {image_prompt}...")
    response = requests.post(HF_API_URL, headers=HEADERS, json=data)

    num_images = len(os.listdir("generated_images"))

    if response.status_code == 200:
        image_path = os.path.join(IMAGE_SAVE_DIR, f"generated_image_{num_images}.png")
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"✅ Image saved as {image_path}")
        return f"generated_images/generated_image_{num_images}.png"  # Path formatted for Django static usage
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")
        return None  # Return None if there was an error
