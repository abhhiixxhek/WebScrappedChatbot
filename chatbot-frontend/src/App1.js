import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [temperature, setTemperature] = useState(0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState("");
  const [urlHistory, setUrlHistory] = useState([]);
  const [activeUrl, setActiveUrl] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    fetchUrlHistory();
  }, []);

  const fetchUrlHistory = async () => {
    try {
      const res = await axios.get("http://localhost:5000/url_history");
      setUrlHistory(res.data.urls || []);
    } catch (err) {
      console.error("Failed to fetch URL history");
    }
  };

  const handleAddUrl = async () => {
    if (!url) return alert("Please enter a URL");
    try {
      const res = await axios.post("http://localhost:5000/add_url", { url });
      alert(res.data.message);
      setActiveUrl(url);
      setUrl("");
      fetchUrlHistory();
    } catch (err) {
      alert("Failed to add URL.");
    }
  };

  const handleSubmit = async () => {
    if (!activeUrl) return alert("Please index a site first.");
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/get_answer", {
        question,
        temperature
      });
      const botAnswer = response.data?.answer || "No valid answer received.";
      setAnswer(botAnswer);
      setChatHistory(prev => [...prev, { role: "user", text: question }, { role: "bot", text: botAnswer }]);
    } catch (error) {
      setAnswer("Sorry, something went wrong!");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <aside className="sidebar">
        <h2>Chat History</h2>
        <div className="chat-box">
          {chatHistory.map((entry, index) => (
            <p key={index}><strong>{entry.role === "user" ? "You" : "Bot"}:</strong> {entry.text}</p>
          ))}
        </div>

        <div className="url-history">
          <h3>Indexed URLs</h3>
          {urlHistory.map((item, i) => (
            <button
              key={i}
              className={`url-btn ${item === activeUrl ? "active" : ""}`}
              onClick={() => setActiveUrl(item)}
            >
              {item}
            </button>
          ))}
        </div>

        <div className="url-input">
          <input
            type="text"
            placeholder="Enter new URL to index"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={handleAddUrl}>Index</button>
        </div>
      </aside>

      <main className="chat-area">
        <h1>AI ChatBot</h1>
        <p>Ask anything or re-index a website!</p>

        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <div className="slider-container">
          <label>Temperature</label>
          <input
            type="range"
            min="0"
            max="10"
            value={temperature}
            onChange={(e) => setTemperature(Number(e.target.value))}
            disabled={loading}
          />
          <span>{temperature}</span>
        </div>
        <button onClick={handleSubmit} disabled={loading || !question}>
          Get Answer
        </button>

        {loading && <div className="loading"><div className="spinner"></div></div>}

        {answer && <div className="answer-section">{answer}</div>}
      </main>
    </div>
  );
}

export default App;
