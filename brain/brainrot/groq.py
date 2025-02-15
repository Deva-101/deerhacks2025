import os
import groq

# Load API key securely from environment variables
api_key = "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"
if not api_key:
    raise ValueError("API key not found. Set the GROQ_API_KEY environment variable.")

# Initialize Groq client
client = groq.Client(api_key=api_key)

# Define the system message to guide the AI
system_prompt = "You are an advanced AI assistant, capable of answering questions concisely and accurately."

def get_groq_response(user_input):
    """Function to get a response from Groq's AI"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Choose the right model
        messages=[
            {"role": "system", "content": system_prompt},  # System prompt
            {"role": "user", "content": user_input}  # User input
        ],
        temperature=0.7  # Adjust temperature for randomness
    )

    return response.choices[0].message.content.strip()
