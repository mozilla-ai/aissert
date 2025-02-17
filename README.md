# AIssert

A lightweight testing suite for AI applications to ensure your generative outputs behave as expected.

This repo contains a sample app (chatbot) that you can ask questions about the following context:

```
On a warm spring afternoon, the city park was alive with activity. 
Alice, a literature enthusiast, was sitting on a brightly colored bench under the shade of a centuries-old oak tree, deeply immersed in a thick, worn-out novel. 
Nearby, Bob, a longtime friend, was engaged in an animated conversation with another visitor about recent community events and local happenings. 
The park was a melting pot of cultures—families picnicking on the grass, joggers pacing along winding paths, and street performers entertaining passersby with music and dance. 
As the day progressed, a small group of musicians arrived and began playing a gentle melody, blending harmoniously with the ambient chatter and the rustling of leaves. 
People spoke in various languages including English, Spanish, and French, reflecting the vibrant diversity of the neighborhood. 
This dynamic environment not only provided a scenic escape from the bustle of city life but also served as a microcosm of the city's rich cultural tapestry.
```

The idea behind this project is to give an example of what AIssert could be, a way of testing LLMs integreations with product apps.


## Installation

1. Create the virtual environment
```
python3 -m venv .venv source .venv/bin/activate
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the app
```
python backend/main.py 
```

Open the file [index.html](frontend/index.html) in your browser and then ou can ask the chatbot anything about the context.


Running tests (the interesting part about AIssert)
```
python -m backend/test_llm
```

One of the AIssert tests we have will fail, as we are checking whether the prompt language and output language match (And this won't be true for anything that's not english)



There are different ways of fixing this test (maybe using a model that would do that automatically, injecting instructions in the prompt, etc.)


We could have hundreds of small tests like this, that any developer can run when they iterate their model or their prompts. Think about PII leakage, gender bias, Prompt injection, token optimization etc.