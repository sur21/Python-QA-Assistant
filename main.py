from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import PythonQARAG
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

load_dotenv()

# Initialize RAG system
rag_system = PythonQARAG()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if os.path.exists("./chroma_db"):
            print("Loading existing vector database...")
            rag_system.load_index()
            print("Vector database loaded successfully.")
        else:
            print("No vector database found.")
    except Exception as e:
        print(f"Startup Error: {e}")

    yield


app = FastAPI(
    title="Python Q&A Assistant",
    version="1.0.0",
    lifespan=lifespan
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {
        "message": "Python Q&A Assistant API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if len(question) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question must be at least 3 characters long."
        )

    try:
        answer = rag_system.ask(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}"
        )