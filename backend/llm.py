import os
from transformers import pipeline, set_seed

# Use a Hugging Face model identifier. The default here is microsoft/DialoGPT-small.
DEFAULT_MODEL_NAME = "distilbert/distilbert-base-cased-distilled-squad"
MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)

# Load the model and tokenizer using the transformers pipeline.
question_answerer = pipeline("question-answering", model=MODEL_NAME)
context = r"""
On a warm spring afternoon, the city park was alive with activity. 
Alice, a literature enthusiast, was sitting on a brightly colored bench under the shade of a centuries-old oak tree, deeply immersed in a thick, worn-out novel. 
Nearby, Bob, a longtime friend, was engaged in an animated conversation with another visitor about recent community events and local happenings. 
The park was a melting pot of cultures—families picnicking on the grass, joggers pacing along winding paths, and street performers entertaining passersby with music and dance. 
As the day progressed, a small group of musicians arrived and began playing a gentle melody, blending harmoniously with the ambient chatter and the rustling of leaves. 
People spoke in various languages including English, Spanish, and French, reflecting the vibrant diversity of the neighborhood. 
This dynamic environment not only provided a scenic escape from the bustle of city life but also served as a microcosm of the city's rich cultural tapestry.
"""
def query_llm(prompt: str) -> str:
    """
    Query the Hugging Face model with a prompt and return its generated text.
    """
    # Generate a response. Adjust parameters (max_length, top_p, top_k, etc.) as needed.
    result = question_answerer(prompt, context)
    print(result)
    answer = result['answer']
    print(answer)
    # Optionally remove the prompt from the generated text if it repeats.
    if answer.startswith(prompt):
        answer = answer[len(prompt):].strip()
    
    return answer