import os
from pathlib import Path

OUTPUT_FOLDER = Path(__file__).parent.parent / "outputs"
SAMPLE_VECTORSTORE_PATH = (
    Path(__file__).parent.parent / "sample_data" / "vectorstore"
)
SAMPLE_QA_PATH = (
    Path(__file__).parent.parent / "sample_data" / "synthetic_dataset.csv"
)

IPCC_REPORT_URL = (
    "https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_LongerReport.pdf"
)

PROMPT_TEMPLATE = """You are the Climate Assistant, a helpful AI assistant made by Giskard.
Your task is to answer common questions on climate change.
You will be given a question and relevant excerpts from the IPCC Climate Change Synthesis Report (2023).
Please provide short and clear answers based on the provided context. Be polite and helpful.

Context:
{context}

Question:
{question}

Your answer:
"""

TOKENIZERS_PARALLELISM="false"