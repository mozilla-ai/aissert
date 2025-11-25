"""Test suite demonstrating pytest compatibility with aissert."""

from typing import Any

from aissert_lib.base import question_language_equals_answer_language_metric, some_metric
from pytest_aissert.decorators import ai_test, llm_judge


@ai_test(name="language_test")
def test_question_language_equals_answer_language(question_yaml: dict[str, Any], answer_yaml: dict[str, Any]) -> float:  # noqa: ANN401
    """Test that question and answer are in the same language."""
    question = question_yaml["text"]
    answer = answer_yaml["text"]
    return question_language_equals_answer_language_metric(question, answer)


@ai_test(threshold=0.9, name="another_test")
def test_another_test() -> float:
    """Test using some_metric with empty strings."""
    return some_metric("", "")


@llm_judge(threshold=0.9, name="llm_judge_test")
def test_llm() -> float:
    """Test using LLM judge with some_metric."""
    return some_metric("", "")
