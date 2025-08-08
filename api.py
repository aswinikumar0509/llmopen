from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from src.components.retrival import retrieve_and_score_query
from src.components.tools import summarizer_fn

# FastAPI app instance
app = FastAPI(title="Legal RAG Assistant API", version="1.0")

# Global conversation memory (in-memory)
memory = ConversationBufferMemory(return_messages=True)


# Request/Response Schemas
class QueryRequest(BaseModel):
    query: str


class RetrieveResponse(BaseModel):
    answer: str
    similarity: float
    faithfulness: float


class SummaryRequest(BaseModel):
    answer: str


class SummaryResponse(BaseModel):
    summary: str


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve_answer(request: QueryRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        answer, similarity, faithfulness = retrieve_and_score_query(query, memory=memory)
        return RetrieveResponse(answer=answer, similarity=similarity, faithfulness=faithfulness)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", response_model=SummaryResponse)
def summarize_answer(request: SummaryRequest):
    answer = request.answer.strip()

    if not answer:
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    try:
        summary = summarizer_fn(answer)
        return SummaryResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Welcome to Legal RAG Assistant API! Use /retrieve or /summarize."}
