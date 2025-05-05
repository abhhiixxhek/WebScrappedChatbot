# 🤖 WebScrappedChatbot – Local RAG Chatbot with Pinecone & React

A powerful chatbot system that scrapes content from websites, indexes it using **Ollama embeddings** and **Pinecone**, and delivers intelligent answers through a sleek **React.js frontend**. Built with a local **Flask API backend** and optimized for fast retrieval, customization, and a ChatGPT-style user experience.

---

## 🔍 How It Works

### 🌐 1. Web Scraping & Chunking

* Users submit URLs via the React frontend.
* The Flask backend uses `WebBaseLoader` to scrape content.
* Text is split into manageable chunks for embedding.

### 🧠 2. Embedding & Indexing with Ollama + Pinecone

* Uses `nomic-embed-text` from Ollama to embed text.
* Embeddings, along with metadata, are indexed into **Pinecone** using cosine similarity.
* Duplicate prevention logic ensures URLs aren’t indexed repeatedly.

### 💬 3. Query & Retrieval

* Queries are embedded and matched against Pinecone vectors.
* Top-k most relevant chunks are retrieved and compiled as context.

### 📝 4. Response Generation via Local LLM

* The retrieved context is passed into `llama3` via Ollama.
* A custom prompt template ensures concise and factual answers.

### 🖥️ 5. React.js Frontend

* A smooth, modern interface inspired by ChatGPT.
* Sidebar shows indexed URL history.
* Users can re-enter URLs and ask questions with temperature control.


---

## ⚙️ Features

* 🌐 **Web page scraping + dynamic re-indexing**
* 🧠 **Local embedding with Ollama**
* 📡 **Semantic search with Pinecone**
* 🧾 **RAG (Retrieval-Augmented Generation) pipeline**
* 💻 **React.js frontend styled like ChatGPT**
* 🧪 **Temperature slider for response creativity**
* 🕘 **URL indexing history tracking**

---

## 🚀 Setup Instructions

### ✅ Prerequisites

* Python 3.8+
* Node.js (for React frontend)
* Ollama installed and running
* Pinecone account & API key
* CUDA (optional for GPU acceleration)

---

### 🔧 Backend Setup (Flask API)

1. **Clone the repository**

   ```bash
   git clone https://github.com/abhhiixxhek/WebScrappedChatbot.git
   cd WebScrappedChatbot
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:

   ```
   PINECONE_API_KEY=your_api_key_here
   PINECONE_ENVIRONMENT=us-west-1  # or your region
   ```

4. **Run the Flask server**

   ```bash
   python app.py
   ```

---

### 🌐 Frontend Setup (React.js)

1. **Navigate to the frontend folder**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start the frontend**

   ```bash
   npm start
   ```

The React app will run on [http://localhost:3000](http://localhost:3000) and connect to your Flask backend at port `5000`.

---

## 🧪 Usage Flow

1. Enter a URL in the left sidebar.
2. Ask a question about the content.
3. Toggle the temperature to control answer creativity.
4. View past indexed URLs and re-query easily.

---



## 📌 Technologies Used

| Layer     | Tech Used                                         |
| --------- | ------------------------------------------------- |
| Embedding | [Ollama](https://ollama.com) - `nomic-embed-text` |
| Vector DB | [Pinecone](https://www.pinecone.io)               |
| LLM       | `llama3` from Ollama                              |
| Backend   | Flask + Python                                    |
| Frontend  | React.js + Custom CSS                             |

---

## 🙏 Acknowledgements

* [Ollama](https://www.ollama.com) – Local LLM & Embedding engine
* [Pinecone](https://www.pinecone.io) – Fast vector database
* [LangChain](https://www.langchain.com) – Web scraping and document loading
* [React](https://reactjs.org/) – UI framework

---

