import os

from dotenv import load_dotenv

from groq import Groq

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Load environment variables
load_dotenv()

# Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ChromaDB
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)


# Retrieve documents
def retrieve_documents(query):

    results = vector_store.similarity_search(query, k=2)

    return results


# Generate answer
def generate_answer(query):

    docs = retrieve_documents(query)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    sources = list(set([
        doc.metadata["source"].split("\\")[-1]
        for doc in docs
    ]))

    prompt = f"""
You are an AI assistant for SWS AI employees.

Answer ONLY from the provided context.

If the answer is not found in the context, say:
"I don't have that information in the company documents."

Context:
{context}

Question:
{query}
"""

    completion = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    answer = completion.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }