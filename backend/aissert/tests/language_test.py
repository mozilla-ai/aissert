import langid

class LanguageTest:
    """
    Checks whether the answer is in the same language as the question.
    Uses the langid library which supports multiple languages.
    """
    def __init__(self, question):
        self.name = "LanguageTest"
        self.question = question
        # Detect the language of the question
        self.question_language, _ = langid.classify(question)

    def run(self, answer: str):
        # Detect the language of the answer
        answer_language, _ = langid.classify(answer)
        if self.question_language != answer_language:
            return (
                False,
                f"Language mismatch: question is '{self.question_language}', answer is '{answer_language}'."
            )
        return True, f"Language match: both are '{self.question_language}'."
