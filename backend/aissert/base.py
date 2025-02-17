# aissert/base.py
class AIssert:
    def __init__(self):
        self.tests = []

    def add_test(self, test):
        """
        Add a test. A test must have:
          - a .name attribute
          - a .run(text) method that returns (bool, message)
        """
        self.tests.append(test)

    def run_all(self, text):
        """
        Runs all tests on the provided text and returns a dict with the results.
        """
        results = {}
        for test in self.tests:
            status, message = test.run(text)
            results[test.name] = {"passed": status, "message": message}
        return results
