# SWS AI Document Hub – RAG Chatbot

## Overview

SWS AI Document Hub is a Retrieval-Augmented Generation (RAG) based AI assistant built for answering company policy and HR-related questions using internal PDF documents.

The system processes company PDF documents, converts them into embeddings, stores them in a vector database, retrieves semantically relevant chunks, and generates grounded answers using an LLM.

This project was built using Python, FastAPI, ChromaDB, Sentence Transformers, and Groq LLM APIs.

---

# Features

* PDF document ingestion
* Automatic text extraction
* Text chunking for semantic retrieval
* Embedding generation using Sentence Transformers
* ChromaDB vector database integration
* Semantic similarity search
* RAG-powered grounded answers
* Groq LLM integration
* FastAPI backend API
* Modern chat UI
* Source document tracking
* PDF upload support
* Typing/loading indicator
* Responsive UI

---

# Tech Stack

## Backend

* Python
* FastAPI
* LangChain
* ChromaDB
* Sentence Transformers
* Groq API

## Frontend

* HTML
* CSS
* JavaScript
* Livvic Font

---

# Architecture

## 1. Document Ingestion Pipeline

The uploaded PDF documents are:

1. Loaded using PyMuPDF
2. Parsed and converted into text
3. Split into chunks using RecursiveCharacterTextSplitter
4. Converted into embeddings using:

   * `sentence-transformers/all-MiniLM-L6-v2`
5. Stored inside ChromaDB vector database

---

## 2. Semantic Retrieval

When the user asks a question:

1. The query is converted into embeddings
2. ChromaDB performs semantic similarity search
3. Top-k relevant chunks are retrieved

---

## 3. RAG Generation

The retrieved chunks + user question are passed to the LLM.

The LLM is instructed to:

* answer ONLY from the provided context
* avoid hallucinations
* return grounded answers
* show source documents

---

# Why ChromaDB?

ChromaDB was chosen because:

* lightweight
* easy local setup
* fast semantic retrieval
* ideal for RAG prototypes
* no external cloud dependency

---

# Embedding Model

Model Used:

```bash
sentence-transformers/all-MiniLM-L6-v2
```

Reason:

* lightweight
* fast
* strong semantic search performance
* works well for local RAG systems

---

# LLM Used

Groq API with:

```bash
llama-3.1-8b-instant
```

Reason:

* very fast inference
* low latency
* high quality responses
* ideal for real-time chat applications

---

# Project Structure

```bash
rag_chatbot/
│
├── backend/
│   ├── documents/
│   ├── chroma_db/
│   ├── app.py
│   ├── ingest.py
│   ├── rag_pipeline.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── README.md
└── .gitignore
```

---

# API Endpoint

## Chat Endpoint

```http
POST /api/chat
```

### Request

```json
{
  "question": "What is the leave policy?"
}
```

### Response

```json
{
  "answer": "Employees are entitled to 18 days of earned leave...",
  "sources": [
    "SWS-AI-leave-policy.pdf"
  ]
}
```

---

# Upload Endpoint

```http
POST /api/upload
```

Used for uploading new PDF documents dynamically.

---

# How to Run

## 1. Clone Repository

```bash
git clone https://github.com/rambaburavi/rag_chatbot.git
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Environment

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 5. Start Backend

```bash
cd backend
uvicorn app:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## 6. Open Frontend

Open:

```bash
frontend/index.html
```

in browser.

---

# Semantic Search Explanation

Traditional keyword search matches exact words.

Semantic search converts text into vectors (embeddings) and retrieves content based on meaning rather than exact keywords.

Example:

* "WFH rules"
* "remote work guidelines"

Both retrieve similar chunks because their embeddings are semantically close.

---

# Chunking Strategy

Chunk Size:

```bash
500
```

Chunk Overlap:

```bash
50
```

Reason:

* preserves context
* improves retrieval accuracy
* avoids cutting important information

---

# Future Improvements

* Authentication system
* Multi-user chat sessions
* Conversation memory
* Streaming responses
* Cloud vector databases
* Deployment on Render/Vercel
* React frontend upgrade
* Role-based access

---

# Final Result

This project demonstrates:

* End-to-end RAG pipeline
* Vector search
* Semantic retrieval
* LLM grounding
* Production-style backend architecture
* Modern AI assistant UI

---

# Author

Rambabu Ravi

GitHub:

```bash
https://github.com/rambaburavi/rag_chatbot
```
