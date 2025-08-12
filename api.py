from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from langchain.memory import ConversationBufferMemory
from src.components.retrival import retrieve_and_score_query
from src.components.tools import summarizer_fn, legal_drafting_fn

# Initialize FastAPI
app = FastAPI(title="Vakki: Legal Research Assistant API")

# Global memory store (per server instance)
chat_memory = ConversationBufferMemory(return_messages=True)
retrieved_answer = None
retrieved_sources = []

# Request models
class QueryRequest(BaseModel):
    query: str

class SummarizeRequest(BaseModel):
    text: str

class DraftRequest(BaseModel):
    instructions: str


@app.post("/retrieve")
def retrieve_answer(req: QueryRequest):
    """
    Retrieve a legal answer from the knowledge base.
    """
    global retrieved_answer, retrieved_sources
    try:
        answer, similarity, faithfulness, sources = retrieve_and_score_query(
            req.query, memory=chat_memory
        )
        retrieved_answer = answer
        retrieved_sources = sources

        return {
            "answer": answer,
            "similarity_score": similarity,
            "faithfulness_score": faithfulness,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize")
def summarize_answer(req: SummarizeRequest):
    """
    Summarize the given answer text.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="No text provided for summarization.")

    try:
        summary = summarizer_fn(req.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/draft")
def draft_legal_document(req: DraftRequest):
    """
    Draft a legal document from provided instructions.
    """
    if not req.instructions.strip():
        raise HTTPException(status_code=400, detail="No drafting instructions provided.")

    try:
        draft = legal_drafting_fn(req.instructions)
        return {"draft": draft}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory")
def get_conversation_memory():
    """
    Return stored conversation memory messages.
    """
    messages = [
        {"role": "user" if msg.type == "human" else "assistant", "content": msg.content}
        for msg in chat_memory.chat_memory.messages
    ]
    return {"messages": messages}
