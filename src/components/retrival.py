import numpy as np
from typing import Tuple, List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory

from src.common.logger import get_logger
from src.components.llm import rag_chain, retriever

logger = get_logger(__name__)


def retrieve_and_score_query(
    query: str,
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    top_k: int = 5,
    memory: ConversationBufferMemory = None
) -> Tuple[str, float, float, List[Dict[str, str]]]:
    """
    Executes a legal RAG query, returns answer with source PDF metadata.
    """
    try:
        logger.info(f"🔍 Query: {query}")
        embedding = HuggingFaceEmbeddings(model_name=embedding_model_name)

        if memory:
            history = memory.buffer
            combined_query = f"{history}\nUser: {query}"
        else:
            combined_query = query

        # 🔍 Step 1: Retrieve relevant documents
        retrieved_docs: List[Document] = retriever.get_relevant_documents(query)

        if not retrieved_docs:
            return "❗ No relevant documents found.", 0.0, 0.0, []

        # 📚 Step 2: Prepare detailed context with metadata
        context_chunks = []
        sources = []

        for doc in retrieved_docs[:top_k]:
            meta = doc.metadata
            source = meta.get("source", "unknown.pdf")
            page = meta.get("page", "N/A")
            content = doc.page_content.strip().replace("\n", " ")

            # Build a source-annotated content block
            chunk = (
                f"{content}\n"
                f"📄 **Source**: `{source}` | **Page**: {page}"
            )
            context_chunks.append(chunk)

            sources.append({
                "source": source,
                "page": page,
                "excerpt": content[:1000]
            })

        # Combine chunks for context input to the LLM
        full_context = "\n\n---\n\n".join(context_chunks)

        # 🧠 Step 3: LLM call with full context
        response = rag_chain.invoke({
            "input": query,
            "context": full_context
        })

        answer = response.get("answer", "").strip()
        if not answer:
            answer = "⚠️ No clear answer could be generated from the retrieved legal documents."

        # 📐 Step 4: Embedding-based scoring
        query_emb = embedding.embed_query(query)
        answer_emb = embedding.embed_query(answer)
        context_embs = embedding.embed_documents([doc.page_content for doc in retrieved_docs[:top_k]])
        avg_context_emb = np.mean(context_embs, axis=0)

        similarity = cosine_similarity([query_emb], [answer_emb])[0][0]
        faithfulness = cosine_similarity([avg_context_emb], [answer_emb])[0][0]

        logger.info(f"✅ Similarity (query ↔ answer): {similarity:.4f}")
        logger.info(f"✅ Faithfulness (context ↔ answer): {faithfulness:.4f}")

        # 💾 Step 5: Update memory
        if memory:
            memory.chat_memory.add_user_message(query)
            memory.chat_memory.add_ai_message(answer)
            memory.chat_memory.add_ai_message(sources)

        # 📄 Step 6: Format readable sources section with clickable links
        sources_text = "\n\n📚 **Sources Referenced:**\n"
        for s in sources:
            source_path = s['source']
            # Make link clickable if it's a URL or PDF file path
            link = f"[{source_path}]({source_path})" if source_path.startswith("http") or source_path.endswith(".pdf") else f"`{source_path}`"
            sources_text += f"- 📄 {link} (Page {s['page']}): {s['excerpt']}...\n"

        final_output = f"{answer}\n\n{sources_text.strip()}"

        return final_output, similarity, faithfulness, sources

    except Exception as e:
        logger.error(f"❌ Retrieval failed: {e}")
        raise e
