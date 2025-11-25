"""Metrics for evaluating NLP question-answer pairs."""

import langid


def question_language_equals_answer_language_metric(q: str, a: str) -> int:
    """Check if question and answer are in the same language.

    Args:
        q: Question text.
        a: Answer text.

    Returns:
        1 if languages match, 0 otherwise.
    """
    q_language, _ = langid.classify(q)
    a_language, _ = langid.classify(a)
    if q_language != a_language:
        return 0
    return 1


def some_metric(input: str, output: str) -> float:
    """Placeholder metric function.

    Args:
        input: Input text.
        output: Output text.

    Returns:
        Fixed metric value of 0.8.
    """
    return 0.8
