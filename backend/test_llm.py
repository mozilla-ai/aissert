import unittest
from .llm import query_llm
from .aissert.base import AIssert
from .aissert.tests.language_test import LanguageTest

class TestLLMQuery(unittest.TestCase):
    def test_query_llm_returns_text(self):
        prompt = "Where is Alice?"
        response = query_llm(prompt)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0, "LLM response should not be empty")

    def test_language_match_english(self):
        question = "What's happening in the park?"
        answer = query_llm(question)
        suite = AIssert()
        lang_test = LanguageTest(question)
        suite.add_test(lang_test)
        results = suite.run_all(answer)
        for test_name, result in results.items():
            self.assertTrue(result["passed"], msg=result["message"])

    def test_language_match_spanish(self):
        question = "¿Que está pasando en el parque?"
        answer = query_llm(question)
        suite = AIssert()
        lang_test = LanguageTest(question)
        suite.add_test(lang_test)
        results = suite.run_all(answer)
        for test_name, result in results.items():
            self.assertTrue(result["passed"], msg=result["message"])


if __name__ == "__main__":
    unittest.main()
