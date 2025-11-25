"""Integration tests for climate QA chatbot using Giskard test suite."""

import os
from pathlib import Path

import pandas as pd
import pytest
from chatbot import Chatbot
from giskard import Dataset, Model, Suite
from giskard.llm import set_embedding_model, set_llm_model
from giskard.testing.tests.llm import (
    test_llm_char_injection,
    test_llm_correctness,
    test_llm_ground_truth_similarity,
    test_llm_output_plausibility,
    test_llm_single_output_against_requirement,
)
from loguru import logger
from settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, SAMPLE_QA_PATH, SAMPLE_VECTORSTORE_PATH, TOKENIZERS_PARALLELISM

os.environ["TOKENIZERS_PARALLELISM"] = TOKENIZERS_PARALLELISM
set_llm_model("mistral/mistral-large-latest")
set_embedding_model("mistral/mistral-embed")

logger.debug(f"Using {SAMPLE_VECTORSTORE_PATH=}")
logger.debug(f"Using {IPCC_REPORT_URL=}")
logger.debug(f"Using {PROMPT_TEMPLATE=}")


# Cannot be a fixture, as suite needs to access it directly
def create_dataset():
    """Create a Giskard dataset from sample QA CSV file.

    Returns:
        Giskard Dataset instance with test data.
    """
    df = pd.read_csv(SAMPLE_QA_PATH)

    wrapped_dataset = Dataset(name="Test Data Set", df=df, target="expected_answer")

    return wrapped_dataset


chatbot = Chatbot(
    pdf=IPCC_REPORT_URL,
    prompt_template=PROMPT_TEMPLATE,
    local=False,
    serialized_db_path=Path(SAMPLE_VECTORSTORE_PATH),
)

app_entrypoint = Model(
    model=chatbot.predict,
    model_type="text_generation",
    name="mistralchatbot",
    description="This model answers questions about the IPCC report.",
    feature_names=["question"],
)


suite = (
    Suite(
        default_params={
            "model": app_entrypoint,
            "dataset": create_dataset(),
        }
    )
    .add_test(test_llm_output_plausibility(threshold=0.5))
    .add_test(test_llm_char_injection(threshold=0.5))
    .add_test(test_llm_ground_truth_similarity(threshold=0.5))
    .add_test(test_llm_correctness(threshold=0.5))
    .add_test(
        test_llm_single_output_against_requirement(
            threshold=0.5, requirement="The actual answer should be in the same language as the input question."
        )
    )
)


@pytest.mark.parametrize("test_partial", suite.to_unittest(), ids=lambda t: t.fullname)
def test_chatbot(test_partial):
    """Execute parametrized Giskard test cases for the chatbot.

    Args:
        test_partial: Giskard test partial to execute.
    """
    test_partial.execute()
