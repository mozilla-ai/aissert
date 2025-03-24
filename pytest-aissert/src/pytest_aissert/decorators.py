import pytest
from decorator import decorator

current_report = {}

def get_current_report():
    return current_report


def ai_test(threshold=0.5, *args, **kwargs):
    name = kwargs['name']
    def ai_test_dec(func, *args, **kwargs):
        # Add functionality before the original function call
        metric = func(*args, **kwargs)
        # Add functionality after the original function call
        current_report[name] = metric
        assert metric >= threshold
    return decorator(ai_test_dec)

# taken from https://www.evidentlyai.com/llm-guide/llm-as-a-judge#evaluation-by-criteria

def evaluate_response(response: str, question: str):
    testing_prompt = f"Evaluate the following RESPONSE based on the given QUESTION. A complete response is one that fully addresses all parts of the question. Return one of the following labels: 'Complete' or 'Incomplete.'\nQUESTION: {question}\nRESPONSE: {response}"

def reference_answer(response: str, reference: str):
    testing_prompt = f"Compare the generated RESPONSE to the REFERENCE answer. Evaluate if the generated response correctly conveys the same meaning, even if the wording is different. Return one of these labels: 'Correct’ or 'Incorrect.'\nREFERENCE: {reference}\nRESPONSE: {response}"

def context_assessment(context: str, question: str):
    testing_prompt = f"Evaluate the relevance of the CONTEXT in answering the QUESTION. A relevant CONTEXT contains information that helps answer the question, even if partially. Return one of the following labels: 'Relevant', or 'Irrelevant.'\nCONTEXT: '{context}'\nQUESTION: {question}"

def context_assessment(context: str, response: str):
    testing_prompt = f"Evaluate the following RESPONSE for faithfulness to the CONTEXT. A faithful RESPONSE should only include information present in the CONTEXT, avoid inventing new details, and not contradict the CONTEXT. Return one of the following labels: 'Faithful' or 'Not Faithful'.\nCONTEXT: '{context}'\RESPONSE: {response}"