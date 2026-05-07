from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile, File

import shutil

from rag_pipeline import generate_answer
from ingest import ingest_documents


# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schema
class ChatRequest(BaseModel):
    question: str


# Home endpoint
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


# Upload endpoint
@app.post("/api/upload")
def upload_file(file: UploadFile = File(...)):

    save_path = f"documents/{file.filename}"

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    # Re-run ingestion
    ingest_documents()

    return {
        "message": f"{file.filename} uploaded successfully"
    }