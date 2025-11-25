"""Pytest plugin for aissert AI testing framework."""

from pathlib import Path

import pytest
import yaml

import pytest_aissert.decorators as decorators


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest configuration options for aissert plugin."""
    parser.addini("HELLO", "Dummy pytest.ini setting")


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Load tests from external YAML files.

    This allows parametrizing tests with test cases found in YAML data files.
    """
    # TODO externalize
    if all(x in metafunc.fixturenames for x in ["question_yaml", "answer_yaml"]):
        q_yaml_path = Path("tests/questions/example_001.yaml")
        with q_yaml_path.open() as q_yaml_file:
            q_yaml = yaml.safe_load(q_yaml_file)
        a_yaml_path = Path("tests/answers/example_001.yaml")
        with a_yaml_path.open() as a_yaml_file:
            a_yaml = yaml.safe_load(a_yaml_file)
        metafunc.parametrize(
            ("question_yaml", "answer_yaml"),
            [
                (q_yaml, a_yaml),
                (q_yaml, a_yaml),
            ],
            scope="session",
        )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Print AI test metrics report at end of test session."""
    print(f"<<< {decorators.current_report} >>>")
