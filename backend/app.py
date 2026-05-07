from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag_pipeline import generate_answer


# Create FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body schema
class ChatRequest(BaseModel):
    question: str


# Root endpoint
@app.get("/")
def home():

    return {
        "message": "SWS AI RAG Chatbot API Running"
    }


# Chat endpoint
@app.post("/api/chat")
def chat(request: ChatRequest):

    result = generate_answer(request.question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }