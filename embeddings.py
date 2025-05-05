import os
import uuid
import pinecone
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
import ollama

# === Configuration ===
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")
pinecone.init(api_key=api_key, environment=environment)
index_name = "my-documents"
dimension = 1536
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=dimension)
index = pinecone.Index(index_name)

embedding_model = "nomic-embed-text"
text_splitter = CharacterTextSplitter(chunk_size=3400, chunk_overlap=300)

def index_url(url: str):
    loader = WebBaseLoader([url])
    docs = loader.load()

    for doc in docs:
        chunks = text_splitter.create_documents([doc.page_content])
        for i, chunk in enumerate(chunks):
            chunk.metadata["source"] = doc.metadata.get("source", url)
            embedding = ollama.embeddings(model=embedding_model, prompt=chunk.page_content)["embedding"]
            vector_id = str(uuid.uuid4())
            # Upsert into Pinecone
            index.upsert([
                (vector_id, embedding, {"source": chunk.metadata["source"], "chunk_id": i})
            ])
    return True
