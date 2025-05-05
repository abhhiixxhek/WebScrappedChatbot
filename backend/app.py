from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
from pinecone import Pinecone, ServerlessSpec
import os
import uuid
import json
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-west-1")
PINECONE_INDEX_NAME = "my-documents"
URL_HISTORY_FILE = "url_history.json"

# === Initialize Pinecone ===
pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )

index = pc.Index(PINECONE_INDEX_NAME)

# === Embedding and LLM Model Config ===
embedding_model = "nomic-embed-text"
llm_model = "llama3.2"

# === Initialize Flask App ===
app = Flask(__name__)
CORS(app)

# === Prompt Template ===
template = """
Use the following pieces of context to answer the question as clearly and informatively as possible.
Structure the answer with proper sections or points if needed.
Ensure high quality, completeness, and clarity in the response.
Avoid filler; just give rich and accurate information based strictly on the context.
End the answer with "Thanks for asking!"

{context}
Question: {question}
Answer:"""


# === URL History Management ===
def load_url_history():
    if os.path.exists(URL_HISTORY_FILE):
        with open(URL_HISTORY_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_url_history(history_set):
    with open(URL_HISTORY_FILE, 'w') as f:
        json.dump(list(history_set), f)

indexed_urls = load_url_history()

# === Helper Functions ===

def index_url(url):
    if url in indexed_urls:
        return False, f"{url} has already been indexed."

    try:
        loader = WebBaseLoader([url])
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=3400, chunk_overlap=300)

        for doc in documents:
            chunks = splitter.create_documents([doc.page_content])
            for i, chunk in enumerate(chunks):
                emb = ollama.embeddings(model=embedding_model, prompt=chunk.page_content)["embedding"]
                doc_id = str(uuid.uuid4())
                index.upsert(vectors=[
                    {
                        "id": doc_id,
                        "values": emb,
                        "metadata": {
                            "source": doc.metadata.get("source", url),
                            "chunk_id": i,
                            "text": chunk.page_content
                        }
                    }
                ])
        indexed_urls.add(url)
        save_url_history(indexed_urls)
        return True, f"Successfully indexed {url} with {len(chunks)} chunks."

    except Exception as e:
        return False, f"Error indexing {url}: {str(e)}"

def query_pinecone(query_text: str, top_k: int = 2):
    try:
        emb = ollama.embeddings(model=embedding_model, prompt=query_text)["embedding"]
        result = index.query(vector=emb, top_k=top_k, include_metadata=True)
        contexts = [match["metadata"]["text"] for match in result["matches"]]
        return "\n".join(contexts) if contexts else "I couldn't find anything relevant."
    except Exception as e:
        return f"Error querying vector store: {str(e)}"

def generate_response(prompt: str, temperature: float):
    try:
        return ollama.generate(model=llm_model, prompt=prompt, options={"temperature": temperature})["response"]
    except Exception as e:
        return f"Error generating response: {str(e)}"

# === API Endpoints ===

@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    success, message = index_url(url)
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code

@app.route('/url_history', methods=['GET'])
def get_url_history():
    return jsonify({"urls": sorted(indexed_urls)}), 200

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get("question", "")
    temperature = float(data.get("temperature", 0.0))

    context = query_pinecone(question)
    if "Error" in context:
        return jsonify({"error": context}), 500

    prompt = template.format(context=context, question=question)
    answer = generate_response(prompt, temperature)
    return jsonify({"answer": answer})

# === Run Server ===
if __name__ == "__main__":
    app.run(port=5000)
