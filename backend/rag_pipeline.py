from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load same embedding model used during ingestion
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load ChromaDB
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# Retrieval function
def retrieve_documents(query):

    results = vector_store.similarity_search(query, k=3)

    return results

# Test query
query = "What is the leave policy?"

results = retrieve_documents(query)

for i, doc in enumerate(results):

    print(f"\n========== Result {i+1} ==========")

    print(doc.page_content)

    print("\nMetadata:", doc.metadata)