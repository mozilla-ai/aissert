import langid

def question_language_equals_answer_language_metric(q: str, a:str):
    q_language, _ = langid.classify(q)
    a_language, _ = langid.classify(a)
    if q_language != a_language:
        metric = 0
    metric = 1
    return metric

def some_metric(input:str, output:str):
    return 0.8

