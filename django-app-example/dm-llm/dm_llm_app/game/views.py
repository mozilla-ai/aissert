import os
import requests
import traceback
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# A fixed DM instruction for the system prompt
BASE_DM_INSTRUCTION = (
    "You are a Dungeon Master. Narrate the story based solely on the following context. "
    "Stay in character, do not add extraneous information, and follow the specified settings.\n\n"
)

def build_prompt(data):
    # Extract variables from the incoming data
    world_context = data.get("world_context", "")
    genre = data.get("genre", "")
    difficulty = data.get("difficulty", "")
    narrative_tone = data.get("narrative_tone", "")
    campaign_name = data.get("campaign_name", "")
    user_question = data.get("user_question", "")

    # Construct the dynamic part of the prompt
    prompt_body = (
        f"World Context: {world_context}\n"
        f"Genre: {genre}\n"
        f"Difficulty: {difficulty}\n"
        f"Narrative Tone: {narrative_tone}\n"
        f"Campaign Name: {campaign_name}\n\n"
        f"Now, here is the player's prompt: {user_question}"
    )
    return BASE_DM_INSTRUCTION + prompt_body

@api_view(['POST'])
def dungeon_view(request):
    # Validate incoming data
    required_fields = ["world_context", "genre", "difficulty", "narrative_tone", "campaign_name", "user_question"]
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"Missing field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

    # Build the final prompt
    final_prompt = build_prompt(request.data)

    # Make the API call to the LLM provider using settings
    llm_provider = settings.LLM_PROVIDER.lower()
    api_endpoint = settings.LLM_API_ENDPOINT
    api_key = settings.LLM_API_KEY

    # This is a simplified example assuming an OpenAI-like API; you might need to adapt it.
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": final_prompt}
        ],
        "max_tokens": 150
    }

    try:
        response = requests.post(api_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        llm_result = response.json()
        # Adjust extraction based on the chat API structure:
        narrative = llm_result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return Response({"narrative": narrative})
