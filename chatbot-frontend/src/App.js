import React, { useState } from "react";
import axios from "axios";
import "./App.css";

// Main App Component
function App() {
  const [question, setQuestion] = useState(""); // State for storing the question
  const [temperature, setTemperature] = useState(0); // State for storing the temperature value
  const [answer, setAnswer] = useState(""); // State for storing the answer from the backend
  const [loading, setLoading] = useState(false); // State for loading indicator

  // Handle form submission for getting the answer
  const handleSubmit = async () => {
    setLoading(true); // Start loading
    try {
      // Make a POST request to Flask backend
      const response = await axios.post("http://localhost:5000/get_answer", {
        question: question,
        temperature: temperature
      });

      // Check if response.data has the expected structure
      if (response.data && response.data.answer) {
        setAnswer(response.data.answer); // Set the response as the answer
      } else {
        setAnswer("Sorry, no valid answer received.");
      }
    } catch (error) {
      console.error(error);
      setAnswer("Sorry, something went wrong! Please try again."); // Handle errors
    }
    setLoading(false); // End loading
  };

  return (
    <div className="App">
      <header>
        <h1>AI ChatBot</h1>
        <p>Ask your question and let the AI answer!</p>
      </header>

      {/* Input section for the user to ask questions */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading} // Disable input while loading
        />

        <div className="slider-container">
          <label>Temperature</label>
          <input
            type="range"
            min="0"
            max="10"
            value={temperature}
            onChange={(e) => setTemperature(e.target.value)}
            disabled={loading} // Disable slider while loading
          />
          <span>{temperature}</span>
        </div>
      </div>

      {/* Submit button */}
      <button
        onClick={handleSubmit}
        disabled={loading || !question} // Disable button if no question is entered
      >
        Get Answer
      </button>

      {/* Loading indicator */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      )}

      {/* Displaying the AI's response */}
      <div className="answer-section">
        {answer && <p className="answer">{answer}</p>}
      </div>
    </div>
  );
}

export default App;
