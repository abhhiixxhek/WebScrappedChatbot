from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import chromadb
import os

# === Configuration ===
embedding_model = 'nomic-embed-text'
model = 'llama3.2'
persist_directory = './VectorStore'

# Ensure persist directory exists
os.makedirs(persist_directory, exist_ok=True)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_collection("document_collection")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# === Prompt Template ===
template = """Use the following pieces of context to answer the question. 
If pieces of context do not contain the answer use your internal knowledge.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum for the answer. Keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Answer:"""


# === Core Functions ===
def query_vector_store(prompt, n_results=2):
    response = ollama.embeddings(model=embedding_model, prompt=prompt)
    query_embedding = response["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    sources = [metadata['source'] for metadata in results['metadatas'][0]] if results['metadatas'] else ["No result found."]
    return sources

def generate_response(prompt, temperature=0):
    response = ollama.generate(model=model, prompt=prompt, options={"temperature": temperature})
    return response['response']

# === Route for React frontend ===
@app.route('/get_answer', methods=['POST'])
def get_answer_api():
    try:
        data = request.get_json()  # Get data from React
        question = data.get('question')  # Get question from request
        temperature = float(data.get('temperature', 0))  # Get temperature (creativity level)
        
        retrieved_sources = query_vector_store(question, n_results=2)
        context = ", ".join(retrieved_sources)
        
        combined_prompt = template.format(context=context, question=question)
        response = generate_response(combined_prompt, temperature)
        
        return jsonify({"answer": response})  # Return the response as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a simple route for the root endpoint
@app.route('/')
def index():
    return "Welcome to the AI Chatbot API!"  # You can return any content here.

# Run the Flask app
if __name__ == "__main__":
    app.run(port=5000)  # Ensure Flask runs on the correct port
