"""Decorators and prompt generators for AI-based testing."""

from collections.abc import Callable
from typing import Any

from decorator import decorator

current_report = {}


def get_current_report() -> dict:
    """Get the current test report dictionary.

    Returns:
        Dictionary containing test metrics by name.
    """
    return current_report


def ai_test(threshold: float = 0.5, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:  # noqa: ANN401
    """Decorator for AI-based test assertions with threshold.

    Args:
        threshold: Minimum metric value required to pass (default 0.5).
        *args: Additional positional arguments.
        **kwargs: Must include 'name' for the test identifier.

    Returns:
        Decorated function that asserts metric meets threshold.
    """
    name = kwargs["name"]

    def ai_test_dec(func: Callable[..., float], *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        # Add functionality before the original function call.
        metric = func(*args, **kwargs)
        # Add functionality after the original function call.
        current_report[name] = metric
        assert metric >= threshold

    return decorator(ai_test_dec)


def llm_judge(threshold: float = 0.5, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:  # noqa: ANN401
    """Decorator for LLM-as-a-judge test assertions with threshold.

    This decorator is specifically designed for tests that use LLM-based
    evaluation metrics. It works similarly to ai_test but is semantically
    intended for tests that leverage LLM judges using the provided prompt
    generators (evaluate_response, reference_answer, etc.).

    Args:
        threshold: Minimum metric value required to pass (default 0.5).
        *args: Additional positional arguments.
        **kwargs: Must include 'name' for the test identifier.

    Returns:
        Decorated function that asserts metric meets threshold.
    """
    name = kwargs["name"]

    def llm_judge_dec(func: Callable[..., float], *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        # Add functionality before the original function call.
        metric = func(*args, **kwargs)
        # Add functionality after the original function call.
        current_report[name] = metric
        assert metric >= threshold

    return decorator(llm_judge_dec)


# taken from https://www.evidentlyai.com/llm-guide/llm-as-a-judge#evaluation-by-criteria


def evaluate_response(response: str, question: str) -> str:
    """Generate prompt to evaluate response completeness.

    Args:
        response: The response text to evaluate.
        question: The question that was asked.

    Returns:
        Evaluation prompt string.
    """
    return (
        f"Evaluate the following RESPONSE based on the given QUESTION. "
        f"A complete response is one that fully addresses all parts of the question. "
        f"Return one of the following labels: 'Complete' or 'Incomplete.'\n"
        f"QUESTION: {question}\nRESPONSE: {response}"
    )


def reference_answer(response: str, reference: str) -> str:
    """Generate prompt to compare response against reference answer.

    Args:
        response: The generated response to evaluate.
        reference: The reference answer to compare against.

    Returns:
        Comparison prompt string.
    """
    return (
        f"Compare the generated RESPONSE to the REFERENCE answer. "
        f"Evaluate if the generated response correctly conveys the same meaning, "
        f"even if the wording is different. "
        f"Return one of these labels: 'Correct' or 'Incorrect.'\n"
        f"REFERENCE: {reference}\nRESPONSE: {response}"
    )


def context_relevance(context: str, question: str) -> str:
    """Generate prompt to evaluate context relevance to question.

    Args:
        context: The context text to evaluate.
        question: The question being asked.

    Returns:
        Relevance evaluation prompt string.
    """
    return (
        f"Evaluate the relevance of the CONTEXT in answering the QUESTION. "
        f"A relevant CONTEXT contains information that helps answer the question, even if partially. "
        f"Return one of the following labels: 'Relevant', or 'Irrelevant.'\n"
        f"CONTEXT: '{context}'\nQUESTION: {question}"
    )


def context_faithfulness(context: str, response: str) -> str:
    """Generate prompt to evaluate response faithfulness to context.

    Args:
        context: The source context text.
        response: The response text to evaluate.

    Returns:
        Faithfulness evaluation prompt string.
    """
    return (
        f"Evaluate the following RESPONSE for faithfulness to the CONTEXT. "
        f"A faithful RESPONSE should only include information present in the CONTEXT, "
        f"avoid inventing new details, and not contradict the CONTEXT. "
        f"Return one of the following labels: 'Faithful' or 'Not Faithful'.\n"
        f"CONTEXT: '{context}'\nRESPONSE: {response}"
    )
