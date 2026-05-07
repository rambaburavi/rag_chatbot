import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCUMENTS_PATH = "documents"
CHROMA_DB_PATH = "chroma_db"

documents = []

for file in os.listdir(DOCUMENTS_PATH):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(DOCUMENTS_PATH, file)

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        documents.extend(docs)

print(f"Loaded {len(documents)} pages from PDFs")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=CHROMA_DB_PATH
)

print("Embeddings stored successfully in ChromaDB")