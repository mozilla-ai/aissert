# Introduction

AIssert is a library that can be used to run tests and provide metrics for your LLM applications. These metrics are written in Python and can be integrated in different contexts:

* As standalone executables for use in environments like shell, PowerShell, or GitHub action scripts
* As pytest suites generating both a pass/fail evaluation and a metric JSON document

# How to write new tests

Tests are pytest test functions that return a
