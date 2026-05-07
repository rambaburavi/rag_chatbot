import ollama

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load ChromaDB
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)


# Retrieve relevant chunks
def retrieve_documents(query):

    results = vector_store.similarity_search(query, k=3)

    return results


# Generate final answer
def generate_answer(query):

    docs = retrieve_documents(query)

    # Combine retrieved chunks
    context = "\n\n".join([doc.page_content for doc in docs])

    # Extract source documents
    sources = list(set([doc.metadata["source"] for doc in docs]))

    # Prompt for the LLM
    prompt = f"""
You are an AI assistant for SWS AI company employees.

Answer ONLY from the provided context.

If the answer is not found in the context, say:
"I don't have that information in the company documents."

Context:
{context}

Question:
{query}
"""

    # Call local Mistral model via Ollama
    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": sources
    }


# Test Query
query = "What is the leave policy?"

result = generate_answer(query)

print("\n========== FINAL ANSWER ==========\n")

print(result["answer"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print(source)