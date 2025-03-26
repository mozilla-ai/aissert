from loguru import logger
import os
import pytest
from pathlib import Path
from giskard import Dataset, Model, Suite
from giskard.testing.tests.llm import (
    test_llm_output_plausibility,
    test_llm_char_injection,
    test_llm_ground_truth_similarity,
    test_llm_correctness,
    test_llm_single_output_against_requirement,
)

import pandas as pd
from chatbot import Chatbot
from settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, SAMPLE_VECTORSTORE_PATH, SAMPLE_QA_PATH, TOKENIZERS_PARALLELISM

os.environ["TOKENIZERS_PARALLELISM"] = TOKENIZERS_PARALLELISM


logger.debug(f"Using {SAMPLE_VECTORSTORE_PATH=}")
logger.debug(f"Using {IPCC_REPORT_URL=}")
logger.debug(f"Using {PROMPT_TEMPLATE=}")


# Cannot be a fixture, as suite needs to access it directly
def create_dataset():
    df = pd.read_csv(SAMPLE_QA_PATH)

    wrapped_dataset = Dataset(
        name="Test Data Set", df=df, target="expected_answer"
    )

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
    .add_test(test_llm_single_output_against_requirement(threshold=0.5, requirement="The actual answer should be in the same language as the input question."))
)


@pytest.mark.parametrize("test_partial", suite.to_unittest(), ids=lambda t: t.fullname)
def test_chatbot(test_partial):
    test_partial.execute()
