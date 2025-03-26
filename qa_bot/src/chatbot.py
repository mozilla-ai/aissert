from loguru import logger
import os
from pathlib import Path
from typing import Optional


from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms.llamafile import Llamafile
from langchain_community.embeddings import LlamafileEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

import pandas as pd

from settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, OUTPUT_FOLDER


class Chatbot:
    def __init__(
        self,
        pdf: str,
        prompt_template: str,
        local: bool = False,
        output_folder: Path = OUTPUT_FOLDER,
        serialized_db_path: Optional[str] = None,
    ):
        self.pdf = pdf
        self.prompt_template = prompt_template
        self.output_folder = Path(output_folder)
        if local:
            self.llm = Llamafile()
            self.embeddings = LlamafileEmbeddings()
        else:
            self.llm = ChatMistralAI()
            self.embeddings = MistralAIEmbeddings()

        self.context_db = self._initialize_context_storage(serialized_db_path)
        self.chain = self._create_chain()

    def _initialize_context_storage(self, serialized_db_path: Optional[str]) -> FAISS:
        """Initialize the vector storage of embedded chunks (context)."""
        if serialized_db_path and os.path.exists(serialized_db_path):
            db = FAISS.load_local(
                serialized_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            logger.info(f"Loaded context storage from {serialized_db_path}")
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100, add_start_index=True
            )
            docs = PyPDFLoader(self.pdf).load_and_split(text_splitter)
            db = FAISS.from_documents(docs, self.embeddings)
            os.makedirs(self.output_folder, exist_ok=True)
            db.save_local(self.output_folder / "vectorstore")

            logger.info(
                f"Saved new context storage in {self.output_folder /'vectorstore'}"
            )

        return db

    def _create_chain(self) -> RetrievalQA:
        """Create the RetrievalQA chain using the initialized components."""
        prompt = PromptTemplate(
            template=self.prompt_template, input_variables=["question", "context"]
        )
        climate_qa_chain = RetrievalQA.from_llm(
            llm=self.llm, retriever=self.context_db.as_retriever(), prompt=prompt
        )

        logger.info("Climate QA chain created")
        return climate_qa_chain

    def predict(self, df: pd.DataFrame):
        """Wraps the LLM call in a simple Python function.

        Args:
            df: A pandas.DataFrame containing a 'question' column.

        Returns:
            A list of model outputs, one for each row in the DataFrame.
        """
        return [self.chain.invoke({"query": question}) for question in df["question"]]


if __name__ == "__main__":
    use_serialized = True
    serialized_db_path = OUTPUT_FOLDER / "vectorstore" if use_serialized else None

    chatbot = Chatbot(
        pdf=IPCC_REPORT_URL,
        prompt_template=PROMPT_TEMPLATE,
        local=False,
        output_folder=OUTPUT_FOLDER,
        serialized_db_path=serialized_db_path,
    )
    response = chatbot.predict(
        pd.DataFrame({"question": ["Is sea level rise avoidable? When will it stop?"]})
    )
    logger.info(response)
