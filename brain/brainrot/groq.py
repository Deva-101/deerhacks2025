#!/usr/bin/env python3
"""

A script that can analyze dreams using Groq's AI model by default,
but also allows an override of the system prompt for other scenarios.

Usage:
1. Ensure you have installed the 'groq' Python client.
2. Set your environment variable 'GROQ_API_KEY' to your Groq API key
   (or edit the code to include it directly—although this is not 
   recommended for production).
3. Run the script: python analyze_dream.py
4. Enter your dream text when prompted, or specify a different system prompt,
   and receive a processed response from the AI.

Important:
- This script is for demonstration/hackathon purposes. 
- Not intended for production without additional security & error handling.
"""

import os
import groq

# ------------------------------------------------------------------------------
# 1. Load API Key from Environment Variable (Recommended for Security)
# ------------------------------------------------------------------------------
api_key = "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" # <--- Replace "-" with a fallback if needed
if not api_key:
    raise ValueError("API key not found. Set the GROQ_API_KEY environment variable.")

# ------------------------------------------------------------------------------
# 2. Initialize Groq Client
# ------------------------------------------------------------------------------
client = groq.Client(api_key=api_key)

# ------------------------------------------------------------------------------
# 3. Default Dream Analysis Prompt
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# 4. Function to Query Groq's AI Model (Allows System Prompt Override)
# ------------------------------------------------------------------------------
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