from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.components.vector import store_documents_in_pinecone , load_existing_docsearch
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from src.components.prompt import prompt
from src.components.data_ingestion import load_documents_from_text_file, filter_to_minimal_docs
from src.components.data_embedding import prepare_text_chunks_with_embeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import os


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
os.environ["OpenAI_API_KEY"] = OpenAI_API_KEY


os.environ["GROQ_API_KEY"] = GROQ_API_KEY


llm = ChatOpenAI(
    model_name="gpt-4",  
    temperature=0.5,
    top_p=0.9
)



docsearch = load_existing_docsearch("test-txt-chatbot1")
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":5})


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
