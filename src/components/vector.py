from typing import List
from dotenv import load_dotenv
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
import os
import sys

logger = get_logger(__name__)


def store_documents_in_pinecone(
    texts_chunk: List[Document],
    embedding,
    index_name: str = "test-txt-chatbot1",
    dimension: int = 384,
    metric: str = "cosine",
    cloud: str = "aws",
    region: str = "us-east-1",
):
    """
    Stores chunked documents into a Pinecone vector store with batching to avoid payload size limits.
    """
    try:
        load_dotenv()

        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        hf_token = os.getenv("hf_token")

        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is missing from environment variables.")
        
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
        os.environ["hf_token"] = hf_token or ""

        # Initialize Pinecone client
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        # Create index if it doesn't exist
        if not pc.has_index(index_name):
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud=cloud, region=region)
            )
            logger.info(f"✅ Created Pinecone index '{index_name}'.")

        # Helper: batching iterator
        def batch_iter(data, size=50):  # use small batches to stay under 4MB
            for i in range(0, len(data), size):
                yield data[i:i + size]

        total_uploaded = 0
        for batch in batch_iter(texts_chunk, size=50):
            try:
                # Create vector store for each small batch
                PineconeVectorStore.from_documents(
                    documents=batch,
                    embedding=embedding,
                    index_name=index_name
                )
                total_uploaded += len(batch)
                logger.info(f"✅ Uploaded batch of {len(batch)} documents (Total uploaded: {total_uploaded}).")
            except Exception as batch_err:
                logger.error(f"❌ Failed to upload a batch: {batch_err}")
                raise CustomException(f"Batch upload error: {batch_err}")

        logger.info(f"🎉 Successfully stored {total_uploaded} documents in Pinecone index '{index_name}'.")
        return True

    except Exception as e:
        logger.error(f"❌ Error storing documents in Pinecone: {e}")
        raise CustomException(f"Failed to store documents in Pinecone: {e}")


def load_existing_docsearch(index_name: str = "test-txt-chatbot1") -> PineconeVectorStore:
    """
    Loads an existing Pinecone index using OpenAI embeddings.
    """
    try:
        load_dotenv()

        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not PINECONE_API_KEY or not OPENAI_API_KEY:
            raise ValueError("Missing Pinecone or OpenAI API key in environment.")

        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        logger.info(f"Loading Pinecone index '{index_name}'...")
        docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
        logger.info(f"✅ Successfully loaded Pinecone index '{index_name}'.")
        return docsearch

    except Exception as e:
        logger.error(f"❌ Error loading Pinecone index: {e}")
        raise CustomException(f"Error loading Pinecone index: {e}")
