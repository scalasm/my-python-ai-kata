"""This module provides facades for dealing with Vector stores.

It simplifies loading, processing, splitting, and vectorizing LangGraph documentation
using LangChain, OpenAI embeddings, and SKLearnVectorStore.
"""

import os
import re
from typing import Optional

import tiktoken
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


class VectorStoreFactory:
    """A helper class for managing vector stores.

    This includes loading, processing, splitting, and vectorizing documents.
    """

    def __init__(self, work_dir: Optional[str] = None):
        """Initialize the VectorStoreHelper with a working directory.

        Args:
            work_dir (Optional[str]): The directory where vector store files will
                be saved. Defaults to the current working directory.
        """
        self.work_dir = work_dir or os.getcwd()
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

    @property
    def parquet_path(self) -> str:
        """Get the path to the SKLearnVectorStore parquet file.

        Returns:
            str: The path to the parquet file.
        """
        return os.path.join(self.work_dir, "sklearn_vectorstore.parquet")

    def count_tokens(self, text: str, model: str = "cl100k_base") -> int:
        """Count the number of tokens in the text using tiktoken.

        Args:
            text (str): The text to count tokens for.
            model (str): The tokenizer model to use (default: cl100k_base for GPT-4).

        Returns:
            int: Number of tokens in the text.
        """
        encoder = tiktoken.get_encoding(model)
        return len(encoder.encode(text))

    def bs4_extractor(self, html: str) -> str:
        """Extract and clean text content from HTML using BeautifulSoup.

        Args:
            html (str): The HTML content to extract text from.

        Returns:
            str: The cleaned text content.
        """
        soup = BeautifulSoup(html, "lxml")
        main_content = soup.find("article", class_="md-content__inner")
        content = main_content.get_text() if main_content else soup.text
        return re.sub(r"\n\n+", "\n\n", content).strip()

    def load_langgraph_docs(
        self, urls: list[str], max_depth: int
    ) -> tuple[list[Document], list[int]]:
        """Load LangGraph documentation from the official website.

        Args:
            urls (list[str]): List of URLs to fetch documentation from.
            max_depth (int): Maximum depth for recursive URL loading.

        Returns:
            tuple[list[Document], list[int]]: A list of Document objects and their
            token counts.
        """
        print("Loading LangGraph documentation...")
        docs: list[Document] = []
        for url in urls:
            loader = RecursiveUrlLoader(
                url,
                max_depth=max_depth,
                extractor=self.bs4_extractor,
            )
            docs.extend(loader.lazy_load())

        print(f"Loaded {len(docs)} documents from LangGraph documentation.")
        tokens_per_doc = [self.count_tokens(doc.page_content) for doc in docs]
        print(f"Total tokens in loaded documents: {sum(tokens_per_doc)}")
        return docs, tokens_per_doc

    def save_llms_full(self, documents: list[Document], output_filename: str) -> None:
        """Save the documents to a file.

        Args:
            documents (list[Document]): List of Document objects to save.
            output_filename (str): The filename to save the documents to.
        """
        output_filename = os.path.join(self.work_dir, output_filename)
        with open(output_filename, "w") as f:
            for i, doc in enumerate(documents):
                source = doc.metadata.get("source", "Unknown URL")
                f.write(
                    f"DOCUMENT {i + 1}\nSOURCE: {source}\nCONTENT:\n"
                    f"{doc.page_content}\n\n{'=' * 80}\n\n"
                )
        print(f"Documents concatenated into {output_filename}")

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split documents into smaller chunks for improved retrieval.

        Args:
            documents (list[Document]): List of Document objects to split.

        Returns:
            list[Document]: A list of split Document objects.
        """
        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=8000, chunk_overlap=500
        )
        split_docs = text_splitter.split_documents(documents)
        print(f"Created {len(split_docs)} chunks from documents.")
        return split_docs

    def create_vectorstore(self, splits: list[Document]) -> VectorStore:
        """Create a vector store from document chunks using SKLearnVectorStore.

        Args:
            splits (list[Document]): List of split Document objects to embed.

        Returns:
            VectorStore: A vector store containing the embedded documents.
        """
        print("Creating SKLearnVectorStore...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        vectorstore = SKLearnVectorStore.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_path=self.parquet_path,
            serializer="parquet",
        )
        vectorstore.persist()
        print(f"SKLearnVectorStore was persisted to {self.parquet_path}")
        return vectorstore

    def create_vectore_store(self, urls: list[str], max_depth: int = 2) -> None:
        """Create a vector store from LangGraph documentation.

        Args:
            urls (list[str]): List of URLs to fetch documentation from.
            max_depth (int): Maximum depth for recursive URL loading. Defaults to 2.
        """
        documents, _ = self.load_langgraph_docs(urls, max_depth)
        self.save_llms_full(documents, "llms_full.txt")
        split_docs = self.split_documents(documents)
        self.create_vectorstore(split_docs)
        print("Vector store creation complete.")


class VectorStoreQueryHelper:
    """Helper class for querying a vector store."""

    def __init__(self, parquet_path: str):
        """Initialize with the path to the parquet file.

        Args:
            parquet_path (str): Path to the SKLearnVectorStore parquet file.
        """
        self.parquet_path = parquet_path
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.vectorstore = SKLearnVectorStore(
            embedding=embeddings, persist_path=parquet_path, serializer="parquet"
        )

    @property
    def llms_full_path(self) -> str:
        """Get the path to the llms_full.txt file.

        Returns:
            str: The path to the llms_full.txt file.
        """
        return os.path.join(os.path.dirname(self.parquet_path), "llms_full.txt")

    def get_llms_full(self) -> str:
        """Get the contents of the llms_full.txt file.

        Returns:
            str: The contents of the llms_full.txt file.
        """
        try:
            with open(self.llms_full_path) as file:
                return file.read()
        except FileNotFoundError:
            return "llms_full.txt not found. Please ensure the vector store has been created."

    def query(self, query: str, k: int = 3) -> list[Document]:
        """Query the vector store and return relevant documents.

        Args:
            query (str): Query string.
            k (int): Number of top relevant documents to retrieve. Defaults to 3.

        Returns:
            list[Document]: List of relevant documents.
        """
        print(f"Querying vector store for: {query}")
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        relevant_docs = retriever.invoke(query)
        print(f"Retrieved {len(relevant_docs)} relevant documents")
        return relevant_docs


if __name__ == "__main__":
    work_dir = os.path.join(os.getcwd(), "vector_store_data")
    print(
        f"Creating a sample Vector store in {work_dir!r} using Langgraph online documentation ..."
    )

    urls = [
        "https://langchain-ai.github.io/langgraph/",
        "https://langchain-ai.github.io/langgraph/tutorials/workflows/",
        "https://langchain-ai.github.io/langgraph/tutorials/introduction/",
        "https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/",
    ]
    # Watch out - if you recursively load too many URLs, you may hit 300K max token limit
    # from OpenAI embedding model!
    max_depth = 3  # this triggers about 221K tokens

    vector_store_factory = VectorStoreFactory(work_dir=work_dir)
    vector_store_factory.create_vectore_store(urls, max_depth)
    print("Vector store created successfully.")

    query_helper = VectorStoreQueryHelper(
        parquet_path=vector_store_factory.parquet_path
    )

    # Run an example querry
    query = "What is LangGraph?"
    relevant_docs = query_helper.query(query)

    for doc in relevant_docs:
        print(doc.metadata["source"])
        print(doc.page_content[:500])
