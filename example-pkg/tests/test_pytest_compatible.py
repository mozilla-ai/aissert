from pytest_aissert.decorators import ai_metric
from aissert.test_lib.base import question_language_equals_answer_language_metric, some_metric

@ai_metric(name="language_test")
def test_question_language_equals_answer_language(question_yaml, answer_yaml):
    question = question_yaml['text']
    answer = answer_yaml['text']
    return question_language_equals_answer_language_metric(question, answer)

@ai_metric(threshold=0.9, name="another_test")
def test_another_test():
    return some_metric("", "")
